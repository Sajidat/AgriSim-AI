# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# pages/8_Architecture_Deployment.py — AgriSim AI
# Module : Architecture globale & Déploiement
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import streamlit.components.v1 as components

from utils import CSS, sidebar_logo, footer


st.set_page_config(
    page_title="Architecture & Déploiement — AgriSim AI",
    page_icon="🏗️",
    layout="wide",
)

st.markdown(CSS, unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    sidebar_logo()

    st.page_link("app.py",                              label="🏠  Accueil")
    st.page_link("pages/1_Dashboard.py",                label="📊  Dashboard")
    st.page_link("pages/2_Prediction.py",               label="🌱  Prédiction")
    st.page_link("pages/3_Historique.py",               label="📋  Historique")
    st.page_link("pages/4_IA_Explicable.py",            label="🔍  IA Explicable")
    st.page_link("pages/5_Performances_ML.py",          label="⚙️  Performances ML")
    st.page_link("pages/6_Data_ML_Pipeline.py",         label="🗄️  Data & ML Pipeline")
    st.page_link("pages/7_Backend_API.py",              label="⚙️  Backend & API")
    st.page_link("pages/8_Architecture_Deployment.py",  label="🏗️  Architecture")
    st.page_link("pages/9_Frontend_UI.py",              label="🎨  Frontend & UX")
    st.page_link("pages/10_Formulaire_Complet.py", label="📝  Formulaire complet")


# ── Titre ─────────────────────────────────────────────────────
st.markdown(
    """
    <div class="section-header">Architecture & Déploiement</div>
    <p class="section-sub">
        Structure globale d'AgriSim AI : services, communication,
        conteneurisation Docker et stratégie de déploiement cloud.
    </p>
    """,
    unsafe_allow_html=True,
)

# ── Dashboard interactif ──────────────────────────────────────
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
  --border:rgba(0,0,0,0.09);--border2:rgba(0,0,0,0.17);
  --r:8px;--rl:12px;
  --green-50:#EAF3DE;--green-100:#C0DD97;--green-200:#97C459;
  --green-400:#639922;--green-600:#3B6D11;--green-800:#27500A;
  --teal-50:#E1F5EE;--teal-100:#9FE1CB;--teal-400:#1D9E75;--teal-600:#0F6E56;--teal-800:#085041;
  --amber-50:#FAEEDA;--amber-100:#FAC775;--amber-400:#BA7517;--amber-800:#633806;
  --blue-50:#E6F1FB;--blue-100:#B5D4F4;--blue-400:#378ADD;--blue-600:#185FA5;--blue-800:#0C447C;
  --purple-50:#EEEDFE;--purple-100:#CECBF6;--purple-400:#7F77DD;--purple-600:#534AB7;--purple-800:#3C3489;
  --coral-50:#FAECE7;--coral-100:#F5C4B3;--coral-400:#D85A30;--coral-600:#993C1D;--coral-800:#712B13;
  --slate-50:#EEF0F5;--slate-100:#CDD2DF;--slate-400:#6B7494;--slate-600:#3D4A6B;--slate-800:#252D47;
}
@media(prefers-color-scheme:dark){:root{
  --bg:#1e1d1b;--bg2:#28271f;--bg3:#302f27;
  --text:#e8e6df;--text2:#9c9a92;--text3:#6b6a64;
  --border:rgba(255,255,255,0.09);--border2:rgba(255,255,255,0.17);
  --green-50:#1a2910;--green-100:#2f4a1b;--green-600:#7db83a;--green-800:#b8e07a;
  --teal-50:#0a2218;--teal-100:#0e3828;--teal-600:#3ecfa0;--teal-800:#9ae8d0;
  --amber-50:#2a1e08;--amber-100:#3d2d0a;--amber-400:#d4922a;--amber-800:#f5cc7a;
  --blue-50:#0a1e30;--blue-100:#0d3050;--blue-400:#5ca8f0;--blue-600:#8dc6f7;--blue-800:#c0dffb;
  --purple-50:#1a1838;--purple-100:#2e2860;--purple-400:#9b94e8;--purple-800:#e0dcfd;
  --coral-50:#2a1008;--coral-100:#401810;--coral-400:#e8784a;--coral-800:#fcd3be;
  --slate-50:#1a1d26;--slate-100:#252a3a;--slate-400:#8891b0;--slate-600:#a8b2cf;--slate-800:#d0d5e8;
}}
body{font-family:var(--font);font-size:14px;color:var(--text);background:var(--bg);padding:1.25rem 1rem 2.5rem;line-height:1.5}

