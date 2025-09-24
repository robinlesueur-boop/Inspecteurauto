from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import hashlib
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
JWT_SECRET = os.environ.get('JWT_SECRET', 'automotive-inspector-secret-key-2024')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = timedelta(days=7)

# Security
security = HTTPBearer()

app = FastAPI(title="Automotive Inspector Training Platform")
api_router = APIRouter(prefix="/api")

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    is_enrolled: bool = False
    enrollment_date: Optional[datetime] = None
    progress: Dict[str, Any] = Field(default_factory=dict)
    quiz_scores: Dict[str, int] = Field(default_factory=dict)
    completed_modules: List[str] = Field(default_factory=list)
    final_exam_score: Optional[int] = None
    is_certified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Module(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    duration_minutes: int
    content: str
    order: int
    quiz_questions: List[Dict[str, Any]] = Field(default_factory=list)

class QuizSubmission(BaseModel):
    module_id: str
    answers: Dict[str, str]  # question_id -> selected_answer

class QuizResult(BaseModel):
    module_id: str
    score: int
    total_questions: int
    passed: bool
    answers: Dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FinalExam(BaseModel):
    answers: Dict[str, str]  # question_id -> selected_answer

class FinalExamResult(BaseModel):
    score: int
    total_questions: int
    passed: bool
    answers: Dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Authentication utilities
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + JWT_EXPIRATION_TIME
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Remove hashed_password before creating User object
    user_dict = {k: v for k, v in user.items() if k != 'hashed_password'}
    return User(**user_dict)

# Initialize course modules with detailed content
COURSE_MODULES = [
    {
        "id": "module-1",
        "title": "Diagnostic et Positionnement",
        "description": "Auto-évaluation des compétences et définition du parcours personnalisé",
        "duration_minutes": 30,
        "order": 1,
        "content": """
        <h2>Module 1 : Diagnostic et Positionnement</h2>
        
        <h3>🎯 Objectifs du Module</h3>
        <ul>
            <li>Évaluer vos compétences techniques actuelles</li>
            <li>Identifier vos points forts et axes d'amélioration</li>
            <li>Personnaliser votre parcours de formation</li>
            <li>Comprendre les enjeux du métier d'inspecteur automobile</li>
        </ul>

        <h3>🔍 Auto-évaluation des Compétences</h3>
        
        <h4>Compétences Mécaniques de Base</h4>
        <p>Avant de commencer votre formation, il est essentiel d'évaluer votre niveau actuel en mécanique automobile :</p>
        
        <div style="background: #1e293b; padding: 20px; border-radius: 8px; margin: 16px 0;">
            <h5>📋 Grille d'Auto-évaluation</h5>
            <p><strong>Niveau Débutant (0-2 points par domaine) :</strong></p>
            <ul>
                <li>Moteur : Notions de base sur le fonctionnement</li>
                <li>Transmission : Différence boîte manuelle/automatique</li>
                <li>Freinage : Connaissance des composants principaux</li>
                <li>Électronique : Utilisation basique d'un multimètre</li>
            </ul>
            
            <p><strong>Niveau Intermédiaire (3-4 points par domaine) :</strong></p>
            <ul>
                <li>Moteur : Diagnostic de pannes courantes</li>
                <li>Transmission : Identification des symptômes d'usure</li>
                <li>Freinage : Contrôle épaisseur plaquettes/disques</li>
                <li>Électronique : Lecture codes défauts OBD</li>
            </ul>
            
            <p><strong>Niveau Avancé (5 points par domaine) :</strong></p>
            <ul>
                <li>Moteur : Analyse compression, régime ralenti</li>
                <li>Transmission : Évaluation état embrayage, boîte</li>
                <li>Freinage : Test efficacité, géométrie</li>
                <li>Électronique : Diagnostic approfondi calculateurs</li>
            </ul>
        </div>

        <h4>Expérience Professionnelle</h4>
        <p>Votre parcours professionnel influence directement votre approche de l'inspection :</p>
        
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Profil</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Points forts</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Axes de développement</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Mécanicien</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Diagnostic technique approfondi</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Relation client, rédaction rapports</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Contrôleur technique</strong></td>
                <td style="padding: 12px; border: 1st solid #4b5563;">Méthodologie, respect procédures</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Expertise moteur, conseil client</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Commercial auto</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Relation client, négociation</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Connaissances techniques approfondies</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Reconversion</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Motivation, regard neuf</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Bases techniques complètes</td>
            </tr>
        </table>

        <h3>📊 Définition de Votre Parcours Personnalisé</h3>
        
        <p>Selon votre profil, nous recommandons un parcours adapté :</p>
        
        <h4>🚀 Parcours Accéléré (Professionnels expérimentés)</h4>
        <ul>
            <li>Focus sur les modules 2, 4, 6 et 8</li>
            <li>Révision rapide des bases mécaniques</li>
            <li>Accent mis sur la méthodologie AutoJust</li>
            <li>Développement business et relation client</li>
        </ul>

        <h4>⚡ Parcours Standard (Niveau intermédiaire)</h4>
        <ul>
            <li>Suivi linéaire des 8 modules</li>
            <li>Attention particulière aux modules 3 et 5</li>
            <li>Exercices pratiques renforcés</li>
            <li>Validation étape par étape</li>
        </ul>

        <h4>🎓 Parcours Renforcé (Débutants)</h4>
        <ul>
            <li>Module 3 étendu avec ressources supplémentaires</li>
            <li>Exercices pratiques nombreux</li>
            <li>Support pédagogique personnalisé</li>
            <li>Validation progressive avec feedback</li>
        </ul>

        <h3>🏆 Les Enjeux du Métier d'Inspecteur</h3>
        
        <h4>Mission et Responsabilités</h4>
        <p>L'inspecteur automobile est un expert indépendant qui :</p>
        <ul>
            <li><strong>Évalue objectivement</strong> l'état d'un véhicule</li>
            <li><strong>Informe</strong> le client sur les risques et opportunités</li>
            <li><strong>Protège</strong> l'acheteur contre les vices cachés</li>
            <li><strong>Facilite</strong> les transactions en apportant la confiance</li>
        </ul>

        <h4>Marché et Opportunités</h4>
        <div style="background: #065f46; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>📈 Statistiques du Marché</h5>
            <ul>
                <li><strong>5,2 millions</strong> de véhicules d'occasion vendus/an en France</li>
                <li><strong>15%</strong> seulement font l'objet d'une inspection</li>
                <li><strong>Potentiel de croissance énorme</strong> avec la démocratisation</li>
                <li><strong>Tarif moyen :</strong> 200-300€ par inspection</li>
            </ul>
        </div>

        <h4>Défis et Exigences du Métier</h4>
        <ul>
            <li><strong>Précision technique :</strong> Aucune erreur n'est permise</li>
            <li><strong>Impartialité :</strong> Résister aux pressions commerciales</li>
            <li><strong>Pédagogie :</strong> Expliquer clairement les constats</li>
            <li><strong>Réactivité :</strong> Intervention rapide sur demande</li>
            <li><strong>Formation continue :</strong> Évolution technologique constante</li>
        </ul>

        <h3>🎯 Objectifs de Fin de Formation</h3>
        
        <p>À l'issue de cette formation, vous serez capable de :</p>
        
        <div style="background: #1e40af; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>💼 Compétences Professionnelles</h5>
            <ul>
                <li>Réaliser une inspection complète en 90 minutes</li>
                <li>Évaluer avec précision l'état de 200+ points de contrôle</li>
                <li>Rédiger un rapport professionnel détaillé</li>
                <li>Formuler un avis moteur expert selon le modèle/kilométrage</li>
                <li>Gérer la relation client avec diplomatie</li>
                <li>Fixer vos tarifs et développer votre activité</li>
            </ul>
        </div>

        <h3>📋 Plan de Formation Personnalisé</h3>
        
        <p>Votre progression sera suivie grâce à :</p>
        <ul>
            <li><strong>Quiz d'évaluation</strong> à chaque module (minimum 70%)</li>
            <li><strong>Cas pratiques</strong> avec véhicules réels</li>
            <li><strong>Exercices de rédaction</strong> de rapports</li>
            <li><strong>Simulations</strong> de relation client</li>
            <li><strong>Examen final</strong> de 50 questions (seuil 70%)</li>
        </ul>

        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>⚠️ Points d'Attention</h5>
            <ul>
                <li>La formation théorique ne remplace pas la pratique terrain</li>
                <li>L'expérience s'acquiert avec le temps et la répétition</li>
                <li>La formation continue est indispensable</li>
                <li>Le réseau professionnel est crucial pour le développement</li>
            </ul>
        </div>

        <h3>🚀 Prêt à Commencer ?</h3>
        
        <p>Maintenant que vous avez évalué votre profil et défini vos objectifs, passons aux fondamentaux de l'inspection automobile dans le module suivant.</p>
        
        <p><em>Durée estimée de ce module : 30 minutes de lecture + 15 minutes pour le quiz d'auto-évaluation.</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Combien de véhicules d'occasion sont vendus annuellement en France ?",
                "options": ["3,5 millions", "5,2 millions", "7,1 millions", "8,9 millions"],
                "correct_answer": "5,2 millions"
            },
            {
                "id": "q2",
                "question": "Quel pourcentage de véhicules d'occasion fait actuellement l'objet d'une inspection ?",
                "options": ["5%", "15%", "25%", "35%"],
                "correct_answer": "15%"
            },
            {
                "id": "q3",
                "question": "Quel est le tarif moyen d'une inspection automobile ?",
                "options": ["100-150€", "200-300€", "350-400€", "450-500€"],
                "correct_answer": "200-300€"
            },
            {
                "id": "q4",
                "question": "Combien de temps dure approximativement une inspection complète ?",
                "options": ["60 minutes", "90 minutes", "120 minutes", "150 minutes"],
                "correct_answer": "90 minutes"
            },
            {
                "id": "q5",
                "question": "Quelle est la première qualité d'un inspecteur automobile ?",
                "options": ["Rapidité", "Impartialité", "Convivialité", "Flexibilité"],
                "correct_answer": "Impartialité"
            },
            {
                "id": "q6",
                "question": "Le parcours 'Renforcé' est recommandé pour quel profil ?",
                "options": ["Mécaniciens expérimentés", "Contrôleurs techniques", "Débutants", "Commerciaux auto"],
                "correct_answer": "Débutants"
            },
            {
                "id": "q7",
                "question": "Combien de points de contrôle comprend la méthodologie AutoJust ?",
                "options": ["150+", "200+", "250+", "300+"],
                "correct_answer": "200+"
            },
            {
                "id": "q8",
                "question": "Quel est le seuil de réussite pour les quiz de modules ?",
                "options": ["60%", "70%", "80%", "90%"],
                "correct_answer": "70%"
            },
            {
                "id": "q9",
                "question": "La formation continue est-elle obligatoire pour un inspecteur ?",
                "options": ["Non, pas nécessaire", "Recommandée", "Indispensable", "Uniquement la première année"],
                "correct_answer": "Indispensable"
            },
            {
                "id": "q10",
                "question": "Quel niveau permet de diagnostiquer des pannes courantes ?",
                "options": ["Débutant", "Intermédiaire", "Avancé", "Expert"],
                "correct_answer": "Intermédiaire"
            },
            {
                "id": "q11",
                "question": "L'inspecteur doit-il résister aux pressions commerciales ?",
                "options": ["Non, il doit s'adapter", "Parfois", "Oui, absolument", "Cela dépend du client"],
                "correct_answer": "Oui, absolument"
            },
            {
                "id": "q12",
                "question": "Combien de questions comprend l'examen final ?",
                "options": ["30 questions", "40 questions", "50 questions", "60 questions"],
                "correct_answer": "50 questions"
            }
        ]
    },
    {
        "id": "module-2",
        "title": "Fondamentaux de l'Inspection",
        "description": "Rôle, missions, cadre réglementaire et déontologie de l'inspecteur automobile",
        "duration_minutes": 90,
        "order": 2,
        "content": """
        <h2>Module 2 : Fondamentaux de l'Inspection Automobile</h2>
        
        <h3>🎯 Objectifs du Module</h3>
        <ul>
            <li>Maîtriser le rôle et les missions de l'inspecteur automobile</li>
            <li>Comprendre les principes de transparence et d'impartialité</li>
            <li>Connaître le cadre réglementaire français et européen</li>
            <li>Intégrer les responsabilités légales et la déontologie</li>
        </ul>

        <h3>👨‍🔧 Rôle et Missions de l'Inspecteur</h3>
        
        <h4>Définition du Métier</h4>
        <p>L'inspecteur automobile est un <strong>expert technique indépendant</strong> spécialisé dans l'évaluation complète de véhicules. Il intervient comme tiers de confiance dans les transactions automobiles.</p>
        
        <div style="background: #1e293b; padding: 20px; border-radius: 8px; margin: 16px 0;">
            <h5>🎯 Missions Principales</h5>
            <ul>
                <li><strong>Inspection technique complète :</strong> Évaluation de l'état mécanique, esthétique et sécuritaire</li>
                <li><strong>Rédaction de rapport détaillé :</strong> Document officiel avec photos et recommandations</li>
                <li><strong>Conseil expert :</strong> Accompagnement du client dans sa décision d'achat</li>
                <li><strong>Estimation de valeur :</strong> Évaluation du prix de marché selon l'état</li>
                <li><strong>Détection de vices cachés :</strong> Identification des défauts non apparents</li>
                <li><strong>Formation du client :</strong> Explication des enjeux techniques</li>
            </ul>
        </div>

        <h4>Contextes d'Intervention</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Type d'intervention</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Client</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Objectif</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Enjeu</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Achat particulier</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Acheteur privé</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Sécuriser l'achat</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">5 000 - 50 000€</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Expertise assurance</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Compagnie d'assurance</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Évaluer les dommages</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Remboursement sinistre</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Fin de leasing</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Société de leasing</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">État de restitution</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Facturation dégradations</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Vente aux enchères</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Maison de ventes</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Estimation préalable</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Prix de réserve</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Litige commercial</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Tribunal/Avocat</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Expertise judiciaire</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Dommages et intérêts</td>
            </tr>
        </table>

        <h3>⚖️ Principes de Transparence et Impartialité</h3>
        
        <h4>Transparence Absolue</h4>
        <p>La transparence constitue le fondement de la crédibilité professionnelle :</p>
        
        <ul>
            <li><strong>Méthodologie explicite :</strong> Explication claire du processus d'inspection</li>
            <li><strong>Critères objectifs :</strong> Grille de notation standardisée et publique</li>
            <li><strong>Photos systématiques :</strong> Documentation visuelle de tous les points contrôlés</li>
            <li><strong>Sources d'information :</strong> Référencement des bases de données utilisées</li>
            <li><strong>Limites de l'expertise :</strong> Clarification de ce qui n'est pas contrôlable</li>
        </ul>

        <div style="background: #065f46; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>📋 Checklist Transparence</h5>
            <ul>
                <li>✅ Présentation de la méthodologie avant intervention</li>
                <li>✅ Explication des outils utilisés</li>
                <li>✅ Durée prévisionnelle communiquée</li>
                <li>✅ Tarification claire et détaillée</li>
                <li>✅ Remise du rapport dans les 24h</li>
                <li>✅ Disponibilité pour questions post-inspection</li>
            </ul>
        </div>

        <h4>Impartialité Rigoureuse</h4>
        <p>L'impartialité garantit la fiabilité de l'évaluation :</p>
        
        <ul>
            <li><strong>Indépendance financière :</strong> Aucun lien commercial avec vendeur/acheteur</li>
            <li><strong>Neutralité émotionnelle :</strong> Évaluation basée uniquement sur les faits</li>
            <li><strong>Résistance aux pressions :</strong> Maintien des conclusions malgré les influences</li>
            <li><strong>Égalité de traitement :</strong> Même rigueur quel que soit le client</li>
        </ul>

        <h4>Gestion des Conflits d'Intérêts</h4>
        
        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🚫 Situations à Éviter Absolument</h5>
            <ul>
                <li>Inspection d'un véhicule que vous souhaitez acheter</li>
                <li>Recommandation d'un garage partenaire</li>
                <li>Commission sur une vente suite à votre expertise</li>
                <li>Pression pour modifier vos conclusions</li>
                <li>Double expertise pour le même véhicule (vendeur + acheteur)</li>
            </ul>
        </div>

        <h3>📜 Cadre Réglementaire de l'Inspection</h3>
        
        <h4>Réglementation Française</h4>
        
        <h5>Code de la Consommation</h5>
        <p>Articles L217-1 à L217-32 relatifs à la conformité et aux vices cachés :</p>
        <ul>
            <li><strong>Garantie de conformité :</strong> 2 ans pour défauts existants à la livraison</li>
            <li><strong>Garantie des vices cachés :</strong> Défauts rendant le bien impropre à l'usage</li>
            <li><strong>Obligation d'information :</strong> Devoir du vendeur professionnel</li>
        </ul>

        <h5>Code Civil</h5>
        <p>Articles 1641 à 1649 sur la garantie des défauts cachés :</p>
        <ul>
            <li>Défaut caché existant lors de la vente</li>
            <li>Défaut suffisamment grave</li>
            <li>Défaut inconnu de l'acheteur</li>
        </ul>

        <h4>Réglementation Européenne</h4>
        
        <h5>Directive 2011/83/UE (Droits des consommateurs)</h5>
        <ul>
            <li>Information précontractuelle obligatoire</li>
            <li>Droit de rétractation (14 jours pour vente à distance)</li>
            <li>Garantie légale de conformité (2 ans minimum)</li>
        </ul>

        <h5>Règlement RGPD (Protection des données)</h5>
        <ul>
            <li>Consentement explicite pour collecte de données</li>
            <li>Droit à l'effacement et à la portabilité</li>
            <li>Registre des traitements obligatoire</li>
        </ul>

        <h3>⚖️ Responsabilités Légales</h3>
        
        <h4>Responsabilité Civile Professionnelle</h4>
        
        <div style="background: #1e40af; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>💼 Assurance RC Professionnelle Obligatoire</h5>
            <p><strong>Montants de garantie recommandés :</strong></p>
            <ul>
                <li>Dommages corporels : 4 500 000€ minimum</li>
                <li>Dommages matériels : 1 500 000€ minimum</li>
                <li>Défense-recours : 300 000€ minimum</li>
                <li>Franchise : 500€ maximum</li>
            </ul>
        </div>

        <h4>Responsabilité Pénale</h4>
        <p>L'inspecteur peut engager sa responsabilité pénale en cas de :</p>
        <ul>
            <li><strong>Faux et usage de faux :</strong> Rapport mensonger (5 ans de prison, 75 000€ d'amende)</li>
            <li><strong>Escroquerie :</strong> Tromperie sur l'état du véhicule (5 ans, 375 000€)</li>
            <li><strong>Mise en danger d'autrui :</strong> Non-signalement d'un défaut de sécurité</li>
        </ul>

        <h4>Responsabilité Administrative</h4>
        <ul>
            <li>Respect des obligations déclaratives (URSSAF, impôts)</li>
            <li>Tenue des registres professionnels</li>
            <li>Formation continue obligatoire</li>
        </ul>

        <h3>🏛️ Code de Déontologie Professionnelle</h3>
        
        <h4>Principes Fondamentaux</h4>
        
        <div style="background: #581c87; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🎯 Les 10 Commandements de l'Inspecteur</h5>
            <ol>
                <li><strong>Compétence :</strong> Maintenir et développer ses connaissances techniques</li>
                <li><strong>Intégrité :</strong> Honnêteté absolue dans les constats</li>
                <li><strong>Objectivité :</strong> Évaluation basée uniquement sur les faits</li>
                <li><strong>Confidentialité :</strong> Protection des informations clients</li>
                <li><strong>Indépendance :</strong> Liberté de jugement préservée</li>
                <li><strong>Responsabilité :</strong> Assume les conséquences de ses actes</li>
                <li><strong>Respect :</strong> Courtoisie envers tous les intervenants</li>
                <li><strong>Loyauté :</strong> Fidélité aux engagements pris</li>
                <li><strong>Diligence :</strong> Célérité dans l'exécution des missions</li>
                <li><strong>Formation :</strong> Mise à jour permanente des compétences</li>
            </ol>
        </div>

        <h4>Relations avec les Clients</h4>
        <ul>
            <li><strong>Information préalable :</strong> Explication claire de la prestation</li>
            <li><strong>Consentement éclairé :</strong> Validation de la compréhension client</li>
            <li><strong>Respect des délais :</strong> Tenue des engagements temporels</li>
            <li><strong>Confidentialité :</strong> Non-divulgation d'informations privées</li>
            <li><strong>Suivi post-intervention :</strong> Disponibilité pour explications</li>
        </ul>

        <h4>Relations avec les Confrères</h4>
        <ul>
            <li><strong>Respect mutuel :</strong> Pas de dénigrement de collègues</li>
            <li><strong>Partage d'expérience :</strong> Contribution à l'évolution métier</li>
            <li><strong>Tarification éthique :</strong> Pas de concurrence déloyale</li>
            <li><strong>Entraide professionnelle :</strong> Solidarité en cas de difficulté</li>
        </ul>

        <h3>📋 Obligations Administratives</h3>
        
        <h4>Statut Juridique</h4>
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Statut</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Avantages</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Inconvénients</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">CA maxi</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Micro-entreprise</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Simplicité, charges réduites</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Plafond CA, pas de TVA</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">72 600€</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>EURL</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Flexibilité, protection</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Comptabilité, charges sociales</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Illimité</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>SASU</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Statut cadre, dividendes</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Charges élevées</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Illimité</td>
            </tr>
        </table>

        <h4>Obligations Déclaratives</h4>
        <ul>
            <li><strong>Déclaration d'activité :</strong> CFE dans les 15 jours</li>
            <li><strong>Immatriculation :</strong> RCS ou Répertoire des Métiers</li>
            <li><strong>Assurance :</strong> RC Pro + véhicule professionnel</li>
            <li><strong>Formation :</strong> Stage SPI (Stage de Préparation à l'Installation)</li>
        </ul>

        <h3>🔍 Cas Pratiques Déontologiques</h3>
        
        <h4>Situation 1 : Conflit d'Intérêt</h4>
        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <p><strong>Cas :</strong> Un ami vous demande d'inspecter un véhicule qu'il souhaite vendre.</p>
            <p><strong>Problème :</strong> Risque de complaisance, crédibilité compromise</p>
            <p><strong>Solution :</strong> Refuser poliment et orienter vers un confrère</p>
        </div>

        <h4>Situation 2 : Pression Commerciale</h4>
        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <p><strong>Cas :</strong> Le vendeur vous propose une "prime" pour un rapport favorable.</p>
            <p><strong>Problème :</strong> Corruption, faux en écriture</p>
            <p><strong>Solution :</strong> Refus catégorique, documenter la tentative</p>
        </div>

        <h4>Situation 3 : Découverte Importante</h4>
        <div style="background: #065f46; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <p><strong>Cas :</strong> Découverte d'un défaut de sécurité critique non déclaré.</p>
            <p><strong>Action :</strong> Signalement immédiat, refus de valider la transaction</p>
            <p><strong>Justification :</strong> Sécurité publique prioritaire</p>
        </div>

        <h3>📚 Points Clés à Retenir</h3>
        
        <ul>
            <li>L'inspecteur est un <strong>expert indépendant</strong> au service de la sécurité des transactions</li>
            <li>La <strong>transparence</strong> et l'<strong>impartialité</strong> sont les piliers de la crédibilité</li>
            <li>Le <strong>cadre légal</strong> protège autant qu'il engage la responsabilité</li>
            <li>La <strong>déontologie</strong> guide les décisions dans les situations complexes</li>
            <li>La <strong>formation continue</strong> est une obligation professionnelle et éthique</li>
        </ul>

        <p><em>Durée estimée : 90 minutes de lecture + 20 minutes pour le quiz</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quel est le rôle principal d'un inspecteur automobile ?",
                "options": ["Vendre des véhicules", "Expert technique indépendant", "Réparateur automobile", "Commercial auto"],
                "correct_answer": "Expert technique indépendant"
            },
            {
                "id": "q2",
                "question": "Dans quels contextes l'inspecteur peut-il intervenir ?",
                "options": ["Uniquement vente particuliers", "Assurance et leasing uniquement", "Ventes, assurance, leasing, expertises", "Uniquement litiges"],
                "correct_answer": "Ventes, assurance, leasing, expertises"
            },
            {
                "id": "q3",
                "question": "Quelle est la durée de la garantie de conformité selon le Code de la Consommation ?",
                "options": ["1 an", "2 ans", "3 ans", "5 ans"],
                "correct_answer": "2 ans"
            },
            {
                "id": "q4",
                "question": "Le montant minimum recommandé pour l'assurance RC Pro en dommages corporels est :",
                "options": ["1 500 000€", "3 000 000€", "4 500 000€", "6 000 000€"],
                "correct_answer": "4 500 000€"
            },
            {
                "id": "q5",
                "question": "En cas de faux et usage de faux, l'inspecteur risque :",
                "options": ["Amende uniquement", "5 ans de prison + 75 000€", "Interdiction d'exercer", "Blâme professionnel"],
                "correct_answer": "5 ans de prison + 75 000€"
            },
            {
                "id": "q6",
                "question": "Quel est le premier principe du code de déontologie ?",
                "options": ["Rapidité", "Compétence", "Rentabilité", "Convivialité"],
                "correct_answer": "Compétence"
            },
            {
                "id": "q7",
                "question": "Le plafond de CA pour une micro-entreprise de services est :",
                "options": ["36 800€", "72 600€", "176 200€", "Illimité"],
                "correct_answer": "72 600€"
            },
            {
                "id": "q8",
                "question": "L'inspecteur doit-il refuser d'inspecter le véhicule d'un ami ?",
                "options": ["Non, pas de problème", "Oui, conflit d'intérêt", "Ça dépend du prix", "Avec une remise"],
                "correct_answer": "Oui, conflit d'intérêt"
            },
            {
                "id": "q9",
                "question": "La formation continue est-elle obligatoire ?",
                "options": ["Non", "Recommandée", "Obligatoire", "Uniquement les 3 premières années"],
                "correct_answer": "Obligatoire"
            },
            {
                "id": "q10",
                "question": "En cas de défaut de sécurité critique, l'inspecteur doit :",
                "options": ["L'ignorer si le client insiste", "Le mentionner discrètement", "Signaler immédiatement", "Négocier un arrangement"],
                "correct_answer": "Signaler immédiatement"
            },
            {
                "id": "q11",
                "question": "Le délai de remise du rapport doit être :",
                "options": ["Immédiat", "24h maximum", "48h maximum", "1 semaine"],
                "correct_answer": "24h maximum"
            },
            {
                "id": "q12",
                "question": "L'indépendance de l'inspecteur signifie :",
                "options": ["Travailler seul", "Pas de lien commercial avec vendeur/acheteur", "Choisir ses horaires", "Fixer ses tarifs"],
                "correct_answer": "Pas de lien commercial avec vendeur/acheteur"
            }
        ]
    }
]

# Routes - Authentication
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    user_dict = user_data.dict()
    user_dict.pop('password')  # Remove plain password
    
    # Create User object for response (without hashed_password)
    user = User(**user_dict)
    
    # Add hashed_password for database storage
    user_dict_for_db = user.dict()
    user_dict_for_db['hashed_password'] = hashed_password
    
    # Store in database with hashed_password
    await db.users.insert_one(user_dict_for_db)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = await db.users.find_one({"email": user_credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Check if user has hashed_password field
    if 'hashed_password' not in user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    if not verify_password(user_credentials.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = create_access_token(data={"sub": user['email']})
    
    # Remove hashed_password before creating User object
    user_dict = {k: v for k, v in user.items() if k != 'hashed_password'}
    user_obj = User(**user_dict)
    
    return Token(access_token=access_token, token_type="bearer", user=user_obj)

# Routes - Course Management
@api_router.get("/modules", response_model=List[Dict[str, Any]])
async def get_modules():
    return COURSE_MODULES

@api_router.get("/modules/{module_id}")
async def get_module(module_id: str):
    module = next((m for m in COURSE_MODULES if m["id"] == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    return module

# Routes - Quiz & Progress
@api_router.post("/quiz/submit", response_model=QuizResult)
async def submit_quiz(quiz_submission: QuizSubmission, current_user: User = Depends(get_current_user)):
    # Find module
    module = next((m for m in COURSE_MODULES if m["id"] == quiz_submission.module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    
    # Calculate score
    total_questions = len(module["quiz_questions"])
    correct_answers = 0
    
    for question in module["quiz_questions"]:
        user_answer = quiz_submission.answers.get(question["id"])
        if user_answer == question["correct_answer"]:
            correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100)
    passed = score >= 70
    
    # Update user progress
    await db.users.update_one(
        {"email": current_user.email},
        {
            "$set": {
                f"quiz_scores.{quiz_submission.module_id}": score,
                f"progress.{quiz_submission.module_id}": "completed" if passed else "failed"
            },
            "$addToSet": {"completed_modules": quiz_submission.module_id} if passed else {}
        }
    )
    
    result = QuizResult(
        module_id=quiz_submission.module_id,
        score=score,
        total_questions=total_questions,
        passed=passed,
        answers=quiz_submission.answers
    )
    
    return result

@api_router.get("/user/progress")
async def get_user_progress(current_user: User = Depends(get_current_user)):
    # Get updated user data
    user = await db.users.find_one({"email": current_user.email})
    return {
        "completed_modules": user.get("completed_modules", []),
        "quiz_scores": user.get("quiz_scores", {}),
        "progress": user.get("progress", {}),
        "total_modules": len(COURSE_MODULES)
    }

@api_router.get("/user/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    user = await db.users.find_one({"email": current_user.email})
    # Remove hashed_password before creating User object
    user_dict = {k: v for k, v in user.items() if k != 'hashed_password'}
    user_obj = User(**user_dict)
    return user_obj

# Initialize modules in database on startup
@app.on_event("startup")
async def initialize_modules():
    for module in COURSE_MODULES:
        existing = await db.modules.find_one({"id": module["id"]})
        if not existing:
            await db.modules.insert_one(module)

# Include router
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()