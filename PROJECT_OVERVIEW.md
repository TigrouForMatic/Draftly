# 🚀 Draftly - Générateur de documents professionnels IA

## 📋 Aperçu du projet

Draftly est une plateforme intelligente qui automatise la création de documents professionnels grâce à l'intelligence artificielle. Conçu pour les TPE, agences, et professions libérales, il permet de générer rapidement des devis, factures, contrats et autres documents essentiels.

## 🎯 Objectifs du projet

### Business
- **Cible** : TPE, agences, professions libérales
- **Valeur ajoutée** : Automatisation et IA pour la génération de documents
- **Monétisation** : Abonnement ou pay-per-use
- **Potentiel** : Marché peu digitalisé avec un besoin réel

### Technique
- **MVP en 5 mois** : Développement progressif et itératif
- **Stack moderne** : FastAPI + React + IA
- **Scalabilité** : Architecture modulaire et extensible
- **Qualité** : Code propre, tests, documentation

## 🏗️ Architecture technique

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/              # Routes API REST
│   ├── core/             # Configuration et sécurité
│   ├── models/           # Modèles SQLAlchemy
│   ├── schemas/          # Schémas Pydantic
│   └── services/         # Services métier (IA, documents)
├── main.py               # Point d'entrée
├── requirements.txt      # Dépendances Python
└── start.py             # Script d'initialisation
```

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/       # Composants réutilisables
│   ├── pages/           # Pages de l'application
│   ├── services/        # Services API
│   ├── contexts/        # Contextes React (Auth)
│   └── types/           # Types TypeScript
├── package.json         # Dépendances Node.js
└── tailwind.config.js   # Configuration Tailwind
```

## 🛠️ Stack technique

### Backend
- **Framework** : FastAPI (Python)
- **Base de données** : PostgreSQL / SQLite
- **ORM** : SQLAlchemy
- **Validation** : Pydantic
- **IA** : OpenAI API + LangChain
- **Génération** : python-docx + Jinja2 + WeasyPrint

### Frontend
- **Framework** : React 18 + TypeScript
- **Styling** : Tailwind CSS
- **Formulaires** : React Hook Form + Yup
- **Routing** : React Router DOM
- **HTTP** : Axios
- **UI** : Headless UI + Heroicons

### Infrastructure
- **Authentification** : JWT + Auth0 (optionnel)
- **Déploiement** : Vercel (frontend) + Railway/Render (backend)
- **Conteneurisation** : Docker + Docker Compose

## 📊 Fonctionnalités

### ✅ Implémentées (MVP)
- [x] Authentification utilisateur (JWT)
- [x] Gestion des templates (CRUD)
- [x] Génération de documents avec IA
- [x] Export DOCX/PDF
- [x] Interface moderne et responsive
- [x] API REST complète
- [x] Base de données avec migrations

### 🔄 En développement
- [ ] Gestion avancée des documents
- [ ] Templates spécialisés par métier
- [ ] Historique et versioning
- [ ] Collaboration en temps réel

### 🚀 Roadmap (5 mois)
- **Mois 1** : Maquettes + stack + 1er modèle (devis) ✅
- **Mois 2** : IA + génération dynamique + preview ✅
- **Mois 3** : Auth + base client + modèles personnalisés ✅
- **Mois 4** : Export PDF + historique + dashboard ✅
- **Mois 5** : Mise en ligne + freemium + tests utilisateurs

## 🎨 Cas d'usage

### Freelances
- **Devis automatisés** : Génération rapide de devis personnalisés
- **Factures** : Création automatique avec calculs
- **Contrats** : Templates juridiques adaptés

### Agences
- **Contrats de prestation** : Templates spécialisés
- **CGV** : Conditions générales de vente
- **Lettres commerciales** : Communication professionnelle

### Professions libérales
- **Documents juridiques** : Contrats, lettres
- **Documents comptables** : Factures, devis
- **Documents RH** : Contrats de travail, lettres

## 🔧 Installation et démarrage

### Démarrage rapide
```bash
# Cloner le projet
git clone https://github.com/votre-username/draftly.git
cd draftly

# Démarrer avec le script automatique
./start.sh
```

### Installation manuelle
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python start.py
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## 📈 Métriques et KPIs

### Technique
- **Performance** : < 2s pour la génération de documents
- **Disponibilité** : 99.9% uptime
- **Sécurité** : Authentification JWT, validation des données

### Business
- **Temps de génération** : -80% vs méthode manuelle
- **Taux d'adoption** : Objectif 70% des utilisateurs actifs
- **Satisfaction** : Objectif 4.5/5 sur les avis utilisateurs

## 🚀 Déploiement

### Développement
- **Local** : Docker Compose ou script `start.sh`
- **Staging** : Vercel Preview + Railway Preview
- **Production** : Vercel + Railway/Render

### Variables d'environnement
```env
# Backend
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
DATABASE_URL=postgresql://...

# Frontend
REACT_APP_API_URL=https://api.draftly.com
```

## 🧪 Tests

### Backend
```bash
cd backend
pytest
black .
isort .
flake8
```

### Frontend
```bash
cd frontend
npm test
npm run build
```

## 📚 Documentation

- **API** : http://localhost:8000/docs (Swagger)
- **Guide utilisateur** : `docs/GETTING_STARTED.md`
- **Architecture** : `docs/ARCHITECTURE.md`
- **Déploiement** : `docs/DEPLOYMENT.md`

## 🤝 Contribution

### Workflow
1. Fork du repository
2. Création d'une branche feature
3. Développement avec tests
4. Pull Request avec description
5. Review et merge

### Standards
- **Code** : Black, isort, flake8 (Python)
- **Tests** : Pytest avec couverture > 80%
- **Commits** : Conventional Commits
- **PR** : Template avec checklist

## 📞 Support

- **Documentation** : Wiki GitHub
- **Issues** : GitHub Issues
- **Discussions** : GitHub Discussions
- **Email** : support@draftly.com

## 📄 Licence

MIT License - Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**Draftly** - Révolutionnez la création de documents professionnels avec l'IA 🚀 