/* ── Metrics ── */
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(115px,1fr));gap:10px;margin-bottom:1.5rem}
.metric{background:var(--bg2);border-radius:var(--r);padding:11px 13px}
.metric .lbl{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px}
.metric .val{font-size:15px;font-weight:500}
.metric .sub{font-size:10px;color:var(--text3);margin-top:1px}
.green .val{color:var(--green-600)}.blue .val{color:var(--blue-600)}
.amber .val{color:var(--amber-400)}.teal .val{color:var(--teal-600)}
.purple .val{color:var(--purple-600)}.slate .val{color:var(--slate-600)}

/* ── Tabs ── */
.tabs{display:flex;flex-wrap:wrap;gap:2px;border-bottom:0.5px solid var(--border);margin-bottom:1.5rem}
.tab{font-size:13px;padding:8px 13px;cursor:pointer;border:none;background:none;color:var(--text2);border-bottom:2px solid transparent;margin-bottom:-0.5px;border-radius:4px 4px 0 0;transition:color .15s,background .15s,border-color .15s;font-family:var(--font)}
.tab:hover{color:var(--text);background:var(--bg2)}
.tab.active{color:var(--slate-600);border-bottom-color:var(--slate-400);font-weight:500}
.panel{display:none}.panel.active{display:block}

/* ── Layout ── */
.slbl{font-size:11px;font-weight:500;color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px}
.card{background:var(--bg);border:0.5px solid var(--border);border-radius:var(--rl);padding:1rem 1.25rem;margin-bottom:1rem}
.card-title{font-size:12px;font-weight:500;color:var(--text2);margin-bottom:10px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.three-col{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
@media(max-width:560px){.two-col,.three-col{grid-template-columns:1fr}}
.chart-wrap{position:relative}
.h160{height:160px}.h200{height:200px}.h240{height:240px}.h280{height:280px}.h320{height:320px}
code{font-family:'SFMono-Regular',Consolas,monospace;font-size:11px;background:var(--bg2);padding:2px 6px;border-radius:4px;color:var(--text)}

/* ── KV ── */
.kv{display:flex;justify-content:space-between;align-items:flex-start;padding:8px 0;border-bottom:0.5px solid var(--border);font-size:12px;gap:12px}
.kv:last-child{border-bottom:none}
.kv-k{color:var(--text2);white-space:nowrap;flex-shrink:0}
.kv-v{font-family:'SFMono-Regular',Consolas,monospace;font-size:11px;text-align:right}

/* ── Architecture diagram ── */
.arch-diagram{position:relative;width:100%;padding:1.5rem 1rem}

/* layers */
.layer{border-radius:var(--r);margin-bottom:12px;overflow:hidden}
.layer-label{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;padding:6px 14px;border-bottom:0.5px solid var(--border)}
.layer-body{display:flex;gap:10px;padding:10px 14px;flex-wrap:wrap;align-items:stretch}

.layer.cloud  .layer-label{background:var(--blue-50);  color:var(--blue-800);  border-color:var(--blue-100);}
.layer.cloud  {border:0.5px solid var(--blue-100);}
.layer.docker .layer-label{background:var(--slate-50); color:var(--slate-600); border-color:var(--slate-100);}
.layer.docker {border:0.5px solid var(--slate-100);}
.layer.ext    .layer-label{background:var(--amber-50); color:var(--amber-800); border-color:var(--amber-100);}
.layer.ext    {border:0.5px solid var(--amber-100);}
.layer.data   .layer-label{background:var(--green-50); color:var(--green-800); border-color:var(--green-100);}
.layer.data   {border:0.5px solid var(--green-100);}

/* service boxes */
.svc{flex:1;min-width:120px;border-radius:6px;padding:10px 12px;border:0.5px solid var(--border2);cursor:pointer;transition:transform .15s,box-shadow .15s;position:relative}
.svc:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.12)}
.svc.selected{outline:2px solid var(--blue-400);outline-offset:1px}
.svc-icon{font-size:18px;margin-bottom:5px}
.svc-name{font-size:12px;font-weight:600;margin-bottom:2px}
.svc-tech{font-size:10px;opacity:.75;margin-bottom:4px}
.svc-port{display:inline-block;font-size:9px;padding:1px 6px;border-radius:3px;background:var(--bg3);border:0.5px solid var(--border2);color:var(--text3)}

.svc.frontend {background:var(--purple-50);border-color:var(--purple-100)}
.svc.frontend .svc-name{color:var(--purple-800)}
.svc.backend  {background:var(--blue-50);  border-color:var(--blue-100)}
.svc.backend  .svc-name{color:var(--blue-800)}
.svc.database {background:var(--amber-50); border-color:var(--amber-100)}
.svc.database .svc-name{color:var(--amber-800)}
.svc.ml       {background:var(--green-50); border-color:var(--green-100)}
.svc.ml       .svc-name{color:var(--green-800)}
.svc.weather  {background:var(--teal-50);  border-color:var(--teal-100)}
.svc.weather  .svc-name{color:var(--teal-800)}
.svc.gdrive   {background:var(--coral-50); border-color:var(--coral-100)}
.svc.gdrive   .svc-name{color:var(--coral-800)}
.svc.github   {background:var(--slate-50); border-color:var(--slate-100)}
.svc.github   .svc-name{color:var(--slate-600)}
.svc.render   {background:var(--blue-50);  border-color:var(--blue-100)}
.svc.render   .svc-name{color:var(--blue-800)}

