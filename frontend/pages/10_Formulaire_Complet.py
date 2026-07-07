# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# pages/10_Formulaire_Complet.py — AgriSim AI
# Module : Formulaire avancé + prédiction explicative
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from __future__ import annotations

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import requests
import streamlit as st

from utils import CSS, CONFIG, sidebar_logo, footer, status_html, search_city


st.set_page_config(
    page_title="Formulaire complet — AgriSim AI",
    page_icon="📝",
    layout="wide",
)

st.markdown(CSS, unsafe_allow_html=True)


with st.sidebar:
    sidebar_logo()
    st.page_link("app.py", label="🏠  Accueil")
    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard")
    st.page_link("pages/2_Prediction.py", label="🌱  Prédiction")
    st.page_link("pages/3_Historique.py", label="📋  Historique")
    st.page_link("pages/4_IA_Explicable.py", label="🔍  IA Explicable")
    st.page_link("pages/5_Performances_ML.py", label="⚙️  Performances ML")
    st.page_link("pages/6_Data_ML_Pipeline.py", label="🗄️  Data & ML Pipeline")
    st.page_link("pages/7_Backend_API.py", label="⚙️  Backend & API")
    st.page_link("pages/8_Architecture_Deployment.py", label="🏗️  Architecture")
    st.page_link("pages/9_Frontend_UI.py", label="🎨  Frontend & UX")
    st.page_link("pages/10_Formulaire_Complet.py", label="📝  Formulaire complet")


