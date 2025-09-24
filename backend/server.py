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
    return User(**user)

# Initialize course modules
COURSE_MODULES = [
    {
        "id": "module-1",
        "title": "Diagnostic et Positionnement",
        "description": "Évaluation des connaissances initiales et introduction au métier d'inspecteur automobile",
        "duration_minutes": 90,
        "order": 1,
        "content": """
        <h2>Bienvenue dans votre formation d'Inspecteur Automobile</h2>
        
        <h3>Objectifs du module :</h3>
        <ul>
            <li>Comprendre le rôle et les responsabilités d'un inspecteur automobile</li>
            <li>Évaluer vos connaissances actuelles</li>
            <li>Définir vos objectifs de formation personnalisés</li>
        </ul>

        <h3>Le métier d'inspecteur automobile</h3>
        <p>L'inspecteur automobile est un professionnel spécialisé dans l'évaluation complète des véhicules. Il intervient dans de nombreuses situations :</p>
        <ul>
            <li>Ventes entre particuliers</li>
            <li>Évaluations pour assurances</li>
            <li>Contrôles pour sociétés de leasing</li>
            <li>Inspections pré-achat</li>
        </ul>

        <h3>Méthodologie AutoJust</h3>
        <p>Notre formation se base sur la méthodologie AutoJust, reconnue par plus de 200 points de contrôle couvrant :</p>
        <ul>
            <li>État mécanique complet</li>
            <li>Carrosserie et peinture</li>
            <li>Électronique embarquée</li>
            <li>Historique et documents</li>
            <li>Avis spécifique sur le moteur</li>
        </ul>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Combien de points de contrôle comprend la méthodologie AutoJust ?",
                "options": ["150 points", "200 points", "250 points", "300 points"],
                "correct_answer": "200 points"
            },
            {
                "id": "q2", 
                "question": "Dans quelles situations un inspecteur automobile intervient-il ?",
                "options": ["Uniquement ventes particuliers", "Uniquement assurances", "Ventes, assurances, leasing et pré-achat", "Uniquement contrôles techniques"],
                "correct_answer": "Ventes, assurances, leasing et pré-achat"
            }
        ]
    },
    {
        "id": "module-2",
        "title": "Remise à Niveau Mécanique",
        "description": "Bases essentielles en mécanique automobile, moteur, transmission et électronique",
        "duration_minutes": 120,
        "order": 2,
        "content": """
        <h2>Remise à Niveau Mécanique</h2>
        
        <h3>Moteur thermique - Les fondamentaux</h3>
        <ul>
            <li><strong>Cycle 4 temps :</strong> Admission, compression, combustion, échappement</li>
            <li><strong>Composants essentiels :</strong> Pistons, soupapes, vilebrequin, arbre à cames</li>
            <li><strong>Systèmes annexes :</strong> Refroidissement, lubrification, alimentation</li>
        </ul>

        <h3>Transmission</h3>
        <ul>
            <li><strong>Boîte de vitesses :</strong> Manuelle et automatique</li>
            <li><strong>Embrayage :</strong> Fonctionnement et usure</li>
            <li><strong>Différentiel :</strong> Rôle et diagnostic</li>
        </ul>

        <h3>Systèmes de sécurité</h3>
        <ul>
            <li><strong>Freinage :</strong> Disques, plaquettes, ABS, ESP</li>
            <li><strong>Direction :</strong> Crémaillère, direction assistée</li>
            <li><strong>Suspension :</strong> Amortisseurs, ressorts, géométrie</li>
        </ul>

        <h3>Électronique moderne</h3>
        <ul>
            <li><strong>Calculateurs :</strong> Moteur, ABS, climatisation</li>
            <li><strong>Capteurs :</strong> Température, pression, position</li>
            <li><strong>Diagnostic :</strong> OBD, codes défauts</li>
        </ul>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quelles sont les 4 phases du cycle d'un moteur thermique ?",
                "options": ["Admission, compression, combustion, échappement", "Allumage, compression, explosion, évacuation", "Entrée, compression, inflammation, sortie", "Aspiration, serrage, déflagration, expulsion"],
                "correct_answer": "Admission, compression, combustion, échappement"
            },
            {
                "id": "q2",
                "question": "Que signifie l'acronyme ABS ?",
                "options": ["Anti Blocking System", "Automatic Brake System", "Advanced Braking Security", "Auto Block Safety"],
                "correct_answer": "Anti Blocking System"
            }
        ]
    },
    {
        "id": "module-3", 
        "title": "Méthodologie d'Inspection Terrain",
        "description": "Processus complet d'inspection : carrosserie, intérieur, moteur, électronique et essai routier",
        "duration_minutes": 150,
        "order": 3,
        "content": """
        <h2>Méthodologie d'Inspection Terrain</h2>
        
        <h3>Ordre d'inspection optimisé</h3>
        <ol>
            <li><strong>Contrôle visuel extérieur</strong> (15 min)
                <ul>
                    <li>Tour complet du véhicule</li>
                    <li>État de la carrosserie et peinture</li>
                    <li>Pneumatiques et jantes</li>
                    <li>Éclairage et signalisation</li>
                </ul>
            </li>
            
            <li><strong>Inspection intérieure</strong> (10 min)
                <ul>
                    <li>Sièges et garnissages</li>
                    <li>Tableau de bord et commandes</li>
                    <li>Équipements de sécurité</li>
                </ul>
            </li>
            
            <li><strong>Contrôle moteur</strong> (20 min)
                <ul>
                    <li>Inspection visuelle compartiment moteur</li>
                    <li>Niveaux et fuites</li>
                    <li>Test au ralenti et montée en régime</li>
                    <li>Diagnostic électronique OBD</li>
                </ul>
            </li>
            
            <li><strong>Essai routier</strong> (15 min)
                <ul>
                    <li>Démarrage et arrêt</li>
                    <li>Comportement transmission</li>
                    <li>Freinage et direction</li>
                    <li>Systèmes d'aide à la conduite</li>
                </ul>
            </li>
        </ol>

        <h3>Outils digitaux</h3>
        <p><strong>WebApp AutoJust :</strong> Application mobile pour saisie terrain</p>
        <ul>
            <li>Checklist interactive</li>
            <li>Prise de photos géolocalisées</li>
            <li>Notation automatisée</li>
        </ul>

        <p><strong>WeProov :</strong> Plateforme de constat visuel</p>
        <ul>
            <li>Photos haute résolution</li>
            <li>Annotations et commentaires</li>
            <li>Horodatage certifié</li>
        </ul>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quelle est la durée recommandée pour l'essai routier ?",
                "options": ["10 minutes", "15 minutes", "20 minutes", "25 minutes"],
                "correct_answer": "15 minutes"
            },
            {
                "id": "q2",
                "question": "Dans quel ordre doit-on procéder à l'inspection ?",
                "options": ["Moteur, extérieur, intérieur, essai", "Intérieur, extérieur, moteur, essai", "Extérieur, intérieur, moteur, essai", "Essai, extérieur, intérieur, moteur"],
                "correct_answer": "Extérieur, intérieur, moteur, essai"
            }
        ]
    },
    {
        "id": "module-4",
        "title": "Rédaction du Rapport d'Inspection", 
        "description": "Structuration du rapport, intégration photos et rédaction de l'avis moteur spécialisé",
        "duration_minutes": 90,
        "order": 4,
        "content": """
        <h2>Rédaction du Rapport d'Inspection</h2>
        
        <h3>Structure du rapport professionnel</h3>
        <ol>
            <li><strong>Page de garde</strong>
                <ul>
                    <li>Informations véhicule (marque, modèle, année, km)</li>
                    <li>Date et lieu d'inspection</li>
                    <li>Coordonnées inspecteur certifié</li>
                </ul>
            </li>
            
            <li><strong>Synthèse exécutive</strong>
                <ul>
                    <li>Note globale sur 100</li>
                    <li>Points forts et points d'attention</li>
                    <li>Recommandation d'achat (OUI/NON/AVEC RÉSERVES)</li>
                </ul>
            </li>
            
            <li><strong>Détail par catégories</strong>
                <ul>
                    <li>Carrosserie et esthétique (/20)</li>
                    <li>Mécanique et motorisation (/25)</li>
                    <li>Équipements et électronique (/20)</li>
                    <li>Sécurité et conformité (/20)</li>
                    <li>Documents et historique (/15)</li>
                </ul>
            </li>
            
            <li><strong>Avis moteur spécialisé</strong> (OBLIGATOIRE)
                <ul>
                    <li>Analyse selon kilométrage et modèle</li>
                    <li>Points de vigilance spécifiques</li>
                    <li>Estimation coûts d'entretien prévisionnels</li>
                </ul>
            </li>
        </ol>

        <h3>Intégration photos professionnelles</h3>
        <ul>
            <li><strong>Photos d'ensemble :</strong> 4 angles + intérieur</li>
            <li><strong>Photos détail :</strong> Défauts identifiés</li>
            <li><strong>Photos techniques :</strong> Compartiment moteur, dessous</li>
            <li><strong>Qualité :</strong> Éclairage, netteté, cadrage</li>
        </ul>

        <h3>Restitution client</h3>
        <p><strong>Adaptation B2C :</strong> Langage accessible, vulgarisation technique</p>
        <p><strong>Adaptation B2B :</strong> Terminologie professionnelle, chiffrage précis</p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quelle est la note maximale pour la catégorie 'Mécanique et motorisation' ?",
                "options": ["20 points", "25 points", "30 points", "15 points"],
                "correct_answer": "25 points"
            },
            {
                "id": "q2",
                "question": "L'avis moteur spécialisé est-il obligatoire dans le rapport ?",
                "options": ["Non, c'est optionnel", "Oui, c'est obligatoire", "Seulement pour les véhicules récents", "Seulement sur demande client"],
                "correct_answer": "Oui, c'est obligatoire"
            }
        ]
    },
    {
        "id": "module-5",
        "title": "Relation Client et Aspects Légaux",
        "description": "Communication professionnelle, gestion des objections et cadre légal européen",
        "duration_minutes": 90,
        "order": 5,
        "content": """
        <h2>Relation Client et Aspects Légaux</h2>
        
        <h3>Communication professionnelle</h3>
        <ul>
            <li><strong>Neutralité :</strong> Position d'expert indépendant</li>
            <li><strong>Transparence :</strong> Méthodologie claire et explicite</li>
            <li><strong>Pédagogie :</strong> Vulgarisation des aspects techniques</li>
        </ul>

        <h3>Gestion des objections clients</h3>
        <table border="1" style="width:100%">
            <tr>
                <th>Objection</th>
                <th>Réponse type</th>
            </tr>
            <tr>
                <td>"Votre note est trop sévère"</td>
                <td>"Ma notation suit une grille objective basée sur 200 points de contrôle standardisés"</td>
            </tr>
            <tr>
                <td>"Ce défaut n'est pas important"</td>
                <td>"Chaque point est évalué selon son impact sécurité, fiabilité et coût"</td>
            </tr>
            <tr>
                <td>"Vous cherchez à faire échouer la vente"</td>
                <td>"Mon rôle est d'informer objectivement, la décision reste vôtre"</td>
            </tr>
        </table>

        <h3>Cadre légal européen</h3>
        <ul>
            <li><strong>Responsabilité professionnelle :</strong> RC Pro obligatoire</li>
            <li><strong>Protection données :</strong> RGPD et confidentialité</li>
            <li><strong>Droit de rétractation :</strong> Délais légaux</li>
            <li><strong>Garantie légale :</strong> Vices cachés et conformité</li>
        </ul>

        <h3>Statut professionnel</h3>
        <ul>
            <li><strong>Auto-entrepreneur :</strong> Simplicité et flexibilité</li>
            <li><strong>Micro-entreprise :</strong> Régime fiscal avantageux</li>
            <li><strong>SIRET obligatoire :</strong> Identification professionnelle</li>
        </ul>

        <h3>Tarification professionnelle</h3>
        <ul>
            <li><strong>Particuliers :</strong> 150-250€ selon région</li>
            <li><strong>Professionnels :</strong> 200-350€ selon complexité</li>
            <li><strong>Déplacements :</strong> Facturation km selon barème fiscal</li>
        </ul>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quelle assurance est obligatoire pour exercer comme inspecteur automobile ?",
                "options": ["Assurance auto", "RC Professionnelle", "Assurance habitation", "Mutuelle santé"],
                "correct_answer": "RC Professionnelle"
            },
            {
                "id": "q2",
                "question": "Quelle est la fourchette de tarifs pour les particuliers ?",
                "options": ["100-150€", "150-250€", "200-300€", "250-350€"],
                "correct_answer": "150-250€"
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
    user_dict.pop('password')
    user_dict['hashed_password'] = hashed_password
    
    user = User(**user_dict)
    await db.users.insert_one(user.dict())
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = await db.users.find_one({"email": user_credentials.email})
    if not user or not verify_password(user_credentials.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = create_access_token(data={"sub": user['email']})
    user_obj = User(**user)
    
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
    user_obj = User(**user)
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