/* arrows between layers */
.arrows{display:flex;justify-content:center;gap:40px;margin:4px 0;padding:0 14px;flex-wrap:wrap}
.arr{display:flex;flex-direction:column;align-items:center;gap:1px;font-size:10px;color:var(--text3);min-width:80px}
.arr-line{width:1px;height:18px;background:var(--border2);position:relative}
.arr-line::after{content:'▼';position:absolute;bottom:-6px;left:-4px;font-size:8px;color:var(--border2)}
.arr-label{font-size:9px;color:var(--text3)}

/* detail panel */
.svc-detail{background:var(--bg2);border-radius:var(--r);padding:12px 14px;font-size:12px;line-height:1.7;color:var(--text2);min-height:60px;transition:all .2s;margin-top:4px}
.svc-detail strong{color:var(--text);font-weight:500}

/* ── Flow steps ── */
.flow-step{display:flex;gap:12px;align-items:flex-start;padding:10px 8px;border-radius:var(--r);border-bottom:0.5px solid var(--border);transition:background .12s}
.flow-step:last-child{border-bottom:none}
.fnum{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;flex-shrink:0;margin-top:1px}
.n-blue   {background:var(--blue-50);  color:var(--blue-800)  }
.n-green  {background:var(--green-50); color:var(--green-800) }
.n-amber  {background:var(--amber-50); color:var(--amber-800) }
.n-teal   {background:var(--teal-50);  color:var(--teal-800)  }
.n-purple {background:var(--purple-50);color:var(--purple-800)}
.n-coral  {background:var(--coral-50); color:var(--coral-800) }
.n-slate  {background:var(--slate-50); color:var(--slate-600) }
.fb{flex:1}.ft{font-size:13px;font-weight:500;margin-bottom:2px}.fd{font-size:12px;color:var(--text2)}
.ftag{display:inline-block;font-size:10px;padding:1px 7px;border-radius:4px;border:0.5px solid var(--border2);color:var(--text3);margin-left:6px;vertical-align:middle}

/* ── Env var table ── */
.env-row{display:grid;grid-template-columns:160px 1fr;gap:12px;padding:8px 0;border-bottom:0.5px solid var(--border);font-size:12px;align-items:center}
.env-row:last-child{border-bottom:none}
.env-key{font-family:'SFMono-Regular',Consolas,monospace;font-size:11px;background:var(--bg2);padding:2px 8px;border-radius:4px;color:var(--text);border:0.5px solid var(--border2);display:inline-block}
.env-val{color:var(--text2);font-size:12px}
.env-badge{display:inline-block;font-size:9px;padding:1px 6px;border-radius:3px;margin-left:6px;font-weight:500;vertical-align:middle}
.env-badge.req{background:var(--coral-50);color:var(--coral-800);border:0.5px solid var(--coral-100)}
.env-badge.opt{background:var(--green-50);color:var(--green-800);border:0.5px solid var(--green-100)}

/* ── Legend ── */
.legend{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:8px}
.li{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text2)}
.ldot{width:10px;height:10px;border-radius:50%;flex-shrink:0}

/* ── Synth ── */
.synth{border-left:2px solid var(--slate-400);padding:12px 16px;border-radius:0 var(--r) var(--r) 0;background:var(--slate-50);font-size:13px;color:var(--slate-600);line-height:1.7}
</style>
</head>
<body>

<!-- Métriques -->
<div class="metrics">
  <div class="metric slate"><div class="lbl">Services</div><div class="val">4</div><div class="sub">containers</div></div>
  <div class="metric blue"><div class="lbl">Backend</div><div class="val">FastAPI</div><div class="sub">port 8000</div></div>
  <div class="metric purple"><div class="lbl">Frontend</div><div class="val">Streamlit</div><div class="sub">port 8501</div></div>
  <div class="metric amber"><div class="lbl">Base</div><div class="val">PostgreSQL</div><div class="sub">port 5432</div></div>
  <div class="metric green"><div class="lbl">Modèle ML</div><div class="val">Google Drive</div><div class="sub">Joblib</div></div>
  <div class="metric teal"><div class="lbl">Météo</div><div class="val">Open-Meteo</div><div class="sub">REST API</div></div>
</div>

<!-- Onglets -->
<div class="tabs">
  <button class="tab active" onclick="switchTab('archi',this)">Architecture</button>
  <button class="tab" onclick="switchTab('docker',this)">Docker</button>
  <button class="tab" onclick="switchTab('deploy',this)">Déploiement</button>
  <button class="tab" onclick="switchTab('env',this)">Variables Env.</button>
  <button class="tab" onclick="switchTab('perf',this)">Performances</button>
