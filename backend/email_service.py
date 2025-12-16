from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.sender_email = os.getenv('SENDER_EMAIL', 'noreply@inspecteur-auto.fr')
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            logger.warning("SendGrid API key not configured - email sending disabled")
    
    def send_welcome_email(self, recipient_email: str, full_name: str, username: str) -> bool:
        """
        Send welcome email after successful payment
        
        Args:
            recipient_email: User's email address
            full_name: User's full name
            username: User's username for login
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning("Email sending is disabled - no API key configured")
            return False
        
        subject = "Bienvenue sur votre formation Inspecteur Auto !"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9fafb;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .credentials-box {{
                    background: white;
                    border: 2px solid #2563eb;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .button {{
                    display: inline-block;
                    background: #2563eb;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #666;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                li {{
                    padding: 8px 0;
                    border-bottom: 1px solid #e5e7eb;
                }}
                li:before {{
                    content: "✓ ";
                    color: #10b981;
                    font-weight: bold;
                    margin-right: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚗 Bienvenue sur Inspecteur Auto !</h1>
                </div>
                <div class="content">
                    <h2>Bonjour {full_name},</h2>
                    
                    <p>Félicitations ! Votre paiement a été traité avec succès et vous avez maintenant accès à la formation complète d'inspecteur automobile.</p>
                    
                    <div class="credentials-box">
                        <h3>🔐 Vos identifiants d'accès :</h3>
                        <p><strong>Email :</strong> {recipient_email}</p>
                        <p><strong>Nom d'utilisateur :</strong> {username}</p>
                        <p style="color: #dc2626; font-size: 14px;">
                            ⚠️ Conservez ces identifiants en lieu sûr
                        </p>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://inspecteur-auto.fr/login" class="button">
                            Accéder à la plateforme
                        </a>
                    </div>
                    
                    <h3>📚 Ce qui vous attend :</h3>
                    <ul>
                        <li>8 modules de formation (9 heures de contenu)</li>
                        <li>Méthode méthode d'inspection exclusive</li>
                        <li>Quizzes d'évaluation après chaque module</li>
                        <li>Certificat officiel à l'issue de la formation</li>
                        <li>Accès au forum communauté à vie</li>
                    </ul>
                    
                    <h3>🎯 Prochaines étapes :</h3>
                    <ol style="padding-left: 20px;">
                        <li>Connectez-vous à la plateforme avec vos identifiants</li>
                        <li>Passez l'évaluation de connaissances mécaniques (12 questions)</li>
                        <li>Commencez votre parcours avec le Module 1</li>
                    </ol>
                    
                    <h3>📞 Besoin d'aide ?</h3>
                    <p>Notre équipe de support technique est disponible pour vous accompagner :</p>
                    <ul>
                        <li><strong>Email :</strong> support@inspecteur-auto.fr</li>
                        <li><strong>Téléphone :</strong> 01 23 45 67 89</li>
                        <li><strong>Horaires :</strong> Lundi-Vendredi, 9h-18h</li>
                    </ul>
                    
                    <p style="margin-top: 30px;">
                        Nous vous souhaitons un excellent parcours de formation !
                    </p>
                    
                    <p><strong>L'équipe Inspecteur Auto</strong></p>
                </div>
                
                <div class="footer">
                    <p>© 2025 Inspecteur Auto - Formation Professionnelle Certifiée Qualiopi</p>
                    <p>Cet email a été envoyé à {recipient_email}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        try:
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient_email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"Welcome email sent successfully to {recipient_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending welcome email: {str(e)}")
            return False

# Global instance
email_service = EmailService()