st.markdown(
    """
    <div class="section-header">Formulaire complet de prédiction</div>
    <p class="section-sub">
        Saisissez les données compréhensibles par l’utilisateur. La ville doit être sélectionnée
        depuis l’API afin d’éviter les zones inexistantes.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    status_html(
        "success",
        "Saisie contrôlée",
        "La zone est rattachée à l’API de recherche de villes. Les coordonnées, le pH, le NDVI, l’ET0 et le stress hydrique sont ensuite calculés automatiquement."
    ),
    unsafe_allow_html=True,
)


defaults = {
    "fc_culture": "Maïs",
    "fc_zone": "Paris",
    "fc_temperature": 25.0,
    "fc_temperature_max": 30.0,
    "fc_humidite": 65.0,
    "fc_pluviometrie": 120.0,
    "fc_type_sol": "limoneux",
    "fc_engrais": 70,
    "fc_irrigation": "oui",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def auto_ph_from_soil(type_sol: str) -> float:
    ph_map = {
        "limoneux": 6.8,
        "argileux": 6.5,
        "sableux": 6.2,
        "humifere": 6.0,
        "calcaire": 7.8,
        "lateritique": 5.5,
    }
    return ph_map.get(type_sol, 6.8)


def auto_enrich(
    latitude: float,
    longitude: float,
    country: str,
    admin1: str,
    temperature: float,
    temperature_max: float,
    pluviometrie: float,
    type_sol: str,
) -> dict:
    ph = auto_ph_from_soil(type_sol)
    et0 = round(max(0.0, temperature * 0.18), 2)
    stress_hydrique = round(pluviometrie / (temperature + 1), 3)

    if pluviometrie >= 800:
        ndvi = 0.72
    elif pluviometrie >= 400:
        ndvi = 0.62
    elif pluviometrie >= 150:
        ndvi = 0.52
    else:
        ndvi = 0.35

    return {
        "latitude": latitude,
        "longitude": longitude,
        "country": country,
        "admin1": admin1,
        "ph": ph,
        "et0": et0,
        "stress_hydrique": stress_hydrique,
        "ndvi": ndvi,
        "ndvi_source": "auto_simulated",
        "temperature_max": temperature_max,
    }


def rendement_level(rendement: float) -> tuple[str, str, str]:
    if rendement < 3:
        return (
            "danger",
            "Rendement faible",
            "Le rendement estimé est faible. Une amélioration des pratiques agricoles est recommandée.",
        )
    if rendement < 5:
        return (
            "warning",
            "Rendement moyen",
            "Le rendement est acceptable mais peut être optimisé avec de meilleurs paramètres.",
        )
    return (
        "success",
        "Bon rendement",
        "Les conditions saisies semblent favorables pour cette culture.",
    )


def generate_recommendations(payload: dict, rendement: float) -> list[str]:
    recos = []

    if rendement < 3:
        recos.append("Revoir les conditions de culture : le rendement prédit est faible.")
        recos.append("Vérifier la qualité du sol et envisager un apport organique ou minéral adapté.")

    if payload["pluviometrie"] < 100:
        recos.append("La pluviométrie est faible : renforcer l’irrigation ou choisir une culture plus résistante au stress hydrique.")

    if payload["pluviometrie"] > 900:
        recos.append("La pluviométrie est très élevée : surveiller le drainage du sol et les risques de maladies fongiques.")

    if payload["temperature"] > 35:
        recos.append("La température est élevée : éviter les périodes de forte chaleur et adapter le calendrier cultural.")

    if payload["temperature"] < 10:
        recos.append("La température est basse : privilégier des cultures adaptées aux climats frais.")

    if payload["humidite"] < 30:
        recos.append("L’humidité est faible : surveiller l’évaporation et l’état hydrique du sol.")

    if payload["engrais"] < 40:
        recos.append("La dose d’engrais semble faible : envisager un apport progressif selon les besoins de la culture.")

    if payload["engrais"] > 200:
        recos.append("La dose d’engrais est élevée : attention au surdosage et aux pertes par lessivage.")

    if payload["irrigation"] == "non" and payload["pluviometrie"] < 300:
        recos.append("Sans irrigation et avec une faible pluie, le rendement peut être limité. Une irrigation contrôlée est recommandée.")

    if payload["ph"] < 5.8:
        recos.append("Le pH calculé est acide : un amendement calcique peut être envisagé selon analyse du sol.")

    if payload["ph"] > 7.5:
        recos.append("Le pH calculé est alcalin : surveiller la disponibilité du fer, du zinc et du phosphore.")

    if not recos:
        recos.append("Les paramètres saisis sont globalement cohérents. Maintenir un suivi météo et agronomique régulier.")

    return recos


def validate_inputs(
    zone: str,
    latitude: float | None,
    longitude: float | None,
    temperature: float,
    temperature_max: float,
    pluviometrie: float,
    humidite: float,
) -> list[str]:
    errors = []

    if not zone.strip():
        errors.append("Vous devez sélectionner une ville existante dans la liste proposée.")

    if latitude is None or longitude is None:
        errors.append("Les coordonnées de la ville sont absentes. Sélectionnez une ville retournée par l’API.")

    if temperature_max < temperature:
        errors.append("La température maximale doit être supérieure ou égale à la température moyenne.")

    if pluviometrie == 0:
        errors.append("La pluviométrie est nulle : le rendement risque d’être faible.")

    if humidite < 10:
        errors.append("L’humidité semble très faible : vérifie la valeur saisie.")

    return errors


col_a, col_b = st.columns(2)

with col_a:
    if st.button("⚡ Remplir avec données exemple", width="stretch"):
        st.session_state.update(defaults)
        st.toast("Données exemple chargées ✅")

with col_b:
    if st.button("🧹 Réinitialiser", width="stretch"):
        st.session_state.update(defaults)
        st.toast("Formulaire réinitialisé ✅")


st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)


with st.form("formulaire_complet_prediction"):
    st.markdown('<div class="section-header">1. Informations générales</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        culture = st.selectbox(
            "Culture",
            [
                "Blé", "Maïs", "Riz (paddy)", "Soja", "Orge", "Coton",
                "Manioc", "Mangue", "Sorgho", "Arachide", "Orange",
                "Pomme de terre", "Banane", "Tomate",
            ],
            key="fc_culture",
        )

    with c2:
        city_query = st.text_input("Rechercher une ville", key="fc_zone")

        cities = search_city(city_query) if city_query and len(city_query.strip()) >= 2 else []

        if cities:
            city_options = [
                f"{c['name']} — {c.get('admin1', '')} · {c.get('country', '')}"
                for c in cities
            ]

            selected_city_label = st.selectbox(
                "Ville existante",
                city_options,
                key="fc_city_selected",
            )

            selected_city = cities[city_options.index(selected_city_label)]

            zone = selected_city["name"]
            latitude = selected_city["latitude"]
            longitude = selected_city["longitude"]
            country = selected_city.get("country", "")
            admin1 = selected_city.get("admin1", "")

            st.caption(f"Ville sélectionnée : {zone}, {admin1}, {country}")

        else:
            zone = ""
            latitude = None
            longitude = None
            country = ""
            admin1 = ""

            st.warning("Saisissez au moins 2 lettres puis choisissez une ville existante.")

    st.markdown('<div class="section-header">2. Données météo observées ou estimées</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        temperature = st.number_input("Température moyenne (°C)", -20.0, 60.0, step=0.1, key="fc_temperature")

    with m2:
        temperature_max = st.number_input("Température maximale (°C)", -20.0, 70.0, step=0.1, key="fc_temperature_max")

    with m3:
        humidite = st.number_input("Humidité (%)", 0.0, 100.0, step=0.5, key="fc_humidite")

    with m4:
        pluviometrie = st.number_input("Pluviométrie (mm)", 0.0, 5000.0, step=1.0, key="fc_pluviometrie")

    st.markdown('<div class="section-header">3. Sol & pratiques agricoles</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        type_sol = st.selectbox(
            "Type de sol",
            ["limoneux", "argileux", "sableux", "humifere", "calcaire", "lateritique"],
            key="fc_type_sol",
        )

    with p2:
        engrais = st.slider("Engrais (kg/ha)", 0, 300, step=5, key="fc_engrais")

    with p3:
        irrigation = st.radio("Irrigation", ["oui", "non"], horizontal=True, key="fc_irrigation")

    submit = st.form_submit_button("🌱 Lancer la prédiction complète", width="stretch")


if not zone or latitude is None or longitude is None:
    st.markdown(
        status_html(
            "warning",
            "Ville non sélectionnée",
            "Veuillez rechercher une ville puis sélectionner une ville existante dans la liste pour générer les données enrichies."
        ),
        unsafe_allow_html=True,
    )
    footer()
    st.stop()


auto_data = auto_enrich(
    latitude=latitude,
    longitude=longitude,
    country=country,
    admin1=admin1,
    temperature=temperature,
    temperature_max=temperature_max,
    pluviometrie=pluviometrie,
    type_sol=type_sol,
)

payload = {
    "culture": culture,
    "zone": zone,
    "latitude": auto_data["latitude"],
    "longitude": auto_data["longitude"],
    "temperature": temperature,
    "temperature_max": auto_data["temperature_max"],
    "humidite": humidite,
    "pluviometrie": pluviometrie,
    "et0": auto_data["et0"],
    "stress_hydrique": auto_data["stress_hydrique"],
    "ndvi": auto_data["ndvi"],
    "type_sol": type_sol,
    "ph": auto_data["ph"],
    "engrais": engrais,
    "irrigation": irrigation,
    "ndvi_source": auto_data["ndvi_source"],
}

preview_df = pd.DataFrame([payload])

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-header">Données enrichies automatiquement</div>', unsafe_allow_html=True)

a1, a2, a3, a4 = st.columns(4)
a1.metric("Latitude", f"{auto_data['latitude']:.4f}")
a2.metric("Longitude", f"{auto_data['longitude']:.4f}")
a3.metric("pH calculé", f"{auto_data['ph']:.1f}")
a4.metric("NDVI", f"{auto_data['ndvi']:.2f}")

st.markdown(
    status_html(
        "warning",
        "Variables techniques calculées",
        f"Ville sélectionnée : {zone}, {admin1}, {country}. Type de sol saisi : {type_sol}. Le pH, l’ET0, le stress hydrique, le NDVI et les coordonnées sont calculés automatiquement."
    ),
    unsafe_allow_html=True,
)

st.dataframe(preview_df, width="stretch")

st.download_button(
    "Télécharger les données complètes (CSV)",
    data=preview_df.to_csv(index=False).encode("utf-8"),
    file_name=f"donnees_formulaire_complet_{date.today()}.csv",
    mime="text/csv",
    width="stretch",
)


if submit:
    errors = validate_inputs(
        zone=zone,
        latitude=latitude,
        longitude=longitude,
        temperature=temperature,
        temperature_max=temperature_max,
        pluviometrie=pluviometrie,
        humidite=humidite,
    )

    if errors:
        for err in errors:
            st.warning(err)
        st.stop()

    try:
        response = requests.post(
            f"{CONFIG.api_url}/predict/manual",
            json=payload,
            timeout=30,
        )

        if response.status_code == 404:
            st.error("La route /predict/manual n’existe pas encore dans le backend.")
            st.stop()

        response.raise_for_status()
        result = response.json()

        rendement = float(result.get("rendement_predit", 0))
        level, title, body = rendement_level(rendement)
        recos = generate_recommendations(payload, rendement)

        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Résultat de la prédiction complète</div>', unsafe_allow_html=True)

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Rendement prédit", f"{rendement} t/ha")
        r2.metric("Culture", result.get("culture", culture))
        r3.metric("Zone", result.get("zone", zone))
        r4.metric("Irrigation", result.get("irrigation", irrigation))

        st.markdown(status_html(level, title, body), unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="interpret-box">
                <div class="interpret-box-label">Explication de la prédiction</div>
                <p>
                    Pour la culture <strong>{culture}</strong> dans la zone <strong>{zone}</strong>,
                    le modèle estime un rendement de <strong>{rendement} t/ha</strong>.
                    Cette prédiction repose sur une température moyenne de <strong>{temperature} °C</strong>,
                    une pluviométrie de <strong>{pluviometrie} mm</strong>, une humidité de
                    <strong>{humidite} %</strong>, un sol <strong>{type_sol}</strong> avec un pH calculé de
                    <strong>{auto_data["ph"]}</strong>, et une dose d’engrais de
                    <strong>{engrais} kg/ha</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-header">Solutions proposées</div>', unsafe_allow_html=True)

        for reco in recos:
            st.markdown(
                status_html(
                    "success" if rendement >= 5 else "warning",
                    "Recommandation",
                    reco,
                ),
                unsafe_allow_html=True,
            )

        result_df = pd.DataFrame([result])

        st.download_button(
            "Télécharger le résultat complet (CSV)",
            data=result_df.to_csv(index=False).encode("utf-8"),
            file_name=f"prediction_complete_{culture}_{date.today()}.csv",
            mime="text/csv",
            width="stretch",
        )

        with st.expander("Voir la réponse JSON complète"):
            st.json(result)

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
        st.markdown(
            status_html(
                "danger",
                "Backend inaccessible ou route absente",
                "Vérifie que le backend est lancé et que la route /predict/manual existe."
            ),
            unsafe_allow_html=True,
        )


st.markdown(
    """
    <div class="interpret-box">
        <div class="interpret-box-label">Lecture technique</div>
        <p>
            Ce formulaire distingue les données utilisateur des variables techniques.
            L’utilisateur sélectionne une ville existante depuis l’API, puis renseigne la culture,
            la météo, le type de sol, l’engrais et l’irrigation. Le système calcule ensuite
            les coordonnées, le pH, le NDVI, l’ET0 et le stress hydrique pour construire
            l’entrée complète attendue par le modèle ML.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

footer()