</div>


<!-- ══════════════════ ARCHITECTURE ══════════════════ -->
<div id="tab-archi" class="panel active">

  <div class="slbl">Schéma d'architecture — cliquez sur un service</div>

  <!-- Couche Cloud -->
  <div class="layer cloud">
    <div class="layer-label">☁️ Cloud — Render.com / Hugging Face Spaces</div>
    <div class="layer-body">
      <div class="svc frontend" onclick="showSvc(this,'frontend')">
        <div class="svc-icon">🎨</div>
        <div class="svc-name">Frontend</div>
        <div class="svc-tech">Streamlit · Python</div>
        <span class="svc-port">:8501</span>
      </div>
      <div class="svc backend" onclick="showSvc(this,'backend')">
        <div class="svc-icon">⚙️</div>
        <div class="svc-name">Backend</div>
        <div class="svc-tech">FastAPI · Uvicorn</div>
        <span class="svc-port">:8000</span>
      </div>
      <div class="svc database" onclick="showSvc(this,'database')">
        <div class="svc-icon">🗄️</div>
        <div class="svc-name">PostgreSQL</div>
        <div class="svc-tech">SQLAlchemy ORM</div>
        <span class="svc-port">:5432</span>
      </div>
      <div class="svc ml" onclick="showSvc(this,'ml')">
        <div class="svc-icon">🤖</div>
        <div class="svc-name">Modèle ML</div>
        <div class="svc-tech">Scikit-learn · Joblib</div>
        <span class="svc-port">runtime</span>
      </div>
    </div>
  </div>

  <!-- Flèches -->
  <div class="arrows">
    <div class="arr"><div class="arr-line"></div><div class="arr-label">HTTP REST</div></div>
    <div class="arr"><div class="arr-line"></div><div class="arr-label">SQLAlchemy</div></div>
    <div class="arr"><div class="arr-line"></div><div class="arr-label">lru_cache</div></div>
  </div>

  <!-- Couche Services externes -->
  <div class="layer ext">
    <div class="layer-label">🌐 Services externes</div>
    <div class="layer-body">
      <div class="svc weather" onclick="showSvc(this,'weather')">
        <div class="svc-icon">🌦️</div>
        <div class="svc-name">Open-Meteo</div>
        <div class="svc-tech">REST API · Météo</div>
        <span class="svc-port">HTTPS</span>
      </div>
      <div class="svc gdrive" onclick="showSvc(this,'gdrive')">
        <div class="svc-icon">📦</div>
        <div class="svc-name">Google Drive</div>
        <div class="svc-tech">model.pkl · metadata</div>
        <span class="svc-port">download</span>
      </div>
      <div class="svc github" onclick="showSvc(this,'github')">
        <div class="svc-icon">🐙</div>
        <div class="svc-name">GitHub</div>
        <div class="svc-tech">Code source · CI/CD</div>
        <span class="svc-port">git push</span>
      </div>
    </div>
  </div>

  <div class="svc-detail" id="svc-detail">Cliquez sur un service pour afficher ses détails techniques.</div>

  <!-- Flux de communication en texte -->
  <div style="margin-top:1rem">
    <div class="slbl">Flux de communication</div>
    <div class="two-col">
      <div class="card">
        <div class="card-title">Flux entrant (requêtes)</div>
        <div class="kv"><span class="kv-k">Utilisateur → Frontend</span><span class="kv-v">HTTPS / navigateur</span></div>
        <div class="kv"><span class="kv-k">Frontend → Backend</span><span class="kv-v">HTTP REST (requests)</span></div>
        <div class="kv"><span class="kv-k">Backend → Open-Meteo</span><span class="kv-v">GET coords + dates</span></div>
        <div class="kv"><span class="kv-k">Backend → PostgreSQL</span><span class="kv-v">INSERT prediction</span></div>
        <div class="kv"><span class="kv-k">Backend → Google Drive</span><span class="kv-v">Download model.pkl</span></div>
      </div>
      <div class="card">
        <div class="card-title">Flux sortant (réponses)</div>
        <div class="kv"><span class="kv-k">Open-Meteo → Backend</span><span class="kv-v">JSON météo (temp, rain…)</span></div>
        <div class="kv"><span class="kv-k">ML → Backend</span><span class="kv-v">float rendement (t/ha)</span></div>
        <div class="kv"><span class="kv-k">PostgreSQL → Backend</span><span class="kv-v">Historique prédictions</span></div>
        <div class="kv"><span class="kv-k">Backend → Frontend</span><span class="kv-v">JSON structuré</span></div>
        <div class="kv"><span class="kv-k">Frontend → Utilisateur</span><span class="kv-v">UI Streamlit rendue</span></div>
      </div>
    </div>
  </div>
