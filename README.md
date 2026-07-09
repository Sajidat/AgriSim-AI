# 🌱 AgriSim AI

AgriSim AI est une plateforme intelligente dédiée à l'agriculture, permettant l'analyse de données agricoles et l'exploitation de modèles d'intelligence artificielle pour aider à la prise de décision.

Le projet repose sur une architecture conteneurisée avec :

* **Backend FastAPI (Python)**
* **Frontend Streamlit (Python)**
* **Base de données PostgreSQL 16**
* **Docker & Docker Compose**

---

## 🏗️ Architecture du projet

```
AgriSim-AI/
│
├── backend/
│   ├── api/              # API FastAPI
│   ├── services/         # Services métier
│   ├── ml/               # Modèles IA / Machine Learning
│   ├── model/            # Modèles de données
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── pages/            # Pages Streamlit
│   ├── app.py            # Application principale
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Technologies utilisées

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* PostgreSQL
* SQLAlchemy

### Frontend

* Streamlit
* Python

### Base de données

* PostgreSQL 16 Alpine

### DevOps

* Docker
* Docker Compose
* Git / GitHub

### Intelligence Artificielle

* Machine Learning
* Analyse de données Python

---

# ⚙️ Installation

## Prérequis

Installer :

* Docker Desktop
* Git

Vérifier les installations :

```bash
docker --version
git --version
```

---

# 📥 Cloner le projet

```bash
git clone https://github.com/Sajidat/AgriSim-AI.git

cd AgriSim-AI
```

---

# 🔐 Configuration des variables d'environnement

Créer un fichier `.env` à la racine :

```env
POSTGRES_USER=agrisim
POSTGRES_PASSWORD=agrisim
POSTGRES_DB=agrisim

DATABASE_URL=postgresql://agrisim:agrisim@db:5432/agrisim
```

---

# 🐳 Lancer l'application avec Docker

Construire et démarrer les services :

```bash
docker compose up --build
```

Pour lancer en arrière-plan :

```bash
docker compose up --build -d
```

---

# 📌 Services disponibles

Après le démarrage :

## Backend FastAPI

URL :

```
http://localhost:8000
```

Documentation Swagger :

```
http://localhost:8000/docs
```

---

## Frontend Streamlit

URL :

```
http://localhost:8501
```

---

## PostgreSQL

Connexion Docker :

```
Host : db
Port : 5432
Database : agrisim
User : agrisim
```

Connexion locale :

```
Host : localhost
Port : 5433
```

---

# 🔎 Commandes utiles Docker

Voir les conteneurs :

```bash
docker compose ps
```

Voir les logs :

```bash
docker compose logs
```

Logs backend :

```bash
docker compose logs backend
```

Logs frontend :

```bash
docker compose logs frontend
```

Arrêter les services :

```bash
docker compose down
```

Supprimer les volumes :

```bash
docker compose down -v
```

---

# 🧪 Vérification du fonctionnement

Les services doivent apparaître en état :

```
agrisim_db          Up
agrisim_backend     Up
agrisim_frontend    Up
```

---

# 🔄 Développement

Après modification du code :

```bash
docker compose up --build
```

Pour suivre les changements :

```bash
docker compose logs -f
```

---

# 📄 Licence

Projet développé dans un cadre académique et professionnel autour des technologies Backend, DevOps et Intelligence Artificielle.
