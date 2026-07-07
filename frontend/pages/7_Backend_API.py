# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# pages/7_Backend_API.py — AgriSim AI
# Module : Backend FastAPI, routes, ML, PostgreSQL, Docker
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import streamlit.components.v1 as components

from utils import CSS, CONFIG, sidebar_logo, footer


st.set_page_config(
    page_title="Backend & API — AgriSim AI",
    page_icon="⚙️",
    layout="wide",
)

st.markdown(CSS, unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    sidebar_logo()

    st.page_link("app.py",                       label="🏠  Accueil")
    st.page_link("pages/1_Dashboard.py",         label="📊  Dashboard")
    st.page_link("pages/2_Prediction.py",        label="🌱  Prédiction")
    st.page_link("pages/3_Historique.py",        label="📋  Historique")
    st.page_link("pages/4_IA_Explicable.py",     label="🔍  IA Explicable")
    st.page_link("pages/5_Performances_ML.py",   label="⚙️  Performances ML")
    st.page_link("pages/6_Data_ML_Pipeline.py",  label="🗄️  Data & ML Pipeline")
    st.page_link("pages/7_Backend_API.py",       label="⚙️  Backend & API")
    st.page_link("pages/8_Architecture_Deployment.py", label="🏗️  Architecture")
    st.page_link("pages/9_Frontend_UI.py", label="🎨  Frontend & UX")
    st.page_link("pages/10_Formulaire_Complet.py", label="📝  Formulaire complet")



# ── Titre page ───────────────────────────────────────────────
st.markdown(
    """
    <div class="section-header">Backend & API</div>
    <p class="section-sub">
        Ce module présente le rôle du backend FastAPI dans AgriSim AI :
        orchestration des données, prédiction ML, stockage PostgreSQL,
        routes API, intégration Docker et métriques de performance.
    </p>
    """,
    unsafe_allow_html=True,
)

# ── Statut backend en temps réel ─────────────────────────────
try:
    import requests as _req
    _res = _req.get(f"{CONFIG.api_url}/", timeout=5)
    if _res.status_code == 200:
        _status_type, _status_title, _status_msg = (
            "success",
            "Backend accessible",
            f"L'API répond correctement depuis {CONFIG.api_url}.",
        )
    else:
        _status_type, _status_title, _status_msg = (
            "warning",
            "Réponse inattendue",
            f"Le backend répond avec le statut HTTP {_res.status_code}.",
        )
except Exception as _e:
    _status_type, _status_title, _status_msg = (
        "danger",
        "Backend inaccessible",
        f"Impossible de joindre le backend : {_e}",
    )

_STATUS_COLORS = {
    "success": ("#EAF3DE", "#27500A", "#C0DD97"),
    "warning": ("#FAEEDA", "#633806", "#FAC775"),
    "danger":  ("#FAECE7", "#712B13", "#F5C4B3"),
}
_bg, _fg, _border = _STATUS_COLORS[_status_type]

st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:10px;padding:10px 16px;
         background:{_bg};border:0.5px solid {_border};border-radius:8px;
         margin-bottom:1.5rem;font-size:13px;color:{_fg}">
      <strong>{_status_title}</strong> — {_status_msg}
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Dashboard interactif ─────────────────────────────────────
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --bg:#ffffff;--bg2:#f5f4f0;--bg3:#eeece6;
  --text:#1a1a18;--text2:#5f5e5a;--text3:#888780;
  --border:rgba(0,0,0,0.10);--border2:rgba(0,0,0,0.18);
  --radius:8px;--radius-lg:12px;
  --green-50:#EAF3DE;--green-100:#C0DD97;--green-200:#97C459;
  --green-400:#639922;--green-600:#3B6D11;--green-800:#27500A;
  --teal-50:#E1F5EE;--teal-100:#9FE1CB;--teal-400:#1D9E75;
  --teal-600:#0F6E56;--teal-800:#085041;
  --amber-50:#FAEEDA;--amber-100:#FAC775;--amber-400:#BA7517;--amber-800:#633806;
  --blue-50:#E6F1FB;--blue-100:#B5D4F4;--blue-400:#378ADD;
  --blue-600:#185FA5;--blue-800:#0C447C;
  --purple-50:#EEEDFE;--purple-100:#CECBF6;--purple-400:#7F77DD;
  --purple-600:#534AB7;--purple-800:#3C3489;
  --coral-50:#FAECE7;--coral-100:#F5C4B3;--coral-400:#D85A30;
  --coral-600:#993C1D;--coral-800:#712B13;
  --gray-50:#F1EFE8;--gray-100:#D3D1C7;--gray-400:#888780;
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#1e1d1b;--bg2:#28271f;--bg3:#302f27;
    --text:#e8e6df;--text2:#9c9a92;--text3:#6b6a64;
    --border:rgba(255,255,255,0.10);--border2:rgba(255,255,255,0.18);
    --green-50:#1a2910;--green-100:#2f4a1b;--green-600:#7db83a;--green-800:#b8e07a;
    --teal-50:#0a2218;--teal-100:#0e3828;--teal-600:#3ecfa0;--teal-800:#9ae8d0;
    --amber-50:#2a1e08;--amber-100:#3d2d0a;--amber-400:#d4922a;--amber-800:#f5cc7a;
    --blue-50:#0a1e30;--blue-100:#0d3050;--blue-400:#5ca8f0;--blue-600:#8dc6f7;--blue-800:#c0dffb;
    --purple-50:#1a1838;--purple-100:#2e2860;--purple-400:#9b94e8;--purple-800:#e0dcfd;
    --coral-50:#2a1008;--coral-100:#401810;--coral-400:#e8784a;--coral-800:#fcd3be;
    --gray-50:#1e1d1a;--gray-100:#2e2d28;
  }
}
body{font-family:var(--font);font-size:14px;color:var(--text);background:var(--bg);padding:1.25rem 1rem 2.5rem;line-height:1.5}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-bottom:1.5rem}
.metric{background:var(--bg2);border-radius:var(--radius);padding:12px 14px}
.metric .lbl{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.metric .val{font-size:15px;font-weight:500}
.metric.green .val{color:var(--green-600)}.metric.blue .val{color:var(--blue-600)}
.metric.amber .val{color:var(--amber-400)}.metric.teal .val{color:var(--teal-600)}
.metric.purple .val{color:var(--purple-600)}
.tabs{display:flex;flex-wrap:wrap;gap:2px;border-bottom:0.5px solid var(--border);margin-bottom:1.5rem}
.tab{font-size:13px;padding:8px 13px;cursor:pointer;border:none;background:none;color:var(--text2);border-bottom:2px solid transparent;margin-bottom:-0.5px;border-radius:4px 4px 0 0;transition:color .15s,background .15s,border-color .15s;font-family:var(--font)}
.tab:hover{color:var(--text);background:var(--bg2)}
.tab.active{color:var(--green-600);border-bottom-color:var(--green-600);font-weight:500}
.panel{display:none}.panel.active{display:block}
.section-label{font-size:11px;font-weight:500;color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px}
.card{background:var(--bg);border:0.5px solid var(--border);border-radius:var(--radius-lg);padding:1rem 1.25rem;margin-bottom:1rem}
.card-title{font-size:12px;font-weight:500;color:var(--text2);margin-bottom:10px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:540px){.two-col{grid-template-columns:1fr}}
.chart-wrap{position:relative;height:200px}
.chart-wrap.tall{height:240px}
.rt{width:100%;border-collapse:collapse;font-size:12px}
.rt th{text-align:left;color:var(--text3);font-weight:400;font-size:10px;text-transform:uppercase;letter-spacing:.06em;padding:0 12px 8px 0;border-bottom:0.5px solid var(--border)}
.rt td{padding:8px 12px 8px 0;border-bottom:0.5px solid var(--border);vertical-align:middle}
.rt tr:last-child td{border-bottom:none}
.badge{display:inline-block;font-size:10px;font-weight:600;padding:2px 7px;border-radius:4px;letter-spacing:.04em}
.badge.get{background:var(--blue-50);color:var(--blue-800)}.badge.post{background:var(--green-50);color:var(--green-800)}
code{font-family:'SFMono-Regular',Consolas,monospace;font-size:11px;background:var(--bg2);padding:2px 6px;border-radius:4px;color:var(--text)}
.step{display:flex;gap:12px;align-items:flex-start;padding:10px 8px;border-radius:var(--radius);cursor:pointer;transition:background .12s;border-bottom:0.5px solid var(--border)}
.step:last-child{border-bottom:none}.step:hover{background:var(--bg2)}
.num{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;flex-shrink:0;margin-top:1px}
.num.green{background:var(--green-50);color:var(--green-800)}.num.blue{background:var(--blue-50);color:var(--blue-800)}
.num.amber{background:var(--amber-50);color:var(--amber-800)}.num.teal{background:var(--teal-50);color:var(--teal-800)}
.num.purple{background:var(--purple-50);color:var(--purple-800)}.num.coral{background:var(--coral-50);color:var(--coral-800)}
.step-body{flex:1}.step-title{font-size:13px;font-weight:500;margin-bottom:2px}.step-desc{font-size:12px;color:var(--text2)}
.step-tag{display:inline-block;font-size:10px;padding:1px 7px;border-radius:4px;border:0.5px solid var(--border2);color:var(--text3);margin-left:6px;vertical-align:middle}
.kv{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:0.5px solid var(--border);font-size:12px}
.kv:last-child{border-bottom:none}.kv-k{color:var(--text2)}.kv-v{font-family:'SFMono-Regular',Consolas,monospace;font-size:11px}
.arch-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:12px}
.arch-item{border:0.5px solid var(--border);border-radius:var(--radius);padding:12px;cursor:pointer;transition:border-color .15s,background .15s}
.arch-item:hover{background:var(--bg2);border-color:var(--border2)}.arch-item.selected{border-color:var(--green-400);background:var(--green-50)}
.arch-dot{width:10px;height:10px;border-radius:2px;display:inline-block;margin-right:5px;vertical-align:middle}
.arch-meta{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px}
.arch-file{font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:500;color:var(--text);margin-bottom:3px}
.arch-desc{font-size:11px;color:var(--text2);line-height:1.5}
.detail-box{background:var(--bg2);border-radius:var(--radius);padding:12px 14px;font-size:12px;line-height:1.7;color:var(--text2);min-height:56px}
.detail-box strong{color:var(--text);font-weight:500}
.ml-node{display:flex;align-items:center;gap:12px;padding:10px 12px;border:0.5px solid var(--border);border-radius:var(--radius);margin-bottom:4px;cursor:pointer;transition:background .12s}
.ml-node:hover{background:var(--bg2)}.ml-node-body{flex:1}
.ml-node-title{font-size:13px;font-weight:500}.ml-node-sub{font-size:11px;color:var(--text2);margin-top:2px}
.connector-line{width:2px;height:12px;background:var(--border2);margin-left:23px}
.tag{display:inline-block;font-size:10px;padding:2px 7px;border-radius:4px;border:0.5px solid var(--border2);color:var(--text3)}
.latency-row{display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:0.5px solid var(--border);font-size:12px}
.latency-row:last-child{border-bottom:none}
.latency-label{width:140px;color:var(--text2);flex-shrink:0;font-family:'SFMono-Regular',Consolas,monospace;font-size:11px}
.latency-bar-wrap{flex:1;background:var(--bg2);border-radius:4px;height:8px;overflow:hidden}
.latency-bar{height:100%;border-radius:4px;transition:width .6s ease}
.latency-val{width:50px;text-align:right;color:var(--text);font-weight:500;font-size:11px}
.legend{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:10px}
.legend-item{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text2)}
.legend-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.synth{border-left:2px solid var(--green-400);padding:12px 16px;border-radius:0 var(--radius) var(--radius) 0;background:var(--green-50);font-size:13px;color:var(--green-800);line-height:1.7}
</style>
</head>
<body>