</div><!-- /archi -->


<!-- ══════════════════ DOCKER ══════════════════ -->
<div id="tab-docker" class="panel">

  <div class="two-col">
    <!-- Timeline démarrage -->
    <div class="card">
      <div class="card-title">Séquence de démarrage Docker Compose</div>
      <div class="flow-step"><div class="fnum n-slate">1</div><div class="fb"><div class="ft">Build des images <span class="ftag">Dockerfile</span></div><div class="fd">Construction des images backend et frontend depuis le code source</div></div></div>
      <div class="flow-step"><div class="fnum n-amber">2</div><div class="fb"><div class="ft">Démarrage PostgreSQL <span class="ftag">:5432</span></div><div class="fd">La base de données démarre en premier, volume persistant monté</div></div></div>
      <div class="flow-step"><div class="fnum n-blue">3</div><div class="fb"><div class="ft">Démarrage Backend <span class="ftag">:8000</span></div><div class="fd">FastAPI + Uvicorn démarre, télécharge model.pkl depuis Google Drive</div></div></div>
      <div class="flow-step"><div class="fnum n-green">4</div><div class="fb"><div class="ft">Healthcheck Backend <span class="ftag">GET /</span></div><div class="fd">Docker Poll : interval 10s, retries 5, timeout 5s</div></div></div>
      <div class="flow-step"><div class="fnum n-purple">5</div><div class="fb"><div class="ft">Démarrage Frontend <span class="ftag">:8501</span></div><div class="fd">Streamlit démarre uniquement après backend healthy</div></div></div>
      <div class="flow-step"><div class="fnum n-teal">6</div><div class="fb"><div class="ft">Application disponible <span class="ftag">✓</span></div><div class="fd">Tous les services sont opérationnels, l'utilisateur peut se connecter</div></div></div>
    </div>

    <!-- Config Docker -->
    <div>
      <div class="card">
        <div class="card-title">Configuration des services</div>
        <div class="kv"><span class="kv-k">backend</span><span class="kv-v">image: agrisim_backend · port: 8000</span></div>
        <div class="kv"><span class="kv-k">frontend</span><span class="kv-v">image: agrisim_frontend · port: 8501</span></div>
        <div class="kv"><span class="kv-k">db</span><span class="kv-v">postgres:15 · port: 5432 · volume</span></div>
        <div class="kv"><span class="kv-k">network</span><span class="kv-v">agrisim_net (bridge interne)</span></div>
        <div class="kv"><span class="kv-k">restart</span><span class="kv-v">unless-stopped</span></div>
        <div class="kv"><span class="kv-k">healthcheck</span><span class="kv-v">curl -f http://backend:8000/</span></div>
      </div>
      <div class="card">
        <div class="card-title">Dépendances entre services</div>
        <div class="chart-wrap h160"><canvas id="chartDeps"></canvas></div>
      </div>
    </div>
  </div>

  <!-- Comparaison local vs prod -->
  <div class="card" style="margin-top:0">
    <div class="card-title">Comparaison environnements</div>
    <div class="chart-wrap h200"><canvas id="chartEnvs"></canvas></div>
  </div>
</div><!-- /docker -->


<!-- ══════════════════ DÉPLOIEMENT ══════════════════ -->
<div id="tab-deploy" class="panel">

  <div class="two-col">
    <!-- Pipeline CI/CD -->
    <div class="card">
      <div class="card-title">Pipeline de déploiement</div>
      <div class="flow-step"><div class="fnum n-slate">1</div><div class="fb"><div class="ft">Développement local <span class="ftag">Docker Compose</span></div><div class="fd">Tests locaux avec docker-compose up, hot-reload activé</div></div></div>
      <div class="flow-step"><div class="fnum n-slate">2</div><div class="fb"><div class="ft">Push GitHub <span class="ftag">main branch</span></div><div class="fd">Code versionné, <code>.gitignore</code> exclut les artefacts ML lourds</div></div></div>
      <div class="flow-step"><div class="fnum n-blue">3</div><div class="fb"><div class="ft">Build Docker <span class="ftag">Render.com</span></div><div class="fd">Render détecte le push, build l'image Docker automatiquement</div></div></div>
      <div class="flow-step"><div class="fnum n-green">4</div><div class="fb"><div class="ft">Déploiement Backend <span class="ftag">render.com/api</span></div><div class="fd">Backend FastAPI déployé, télécharge model.pkl depuis Drive au 1er démarrage</div></div></div>
      <div class="flow-step"><div class="fnum n-purple">5</div><div class="fb"><div class="ft">Déploiement Frontend <span class="ftag">HF Spaces</span></div><div class="fd">Streamlit déployé, <code>API_URL</code> pointe vers le backend Render</div></div></div>
      <div class="flow-step"><div class="fnum n-teal">6</div><div class="fb"><div class="ft">Monitoring <span class="ftag">GET /health</span></div><div class="fd">Render surveille le healthcheck, redémarre automatiquement si nécessaire</div></div></div>
    </div>

    <!-- Stratégie déploiement -->
    <div>
      <div class="card">
        <div class="card-title">Stratégie par composant</div>
        <div class="kv"><span class="kv-k">Code source</span><span class="kv-v">GitHub (versioning)</span></div>
        <div class="kv"><span class="kv-k">Backend API</span><span class="kv-v">Render.com (Docker)</span></div>
        <div class="kv"><span class="kv-k">Frontend UI</span><span class="kv-v">Streamlit Cloud / HF Spaces</span></div>
        <div class="kv"><span class="kv-k">Base PostgreSQL</span><span class="kv-v">Render PostgreSQL managed</span></div>
        <div class="kv"><span class="kv-k">Modèle ML</span><span class="kv-v">Google Drive (download runtime)</span></div>
        <div class="kv"><span class="kv-k">Avantage</span><span class="kv-v">Repo léger, déploiement rapide</span></div>
      </div>
      <div class="card">
        <div class="card-title">Avantages de l'architecture</div>
        <div class="chart-wrap h180"><canvas id="chartAvantages"></canvas></div>
      </div>
    </div>
  </div>

  <!-- Timeline déploiement -->
  <div class="card">
    <div class="card-title">Temps de déploiement estimé par étape (secondes)</div>
    <div class="chart-wrap h200"><canvas id="chartDeployTime"></canvas></div>
  </div>
