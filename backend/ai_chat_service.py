from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import logging

logger = logging.getLogger(__name__)

class AIChatService:
    def __init__(self):
        # Charger la clé au runtime plutôt qu'à l'import
        self.api_key = None
        self.enabled = False
        self.system_message = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the service with API key"""
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        
        if self.api_key:
            self.enabled = True
            print("✅ AI Chat Service enabled with Emergent LLM key")
            self._load_system_message()
        else:
            self.enabled = False
            print("⚠️ Emergent LLM key not configured - AI chat disabled")
    
    def _load_system_message(self):
        """Load system message - will be overridden by reload_config"""
        self.system_message = """Tu es un assistant virtuel expert pour la plateforme de formation "Inspecteur Auto". 

Tu aides les étudiants et visiteurs à comprendre la formation pour devenir inspecteur automobile certifié.

INFORMATIONS CLÉS:
- Durée: 11 heures
- Prix: 297€
- Certification officielle
- 8 modules + quiz
- Taux de réussite: 97%

Tu dois répondre de manière claire et professionnelle en français."""
    
    def reload_config(self):
        """Reload configuration from database"""
        try:
            # Import here to avoid circular dependency
            import asyncio
            from motor.motor_asyncio import AsyncIOMotorClient
            
            async def load():
                mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
                db_name = os.getenv('DB_NAME', 'inspecteur_auto_platform')
                client = AsyncIOMotorClient(mongo_url)
                db = client[db_name]
                
                config = await db.ai_chatbot_config.find_one({})
                if config and config.get('system_prompt'):
                    self.system_message = config['system_prompt']
                    print("✅ AI Chat prompt reloaded from database")
                else:
                    print("⚠️ No custom prompt found, using default")
            
            asyncio.run(load())
        except Exception as e:
            print(f"⚠️ Error reloading AI chat config: {e}")
    
    
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