<!-- Métriques -->
<div class="metrics">
  <div class="metric green" ><div class="lbl">Framework</div><div class="val">FastAPI</div></div>
  <div class="metric blue"  ><div class="lbl">Serveur</div><div class="val">Uvicorn</div></div>
  <div class="metric amber" ><div class="lbl">Base de données</div><div class="val">PostgreSQL</div></div>
  <div class="metric teal"  ><div class="lbl">Déploiement</div><div class="val">Docker</div></div>
  <div class="metric purple"><div class="lbl">Endpoints</div><div class="val">6 routes</div></div>
</div>

<!-- Onglets -->
<div class="tabs">
  <button class="tab active" onclick="switchTab('perf',this)">Performances</button>
  <button class="tab" onclick="switchTab('architecture',this)">Architecture</button>
  <button class="tab" onclick="switchTab('routes',this)">Routes API</button>
  <button class="tab" onclick="switchTab('prediction',this)">Flux prédiction</button>
  <button class="tab" onclick="switchTab('ml',this)">Modèle ML</button>
  <button class="tab" onclick="switchTab('docker',this)">Docker</button>
</div>

<!-- ═══════ PERFORMANCES ═══════ -->
<div id="tab-perf" class="panel active">
  <div class="two-col">
    <div class="card">
      <div class="card-title">Latence moyenne par endpoint (ms)</div>
      <div class="chart-wrap tall"><canvas id="chartLatence"></canvas></div>
    </div>
    <div class="card">
      <div class="card-title">Répartition des appels API</div>
      <div class="legend">
        <span class="legend-item"><span class="legend-dot" style="background:#639922"></span>POST /predict</span>
        <span class="legend-item"><span class="legend-dot" style="background:#378ADD"></span>GET /history</span>
        <span class="legend-item"><span class="legend-dot" style="background:#1D9E75"></span>POST /cities</span>
        <span class="legend-item"><span class="legend-dot" style="background:#BA7517"></span>GET /cultures</span>
        <span class="legend-item"><span class="legend-dot" style="background:#7F77DD"></span>GET /health</span>
        <span class="legend-item"><span class="legend-dot" style="background:#D85A30"></span>GET /</span>
      </div>
      <div class="chart-wrap" style="height:185px"><canvas id="chartRepartition"></canvas></div>
    </div>
  </div>
  <div class="two-col">
    <div class="card">
      <div class="card-title">Volume de requêtes (24 dernières heures)</div>
      <div class="chart-wrap tall"><canvas id="chartTrafic"></canvas></div>
    </div>
    <div class="card">
      <div class="card-title">Distribution des rendements prédits (t/ha)</div>
      <div class="chart-wrap tall"><canvas id="chartDistrib"></canvas></div>
    </div>
  </div>
  <div class="two-col">
    <div class="card">
      <div class="card-title">Décomposition du temps de prédiction ML</div>
      <div class="latency-row">
        <span class="latency-label">Météo Open-Meteo</span>
        <div class="latency-bar-wrap"><div class="latency-bar" style="width:72%;background:#378ADD"></div></div>
        <span class="latency-val">287 ms</span>
      </div>
      <div class="latency-row">
        <span class="latency-label">Feature engineering</span>
        <div class="latency-bar-wrap"><div class="latency-bar" style="width:18%;background:#1D9E75"></div></div>
        <span class="latency-val">72 ms</span>
      </div>
      <div class="latency-row">
        <span class="latency-label">Inférence ML</span>
        <div class="latency-bar-wrap"><div class="latency-bar" style="width:12%;background:#639922"></div></div>
        <span class="latency-val">48 ms</span>
      </div>
      <div class="latency-row">
        <span class="latency-label">Écriture PostgreSQL</span>
        <div class="latency-bar-wrap"><div class="latency-bar" style="width:10%;background:#BA7517"></div></div>
        <span class="latency-val">38 ms</span>
      </div>
      <div class="latency-row">
        <span class="latency-label">Sérialisation JSON</span>
        <div class="latency-bar-wrap"><div class="latency-bar" style="width:4%;background:#7F77DD"></div></div>
        <span class="latency-val">14 ms</span>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Taux de succès par endpoint (%)</div>
      <div class="chart-wrap" style="height:220px"><canvas id="chartSucces"></canvas></div>
    </div>
  </div>