</div><!-- /deploy -->


<!-- ══════════════════ VARIABLES ENV ══════════════════ -->
<div id="tab-env" class="panel">

  <div class="two-col">
    <div class="card">
      <div class="card-title">Variables Backend</div>
      <div class="env-row"><span class="env-key">DATABASE_URL</span><span class="env-val">Connexion PostgreSQL (SQLAlchemy)<span class="env-badge req">requis</span></span></div>
      <div class="env-row"><span class="env-key">MODEL_ID</span><span class="env-val">ID Google Drive du fichier model.pkl<span class="env-badge req">requis</span></span></div>
      <div class="env-row"><span class="env-key">METADATA_ID</span><span class="env-val">ID Google Drive des métadonnées ML<span class="env-badge req">requis</span></span></div>
      <div class="env-row"><span class="env-key">ENV</span><span class="env-val">production | development<span class="env-badge opt">optionnel</span></span></div>
      <div class="env-row"><span class="env-key">LOG_LEVEL</span><span class="env-val">info | debug | warning<span class="env-badge opt">optionnel</span></span></div>
    </div>
    <div class="card">
      <div class="card-title">Variables Frontend</div>
      <div class="env-row"><span class="env-key">API_URL</span><span class="env-val">URL du backend FastAPI<span class="env-badge req">requis</span></span></div>
      <div class="env-row"><span class="env-key">API_TIMEOUT</span><span class="env-val">Timeout requêtes HTTP (défaut: 10s)<span class="env-badge opt">optionnel</span></span></div>
      <div class="env-row"><span class="env-key">DEBUG</span><span class="env-val">Affichage logs frontend<span class="env-badge opt">optionnel</span></span></div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Répartition variables par service & criticité</div>
    <div class="chart-wrap h220"><canvas id="chartEnvVars"></canvas></div>
  </div>

  <div class="card">
    <div class="card-title">Exemple .env (développement local)</div>
    <pre style="font-family:'SFMono-Regular',Consolas,monospace;font-size:11px;color:var(--text2);line-height:1.8;overflow-x:auto"># Backend
DATABASE_URL=postgresql://agrisim:password@localhost:5432/agrisim_db
MODEL_ID=1aBcDeFgHiJkLmNoPqRsTuVwXyZ
METADATA_ID=1ZyXwVuTsRqPoNmLkJiHgFeDcBa
ENV=development
LOG_LEVEL=debug

# Frontend
API_URL=http://localhost:8000
API_TIMEOUT=10
DEBUG=true</pre>
  </div>
</div><!-- /env -->


<!-- ══════════════════ PERFORMANCES ══════════════════ -->
<div id="tab-perf" class="panel">

  <div class="two-col">
    <!-- Latence par service -->
    <div class="card">
      <div class="card-title">Latence de démarrage par service (secondes)</div>
      <div class="chart-wrap h220"><canvas id="chartStartup"></canvas></div>
    </div>
    <!-- Charge mémoire -->
    <div class="card">
      <div class="card-title">Consommation mémoire par service (MB)</div>
      <div class="chart-wrap h220"><canvas id="chartMemory"></canvas></div>
    </div>
  </div>

  <div class="two-col">
    <!-- Uptime 30 jours -->
    <div class="card">
      <div class="card-title">Uptime des services (30 derniers jours, %)</div>
      <div class="chart-wrap h200"><canvas id="chartUptime"></canvas></div>
    </div>
    <!-- Taille des images Docker -->
    <div class="card">
      <div class="card-title">Taille des images Docker (MB)</div>
      <div class="chart-wrap h200"><canvas id="chartImageSize"></canvas></div>
    </div>
  </div>
