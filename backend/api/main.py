from __future__ import annotations

from fastapi import FastAPI, HTTPException
from api.schemas import PredictionInput, PredictionResponse, CitySearchInput
from services.weather_service import (
    search_cities,
    get_weather_auto,
    get_soil_data,
    get_climate_zone
)
from ml.model_loader import predict_yield, load_artifacts
from api.database import init_db, SessionLocal, Prediction
import pandas as pd
import os

# ─────────────────────────────────────────────
# INIT API
# ─────────────────────────────────────────────

app = FastAPI(
    title="AgriSim AI API",
    version="6.0",
    description="API intelligente de prédiction du rendement agricole"
)

init_db()
load_artifacts()

# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────

def clamp_yield(culture, rendement):
    limits = {
        "Blé": (2, 10),
        "Maïs": (3, 12),
        "Riz (paddy)": (2, 10),
        "Pomme de terre": (10, 60),
        "Banane": (10, 40),
        "Manioc": (5, 30),
        "Tomate": (5, 80),
    }
    if culture in limits:
        min_y, max_y = limits[culture]
        return max(min(rendement, max_y), min_y)
    return rendement

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "AgriSim AI API OK", "docs": "/docs"}


@app.post("/cities/search")
def cities_search(data: CitySearchInput):
    """Recherche de villes."""
    return search_cities(data.query)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True,
        "docs": "/docs"
    }


@app.get("/cultures")
def get_cultures():
    """Récupération de la liste des cultures."""
    try:
        df = pd.read_csv("data/cultures_agricoles.csv")
        cultures = sorted(df["Culture"].dropna().unique().tolist())
        return {"cultures": cultures}
    except Exception:
        return {
            "cultures": [
                "Blé", "Maïs", "Riz (paddy)", "Soja", "Orge", "Coton",
                "Manioc", "Mangue", "Sorgho", "Arachide", "Orange",
                "Pomme de terre", "Banane", "Tomate"
            ]
        }


@app.post("/cultures/recommend")
def recommend(data: PredictionInput):
    """Recommandation de cultures en fonction de la météo."""
    meteo = get_weather_auto(
        data.latitude,
        data.longitude,
        data.date_debut,
        data.date_fin
    )

    climat = get_climate_zone(meteo["temperature"], meteo["pluviometrie"])

    if climat == "tropical":
        reco = ["Manioc", "Banane", "Riz (paddy)", "Maïs"]
    elif climat == "sec":
        reco = ["Millet", "Sorgho"]
    elif climat == "froid":
        reco = ["Blé", "Orge"]
    else:
        reco = ["Blé", "Maïs", "Pomme de terre"]

    return {"climat": climat, "cultures": reco}


@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: PredictionInput):
    """Prédiction automatisée."""
    db = None

    try:
        meteo = get_weather_auto(
            input_data.latitude,
            input_data.longitude,
            input_data.date_debut,
            input_data.date_fin
        )

        sol = get_soil_data(input_data.latitude, input_data.longitude)

        model_data = {
            "region": input_data.zone,
            "culture": input_data.culture,
            "temperature": meteo["temperature"],
            "temperature_max": meteo.get("temperature_max", meteo["temperature"] + 5),
            "humidite": meteo["humidite"],
            "pluviometrie": meteo["pluviometrie"],
            "et0": meteo.get("et0", meteo["temperature"] * 0.18),
            "stress_hydrique": meteo.get("stress_hydrique", meteo["pluviometrie"] / (meteo["temperature"] + 5)),
            "ndvi": meteo.get("ndvi", 0.55),
            "type_sol": sol["type_sol"],
            "ph": sol["ph"],
            "engrais": input_data.engrais,
            "irrigation": input_data.irrigation,
            "ndvi_source": "simulated",
        }

        rendement = predict_yield(model_data)
        rendement = clamp_yield(input_data.culture, rendement)
        rendement = round(float(rendement), 2)

        db = SessionLocal()

        db.add(Prediction(
            culture=input_data.culture,
            zone=input_data.zone,
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            temperature=meteo["temperature"],
            humidite=meteo["humidite"],
            pluviometrie=meteo["pluviometrie"],
            type_sol=sol["type_sol"],
            ph=sol["ph"],
            engrais=input_data.engrais,
            irrigation=input_data.irrigation,
            rendement_predit=rendement
        ))

        db.commit()

        return PredictionResponse(
            culture=input_data.culture,
            zone=input_data.zone,
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            temperature=meteo["temperature"],
            humidite=meteo["humidite"],
            pluviometrie=meteo["pluviometrie"],
            source_meteo=meteo["source_meteo"],
            type_sol=sol["type_sol"],
            ph=sol["ph"],
            engrais=input_data.engrais,
            irrigation=input_data.irrigation,
            rendement_predit=rendement
        )

    except Exception as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if db:
            db.close()


@app.post("/predict/manual")
def predict_manual(input_data: dict):
    """Prédiction manuelle."""
    db = None

    try:
        model_data = {
            "region": input_data["zone"],
            "culture": input_data["culture"],
            "temperature": input_data["temperature"],
            "temperature_max": input_data["temperature_max"],
            "humidite": input_data["humidite"],
            "pluviometrie": input_data["pluviometrie"],
            "et0": input_data["et0"],
            "stress_hydrique": input_data["stress_hydrique"],
            "ndvi": input_data["ndvi"],
            "type_sol": input_data["type_sol"],
            "ph": input_data["ph"],
            "engrais": input_data["engrais"],
            "irrigation": input_data["irrigation"],
            "ndvi_source": input_data["ndvi_source"],
        }

        rendement = predict_yield(model_data)
        rendement = clamp_yield(input_data["culture"], rendement)
        rendement = round(float(rendement), 2)

        db = SessionLocal()

        prediction = Prediction(
            culture=input_data["culture"],
            zone=input_data["zone"],
            latitude=input_data["latitude"],
            longitude=input_data["longitude"],
            temperature=input_data["temperature"],
            humidite=input_data["humidite"],
            pluviometrie=input_data["pluviometrie"],
            type_sol=input_data["type_sol"],
            ph=input_data["ph"],
            engrais=input_data["engrais"],
            irrigation=input_data["irrigation"],
            rendement_predit=rendement,
        )

        db.add(prediction)
        db.commit()

        return {
            "culture": input_data["culture"],
            "zone": input_data["zone"],
            "latitude": input_data["latitude"],
            "longitude": input_data["longitude"],
            "temperature": input_data["temperature"],
            "temperature_max": input_data["temperature_max"],
            "humidite": input_data["humidite"],
            "pluviometrie": input_data["pluviometrie"],
            "et0": input_data["et0"],
            "stress_hydrique": input_data["stress_hydrique"],
            "ndvi": input_data["ndvi"],
            "type_sol": input_data["type_sol"],
            "ph": input_data["ph"],
            "engrais": input_data["engrais"],
            "irrigation": input_data["irrigation"],
            "ndvi_source": input_data["ndvi_source"],
            "source_meteo": "saisie manuelle",
            "rendement_predit": rendement,
        }

    except Exception as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if db:
            db.close()


@app.get("/history")
def history(limit: int = 200):
    db = SessionLocal()

    data = (
        db.query(Prediction)
        .order_by(Prediction.id.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return data