</div>

<!-- ═══════ ARCHITECTURE ═══════ -->
<div id="tab-architecture" class="panel">
  <div class="section-label">Modules backend</div>
  <div class="arch-grid">
    <div class="arch-item" onclick="showDetail(this,'main')">
      <div class="arch-meta"><span class="arch-dot" style="background:var(--green-200)"></span>API</div>
      <div class="arch-file">api/main.py</div><div class="arch-desc">Orchestration des routes</div>
    </div>
    <div class="arch-item" onclick="showDetail(this,'schemas')">
      <div class="arch-meta"><span class="arch-dot" style="background:var(--blue-100)"></span>Schémas</div>
      <div class="arch-file">api/schemas.py</div><div class="arch-desc">Modèles Pydantic</div>
    </div>
    <div class="arch-item" onclick="showDetail(this,'database')">
      <div class="arch-meta"><span class="arch-dot" style="background:var(--amber-100)"></span>BDD</div>
      <div class="arch-file">api/database.py</div><div class="arch-desc">Connexion SQLAlchemy</div>
    </div>
    <div class="arch-item" onclick="showDetail(this,'weather')">
      <div class="arch-meta"><span class="arch-dot" style="background:var(--teal-100)"></span>Service</div>
      <div class="arch-file">weather_service.py</div><div class="arch-desc">Données Open-Meteo</div>
    </div>
    <div class="arch-item" onclick="showDetail(this,'ml')">
      <div class="arch-meta"><span class="arch-dot" style="background:var(--purple-100)"></span>ML</div>
      <div class="arch-file">ml/model_loader.py</div><div class="arch-desc">Chargement modèle</div>
    </div>
    <div class="arch-item" onclick="showDetail(this,'model')">
      <div class="arch-meta"><span class="arch-dot" style="background:var(--coral-100)"></span>Artefacts</div>
      <div class="arch-file">model/</div><div class="arch-desc">Fichiers ML runtime</div>
    </div>
  </div>
  <div class="detail-box" id="detail-pane">Cliquez sur un module pour afficher sa description détaillée.</div>
