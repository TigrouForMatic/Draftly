# Draftly 🚀

**Générateur de documents professionnels IA**

Draftly est une plateforme intelligente qui automatise la création de documents professionnels grâce à l'intelligence artificielle. Conçu pour les TPE, agences, et professions libérales.

## 🎯 Cas d'usage

- **Devis et factures automatisés** pour freelances
- **Contrats de prestation** pour agences
- **CGV, lettres de résiliation, courriers RH** pour PME
- **Modèles spécialisés** par métier (web, coaching, comptabilité, juridique)

## 🛠️ Stack technique

### Frontend
- **React** avec TypeScript
- **Tailwind CSS** pour le design
- **React Hook Form** pour les formulaires
- **React Query** pour la gestion d'état

### Backend
- **FastAPI** (Python)
- **PostgreSQL** pour la base de données
- **SQLAlchemy** ORM
- **Pydantic** pour la validation

### IA & Génération
- **OpenAI API** pour l'IA
- **LangChain** pour les chaînes de traitement
- **python-docx** pour la génération de documents
- **Jinja2** pour les templates
- **WeasyPrint** pour l'export PDF

### Authentification & Déploiement
- **Auth0** pour l'authentification
- **Vercel** pour le frontend
- **Railway** pour le backend

## 📦 Installation

```bash
# Cloner le projet
git clone https://github.com/votre-username/draftly.git
cd draftly

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

## 🚀 Démarrage rapide

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

## 📋 Roadmap MVP (5 mois)

- **Mois 1** : Maquettes + stack + 1er modèle (devis)
- **Mois 2** : IA + génération dynamique + preview
- **Mois 3** : Auth + base client + modèles personnalisés
- **Mois 4** : Export PDF + historique + dashboard
- **Mois 5** : Mise en ligne + freemium + tests utilisateurs

## 🎨 Fonctionnalités

- ✅ Génération automatique de documents
- ✅ Templates personnalisables
- ✅ Export PDF/DOCX
- ✅ Historique des documents
- ✅ Modèles par métier
- ✅ Interface intuitive
- 🔄 IA conversationnelle
- 🔄 Intégration CRM
- 🔄 Signatures électroniques

## 📄 Licence

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails.