</div><!-- /perf -->


<!-- Synthèse -->
<div style="margin-top:1.5rem">
  <div class="slbl">Synthèse architecture</div>
  <div class="synth">
    L'architecture d'AgriSim AI suit les standards modernes du développement cloud-native :
    séparation stricte frontend/backend, API REST stateless, conteneurisation Docker complète,
    externalisation des artefacts ML lourds, et déploiement automatisé.
    Cette approche garantit scalabilité, maintenabilité et reproductibilité entre
    les environnements de développement et de production.
  </div>
</div>

<script>
const dark = window.matchMedia('(prefers-color-scheme:dark)').matches;
const T2 = dark?'#9c9a92':'#5f5e5a';
const G  = dark?'rgba(255,255,255,0.06)':'rgba(0,0,0,0.06)';

function bOpts(x){ return Object.assign({responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11}}},scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10}}},y:{grid:{color:G},ticks:{color:T2,font:{size:11}}}}},x||{}); }

/* ── Dépendances services (grouped bar) ── */
new Chart(document.getElementById('chartDeps'),{
  type:'bar',
  data:{
    labels:['PostgreSQL','Backend','Frontend'],
    datasets:[
      {label:'Ordre démarrage', data:[1,2,3], backgroundColor:['#BA7517','#378ADD','#7F77DD'],borderRadius:5,borderSkipped:false}
    ]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>'Étape '+c.raw}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10}},min:0,max:4}}
  }
});

/* ── Comparaison environnements ── */
new Chart(document.getElementById('chartEnvs'),{
  type:'bar',
  data:{
    labels:['Démarrage (s)','RAM Backend (MB)','RAM Frontend (MB)','Latence /predict (ms)','Uptime (%)'],
    datasets:[
      {label:'Local',      data:[8,180,120,250,99.5], backgroundColor:dark?'rgba(127,119,221,0.7)':'rgba(83,74,183,0.6)',borderRadius:4,borderSkipped:false},
      {label:'Production', data:[45,220,140,459,99.2], backgroundColor:dark?'rgba(55,138,221,0.7)':'rgba(24,95,165,0.6)',borderRadius:4,borderSkipped:false}
    ]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:true,position:'bottom',labels:{color:T2,font:{size:11},boxWidth:12,padding:10}},tooltip:{titleFont:{size:11},bodyFont:{size:11}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10}},beginAtZero:true}}
  }
});

/* ── Avantages radar ── */
new Chart(document.getElementById('chartAvantages'),{
  type:'radar',
  data:{
    labels:['Scalabilité','Maintenabilité','Sécurité','Performance','Reproductibilité','CI/CD'],
    datasets:[{
      data:[4.2,4.5,3.8,4.0,4.6,4.1],
      backgroundColor:dark?'rgba(55,138,221,0.2)':'rgba(24,95,165,0.12)',
      borderColor:'#378ADD',borderWidth:2,pointBackgroundColor:'#378ADD',pointRadius:3
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'/5'}}},
    scales:{r:{grid:{color:G},ticks:{color:T2,font:{size:9},stepSize:1,backdropColor:'transparent'},pointLabels:{color:T2,font:{size:10}},min:0,max:5}}
  }
});

/* ── Temps déploiement ── */
new Chart(document.getElementById('chartDeployTime'),{
  type:'bar',
  data:{
    labels:['Détection push','Build image backend','Build image frontend','Deploy backend','Deploy frontend','Healthcheck OK'],
    datasets:[{
      data:[5,120,90,45,30,20],
      backgroundColor:['#888780','#378ADD','#7F77DD','#378ADD','#7F77DD','#1D9E75'],
      borderRadius:4,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'s'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'s'},beginAtZero:true}}
  }
});

/* ── Variables env (grouped) ── */
new Chart(document.getElementById('chartEnvVars'),{
  type:'bar',
  data:{
    labels:['Backend','Frontend','Partagées'],
    datasets:[
      {label:'Requises', data:[3,1,0], backgroundColor:dark?'rgba(216,90,48,0.75)':'rgba(153,60,29,0.65)',borderRadius:4,borderSkipped:false},
      {label:'Optionnelles', data:[2,2,0], backgroundColor:dark?'rgba(55,138,221,0.7)':'rgba(24,95,165,0.6)',borderRadius:4,borderSkipped:false}
    ]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:true,position:'bottom',labels:{color:T2,font:{size:11},boxWidth:12,padding:10}},tooltip:{titleFont:{size:11},bodyFont:{size:11}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:11}}},y:{grid:{color:G},ticks:{color:T2,font:{size:11}},beginAtZero:true,max:5}}
  }
});