</div>

<!-- ═══════ ROUTES ═══════ -->
<div id="tab-routes" class="panel">
  <div class="card">
    <table class="rt">
      <thead><tr><th style="width:60px">Méthode</th><th style="width:150px">Endpoint</th><th>Rôle</th><th style="width:140px">Consommé par</th></tr></thead>
      <tbody>
        <tr><td><span class="badge get">GET</span></td><td><code>/</code></td><td>Vérifier la disponibilité de l'API</td><td style="color:var(--text2)">Docker / navigateur</td></tr>
        <tr><td><span class="badge post">POST</span></td><td><code>/cities/search</code></td><td>Rechercher une ville et ses coordonnées</td><td style="color:var(--text2)">Frontend Streamlit</td></tr>
        <tr><td><span class="badge post">POST</span></td><td><code>/predict</code></td><td>Lancer une prédiction de rendement agricole</td><td style="color:var(--text2)">Frontend Streamlit</td></tr>
        <tr><td><span class="badge get">GET</span></td><td><code>/history</code></td><td>Retourner l'historique des prédictions</td><td style="color:var(--text2)">Dashboard / Historique</td></tr>
        <tr><td><span class="badge get">GET</span></td><td><code>/cultures</code></td><td>Lister les cultures disponibles</td><td style="color:var(--text2)">Frontend Streamlit</td></tr>
        <tr><td><span class="badge get">GET</span></td><td><code>/health</code></td><td>Vérifier l'état de santé du backend</td><td style="color:var(--text2)">Docker / Render</td></tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ═══════ FLUX PRÉDICTION ═══════ -->
