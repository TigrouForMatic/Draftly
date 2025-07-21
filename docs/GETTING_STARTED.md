# 🚀 Guide de démarrage rapide - Draftly

## Prérequis

- Python 3.8+
- Node.js 16+
- npm ou yarn

## Installation

### 1. Backend (FastAPI)

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'environnement
cp env.example .env

# Éditer le fichier .env avec vos clés API
# Notamment OPENAI_API_KEY pour l'IA

# Initialiser la base de données
python start.py

# Démarrer le serveur
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera accessible sur : http://localhost:8000
Documentation API : http://localhost:8000/docs

### 2. Frontend (React)

```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm start
```

Le frontend sera accessible sur : http://localhost:3000

## Compte par défaut

Un compte administrateur est créé automatiquement :
- **Email** : admin@draftly.com
- **Mot de passe** : admin123

## Configuration

### Variables d'environnement (Backend)

Créez un fichier `.env` dans le dossier `backend/` :

```env
# Configuration de base
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///./draftly.db

# OpenAI (requis pour l'IA)
OPENAI_API_KEY=your-openai-api-key

# Auth0 (optionnel)
AUTH0_DOMAIN=your-auth0-domain
AUTH0_API_AUDIENCE=your-auth0-audience
AUTH0_ISSUER=your-auth0-issuer

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### Variables d'environnement (Frontend)

Créez un fichier `.env` dans le dossier `frontend/` :

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Utilisation

1. **Connexion** : Utilisez le compte admin ou créez un nouveau compte
2. **Templates** : Parcourez les templates disponibles ou créez les vôtres
3. **Documents** : Créez des documents en utilisant l'IA ou les templates
4. **Export** : Exportez vos documents en DOCX ou PDF

## Fonctionnalités principales

- ✅ Authentification utilisateur
- ✅ Gestion des templates
- ✅ Génération de documents avec IA
- ✅ Export DOCX/PDF
- ✅ Interface moderne et responsive
- ✅ API REST complète

## Structure du projet

```
Draftly/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Routes API
│   │   ├── core/           # Configuration
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── schemas/        # Schémas Pydantic
│   │   └── services/       # Services métier
│   ├── main.py             # Point d'entrée
│   └── requirements.txt    # Dépendances Python
├── frontend/               # Application React
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── pages/          # Pages
│   │   ├── services/       # Services API
│   │   └── types/          # Types TypeScript
│   └── package.json        # Dépendances Node.js
└── docs/                   # Documentation
```

## Développement

### Backend

```bash
# Lancer les tests
pytest

# Formater le code
black .
isort .

# Vérifier la qualité du code
flake8
```

### Frontend

```bash
# Lancer les tests
npm test

# Build de production
npm run build

# Analyser le bundle
npm run analyze
```

## Déploiement

### Backend (Railway/Render)

1. Connectez votre repository GitHub
2. Configurez les variables d'environnement
3. Déployez automatiquement

### Frontend (Vercel)

1. Connectez votre repository GitHub
2. Configurez les variables d'environnement
3. Déployez automatiquement

## Support

Pour toute question ou problème :
- Consultez la documentation API : http://localhost:8000/docs
- Vérifiez les logs du serveur
- Consultez les issues GitHub

## Roadmap

- [ ] Intégration Auth0
- [ ] Signatures électroniques
- [ ] Intégration CRM
- [ ] Templates avancés
- [ ] Collaboration en temps réel
- [ ] Mobile app 