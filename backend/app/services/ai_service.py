import openai
from typing import Dict, Any, Optional
from app.core.config import settings
import json

class AIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
    
    async def generate_document_content(
        self, 
        template_content: str, 
        template_data: Dict[str, Any],
        document_type: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Génère le contenu d'un document en utilisant l'IA
        """
        
        # Construction du prompt
        prompt = f"""
        Tu es un assistant spécialisé dans la génération de documents professionnels.
        
        Type de document: {document_type}
        
        Template à utiliser:
        {template_content}
        
        Données à intégrer:
        {json.dumps(template_data, indent=2, ensure_ascii=False)}
        
        {f"Contexte supplémentaire: {additional_context}" if additional_context else ""}
        
        Instructions:
        1. Génère le contenu du document en respectant le template
        2. Intègre toutes les données fournies
        3. Adapte le ton au type de document (professionnel, formel)
        4. Assure-toi que le document est cohérent et complet
        5. Retourne uniquement le contenu final, sans commentaires
        
        Contenu du document:
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en rédaction de documents professionnels."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération IA: {str(e)}")
    
    async def improve_document(
        self, 
        content: str, 
        improvement_type: str,
        context: Optional[str] = None
    ) -> str:
        """
        Améliore un document existant
        """
        
        improvement_prompts = {
            "grammar": "Corrige la grammaire et l'orthographe",
            "style": "Améliore le style et la fluidité",
            "professional": "Rend le ton plus professionnel",
            "concise": "Rend le texte plus concis",
            "detailed": "Ajoute plus de détails"
        }
        
        prompt = f"""
        Document à améliorer:
        {content}
        
        Type d'amélioration: {improvement_prompts.get(improvement_type, improvement_type)}
        
        {f"Contexte: {context}" if context else ""}
        
        Instructions:
        1. Applique l'amélioration demandée
        2. Conserve le sens et la structure
        3. Retourne le document amélioré
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en amélioration de documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'amélioration: {str(e)}")
    
    async def suggest_improvements(self, content: str) -> Dict[str, str]:
        """
        Suggère des améliorations pour un document
        """
        
        prompt = f"""
        Analyse ce document et suggère des améliorations:
        
        {content}
        
        Retourne tes suggestions au format JSON avec les clés:
        - grammar: corrections grammaticales
        - style: améliorations de style
        - structure: améliorations de structure
        - content: suggestions de contenu
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en analyse de documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            suggestions = json.loads(response.choices[0].message.content.strip())
            return suggestions
            
        except Exception as e:
            return {
                "grammar": "Impossible d'analyser la grammaire",
                "style": "Impossible d'analyser le style",
                "structure": "Impossible d'analyser la structure",
                "content": "Impossible d'analyser le contenu"
            } 