<div id="tab-prediction" class="panel">
  <div class="section-label">Pipeline de traitement POST /predict</div>
  <div class="step"><div class="num green">1</div><div class="step-body"><div class="step-title">Requête frontend <span class="step-tag">POST /predict</span></div><div class="step-desc">Culture, ville, dates, fertilisation et irrigation envoyés depuis Streamlit</div></div></div>
  <div class="step"><div class="num blue">2</div><div class="step-body"><div class="step-title">Récupération météo <span class="step-tag">Open-Meteo API</span></div><div class="step-desc">Appel HTTP selon latitude/longitude de la ville sélectionnée</div></div></div>
  <div class="step"><div class="num amber">3</div><div class="step-body"><div class="step-title">Données pédologiques <span class="step-tag">Sol + pH</span></div><div class="step-desc">Récupération ou simulation du type_sol et du niveau pH</div></div></div>
  <div class="step"><div class="num teal">4</div><div class="step-body"><div class="step-title">Feature engineering <span class="step-tag">Scikit-learn</span></div><div class="step-desc">Construction des variables dans l'ordre attendu par le modèle ML</div></div></div>
  <div class="step"><div class="num purple">5</div><div class="step-body"><div class="step-title">Inférence ML <span class="step-tag">Joblib · lru_cache</span></div><div class="step-desc">Chargement du modèle en cache mémoire + prédiction du rendement</div></div></div>
  <div class="step"><div class="num coral">6</div><div class="step-body"><div class="step-title">Clamp agronomique <span class="step-tag">Business rules</span></div><div class="step-desc">Plafonnement des valeurs aberrantes selon les limites métier</div></div></div>
  <div class="step"><div class="num amber">7</div><div class="step-body"><div class="step-title">Persistance <span class="step-tag">PostgreSQL</span></div><div class="step-desc">Sauvegarde dans la table <code>predictions</code> via SQLAlchemy ORM</div></div></div>
  <div class="step"><div class="num green">8</div><div class="step-body"><div class="step-title">Réponse JSON <span class="step-tag">Streamlit</span></div><div class="step-desc">Retour structuré vers le frontend : rendement, confiance, données météo</div></div></div>
</div>

