#!/bin/bash

echo "🚀 Démarrage de Draftly - Générateur de documents professionnels IA"
echo "================================================================"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Prérequis vérifiés"

# Backend
echo ""
echo "🔧 Configuration du backend..."
cd backend

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel Python..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚙️  Création du fichier de configuration..."
    cp env.example .env
    echo "⚠️  Veuillez configurer votre fichier .env avec vos clés API (notamment OPENAI_API_KEY)"
fi

# Initialiser la base de données
echo "🗄️  Initialisation de la base de données..."
python start.py

# Démarrer le backend en arrière-plan
echo "🚀 Démarrage du serveur backend..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Frontend
echo ""
echo "🎨 Configuration du frontend..."
cd frontend

# Installer les dépendances
echo "📦 Installation des dépendances Node.js..."
npm install

# Démarrer le frontend en arrière-plan
echo "🚀 Démarrage du serveur frontend..."
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 Draftly est en cours de démarrage!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "👤 Compte par défaut:"
echo "   Email: admin@draftly.com"
echo "   Mot de passe: admin123"
echo ""
echo "⏹️  Pour arrêter les serveurs, appuyez sur Ctrl+C"

# Fonction pour nettoyer les processus
cleanup() {
    echo ""
    echo "🛑 Arrêt des serveurs..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre que les processus se terminent
wait 