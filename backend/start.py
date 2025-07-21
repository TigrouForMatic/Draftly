#!/usr/bin/env python3
"""
Script de démarrage pour Draftly Backend
Initialise la base de données et démarre le serveur
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au path Python
sys.path.append(str(Path(__file__).parent))

from app.core.database import create_tables
from app.models import Base, User, Document, Template
from app.core.security import get_password_hash

def init_database():
    """Initialise la base de données avec les tables"""
    print("🔧 Initialisation de la base de données...")
    create_tables()
    print("✅ Base de données initialisée avec succès!")

def create_sample_data():
    """Crée des données d'exemple"""
    from sqlalchemy.orm import sessionmaker
    from app.core.database import engine
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Vérifier si un utilisateur admin existe déjà
        admin_user = db.query(User).filter(User.email == "admin@draftly.com").first()
        
        if not admin_user:
            print("👤 Création de l'utilisateur administrateur...")
            admin_user = User(
                email="admin@draftly.com",
                full_name="Administrateur Draftly",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Utilisateur administrateur créé!")
            print("   Email: admin@draftly.com")
            print("   Mot de passe: admin123")
        
        # Créer des templates d'exemple
        sample_templates = [
            {
                "name": "Devis Freelance",
                "description": "Template de devis pour freelances",
                "category": "freelance",
                "template_content": """
# DEVIS

**{{ entreprise.nom }}**
{{ entreprise.adresse }}
{{ entreprise.telephone }}
{{ entreprise.email }}

---

**DEVIS N° {{ devis.numero }}**
Date: {{ devis.date }}
Valable jusqu'au: {{ devis.validite }}

**Client:**
{{ client.nom }}
{{ client.adresse }}

## Prestations

{% for prestation in prestations %}
**{{ prestation.description }}**
- Quantité: {{ prestation.quantite }}
- Prix unitaire: {{ prestation.prix_unitaire }}€
- Total: {{ prestation.total }}€

{% endfor %}

---

**Total HT:** {{ total_ht }}€
**TVA (20%):** {{ tva }}€
**Total TTC:** {{ total_ttc }}€
                """,
                "is_public": True
            },
            {
                "name": "Contrat de Prestation",
                "description": "Template de contrat pour agences",
                "category": "agence",
                "template_content": """
# CONTRAT DE PRESTATION DE SERVICES

**Entre les soussignés:**

**{{ prestataire.nom }}** (ci-après dénommé "le Prestataire")
{{ prestataire.adresse }}
{{ prestataire.telephone }}
{{ prestataire.email }}

**ET**

**{{ client.nom }}** (ci-après dénommé "le Client")
{{ client.adresse }}
{{ client.telephone }}
{{ client.email }}

---

## Article 1 - Objet

Le présent contrat a pour objet la réalisation de {{ objet_prestation }}.

## Article 2 - Durée

Le contrat prend effet à compter du {{ date_debut }} pour une durée de {{ duree }}.

## Article 3 - Prix

Le montant total de la prestation s'élève à {{ montant }}€ TTC.
                """,
                "is_public": True
            }
        ]
        
        for template_data in sample_templates:
            existing_template = db.query(Template).filter(Template.name == template_data["name"]).first()
            if not existing_template:
                print(f"📄 Création du template: {template_data['name']}")
                template = Template(**template_data)
                db.add(template)
        
        db.commit()
        print("✅ Templates d'exemple créés!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données d'exemple: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Fonction principale"""
    print("🚀 Démarrage de Draftly Backend...")
    
    # Initialiser la base de données
    init_database()
    
    # Créer des données d'exemple
    create_sample_data()
    
    print("\n🎉 Initialisation terminée!")
    print("\nPour démarrer le serveur, exécutez:")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\nOu utilisez le script:")
    print("   python -m uvicorn main:app --reload")

if __name__ == "__main__":
    main() 