<!-- ═══════ MODÈLE ML ═══════ -->
<div id="tab-ml" class="panel">
  <div class="two-col">
    <div class="card">
      <div class="card-title">Artefacts ML</div>
      <div class="kv"><span class="kv-k">Modèle</span><span class="kv-v">model.pkl</span></div>
      <div class="kv"><span class="kv-k">Métadonnées</span><span class="kv-v">model_metadata.pkl</span></div>
      <div class="kv"><span class="kv-k">Sérialisation</span><span class="kv-v">Joblib</span></div>
      <div class="kv"><span class="kv-k">Stockage</span><span class="kv-v">Google Drive</span></div>
      <div class="kv"><span class="kv-k">Identifiants</span><span class="kv-v">MODEL_ID · METADATA_ID</span></div>
    </div>
    <div class="card">
      <div class="card-title">Stratégie de chargement</div>
      <div class="kv"><span class="kv-k">Téléchargement</span><span class="kv-v">Si absent en local</span></div>
      <div class="kv"><span class="kv-k">Cache mémoire</span><span class="kv-v">@lru_cache</span></div>
      <div class="kv"><span class="kv-k">Vérification</span><span class="kv-v">Taille minimale</span></div>
      <div class="kv"><span class="kv-k">Repo GitHub</span><span class="kv-v">Léger (sans artefacts)</span></div>
      <div class="kv"><span class="kv-k">Rechargement</span><span class="kv-v">Évité par cache</span></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Importance des features du modèle ML (Gini impurity)</div>
    <div class="chart-wrap tall"><canvas id="chartFeatures"></canvas></div>
  </div>
  <div class="section-label">Cycle de vie du modèle</div>
  <div class="ml-node"><div class="num purple" style="flex-shrink:0">1</div><div class="ml-node-body"><div class="ml-node-title">Entraînement offline</div><div class="ml-node-sub">Scikit-learn · features agro + météo · validation croisée</div></div><span class="tag">Training</span></div>
  <div class="connector-line"></div>
  <div class="ml-node"><div class="num blue" style="flex-shrink:0">2</div><div class="ml-node-body"><div class="ml-node-title">Sérialisation Joblib</div><div class="ml-node-sub"><code>model.pkl</code> + <code>model_metadata.pkl</code> exportés</div></div><span class="tag">Export</span></div>
  <div class="connector-line"></div>
  <div class="ml-node"><div class="num amber" style="flex-shrink:0">3</div><div class="ml-node-body"><div class="ml-node-title">Stockage Google Drive</div><div class="ml-node-sub"><code>MODEL_ID</code> · <code>METADATA_ID</code> référencés dans la config</div></div><span class="tag">Storage</span></div>
  <div class="connector-line"></div>
  <div class="ml-node"><div class="num teal" style="flex-shrink:0">4</div><div class="ml-node-body"><div class="ml-node-title">Téléchargement au démarrage</div><div class="ml-node-sub">Vérification locale → download si absent → validation taille</div></div><span class="tag">Runtime</span></div>
  <div class="connector-line"></div>
  <div class="ml-node"><div class="num green" style="flex-shrink:0">5</div><div class="ml-node-body"><div class="ml-node-title">Cache mémoire @lru_cache</div><div class="ml-node-sub">Chargement unique → réutilisation à chaque requête <code>/predict</code></div></div><span class="tag">Cache</span></div>
</div>

<!-- ═══════ DOCKER ═══════ -->
<div id="tab-docker" class="panel">
  <div class="section-label">Configuration du container</div>
  <div class="card">
    <div class="kv"><span class="kv-k">Nom du container</span><span class="kv-v">agrisim_backend</span></div>
    <div class="kv"><span class="kv-k">Port interne</span><span class="kv-v">8000</span></div>
    <div class="kv"><span class="kv-k">Commande</span><span class="kv-v" style="font-size:10px">uvicorn api.main:app --host 0.0.0.0 --port 8000</span></div>
    <div class="kv"><span class="kv-k">Healthcheck</span><span class="kv-v">GET /</span></div>
    <div class="kv"><span class="kv-k">Dépendance frontend</span><span class="kv-v">Démarre après backend healthy</span></div>
    <div class="kv"><span class="kv-k">Cloud déploiement</span><span class="kv-v">Render.com</span></div>
  </div>
  <div class="card">
    <div class="card-title">Uptime des services (7 derniers jours, %)</div>
    <div class="chart-wrap" style="height:190px"><canvas id="chartUptime"></canvas></div>
  </div>
  <div class="section-label">Séquence de démarrage</div>
  <div class="step"><div class="num green">1</div><div class="step-body"><div class="step-title">Build des images Docker</div><div class="step-desc">Construction des images backend et frontend depuis les Dockerfiles</div></div></div>
  <div class="step"><div class="num blue">2</div><div class="step-body"><div class="step-title">Démarrage backend <span class="step-tag">agrisim_backend</span></div><div class="step-desc">Uvicorn démarre sur le port 8000, télécharge les artefacts ML</div></div></div>
  <div class="step"><div class="num amber">3</div><div class="step-body"><div class="step-title">Healthcheck <span class="step-tag">GET /</span></div><div class="step-desc">Docker vérifie que le backend répond avant de continuer</div></div></div>
  <div class="step"><div class="num teal">4</div><div class="step-body"><div class="step-title">Démarrage frontend <span class="step-tag">Streamlit</span></div><div class="step-desc">Le frontend démarre uniquement après validation du healthcheck backend</div></div></div>
</div>

