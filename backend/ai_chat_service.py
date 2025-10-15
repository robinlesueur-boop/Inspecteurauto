from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import logging

logger = logging.getLogger(__name__)

class AIChatService:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            logger.warning("Emergent LLM key not configured - AI chat disabled")
        
        # System message pour le contexte de formation
        self.system_message = """Tu es un assistant pédagogique spécialisé dans la formation d'inspecteur automobile. 
Tu aides les étudiants avec leurs questions sur:
- Les 8 modules de la formation Inspecteur Auto
- La mécanique automobile (moteur, transmission, freinage, etc.)
- Les systèmes électroniques et ADAS
- Le diagnostic automobile
- La méthodologie AutoJust d'inspection
- Les aspects réglementaires et légaux
- La carrosserie et le châssis
- Les questions pratiques sur la plateforme de formation

Tu dois:
1. Répondre de manière claire, pédagogique et professionnelle
2. Utiliser un ton encourageant et positif
3. Donner des exemples concrets quand c'est pertinent
4. Si tu ne connais pas la réponse précise, le dire honnêtement
5. Suggérer de contacter le support pour les questions administratives
6. Répondre en français

Sois concis mais complet. Limite tes réponses à 200-300 mots maximum sauf si une explication détaillée est nécessaire."""
    
    async def get_response(self, user_message: str, session_id: str) -> str:
        """
        Get AI response for user message
        
        Args:
            user_message: User's question/message
            session_id: Unique session ID for conversation history
            
        Returns:
            str: AI assistant's response
        """
        if not self.enabled:
            return "Le chat IA n'est pas disponible pour le moment. Veuillez contacter le support."
        
        try:
            # Initialize chat with session
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=self.system_message
            ).with_model("openai", "gpt-4o-mini")
            
            # Create user message
            message = UserMessage(text=user_message)
            
            # Get response
            response = await chat.send_message(message)
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return "Désolé, une erreur s'est produite. Veuillez réessayer ou contacter le support."

# Global instance
ai_chat_service = AIChatService()
