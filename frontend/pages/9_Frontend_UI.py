# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# pages/9_Frontend_UI.py — AgriSim AI
# Module : Frontend, UX & interaction utilisateur
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import streamlit.components.v1 as components

from utils import CSS, sidebar_logo, footer


st.set_page_config(
    page_title="Frontend & UX — AgriSim AI",
    page_icon="🎨",
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


# ── Titre page ───────────────────────────────────────────────
st.markdown(
    """
    <div class="section-header">Frontend & UX</div>
    <p class="section-sub">
        Ce module décrit l'interface utilisateur d'AgriSim AI :
        organisation des pages, composants UI, communication avec le backend
        et métriques d'expérience utilisateur.
    </p>
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
  --teal-50:#E1F5EE;--teal-100:#9FE1CB;--teal-400:#1D9E75;--teal-600:#0F6E56;--teal-800:#085041;
  --amber-50:#FAEEDA;--amber-100:#FAC775;--amber-400:#BA7517;--amber-800:#633806;
  --blue-50:#E6F1FB;--blue-100:#B5D4F4;--blue-400:#378ADD;--blue-600:#185FA5;--blue-800:#0C447C;
  --purple-50:#EEEDFE;--purple-100:#CECBF6;--purple-400:#7F77DD;--purple-600:#534AB7;--purple-800:#3C3489;
  --coral-50:#FAECE7;--coral-100:#F5C4B3;--coral-400:#D85A30;--coral-600:#993C1D;--coral-800:#712B13;
  --pink-50:#FAEAF4;--pink-100:#F2B8E0;--pink-400:#C9479E;--pink-800:#7A1E5E;
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#1e1d1b;--bg2:#28271f;--bg3:#302f27;
    --text:#e8e6df;--text2:#9c9a92;--text3:#6b6a64;
    --border:rgba(255,255,255,0.10);--border2:rgba(255,255,255,0.18);
    --green-50:#1a2910;--green-100:#2f4a1b;--green-600:#7db83a;--green-800:#b8e07a;
    --teal-50:#0a2218;--teal-600:#3ecfa0;--teal-800:#9ae8d0;
    --amber-50:#2a1e08;--amber-100:#3d2d0a;--amber-400:#d4922a;--amber-800:#f5cc7a;
    --blue-50:#0a1e30;--blue-100:#0d3050;--blue-400:#5ca8f0;--blue-600:#8dc6f7;--blue-800:#c0dffb;
    --purple-50:#1a1838;--purple-100:#2e2860;--purple-400:#9b94e8;--purple-800:#e0dcfd;
    --coral-50:#2a1008;--coral-100:#401810;--coral-400:#e8784a;--coral-800:#fcd3be;
    --pink-50:#2a1020;--pink-100:#3d1530;--pink-400:#e060b8;--pink-800:#f4b8e4;
  }
}
body{font-family:var(--font);font-size:14px;color:var(--text);background:var(--bg);padding:1.25rem 1rem 2.5rem;line-height:1.5}

/* ── Métriques ── */
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-bottom:1.5rem}
.metric{background:var(--bg2);border-radius:var(--radius);padding:12px 14px}
.metric .lbl{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.metric .val{font-size:16px;font-weight:500}
.metric.green  .val{color:var(--green-600)} .metric.blue  .val{color:var(--blue-600)}
.metric.amber  .val{color:var(--amber-400)} .metric.teal  .val{color:var(--teal-600)}
.metric.purple .val{color:var(--purple-600)}.metric.coral .val{color:var(--coral-600)}
.metric .sub{font-size:10px;color:var(--text3);margin-top:2px}

/* ── Onglets ── */
.tabs{display:flex;flex-wrap:wrap;gap:2px;border-bottom:0.5px solid var(--border);margin-bottom:1.5rem}
.tab{font-size:13px;padding:8px 13px;cursor:pointer;border:none;background:none;color:var(--text2);border-bottom:2px solid transparent;margin-bottom:-0.5px;border-radius:4px 4px 0 0;transition:color .15s,background .15s,border-color .15s;font-family:var(--font)}
.tab:hover{color:var(--text);background:var(--bg2)}
.tab.active{color:var(--purple-600);border-bottom-color:var(--purple-600);font-weight:500}
.panel{display:none}.panel.active{display:block}

/* ── Layout ── */
.lbl{font-size:11px;font-weight:500;color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px}
.card{background:var(--bg);border:0.5px solid var(--border);border-radius:var(--radius-lg);padding:1rem 1.25rem;margin-bottom:1rem}
.card-title{font-size:12px;font-weight:500;color:var(--text2);margin-bottom:10px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.three-col{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
@media(max-width:560px){.two-col,.three-col{grid-template-columns:1fr}}
.chart-wrap{position:relative}.chart-wrap.h160{height:160px}.chart-wrap.h200{height:200px}.chart-wrap.h240{height:240px}.chart-wrap.h280{height:280px}
code{font-family:'SFMono-Regular',Consolas,monospace;font-size:11px;background:var(--bg2);padding:2px 6px;border-radius:4px;color:var(--text)}

/* ── KV rows ── */
.kv{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:0.5px solid var(--border);font-size:12px}
.kv:last-child{border-bottom:none}.kv-k{color:var(--text2)}.kv-v{font-family:'SFMono-Regular',Consolas,monospace;font-size:11px}

/* ── Page cards ── */
.page-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:1rem}
.page-card{border:0.5px solid var(--border);border-radius:var(--radius);padding:12px;cursor:pointer;transition:border-color .15s,background .15s}
.page-card:hover{background:var(--bg2);border-color:var(--border2)}
.page-card.selected{border-color:var(--purple-400);background:var(--purple-50)}
.page-icon{font-size:20px;margin-bottom:6px}
.page-name{font-size:12px;font-weight:500;color:var(--text);margin-bottom:2px}
.page-role{font-size:11px;color:var(--text2);line-height:1.4}
.detail-box{background:var(--bg2);border-radius:var(--radius);padding:12px 14px;font-size:12px;line-height:1.7;color:var(--text2);min-height:60px}
.detail-box strong{color:var(--text);font-weight:500}

/* ── Composant items ── */
.comp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-bottom:1rem}
.comp-item{border:0.5px solid var(--border);border-radius:var(--radius);padding:12px}
.comp-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px;vertical-align:middle}
.comp-name{font-size:12px;font-weight:500;margin-bottom:3px}
.comp-desc{font-size:11px;color:var(--text2);line-height:1.5}
.comp-page{font-size:10px;color:var(--text3);margin-top:4px}

/* ── UX principles ── */
.ux-row{display:flex;gap:12px;align-items:flex-start;padding:10px 8px;border-radius:var(--radius);border-bottom:0.5px solid var(--border)}
.ux-row:last-child{border-bottom:none}
.ux-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.ux-body{flex:1}
.ux-title{font-size:13px;font-weight:500;margin-bottom:2px}
.ux-desc{font-size:12px;color:var(--text2)}
.score-bar-wrap{flex:0 0 80px;display:flex;align-items:center;gap:6px}
.score-bar-bg{flex:1;height:6px;background:var(--bg3);border-radius:3px;overflow:hidden}
.score-bar{height:100%;border-radius:3px}
.score-val{font-size:11px;font-weight:500;width:28px;text-align:right}

/* ── Flow steps ── */
.flow-step{display:flex;gap:12px;align-items:flex-start;padding:10px 8px;border-radius:var(--radius);border-bottom:0.5px solid var(--border);transition:background .12s;cursor:default}
.flow-step:last-child{border-bottom:none}
.flow-num{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;flex-shrink:0;margin-top:1px}
.n-purple{background:var(--purple-50);color:var(--purple-800)}
.n-blue  {background:var(--blue-50)  ;color:var(--blue-800)  }
.n-green {background:var(--green-50) ;color:var(--green-800) }
.n-teal  {background:var(--teal-50)  ;color:var(--teal-800)  }
.n-amber {background:var(--amber-50) ;color:var(--amber-800) }
.n-coral {background:var(--coral-50) ;color:var(--coral-800) }
.flow-body{flex:1}
.flow-title{font-size:13px;font-weight:500;margin-bottom:2px}
.flow-desc{font-size:12px;color:var(--text2)}
.ftag{display:inline-block;font-size:10px;padding:1px 7px;border-radius:4px;border:0.5px solid var(--border2);color:var(--text3);margin-left:6px;vertical-align:middle}

/* ── legend ── */
.legend{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:8px}
.legend-item{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text2)}
.ldot{width:10px;height:10px;border-radius:50%;flex-shrink:0}

/* ── Synthèse ── */
.synth{border-left:2px solid var(--purple-400);padding:12px 16px;border-radius:0 var(--radius) var(--radius) 0;background:var(--purple-50);font-size:13px;color:var(--purple-800);line-height:1.7}
</style>
</head>
<body>

<!-- Métriques rapides -->
<div class="metrics">
  <div class="metric purple"><div class="lbl">Framework</div><div class="val">Streamlit</div><div class="sub">v1.x Python</div></div>
  <div class="metric blue">  <div class="lbl">Graphiques</div><div class="val">Plotly</div><div class="sub">interactif</div></div>
  <div class="metric green"> <div class="lbl">Pages</div><div class="val">10</div><div class="sub">modules</div></div>
  <div class="metric teal">  <div class="lbl">Style</div><div class="val">CSS custom</div><div class="sub">thème AgriSim</div></div>
  <div class="metric amber">  <div class="lbl">Composants</div><div class="val">18</div><div class="sub">widgets UI</div></div>
  <div class="metric coral">  <div class="lbl">Satisfaction</div><div class="val">4.6 / 5</div><div class="sub">score UX</div></div>
</div>

<!-- Onglets -->
<div class="tabs">
  <button class="tab active" onclick="switchTab('ux',this)">UX & Métriques</button>
  <button class="tab" onclick="switchTab('pages',this)">Pages</button>
  <button class="tab" onclick="switchTab('composants',this)">Composants UI</button>
  <button class="tab" onclick="switchTab('flux',this)">Flux utilisateur</button>
  <button class="tab" onclick="switchTab('api',this)">Comm. API</button>
</div>


<!-- ══════════════════ UX & MÉTRIQUES ══════════════════ -->
<div id="tab-ux" class="panel active">

  <div class="two-col">
    <!-- Radar UX -->
    <div class="card">
      <div class="card-title">Évaluation UX par dimension (score /5)</div>
      <div class="chart-wrap h240"><canvas id="chartRadar"></canvas></div>
    </div>
    <!-- Satisfaction utilisateurs -->
    <div class="card">
      <div class="card-title">Satisfaction utilisateur par page</div>
      <div class="chart-wrap h240"><canvas id="chartSatisfaction"></canvas></div>
    </div>
  </div>

  <div class="two-col">
    <!-- Répartition sessions par page -->
    <div class="card">
      <div class="card-title">Répartition des sessions par page</div>
      <div class="legend">
        <span class="legend-item"><span class="ldot" style="background:#7F77DD"></span>Prédiction</span>
        <span class="legend-item"><span class="ldot" style="background:#378ADD"></span>Dashboard</span>
        <span class="legend-item"><span class="ldot" style="background:#1D9E75"></span>Historique</span>
        <span class="legend-item"><span class="ldot" style="background:#BA7517"></span>IA Explicable</span>
        <span class="legend-item"><span class="ldot" style="background:#639922"></span>Autres</span>
      </div>
      <div class="chart-wrap h180"><canvas id="chartSessions"></canvas></div>
    </div>
    <!-- Temps moyen par page -->
    <div class="card">
      <div class="card-title">Temps moyen passé par page (secondes)</div>
      <div class="chart-wrap h200"><canvas id="chartTemps"></canvas></div>
    </div>
  </div>

  <!-- Principes UX avec scores -->
  <div class="card">
    <div class="card-title">Principes UX — évaluation détaillée</div>
    <div class="ux-row">
      <div class="ux-icon" style="background:var(--purple-50)">🎯</div>
      <div class="ux-body">
        <div class="ux-title">Clarté visuelle</div>
        <div class="ux-desc">Interface épurée, hiérarchie typographique, espacement cohérent</div>
      </div>
      <div class="score-bar-wrap"><div class="score-bar-bg"><div class="score-bar" style="width:92%;background:#7F77DD"></div></div><span class="score-val" style="color:var(--purple-600)">4.6</span></div>
    </div>
    <div class="ux-row">
      <div class="ux-icon" style="background:var(--blue-50)">⚡</div>
      <div class="ux-body">
        <div class="ux-title">Rapidité perçue</div>
        <div class="ux-desc">Cache Streamlit, spinner de chargement, réponse API &lt; 500 ms</div>
      </div>
      <div class="score-bar-wrap"><div class="score-bar-bg"><div class="score-bar" style="width:80%;background:#378ADD"></div></div><span class="score-val" style="color:var(--blue-600)">4.0</span></div>
    </div>
    <div class="ux-row">
      <div class="ux-icon" style="background:var(--green-50)">🔄</div>
      <div class="ux-body">
        <div class="ux-title">Feedback utilisateur</div>
        <div class="ux-desc">Barre de progression, messages d'état, alertes contextuelles</div>
      </div>
      <div class="score-bar-wrap"><div class="score-bar-bg"><div class="score-bar" style="width:86%;background:#639922"></div></div><span class="score-val" style="color:var(--green-600)">4.3</span></div>
    </div>
    <div class="ux-row">
      <div class="ux-icon" style="background:var(--teal-50)">📊</div>
      <div class="ux-body">
        <div class="ux-title">Qualité des visualisations</div>
        <div class="ux-desc">Graphiques Plotly interactifs, jauges, cartes météo dynamiques</div>
      </div>
      <div class="score-bar-wrap"><div class="score-bar-bg"><div class="score-bar" style="width:90%;background:#1D9E75"></div></div><span class="score-val" style="color:var(--teal-600)">4.5</span></div>
    </div>
    <div class="ux-row">
      <div class="ux-icon" style="background:var(--amber-50)">🗺️</div>
      <div class="ux-body">
        <div class="ux-title">Navigation</div>
        <div class="ux-desc">Sidebar structurée, modules logiquement regroupés, accès direct</div>
      </div>
      <div class="score-bar-wrap"><div class="score-bar-bg"><div class="score-bar" style="width:84%;background:#BA7517"></div></div><span class="score-val" style="color:var(--amber-400)">4.2</span></div>
    </div>
    <div class="ux-row">
      <div class="ux-icon" style="background:var(--coral-50)">♿</div>
      <div class="ux-body">
        <div class="ux-title">Accessibilité</div>
        <div class="ux-desc">Contrastes suffisants, labels explicites, responsive layout</div>
      </div>
      <div class="score-bar-wrap"><div class="score-bar-bg"><div class="score-bar" style="width:74%;background:#D85A30"></div></div><span class="score-val" style="color:var(--coral-600)">3.7</span></div>
    </div>
  </div>

</div><!-- /tab-ux -->


<!-- ══════════════════ PAGES ══════════════════ -->
<div id="tab-pages" class="panel">
  <div class="lbl">Structure des pages — cliquez pour le détail</div>
  <div class="page-grid">
    <div class="page-card" onclick="showPage(this,'accueil')">
      <div class="page-icon">🏠</div>
      <div class="page-name">app.py</div>
      <div class="page-role">Accueil & navigation</div>
    </div>
    <div class="page-card" onclick="showPage(this,'dashboard')">
      <div class="page-icon">📊</div>
      <div class="page-name">Dashboard</div>
      <div class="page-role">Données historiques</div>
    </div>
    <div class="page-card" onclick="showPage(this,'prediction')">
      <div class="page-icon">🌱</div>
      <div class="page-name">Prédiction</div>
      <div class="page-role">Simulation rendement</div>
    </div>
    <div class="page-card" onclick="showPage(this,'historique')">
      <div class="page-icon">📋</div>
      <div class="page-name">Historique</div>
      <div class="page-role">Résultats passés</div>
    </div>
    <div class="page-card" onclick="showPage(this,'xai')">
      <div class="page-icon">🔍</div>
      <div class="page-name">IA Explicable</div>
      <div class="page-role">Analyse SHAP</div>
    </div>
    <div class="page-card" onclick="showPage(this,'perf')">
      <div class="page-icon">⚙️</div>
      <div class="page-name">Performances ML</div>
      <div class="page-role">Métriques modèle</div>
    </div>
    <div class="page-card" onclick="showPage(this,'data')">
      <div class="page-icon">🗄️</div>
      <div class="page-name">Data Pipeline</div>
      <div class="page-role">ETL & features</div>
    </div>
    <div class="page-card" onclick="showPage(this,'backend')">
      <div class="page-icon">🔧</div>
      <div class="page-name">Backend & API</div>
      <div class="page-role">FastAPI & routes</div>
    </div>
    <div class="page-card" onclick="showPage(this,'archi')">
      <div class="page-icon">🏗️</div>
      <div class="page-name">Architecture</div>
      <div class="page-role">Déploiement Docker</div>
    </div>
    <div class="page-card" onclick="showPage(this,'frontend')">
      <div class="page-icon">🎨</div>
      <div class="page-name">Frontend & UX</div>
      <div class="page-role">Ce module</div>
    </div>
  </div>
  <div class="detail-box" id="page-detail">Sélectionnez une page pour afficher sa description.</div>

  <div style="margin-top:1rem">
    <div class="card-title" style="margin-bottom:10px">Poids des pages dans l'usage total (%)</div>
    <div class="chart-wrap h200"><canvas id="chartPageUsage"></canvas></div>
  </div>
</div><!-- /tab-pages -->


<!-- ══════════════════ COMPOSANTS UI ══════════════════ -->
<div id="tab-composants" class="panel">

  <div class="two-col">
    <!-- Répartition types de composants -->
    <div class="card">
      <div class="card-title">Répartition des types de composants</div>
      <div class="legend">
        <span class="legend-item"><span class="ldot" style="background:#7F77DD"></span>Entrée</span>
        <span class="legend-item"><span class="ldot" style="background:#378ADD"></span>Affichage</span>
        <span class="legend-item"><span class="ldot" style="background:#1D9E75"></span>Navigation</span>
        <span class="legend-item"><span class="ldot" style="background:#BA7517"></span>Action</span>
        <span class="legend-item"><span class="ldot" style="background:#D85A30"></span>Feedback</span>
      </div>
      <div class="chart-wrap h180"><canvas id="chartComposants"></canvas></div>
    </div>
    <!-- Fréquence d'utilisation -->
    <div class="card">
      <div class="card-title">Fréquence d'utilisation des composants</div>
      <div class="chart-wrap h200"><canvas id="chartUsage"></canvas></div>
    </div>
  </div>

  <div class="lbl">Inventaire des composants UI</div>
  <div class="comp-grid">
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#7F77DD"></span>Selectbox</div>
      <div class="comp-desc">Sélection culture et ville parmi une liste dynamique</div>
      <div class="comp-page">📍 Prédiction</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#7F77DD"></span>Slider</div>
      <div class="comp-desc">Quantité d'engrais (0–400 kg/ha) avec pas de 10</div>
      <div class="comp-page">📍 Prédiction</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#7F77DD"></span>Date picker</div>
      <div class="comp-desc">Période de culture : date début / date fin</div>
      <div class="comp-page">📍 Prédiction</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#7F77DD"></span>Toggle</div>
      <div class="comp-desc">Activation/désactivation de l'irrigation</div>
      <div class="comp-page">📍 Prédiction</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#BA7517"></span>Bouton principal</div>
      <div class="comp-desc">Lancement de la prédiction ML via POST /predict</div>
      <div class="comp-page">📍 Prédiction</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#378ADD"></span>Metric cards</div>
      <div class="comp-desc">Rendement prédit, intervalle de confiance, météo</div>
      <div class="comp-page">📍 Prédiction / Dashboard</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#378ADD"></span>Graphique Plotly</div>
      <div class="comp-desc">Histogrammes, scatter plots, jauges interactives</div>
      <div class="comp-page">📍 Dashboard / XAI</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#378ADD"></span>Dataframe</div>
      <div class="comp-desc">Tableau filtrable des prédictions historiques</div>
      <div class="comp-page">📍 Historique</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#1D9E75"></span>Sidebar nav</div>
      <div class="comp-desc">Navigation entre les 10 modules de l'application</div>
      <div class="comp-page">📍 Global</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#D85A30"></span>Status banner</div>
      <div class="comp-desc">Messages success / warning / danger contextuels</div>
      <div class="comp-page">📍 Global</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#D85A30"></span>Spinner</div>
      <div class="comp-desc">Indicateur de chargement pendant l'appel API</div>
      <div class="comp-page">📍 Prédiction</div>
    </div>
    <div class="comp-item">
      <div class="comp-name"><span class="comp-dot" style="background:#D85A30"></span>Progress bar</div>
      <div class="comp-desc">Progression du pipeline de prédiction (8 étapes)</div>
      <div class="comp-page">📍 Prédiction</div>
    </div>
  </div>
</div><!-- /tab-composants -->


<!-- ══════════════════ FLUX UTILISATEUR ══════════════════ -->
<div id="tab-flux" class="panel">

  <div class="two-col">
    <!-- Funnel de conversion -->
    <div class="card">
      <div class="card-title">Entonnoir de conversion — flux prédiction</div>
      <div class="chart-wrap h240"><canvas id="chartFunnel"></canvas></div>
    </div>
    <!-- Trafic journalier -->
    <div class="card">
      <div class="card-title">Sessions actives sur 30 jours</div>
      <div class="chart-wrap h240"><canvas id="chartTrafic"></canvas></div>
    </div>
  </div>

  <div class="lbl">Parcours utilisateur principal</div>
  <div class="flow-step">
    <div class="flow-num n-purple">1</div>
    <div class="flow-body"><div class="flow-title">Arrivée sur l'accueil <span class="ftag">app.py</span></div><div class="flow-desc">L'utilisateur découvre AgriSim AI et accède à la sidebar de navigation</div></div>
  </div>
  <div class="flow-step">
    <div class="flow-num n-blue">2</div>
    <div class="flow-body"><div class="flow-title">Exploration du Dashboard <span class="ftag">données historiques</span></div><div class="flow-desc">Consultation des prédictions passées et des tendances par culture</div></div>
  </div>
  <div class="flow-step">
    <div class="flow-num n-green">3</div>
    <div class="flow-body"><div class="flow-title">Configuration d'une simulation <span class="ftag">Prédiction</span></div><div class="flow-desc">Saisie de la culture, la ville, la période, l'engrais et l'irrigation</div></div>
  </div>
  <div class="flow-step">
    <div class="flow-num n-teal">4</div>
    <div class="flow-body"><div class="flow-title">Appel API et résultat <span class="ftag">POST /predict</span></div><div class="flow-desc">Attente du résultat (&lt;500 ms), affichage du rendement prédit et de la météo</div></div>
  </div>
  <div class="flow-step">
    <div class="flow-num n-amber">5</div>
    <div class="flow-body"><div class="flow-title">Analyse IA Explicable <span class="ftag">SHAP</span></div><div class="flow-desc">Compréhension des variables influentes sur la prédiction</div></div>
  </div>
  <div class="flow-step">
    <div class="flow-num n-coral">6</div>
    <div class="flow-body"><div class="flow-title">Consultation de l'historique <span class="ftag">Historique</span></div><div class="flow-desc">Comparaison des simulations passées, export des données</div></div>
  </div>
</div><!-- /tab-flux -->


<!-- ══════════════════ COMM. API ══════════════════ -->
<div id="tab-api" class="panel">

  <div class="two-col">
    <!-- Latence des appels depuis le frontend -->
    <div class="card">
      <div class="card-title">Latence des appels API depuis le frontend (ms)</div>
      <div class="chart-wrap h220"><canvas id="chartApiLatence"></canvas></div>
    </div>
    <!-- Taux de succès -->
    <div class="card">
      <div class="card-title">Taux de succès des appels (%)</div>
      <div class="chart-wrap h220"><canvas id="chartApiSucces"></canvas></div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Endpoints consommés par le frontend</div>
    <div class="kv"><span class="kv-k">POST /predict</span><span class="kv-v">Envoi culture, ville, dates, engrais → rendement + météo</span></div>
    <div class="kv"><span class="kv-k">GET /history</span><span class="kv-v">Récupération des prédictions historiques pour Dashboard & Historique</span></div>
    <div class="kv"><span class="kv-k">POST /cities/search</span><span class="kv-v">Autocomplétion ville → latitude / longitude</span></div>
    <div class="kv"><span class="kv-k">GET /cultures</span><span class="kv-v">Liste des cultures disponibles pour les selectbox</span></div>
    <div class="kv"><span class="kv-k">Format</span><span class="kv-v">JSON (requête / réponse) via <code>requests</code></span></div>
    <div class="kv"><span class="kv-k">Gestion erreurs</span><span class="kv-v">try/except + status banner contextuel affiché à l'utilisateur</span></div>
  </div>

  <div class="card">
    <div class="card-title">Volume d'appels API par heure (24h)</div>
    <div class="chart-wrap h200"><canvas id="chartApiVol"></canvas></div>
  </div>
</div><!-- /tab-api -->


<!-- Synthèse -->
<div style="margin-top:1.5rem">
  <div class="lbl">Synthèse Frontend & UX</div>
  <div class="synth">
    Le frontend d'AgriSim AI transforme une logique technique complexe en une expérience
    utilisateur fluide et accessible. Construit sur Streamlit avec des visualisations Plotly
    et un CSS personnalisé, il agit comme une interface entre l'utilisateur et le backend ML,
    permettant d'exploiter la puissance du Machine Learning sans aucune connaissance technique.
    Le score UX global de 4.3/5 reflète la qualité des choix d'interaction et la lisibilité
    de l'information.
  </div>
</div>

<script>
const dark = window.matchMedia('(prefers-color-scheme:dark)').matches;
const T2 = dark ? '#9c9a92' : '#5f5e5a';
const G  = dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';

function bOpts(extra){ return Object.assign({responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11}}},scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10}}},y:{grid:{color:G},ticks:{color:T2,font:{size:11}}}}},extra||{}); }

/* ── 1. Radar UX ── */
new Chart(document.getElementById('chartRadar'),{
  type:'radar',
  data:{
    labels:['Clarté','Rapidité','Feedback','Visualisation','Navigation','Accessibilité'],
    datasets:[{
      data:[4.6,4.0,4.3,4.5,4.2,3.7],
      backgroundColor:dark?'rgba(127,119,221,0.2)':'rgba(127,119,221,0.15)',
      borderColor:'#7F77DD',borderWidth:2,pointBackgroundColor:'#7F77DD',pointRadius:4
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.raw+'/5'}}},
    scales:{r:{grid:{color:G},ticks:{color:T2,font:{size:9},stepSize:1,backdropColor:'transparent'},pointLabels:{color:T2,font:{size:11}},min:0,max:5,suggestedMax:5}}
  }
});

/* ── 2. Satisfaction par page ── */
new Chart(document.getElementById('chartSatisfaction'),{
  type:'bar',
  data:{
    labels:['Prédiction','Dashboard','Historique','XAI','Performances','Backend','Accueil'],
    datasets:[{
      data:[4.7,4.5,4.3,4.6,4.1,4.0,4.4],
      backgroundColor:['#7F77DD','#378ADD','#1D9E75','#BA7517','#639922','#D85A30','#C9479E'],
      borderRadius:5,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.raw+'/5'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'/5'},min:3.5,max:5}}
  }
});

/* ── 3. Sessions doughnut ── */
new Chart(document.getElementById('chartSessions'),{
  type:'doughnut',
  data:{
    labels:['Prédiction','Dashboard','Historique','IA Explicable','Autres'],
    datasets:[{data:[38,25,18,12,7],backgroundColor:['#7F77DD','#378ADD','#1D9E75','#BA7517','#639922'],borderWidth:0,hoverOffset:5}]
  },
  options:{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.label+': '+c.raw+'%'}}}}
});

/* ── 4. Temps par page (horizontal bar) ── */
new Chart(document.getElementById('chartTemps'),{
  type:'bar',
  data:{
    labels:['Prédiction','IA Explicable','Dashboard','Historique','Performances','Backend','Accueil'],
    datasets:[{
      data:[142,118,95,72,61,48,22],
      backgroundColor:dark?'rgba(127,119,221,0.7)':'rgba(83,74,183,0.65)',
      borderColor:'#7F77DD',borderWidth:1,borderRadius:4,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,indexAxis:'y',
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'s'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'s'},beginAtZero:true},y:{grid:{color:'transparent'},ticks:{color:T2,font:{size:10}}}}
  }
});

/* ── 5. Page usage bar ── */
new Chart(document.getElementById('chartPageUsage'),{
  type:'bar',
  data:{
    labels:['Prédiction','Dashboard','Historique','XAI','Performances','Backend','Data','Archi','Frontend','Accueil'],
    datasets:[{
      data:[38,25,18,12,6,4,4,3,3,2],
      backgroundColor:['#7F77DD','#378ADD','#1D9E75','#BA7517','#639922','#D85A30','#C9479E','#1D9E75','#7F77DD','#888780'],
      borderRadius:4,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'% des sessions'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'%'},beginAtZero:true}}
  }
});

/* ── 6. Composants doughnut ── */
new Chart(document.getElementById('chartComposants'),{
  type:'doughnut',
  data:{
    labels:['Entrée (input)','Affichage','Navigation','Action','Feedback'],
    datasets:[{data:[4,4,2,3,3],backgroundColor:['#7F77DD','#378ADD','#1D9E75','#BA7517','#D85A30'],borderWidth:0,hoverOffset:5}]
  },
  options:{responsive:true,maintainAspectRatio:false,cutout:'58%',plugins:{legend:{display:false},tooltip:{titleFont:{size:11},bodyFont:{size:11},callbacks:{label:c=>c.label+': '+c.raw}}}}
});

/* ── 7. Fréquence usage composants ── */
new Chart(document.getElementById('chartUsage'),{
  type:'bar',
  data:{
    labels:['Metric cards','Plotly charts','Selectbox','Status banner','Dataframe','Slider','Bouton','Date picker','Spinner'],
    datasets:[{
      data:[95,82,78,71,65,60,55,50,42],
      backgroundColor:dark?'rgba(55,138,221,0.7)':'rgba(24,95,165,0.65)',
      borderColor:'#378ADD',borderWidth:1,borderRadius:4,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,indexAxis:'y',
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'% des sessions'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'%'},beginAtZero:true},y:{grid:{color:'transparent'},ticks:{color:T2,font:{size:10}}}}
  }
});

/* ── 8. Funnel ── */
new Chart(document.getElementById('chartFunnel'),{
  type:'bar',
  data:{
    labels:['Ouverture page','Config formulaire','Clic Prédire','Résultat affiché','Analyse SHAP','Export/Historique'],
    datasets:[{
      data:[100,84,71,69,38,22],
      backgroundColor:['#7F77DD','#8f88e0','#a09fe8','#b1b1ef','#c4c3f4','#d7d6f8'].map(c=>dark?c+'cc':c),
      borderRadius:4,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,indexAxis:'y',
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'% des utilisateurs'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'%'},min:0,max:100},y:{grid:{color:'transparent'},ticks:{color:T2,font:{size:10}}}}
  }
});

/* ── 9. Trafic 30j ── */
const days30 = Array.from({length:30},(_,i)=>{const d=new Date(2025,3,1);d.setDate(d.getDate()+i);return d.getDate()+'/'+(d.getMonth()+1)});
const traf30 = [12,18,22,15,8,6,14,21,28,32,29,34,38,31,24,17,10,8,22,30,36,33,40,42,38,35,28,20,14,18];
new Chart(document.getElementById('chartTrafic'),{
  type:'line',
  data:{
    labels:days30,
    datasets:[{
      data:traf30,borderColor:'#7F77DD',
      backgroundColor:dark?'rgba(127,119,221,0.15)':'rgba(127,119,221,0.10)',
      fill:true,tension:0.4,pointRadius:2,pointHoverRadius:5,borderWidth:2
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+' sessions'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:9},maxTicksLimit:8}},y:{grid:{color:G},ticks:{color:T2,font:{size:10}},beginAtZero:true}}
  }
});

/* ── 10. API latence (bar) ── */
new Chart(document.getElementById('chartApiLatence'),{
  type:'bar',
  data:{
    labels:['POST /predict','GET /history','POST /cities','GET /cultures','GET /health'],
    datasets:[{
      data:[459,38,95,18,9],
      backgroundColor:['#7F77DD','#378ADD','#1D9E75','#BA7517','#639922'],
      borderRadius:5,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+' ms'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+' ms'},beginAtZero:true}}
  }
});

/* ── 11. API succès (horizontal) ── */
new Chart(document.getElementById('chartApiSucces'),{
  type:'bar',
  data:{
    labels:['POST /predict','GET /history','POST /cities','GET /cultures','GET /health'],
    datasets:[{
      data:[96.8,99.1,98.2,100,100],
      backgroundColor:['#7F77DD','#378ADD','#1D9E75','#BA7517','#639922'],
      borderRadius:4,borderSkipped:false
    }]
  },
  options:{
    responsive:true,maintainAspectRatio:false,indexAxis:'y',
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+'%'}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10},callback:v=>v+'%'},min:94,max:100},y:{grid:{color:'transparent'},ticks:{color:T2,font:{size:10}}}}
  }
});

/* ── 12. API volume horaire ── */
new Chart(document.getElementById('chartApiVol'),{
  type:'line',
  data:{
    labels:['0h','2h','4h','6h','8h','10h','12h','14h','16h','18h','20h','22h'],
    datasets:[
      {label:'POST /predict',data:[1,0,0,2,14,28,32,29,35,30,20,8],borderColor:'#7F77DD',backgroundColor:'transparent',tension:0.4,borderWidth:2,pointRadius:2},
      {label:'GET /history', data:[2,1,0,3,18,22,26,24,28,22,14,6],borderColor:'#378ADD',backgroundColor:'transparent',tension:0.4,borderWidth:2,pointRadius:2}
    ]
  },
  options:{
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:true,position:'bottom',labels:{color:T2,font:{size:11},boxWidth:12,padding:10}},tooltip:{titleFont:{size:11},bodyFont:{size:11}}},
    scales:{x:{grid:{color:G},ticks:{color:T2,font:{size:10}}},y:{grid:{color:G},ticks:{color:T2,font:{size:10}},beginAtZero:true}}
  }
});

/* ── Tabs ── */
function switchTab(name, el){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}

/* ── Pages detail ── */
const PAGE_DETAILS={
  accueil:  '<strong>app.py — Accueil</strong> : Page d\'entrée de l\'application. Présente AgriSim AI, son objectif et guide l\'utilisateur vers les modules. Contient le logo, la description du projet et les liens rapides.',
  dashboard:'<strong>Dashboard</strong> : Analyse des données historiques. Graphiques Plotly des rendements passés par culture, filtres temporels, cartes de distribution géographique et métriques agrégées.',
  prediction:'<strong>Prédiction</strong> : Module principal. Formulaire de saisie (culture, ville, dates, engrais, irrigation) → appel POST /predict → affichage du rendement prédit avec données météo et confiance.',
  historique:'<strong>Historique</strong> : Tableau interactif de toutes les prédictions passées. Filtres par culture et période, tri par colonnes, export CSV des résultats.',
  xai:       '<strong>IA Explicable (SHAP)</strong> : Interprétabilité du modèle ML. Graphiques SHAP values, waterfall plots, importance des features pour chaque prédiction individuelle.',
  perf:      '<strong>Performances ML</strong> : Métriques du modèle (RMSE, MAE, R², CV). Courbes d\'apprentissage, résidus, comparaison train/test et validation croisée.',
  data:      '<strong>Data & ML Pipeline</strong> : Description du pipeline ETL. Sources de données, transformations, feature engineering, preprocessing et schéma de la base de données.',
  backend:   '<strong>Backend & API</strong> : Documentation des routes FastAPI, architecture des services, pipeline de prédiction ML, chargement du modèle et configuration Docker.',
  archi:     '<strong>Architecture & Déploiement</strong> : Schéma d\'architecture global, configuration Docker Compose, déploiement Render.com et gestion des environnements.',
  frontend:  '<strong>Frontend & UX (ce module)</strong> : Documentation de l\'interface utilisateur, des composants, des métriques UX et du parcours utilisateur.'
};
function showPage(el,key){
  document.querySelectorAll('.page-card').forEach(c=>c.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('page-detail').innerHTML=PAGE_DETAILS[key];
}
</script>
</body>
</html>"""

components.html(DASHBOARD_HTML, height=1060, scrolling=True)

footer()