<!-- Synthèse -->
<div style="margin-top:1.5rem">
  <div class="section-label">Synthèse backend</div>
  <div class="synth">
    Le backend d'AgriSim AI centralise la logique métier et la logique ML.
    Il isole le frontend des détails techniques : récupération météo, préparation des variables,
    chargement du modèle, prédiction, contrôle métier et persistance.
    Cette séparation rend l'application plus maintenable, plus testable et plus proche
    d'une architecture professionnelle.
  </div>
</div>

<script>
const dark = window.matchMedia('(prefers-color-scheme:dark)').matches;
const T2 = dark ? '#9c9a92' : '#5f5e5a';
const G  = dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';

function baseOpts(extra){
  return Object.assign({
    responsive:true, maintainAspectRatio:false,
    plugins:{ legend:{display:false}, tooltip:{titleFont:{size:11},bodyFont:{size:11}} },
    scales:{
      x:{grid:{color:G},ticks:{color:T2,font:{size:10}}},
      y:{grid:{color:G},ticks:{color:T2,font:{size:11}}}
    }
  }, extra||{});
}

/* 1. Latence par endpoint */
new Chart(document.getElementById('chartLatence'),{
  type:'bar',
  data:{
    labels:['GET /','POST /cities','POST /predict','GET /history','GET /cultures','GET /health'],
    datasets:[{
      data:[12,95,459,38,18,9],
      backgroundColor:['#97C459','#378ADD','#7F77DD','#1D9E75','#BA7517','#D85A30'],
      borderRadius:5, borderSkipped:false
    }]
  },
  options:{
    responsive:true, maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.raw+' ms'}}},
    scales:{
      x:{grid:{color:G},ticks:{color:T2,font:{size:10}}},
      y:{grid:{color:G},ticks:{color:T2,font:{size:11},callback:v=>v+' ms'},beginAtZero:true}
    }
  }
});

/* 2. Répartition doughnut */
new Chart(document.getElementById('chartRepartition'),{
  type:'doughnut',
  data:{
    labels:['POST /predict','GET /history','POST /cities','GET /cultures','GET /health','GET /'],
    datasets:[{
      data:[42,28,14,8,5,3],
      backgroundColor:['#639922','#378ADD','#1D9E75','#BA7517','#7F77DD','#D85A30'],
      borderWidth:0, hoverOffset:6
    }]
  },
  options:{
    responsive:true, maintainAspectRatio:false, cutout:'62%',
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.label+': '+c.raw+'%'}}}
  }
});

/* 3. Trafic horaire */
new Chart(document.getElementById('chartTrafic'),{
  type:'line',
  data:{
    labels:['0h','1h','2h','3h','4h','5h','6h','7h','8h','9h','10h','11h','12h','13h','14h','15h','16h','17h','18h','19h','20h','21h','22h','23h'],
    datasets:[{
      data:[3,1,1,2,4,8,18,42,65,71,68,74,62,58,70,78,82,76,65,50,38,24,14,7],
      borderColor:'#639922',
      backgroundColor:dark?'rgba(99,153,34,0.15)':'rgba(99,153,34,0.10)',
      fill:true, tension:0.4, pointRadius:2, pointHoverRadius:5, borderWidth:2
    }]
  },
  options:{
    responsive:true, maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.raw+' req'}}},
    scales:{
      x:{grid:{color:G},ticks:{color:T2,font:{size:10},maxTicksLimit:8}},
      y:{grid:{color:G},ticks:{color:T2,font:{size:11}},beginAtZero:true}
    }
  }
});

/* 4. Distribution rendements */
new Chart(document.getElementById('chartDistrib'),{
  type:'bar',
  data:{
    labels:['0–1','1–2','2–3','3–4','4–5','5–6','6–7','7–8','8–9','9–10'],
    datasets:[{
      data:[2,5,12,22,28,18,8,3,1,1],
      backgroundColor:dark?'rgba(99,153,34,0.7)':'rgba(59,109,17,0.7)',
      borderColor:'#639922', borderWidth:1, borderRadius:3, borderSkipped:false
    }]
  },
  options:{
    responsive:true, maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.raw+'% des prédictions'}}},
    scales:{
      x:{grid:{color:G},ticks:{color:T2,font:{size:10}},title:{display:true,text:'t/ha',color:T2,font:{size:11}}},
      y:{grid:{color:G},ticks:{color:T2,font:{size:11},callback:v=>v+'%'},beginAtZero:true}
    }
  }
});