/* ── Démarrage par service ── */
new Chart(document.getElementById('chartStartup'),{
  type:'bar',
  data:{
    labels:['PostgreSQL','Backend (cold)','Backend (warm)','Frontend'],
    datasets:[{
      data:[3.2,42,8,12],
      backgroundColor:['#BA7517','#378ADD','#1D9E75','#7F77DD'],
      borderRadius:5,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'s'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'s'},beginAtZero:true}}
  }
});

/* ── Mémoire ── */
new Chart(document.getElementById('chartMemory'),{
  type:'bar',
  data:{
    labels:['PostgreSQL','Backend','Frontend','Modèle ML (loaded)'],
    datasets:[{
      data:[64,220,140,180],
      backgroundColor:['#BA7517','#378ADD','#7F77DD','#639922'],
      borderRadius:5,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+' MB'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+' MB'},beginAtZero:true}}
  }
});

/* ── Uptime 30j ── */
const days=Array.from({length:30},(_,i)=>i+1+'');
const upB=[100,100,100,100,99.8,100,100,100,100,100,100,100,99.5,100,100,100,100,100,100,100,100,99.9,100,100,100,100,100,100,100,100];
const upF=[100,100,100,100,100,99.7,100,100,100,100,100,100,100,100,99.8,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100];
new Chart(document.getElementById('chartUptime'),{
  type:'line',
  data:{
    labels:days,
    datasets:[
      {label:'Backend', data:upB, borderColor:'#378ADD', backgroundColor:'transparent', tension:0.2, pointRadius:1, borderWidth:2},
      {label:'Frontend',data:upF, borderColor:'#7F77DD', backgroundColor:'transparent', tension:0.2, pointRadius:1, borderWidth:2}
    ]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:true,position:'bottom',labels:{color:T2,font:{size:11},boxWidth:12,padding:10}},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.dataset.label+': '+c.raw+'%'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9},maxTicksLimit:10}},y:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'%'},min:99,max:100.2}}
  }
});

/* ── Taille images Docker ── */
new Chart(document.getElementById('chartImageSize'),{
  type:'doughnut',
  data:{
    labels:['Backend (FastAPI + deps)','Frontend (Streamlit + deps)','Base OS (python:slim)'],
    datasets:[{
      data:[420,380,130],
      backgroundColor:['#378ADD','#7F77DD','#888780'],
      borderWidth:0,hoverOffset:5
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,cutout:'55%',
    plugins:{
      legend:{display:true,position:'bottom',labels:{color:T2,font:{size:11},boxWidth:12,padding:8}},
      tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.label+': '+c.raw+' MB'}}
    }
  }
});

/* ── Tabs ── */
function switchTab(name,el){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}

/* ── Service details ── */
const SVC={
  frontend: '<strong>Frontend — Streamlit</strong> : Interface utilisateur Python. 10 pages, CSS custom, graphiques Plotly. Communique avec le backend via HTTP. Port 8501. Démarrage conditionné au healthcheck backend.',
  backend:  '<strong>Backend — FastAPI + Uvicorn</strong> : Cœur logique de l\'application. Orchestration des services (météo, ML, BDD). 6 routes REST. Port 8000. Cache <code>@lru_cache</code> pour le modèle ML.',
  database: '<strong>PostgreSQL</strong> : Base de données relationnelle. Table <code>predictions</code> pour l\'historique. Connexion via SQLAlchemy ORM. Port 5432. Volume Docker persistant.',
  ml:       '<strong>Modèle ML — Scikit-learn</strong> : Chargé dynamiquement depuis Google Drive au démarrage (si absent). Sérialisé avec Joblib (<code>model.pkl</code>). Maintenu en mémoire par <code>@lru_cache</code>.',
  weather:  '<strong>Open-Meteo API</strong> : API météo gratuite et open-source. Fournit température, précipitations et humidité selon les coordonnées GPS. Appelée à chaque prédiction.',
  gdrive:   '<strong>Google Drive</strong> : Stockage externe pour les artefacts ML lourds (<code>model.pkl</code>, <code>model_metadata.pkl</code>). Permet de garder le repo GitHub léger. Téléchargement unique au cold start.',
  github:   '<strong>GitHub</strong> : Versioning du code source. <code>.gitignore</code> exclut les fichiers ML. Push sur <code>main</code> déclenche le build automatique sur Render.com.',
  render:   '<strong>Render.com</strong> : Plateforme de déploiement cloud. Héberge le backend Docker. Surveillance healthcheck, redémarrage automatique, variables d\'environnement sécurisées.'
};
function showSvc(el,key){
  document.querySelectorAll('.svc').forEach(s=>s.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('svc-detail').innerHTML=SVC[key];
}
</script>
</body>
</html>"""

components.html(DASHBOARD_HTML, height=1080, scrolling=True)

footer()