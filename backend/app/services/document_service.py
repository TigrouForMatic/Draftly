from jinja2 import Template, Environment, FileSystemLoader
from docx import Document as DocxDocument
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
from app.core.config import settings

class DocumentService:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR))
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
    
    def generate_from_template(
        self, 
        template_content: str, 
        template_data: Dict[str, Any]
    ) -> str:
        """
        Génère le contenu d'un document à partir d'un template Jinja2
        """
        try:
            template = Template(template_content)
            return template.render(**template_data)
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du template: {str(e)}")
    
    def create_docx(
        self, 
        content: str, 
        filename: str,
        template_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Crée un fichier DOCX à partir du contenu
        """
        try:
            doc = DocxDocument()
            
            # Ajout du contenu
            paragraphs = content.split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    p = doc.add_paragraph(paragraph.strip())
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            # Sauvegarde du fichier
            file_path = self.upload_dir / f"{filename}.docx"
            doc.save(str(file_path))
            
            return str(file_path)
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création du fichier DOCX: {str(e)}")
    
    def create_pdf_from_docx(self, docx_path: str) -> str:
        """
        Convertit un fichier DOCX en PDF
        """
        try:
            from weasyprint import HTML
            import mammoth
            
            # Conversion DOCX vers HTML
            with open(docx_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html_content = result.value
            
            # Création du PDF
            pdf_path = docx_path.replace('.docx', '.pdf')
            HTML(string=html_content).write_pdf(pdf_path)
            
            return pdf_path
            
        except Exception as e:
            raise Exception(f"Erreur lors de la conversion PDF: {str(e)}")
    
    def create_devis_template(self, data: Dict[str, Any]) -> str:
        """
        Template spécialisé pour les devis
        """
        template_content = """
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

---

**Conditions de paiement:**
{{ conditions_paiement }}

**Signature:**
_________________
        """
        
        return self.generate_from_template(template_content, data)
    
    def create_facture_template(self, data: Dict[str, Any]) -> str:
        """
        Template spécialisé pour les factures
        """
        template_content = """
# FACTURE

**{{ entreprise.nom }}**
{{ entreprise.adresse }}
{{ entreprise.telephone }}
{{ entreprise.email }}

---

**FACTURE N° {{ facture.numero }}**
Date: {{ facture.date }}
Échéance: {{ facture.echeance }}

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

---

**IBAN:** {{ iban }}
**BIC:** {{ bic }}
        """
        
        return self.generate_from_template(template_content, data)
    
    def create_contrat_template(self, data: Dict[str, Any]) -> str:
        """
        Template spécialisé pour les contrats
        """
        template_content = """
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

## Article 4 - Modalités de paiement

{{ modalites_paiement }}

## Article 5 - Obligations des parties

{{ obligations }}

---

**Signature du Prestataire:** _________________
**Signature du Client:** _________________
        """
        
        return self.generate_from_template(template_content, data) 