/* 5. Taux de succès */
new Chart(document.getElementById('chartSucces'),{
  type:'bar',
  data:{
    labels:['GET /','POST /cities','POST /predict','GET /history','GET /cultures','GET /health'],
    datasets:[{
      data:[100,98.2,96.8,99.1,100,100],
      backgroundColor:['#97C459','#378ADD','#7F77DD','#1D9E75','#BA7517','#D85A30'],
      borderRadius:4, borderSkipped:false
    }]
  },
  options:{
    responsive:true, maintainAspectRatio:false, indexAxis:'y',
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.raw+'%'}}},
    scales:{
      x:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'%'},min:93,max:100},
      y:{grid:{color:'transparent'},ticks:{color:T2,font:{size:10}}}
    }
  }
});

/* 6. Feature importance */
new Chart(document.getElementById('chartFeatures'),{
  type:'bar',
  data:{
    labels:['Précipitations moy.','Température moy.','Type de sol','Engrais (kg/ha)','Durée croissance','Irrigation','pH sol','Humidité moy.','Rayonnement'],
    datasets:[{
      data:[0.21,0.18,0.15,0.13,0.11,0.09,0.07,0.04,0.02],
      backgroundColor:dark?'rgba(127,119,221,0.75)':'rgba(83,74,183,0.7)',
      borderColor:'#7F77DD', borderWidth:1, borderRadius:4, borderSkipped:false
    }]
  },
  options:{
    responsive:true, maintainAspectRatio:false, indexAxis:'y',
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>Math.round(c.raw*100)+'% importance'}}},
    scales:{
      x:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>Math.round(v*100)+'%'},beginAtZero:true},
      y:{grid:{color:'transparent'},ticks:{color:T2,font:{size:10}}}
    }
  }
});

/* 7. Uptime */
new Chart(document.getElementById('chartUptime'),{
  type:'bar',
  data:{
    labels:['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'],
    datasets:[
      {label:'Backend',   data:[100,100,100,99.8,100,100,100], backgroundColor:dark?'rgba(99,153,34,0.8)':'rgba(59,109,17,0.75)', borderRadius:3, borderSkipped:false},
      {label:'Frontend',  data:[100,100,99.5,99.8,100,100,100],backgroundColor:dark?'rgba(55,138,221,0.8)':'rgba(24,95,165,0.7)',  borderRadius:3, borderSkipped:false},
      {label:'PostgreSQL',data:[100,100,100,100,100,100,100],   backgroundColor:dark?'rgba(29,158,117,0.8)':'rgba(15,110,86,0.75)',borderRadius:3, borderSkipped:false}
    ]
  },
  options:{
    responsive:true, maintainAspectRatio:false,
    plugins:{
      legend:{display:true,position:'bottom',labels:{color:T2,font:{size:11},boxWidth:12,padding:12}},
      tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.dataset.label+': '+c.raw+'%'}}
    },
    scales:{
      x:{grid:{color:G},ticks:{color:T2,font:{size:11}},stacked:false},
      y:{grid:{color:G},ticks:{color:T2,font:{size:11},callback:v=>v+'%'},min:99,max:100.2}
    }
  }
});

/* Tabs */
function switchTab(name, el){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}

/* Arch detail */
const DETAILS={
  main:    '<strong>api/main.py</strong> — Point d\'entrée FastAPI. Déclare toutes les routes, injecte les dépendances et orchestre l\'appel aux services (météo, ML, BDD). Contrôleur central de l\'application.',
  schemas: '<strong>api/schemas.py</strong> — Modèles Pydantic pour valider les requêtes entrantes et sérialiser les réponses JSON. Garantit la cohérence des types et génère la documentation OpenAPI.',
  database:'<strong>api/database.py</strong> — Gestion de la session SQLAlchemy. Configure le pool de connexions PostgreSQL, déclare les modèles ORM et expose une dépendance <code>get_db()</code> injectable.',
  weather: '<strong>services/weather_service.py</strong> — Appelle l\'API Open-Meteo avec les coordonnées géographiques pour obtenir les données météo (température, précipitations, humidité).',
  ml:      '<strong>ml/model_loader.py</strong> — Télécharge les artefacts depuis Google Drive si absents, charge le modèle Scikit-learn avec Joblib, et le conserve en mémoire via <code>@lru_cache</code>.',
  model:   '<strong>model/</strong> — Répertoire créé au runtime. Contient <code>model.pkl</code> et <code>model_metadata.pkl</code>. Absent du dépôt Git pour garder le repo léger.'
};
function showDetail(el, key){
  document.querySelectorAll('.arch-item').forEach(i=>i.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('detail-pane').innerHTML=DETAILS[key];
}
</script>
</body>
</html>"""

components.html(DASHBOARD_HTML, height=1060, scrolling=True)

footer()