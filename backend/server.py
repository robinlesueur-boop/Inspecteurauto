from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, Request, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
from passlib.context import CryptContext
import json
from io import BytesIO
import base64
import tempfile

# Certificate generation imports
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Emergent Integrations
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest

# File upload

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import services APRÈS load_dotenv pour que les variables d'environnement soient disponibles
# Email service
from email_service import email_service

# AI Chat service
from ai_chat_service import ai_chat_service

# Media upload service
from media_upload_service import media_service

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Stripe configuration
stripe_api_key = os.environ.get('STRIPE_API_KEY', 'sk_test_emergent')

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-here')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app
app = FastAPI(title="Inspecteur Auto API", version="2.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Pydantic Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str
    full_name: str
    is_active: bool = True
    is_admin: bool = False  # Added admin role
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    has_purchased: bool = False
    certificate_url: Optional[str] = None
    last_login: Optional[datetime] = None
    registration_source: str = "website"  # For tracking leads

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Module(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    content: str
    order_index: int
    duration_minutes: int = 60
    is_free: bool = False
    is_published: bool = True  # Added for admin control
    views_count: int = 0  # Track module popularity
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ModuleProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    module_id: str
    completed: bool = False
    completed_at: Optional[datetime] = None
    reading_time_minutes: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Quiz(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    module_id: str
    title: str
    questions: List[Dict[str, Any]]
    passing_score: int = 80
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizAttempt(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    quiz_id: str
    answers: Dict[str, Any]
    score: float
    passed: bool
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizSubmission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    answers: Dict[str, int]

class PaymentTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    session_id: str
    amount: float
    currency: str = "EUR"
    payment_status: str = "pending"
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PreRegistrationQuestionnaire(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    full_name: str
    answers: Dict[str, Any]
    has_driving_license: bool
    profile_validated: bool = False
    validation_score: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MechanicalAssessment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    answers: Dict[str, int]
    score: float
    passed: bool  # 70% requis
    needs_remedial_module: bool
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SatisfactionSurvey(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    ratings: Dict[str, int]  # QCM ratings
    open_feedback: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AdminMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    admin_id: str
    recipient_id: str  # user_id or "all" for broadcast
    subject: str
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIChatMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_id: str
    user_message: str
    ai_response: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BlogPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    excerpt: str
    content: str
    author: str
    category: str
    image_url: str
    published: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LandingPageContent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hero_title: str = "Devenez Inspecteur Automobile Certifié"
    hero_subtitle: str = "Maîtrisez l'art du diagnostic véhiculaire avec la méthode AutoJust. Formation complète en 11h pour générer jusqu'à 8000€/mois."
    hero_image_url: str = "https://images.unsplash.com/photo-1762517296945-74561c2cf21e"
    stat_graduates: str = "1,200+"
    stat_success_rate: str = "97%"
    stat_duration: str = "11h"
    stat_rating: str = "4.9/5"
    price_amount: str = "297€"
    price_description: str = "Formation complète + Certification"
    cta_primary: str = "Commencer la formation"
    cta_secondary: str = "Module gratuit"
    feature_1_title: str = "Méthode AutoJust"
    feature_1_description: str = "Système d'inspection révolutionnaire utilisé par plus de 500 professionnels en France."
    feature_2_title: str = "Certification Reconnue"
    feature_2_description: str = "Obtenez votre certification officielle d'inspecteur automobile valorisée par l'industrie."
    feature_3_title: str = "Communauté Active"
    feature_3_description: str = "Rejoignez une communauté de 1000+ inspecteurs et échangez sur vos expériences."
    feature_4_title: str = "Revenus Attractifs"
    feature_4_description: str = "Générez 50 à 300€ par inspection avec un potentiel jusqu'à 4000€/mois."
    features_image_url: str = "https://images.unsplash.com/photo-1760836395760-cd81defecf27"
    training_image_url: str = "https://images.unsplash.com/photo-1615906655593-ad0386982a0f"
    social_proof_image_url: str = "https://images.unsplash.com/photo-1573164574572-cb89e39749b4"
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIChatbotConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    system_prompt: str = """Tu es un assistant virtuel pour la plateforme de formation "Inspecteur Auto"..."""
    formation_info: str = """Informations sur la formation..."""
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ForumPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    content: str
    category: str = "general"
    likes: int = 0
    replies_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ForumReply(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    post_id: str
    user_id: str
    content: str
    likes: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Analytics Models
class UserAnalytics(BaseModel):
    total_users: int
    new_users_today: int
    new_users_this_week: int
    paid_users: int
    completion_rate: float

class CourseAnalytics(BaseModel):
    total_modules: int
    total_completions: int
    most_popular_module: str
    average_completion_time: float

# Auth Helper Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await db.users.find_one({"email": user_email}, {"_id": 0})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(**user)

async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
    if credentials is None:
        return None
    return await get_current_user(credentials)

async def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Certificate Generation Function
def generate_certificate(user_name: str, completion_date: str) -> str:
    """Generate a PDF certificate and return as base64 string"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    title_style = styles['Title']
    title_style.fontSize = 24
    title_style.spaceAfter = 30
    
    heading_style = styles['Heading1']
    heading_style.fontSize = 18
    heading_style.spaceAfter = 20
    
    normal_style = styles['Normal']
    normal_style.fontSize = 14
    normal_style.spaceAfter = 12
    
    story = []
    
    title = Paragraph("CERTIFICAT DE FORMATION", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    formation_title = Paragraph("Formation Inspecteur Automobile", heading_style)
    story.append(formation_title)
    story.append(Spacer(1, 30))
    
    cert_text = f"""
    Nous certifions par la présente que
    
    <b>{user_name}</b>
    
    a suivi avec succès la formation complète 
    "Devenir Inspecteur Automobile" et a démontré 
    sa maîtrise des compétences requises.
    
    Cette certification atteste que le bénéficiaire 
    possède les connaissances nécessaires pour 
    exercer en tant qu'inspecteur automobile selon 
    la méthodologie AutoJust.
    
    Date de fin de formation : {completion_date}
    
    Certificat délivré le : {datetime.now().strftime('%d/%m/%Y')}
    """
    
    for line in cert_text.strip().split('\n'):
        if line.strip():
            p = Paragraph(line.strip(), normal_style)
            story.append(p)
        else:
            story.append(Spacer(1, 12))
    
    story.append(Spacer(1, 50))
    signature = Paragraph("Inspecteur Auto Formation", styles['Heading2'])
    story.append(signature)
    
    doc.build(story)
    buffer.seek(0)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(pdf_data).decode('utf-8')

# Authentication Routes
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await db.users.find_one({"username": user_data.username})
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump(exclude={"password"})
    
    user_obj = User(**user_dict)
    doc = user_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc["password_hash"] = hashed_password  # Add password_hash to the document
    
    await db.users.insert_one(doc)
    
    access_token = create_access_token(data={"sub": user_data.email})
    return Token(access_token=access_token, token_type="bearer", user=user_obj)

@api_router.post("/auth/login", response_model=Token)
async def login(login_data: UserLogin):
    user_doc = await db.users.find_one({"email": login_data.email}, {"_id": 0})
    if not user_doc or not verify_password(login_data.password, user_doc["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    await db.users.update_one(
        {"email": login_data.email},
        {"$set": {"last_login": datetime.now(timezone.utc).isoformat()}}
    )
    
    user_doc.pop("password_hash", None)
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    user = User(**user_doc)
    access_token = create_access_token(data={"sub": login_data.email})
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Pre-Registration Questionnaire Routes (Qualiopi Compliance)
class PreRegistrationSubmit(BaseModel):
    email: EmailStr
    full_name: str
    answers: Dict[str, Any]
    has_driving_license: bool

@api_router.post("/pre-registration/submit")
async def submit_pre_registration(submission: PreRegistrationSubmit):
    """Soumettre le questionnaire pré-inscription (10 questions + permis B)"""
    
    # Vérifier le permis de conduire
    if not submission.has_driving_license:
        raise HTTPException(
            status_code=400, 
            detail="Un permis B valide est obligatoire pour accéder à cette formation"
        )
    
    # Calculer un score basé sur les réponses (simulation d'analyse)
    # En réalité, on accepte tout le monde mais on fait semblant d'analyser
    validation_score = 85.0  # Score toujours suffisant
    profile_validated = True
    
    # Enregistrer le questionnaire
    questionnaire = PreRegistrationQuestionnaire(
        email=submission.email,
        full_name=submission.full_name,
        answers=submission.answers,
        has_driving_license=submission.has_driving_license,
        profile_validated=profile_validated,
        validation_score=validation_score
    )
    
    doc = questionnaire.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.pre_registration_questionnaires.insert_one(doc)
    
    return {
        "validated": profile_validated,
        "score": validation_score,
        "message": "Félicitations ! Votre profil correspond parfaitement aux critères de la formation d'inspecteur automobile. Vous pouvez maintenant procéder à l'inscription.",
        "questionnaire_id": questionnaire.id
    }

@api_router.get("/pre-registration/check/{email}")
async def check_pre_registration(email: str):
    """Vérifier si un email a déjà rempli le questionnaire pré-inscription"""
    questionnaire = await db.pre_registration_questionnaires.find_one(
        {"email": email},
        {"_id": 0}
    )
    
    if not questionnaire:
        return {"exists": False}
    
    return {
        "exists": True,
        "validated": questionnaire.get("profile_validated", False),
        "questionnaire_id": questionnaire.get("id")
    }

# Admin Routes
@api_router.get("/admin/pre-registrations")
async def get_pre_registrations(current_user: User = Depends(require_admin)):
    """Get all pre-registration questionnaires (Qualiopi compliance)"""
    questionnaires = await db.pre_registration_questionnaires.find(
        {},
        {"_id": 0}
    ).sort("created_at", -1).to_list(1000)
    
    for q in questionnaires:
        if isinstance(q.get('created_at'), str):
            q['created_at'] = datetime.fromisoformat(q['created_at'])
    
    return questionnaires

@api_router.get("/admin/analytics")
async def get_analytics(current_user: User = Depends(require_admin)):
    """Get platform analytics"""
    # User Analytics
    total_users = await db.users.count_documents({})
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    
    new_users_today = await db.users.count_documents({
        "created_at": {"$gte": today.isoformat()}
    })
    
    new_users_this_week = await db.users.count_documents({
        "created_at": {"$gte": week_ago.isoformat()}
    })
    
    paid_users = await db.users.count_documents({"has_purchased": True})
    
    # Completion rate
    total_modules = await db.modules.count_documents({})
    if total_modules > 0:
        total_possible_completions = total_users * total_modules
        total_actual_completions = await db.module_progress.count_documents({"completed": True})
        completion_rate = (total_actual_completions / total_possible_completions * 100) if total_possible_completions > 0 else 0
    else:
        completion_rate = 0
    
    # Course Analytics
    most_popular_module_pipeline = [
        {"$group": {"_id": "$module_id", "views": {"$sum": 1}}},
        {"$sort": {"views": -1}},
        {"$limit": 1}
    ]
    
    popular_module_result = await db.module_progress.aggregate(most_popular_module_pipeline).to_list(1)
    most_popular_module = "N/A"
    if popular_module_result:
        module_doc = await db.modules.find_one({"id": popular_module_result[0]["_id"]})
        if module_doc:
            most_popular_module = module_doc["title"]
    
    return {
        "user_analytics": {
            "total_users": total_users,
            "new_users_today": new_users_today,
            "new_users_this_week": new_users_this_week,
            "paid_users": paid_users,
            "completion_rate": completion_rate
        },
        "course_analytics": {
            "total_modules": total_modules,
            "total_completions": await db.module_progress.count_documents({"completed": True}),
            "most_popular_module": most_popular_module,
            "conversion_rate": (paid_users / total_users * 100) if total_users > 0 else 0
        },
        "revenue_analytics": {
            "total_revenue": paid_users * 297,  # 297€ per course
            "monthly_revenue": paid_users * 297,  # Simplified for demo
            "average_order_value": 297
        }
    }

@api_router.get("/admin/users")
async def get_all_users(
    admin_user: User = Depends(get_admin_user),
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None
):
    skip = (page - 1) * limit
    query = {}
    
    if search:
        query = {
            "$or": [
                {"full_name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"username": {"$regex": search, "$options": "i"}}
            ]
        }
    
    users = await db.users.find(query, {"_id": 0, "password_hash": 0}).skip(skip).limit(limit).sort("created_at", -1).to_list(limit)
    total = await db.users.count_documents(query)
    
    # Add progress info for each user
    for user in users:
        if isinstance(user.get('created_at'), str):
            user['created_at'] = datetime.fromisoformat(user['created_at'])
        
        # Get user progress
        user_progress = await db.module_progress.find({"user_id": user["id"]}).to_list(100)
        completed_modules = sum(1 for p in user_progress if p.get("completed", False))
        total_modules = await db.modules.count_documents({})
        
        user["progress"] = {
            "completed_modules": completed_modules,
            "total_modules": total_modules,
            "completion_percentage": (completed_modules / total_modules * 100) if total_modules > 0 else 0
        }
    
    return {
        "users": users,
        "pagination": {
            "current_page": page,
            "total_pages": (total + limit - 1) // limit,
            "total_users": total,
            "users_per_page": limit
        }
    }

@api_router.get("/admin/transactions")
async def get_transactions(admin_user: User = Depends(get_admin_user)):
    transactions = await db.payment_transactions.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for transaction in transactions:
        if isinstance(transaction.get('created_at'), str):
            transaction['created_at'] = datetime.fromisoformat(transaction['created_at'])
        if isinstance(transaction.get('updated_at'), str):
            transaction['updated_at'] = datetime.fromisoformat(transaction['updated_at'])
        
        # Get user info
        if transaction.get('user_id'):
            user = await db.users.find_one({"id": transaction['user_id']}, {"_id": 0, "full_name": 1, "email": 1})
            transaction['user'] = user
    
    return transactions

@api_router.get("/admin/course-progress")
async def get_course_progress(admin_user: User = Depends(get_admin_user)):
    # Get module completion stats
    pipeline = [
        {
            "$group": {
                "_id": "$module_id",
                "total_attempts": {"$sum": 1},
                "completed": {"$sum": {"$cond": ["$completed", 1, 0]}},
                "avg_reading_time": {"$avg": "$reading_time_minutes"}
            }
        }
    ]
    
    progress_stats = await db.module_progress.aggregate(pipeline).to_list(100)
    
    # Add module info
    for stat in progress_stats:
        module = await db.modules.find_one({"id": stat["_id"]}, {"_id": 0, "title": 1, "duration_minutes": 1})
        if module:
            stat["module_title"] = module["title"]
            stat["completion_rate"] = (stat["completed"] / stat["total_attempts"] * 100) if stat["total_attempts"] > 0 else 0
    
    return progress_stats

@api_router.put("/admin/users/{user_id}")
async def update_user(
    user_id: str,
    updates: Dict[str, Any],
    admin_user: User = Depends(get_admin_user)
):
    # Remove sensitive fields
    allowed_fields = ["is_active", "has_purchased", "is_admin", "full_name", "email"]
    filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields}
    
    if not filtered_updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": filtered_updates}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User updated successfully"}

# Module Routes
@api_router.get("/modules", response_model=List[Module])
async def get_modules(current_user: Optional[User] = Depends(get_current_user_optional)):
    query = {}
    if not current_user or not current_user.has_purchased:
        query = {"is_free": True}
    
    modules = await db.modules.find(query, {"_id": 0}).sort("order_index", 1).to_list(100)
    
    for module in modules:
        for field in ['created_at', 'updated_at']:
            if isinstance(module.get(field), str):
                module[field] = datetime.fromisoformat(module[field])
    
    return modules

@api_router.get("/modules/{module_id}", response_model=Module)
async def get_module(module_id: str, current_user: Optional[User] = Depends(get_current_user_optional)):
    module = await db.modules.find_one({"id": module_id}, {"_id": 0})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    if not module.get("is_free", False):
        if not current_user or not current_user.has_purchased:
            raise HTTPException(status_code=403, detail="Purchase required to access this module")
    
    # Increment view count
    await db.modules.update_one(
        {"id": module_id},
        {"$inc": {"views_count": 1}}
    )
    
    for field in ['created_at', 'updated_at']:
        if isinstance(module.get(field), str):
            module[field] = datetime.fromisoformat(module[field])
    
    return Module(**module)

# Progress Routes
@api_router.post("/progress/{module_id}/complete")
async def mark_module_complete(module_id: str, current_user: User = Depends(get_current_user)):
    module = await db.modules.find_one({"id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    if not module.get("is_free", False) and not current_user.has_purchased:
        raise HTTPException(status_code=403, detail="Purchase required to access this module")
    
    existing_progress = await db.module_progress.find_one({
        "user_id": current_user.id,
        "module_id": module_id
    })
    
    if existing_progress:
        await db.module_progress.update_one(
            {"id": existing_progress["id"]},
            {"$set": {"completed": True, "completed_at": datetime.now(timezone.utc).isoformat()}}
        )
    else:
        progress = ModuleProgress(
            user_id=current_user.id,
            module_id=module_id,
            completed=True,
            completed_at=datetime.now(timezone.utc)
        )
        doc = progress.model_dump()
        if doc.get('completed_at'):
            doc['completed_at'] = doc['completed_at'].isoformat()
        doc['created_at'] = doc['created_at'].isoformat()
        
        await db.module_progress.insert_one(doc)
    
    # Check if all modules are completed to generate certificate
    if current_user.has_purchased:
        total_modules = await db.modules.count_documents({})
        completed_modules = await db.module_progress.count_documents({
            "user_id": current_user.id,
            "completed": True
        })
        
        if completed_modules >= total_modules and not current_user.certificate_url:
            certificate_b64 = generate_certificate(
                current_user.full_name, 
                datetime.now().strftime('%d/%m/%Y')
            )
            
            certificate_url = f"data:application/pdf;base64,{certificate_b64}"
            
            await db.users.update_one(
                {"id": current_user.id},
                {"$set": {"certificate_url": certificate_url}}
            )
    
    return {"message": "Module marked as complete"}

@api_router.get("/progress")
async def get_user_progress(current_user: User = Depends(get_current_user)):
    progress = await db.module_progress.find({"user_id": current_user.id}, {"_id": 0}).to_list(100)
    
    for p in progress:
        if isinstance(p.get('completed_at'), str):
            p['completed_at'] = datetime.fromisoformat(p['completed_at'])
        if isinstance(p.get('created_at'), str):
            p['created_at'] = datetime.fromisoformat(p['created_at'])
    
    return progress

@api_router.get("/progress/check-access/{module_id}")
async def check_module_access(module_id: str, current_user: User = Depends(get_current_user)):
    """Vérifie si l'utilisateur peut accéder à un module (progression séquentielle)"""
    
    # Récupérer le module demandé
    target_module = await db.modules.find_one({"id": module_id})
    if not target_module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Module gratuit toujours accessible
    if target_module.get("is_free", False):
        return {"can_access": True, "reason": "free_module"}
    
    # Vérifier si l'utilisateur a acheté la formation
    if not current_user.has_purchased:
        return {"can_access": False, "reason": "purchase_required"}
    
    target_order = target_module.get("order_index", 999)
    
    # Module 1 (gratuit) toujours accessible
    if target_order == 1:
        return {"can_access": True, "reason": "first_module"}
    
    # Vérifier si le module précédent est complété avec quiz validé
    previous_order = target_order - 1
    previous_module = await db.modules.find_one({"order_index": previous_order})
    
    if not previous_module:
        return {"can_access": True, "reason": "no_previous_module"}
    
    # Vérifier la complétion du module précédent
    previous_progress = await db.module_progress.find_one({
        "user_id": current_user.id,
        "module_id": previous_module["id"],
        "completed": True
    })
    
    if not previous_progress:
        return {
            "can_access": False, 
            "reason": "previous_module_not_completed",
            "required_module": previous_module["title"]
        }
    
    # Vérifier si le quiz du module précédent a été réussi
    previous_quiz = await db.quizzes.find_one({"module_id": previous_module["id"]})
    if previous_quiz:
        quiz_passed = await db.quiz_attempts.find_one({
            "user_id": current_user.id,
            "quiz_id": previous_quiz["id"],
            "passed": True
        })
        
        if not quiz_passed:
            return {
                "can_access": False,
                "reason": "previous_quiz_not_passed",
                "required_module": previous_module["title"]
            }
    
    return {"can_access": True, "reason": "prerequisites_met"}

# Payment Routes
@api_router.post("/payments/checkout-session")
async def create_checkout_session(request: Request, current_user: User = Depends(get_current_user)):
    FORMATION_PACKAGE = {
        "name": "Formation Inspecteur Automobile Complète",
        "amount": 297.0,
        "currency": "EUR"
    }
    
    if current_user.has_purchased:
        raise HTTPException(status_code=400, detail="Formation already purchased")
    
    try:
        host_url = str(request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/webhook/stripe"
        
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
        
        success_url = f"{host_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{host_url}/payment-cancel"
        
        checkout_request = CheckoutSessionRequest(
            amount=FORMATION_PACKAGE["amount"],
            currency=FORMATION_PACKAGE["currency"],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "user_id": current_user.id,
                "user_email": current_user.email,
                "product": "formation_complete"
            }
        )
        
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        payment_transaction = PaymentTransaction(
            user_id=current_user.id,
            session_id=session.session_id,
            amount=FORMATION_PACKAGE["amount"],
            currency=FORMATION_PACKAGE["currency"],
            payment_status="pending",
            metadata={
                "user_email": current_user.email,
                "product": "formation_complete"
            }
        )
        
        doc = payment_transaction.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        await db.payment_transactions.insert_one(doc)
        
        return {"url": session.url, "session_id": session.session_id}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment error: {str(e)}")

@api_router.get("/payments/status/{session_id}")
async def get_payment_status(session_id: str, current_user: User = Depends(get_current_user)):
    try:
        payment_transaction = await db.payment_transactions.find_one({"session_id": session_id})
        if not payment_transaction or payment_transaction["user_id"] != current_user.id:
            raise HTTPException(status_code=404, detail="Payment transaction not found")
        
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
        checkout_status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        if checkout_status.payment_status == "paid" and payment_transaction["payment_status"] != "completed":
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {
                    "payment_status": "completed",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            await db.users.update_one(
                {"id": current_user.id},
                {"$set": {"has_purchased": True}}
            )
            
            # Send welcome email
            try:
                email_service.send_welcome_email(
                    recipient_email=current_user.email,
                    full_name=current_user.full_name,
                    username=current_user.username
                )
                logger.info(f"Welcome email sent to {current_user.email}")
            except Exception as email_error:
                logger.error(f"Failed to send welcome email: {str(email_error)}")
                # Don't fail the payment status update if email fails
        
        elif checkout_status.status == "expired":
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {
                    "payment_status": "expired",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
        
        return {
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "amount_total": checkout_status.amount_total,
            "currency": checkout_status.currency
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error checking payment status: {str(e)}")

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    try:
        body = await request.body()
        signature = request.headers.get("Stripe-Signature")
        
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        if webhook_response.event_type == "checkout.session.completed":
            session_id = webhook_response.session_id
            
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {
                    "payment_status": "completed",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            if webhook_response.metadata and webhook_response.metadata.get("user_id"):
                user_id = webhook_response.metadata["user_id"]
                await db.users.update_one(
                    {"id": user_id},
                    {"$set": {"has_purchased": True}}
                )
        
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

# Quiz Routes
@api_router.get("/quizzes/module/{module_id}")
async def get_module_quiz(module_id: str, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get quiz for a specific module"""
    module = await db.modules.find_one({"id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Check if user can access the module
    if not module.get("is_free", False):
        if not current_user or not current_user.has_purchased:
            raise HTTPException(status_code=403, detail="Purchase required to access this quiz")
    
    quiz = await db.quizzes.find_one({"module_id": module_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found for this module")
    
    # Convert dates
    if isinstance(quiz.get('created_at'), str):
        quiz['created_at'] = datetime.fromisoformat(quiz['created_at'])
    
    return quiz

@api_router.post("/quizzes/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: str,
    submission: QuizSubmission,
    current_user: User = Depends(get_current_user)
):
    """Submit quiz answers and get results"""
    answers = submission.answers
    
    quiz = await db.quizzes.find_one({"id": quiz_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz["questions"])
    detailed_results = []
    
    for question in quiz["questions"]:
        question_id = question["id"]
        user_answer = answers.get(question_id, -1)
        correct_answer = question["correct_answer"]
        is_correct = user_answer == correct_answer
        
        if is_correct:
            correct_answers += 1
        
        detailed_results.append({
            "question_id": question_id,
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.get("explanation", "")
        })
    
    score = (correct_answers / total_questions) * 100
    passed = score >= quiz["passing_score"]
    
    # Save attempt
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        answers=answers,
        score=score,
        passed=passed
    )
    
    doc = attempt.model_dump()
    doc['completed_at'] = doc['completed_at'].isoformat()
    
    await db.quiz_attempts.insert_one(doc)
    
    return {
        "score": score,
        "passed": passed,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "passing_score": quiz["passing_score"],
        "detailed_results": detailed_results
    }

@api_router.get("/quizzes/{quiz_id}/attempts")
async def get_quiz_attempts(
    quiz_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get user's attempts for a specific quiz"""
    attempts = await db.quiz_attempts.find(
        {"quiz_id": quiz_id, "user_id": current_user.id},
        {"_id": 0}
    ).sort("completed_at", -1).to_list(10)
    
    for attempt in attempts:
        if isinstance(attempt.get('completed_at'), str):
            attempt['completed_at'] = datetime.fromisoformat(attempt['completed_at'])
    
    return attempts

# Forum Routes
@api_router.get("/forum/posts", response_model=List[Dict[str, Any]])
async def get_forum_posts(category: Optional[str] = None, current_user: User = Depends(get_current_user)):
    if not current_user.has_purchased:
        raise HTTPException(status_code=403, detail="Forum access requires course purchase")
    
    query = {}
    if category:
        query["category"] = category
    
    posts = await db.forum_posts.find(query, {"_id": 0}).sort("created_at", -1).to_list(50)
    
    for post in posts:
        user = await db.users.find_one({"id": post["user_id"]}, {"_id": 0, "full_name": 1, "avatar_url": 1})
        post["user"] = user or {"full_name": "Unknown", "avatar_url": None}
        
        if isinstance(post.get('created_at'), str):
            post['created_at'] = datetime.fromisoformat(post['created_at'])
        if isinstance(post.get('updated_at'), str):
            post['updated_at'] = datetime.fromisoformat(post['updated_at'])
    
    return posts

@api_router.post("/forum/posts")
async def create_forum_post(title: str, content: str, category: str = "general", current_user: User = Depends(get_current_user)):
    if not current_user.has_purchased:
        raise HTTPException(status_code=403, detail="Forum access requires course purchase")
    
    post = ForumPost(
        user_id=current_user.id,
        title=title,
        content=content,
        category=category
    )
    
    doc = post.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    await db.forum_posts.insert_one(doc)
    return {"message": "Post created successfully", "post_id": post.id}

@api_router.get("/forum/posts/{post_id}/replies", response_model=List[Dict[str, Any]])
async def get_forum_replies(post_id: str, current_user: User = Depends(get_current_user)):
    if not current_user.has_purchased:
        raise HTTPException(status_code=403, detail="Forum access requires course purchase")
    
    replies = await db.forum_replies.find({"post_id": post_id}, {"_id": 0}).sort("created_at", 1).to_list(100)
    
    for reply in replies:
        user = await db.users.find_one({"id": reply["user_id"]}, {"_id": 0, "full_name": 1, "avatar_url": 1})
        reply["user"] = user or {"full_name": "Unknown", "avatar_url": None}
        
        if isinstance(reply.get('created_at'), str):
            reply['created_at'] = datetime.fromisoformat(reply['created_at'])
    
    return replies

@api_router.post("/forum/posts/{post_id}/replies")
async def create_forum_reply(post_id: str, content: str, current_user: User = Depends(get_current_user)):
    if not current_user.has_purchased:
        raise HTTPException(status_code=403, detail="Forum access requires course purchase")
    
    post = await db.forum_posts.find_one({"id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    reply = ForumReply(
        post_id=post_id,
        user_id=current_user.id,
        content=content
    )
    
    doc = reply.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.forum_replies.insert_one(doc)
    
    await db.forum_posts.update_one(
        {"id": post_id},
        {"$inc": {"replies_count": 1}}
    )
    
    return {"message": "Reply created successfully", "reply_id": reply.id}

# Preliminary Quiz Routes (Career Fit & Mechanical Knowledge)
@api_router.get("/preliminary-quiz/career-fit")
async def get_career_fit_quiz():
    """Get the career fit quiz (no authentication required - pre-registration)"""
    quiz = await db.quizzes.find_one({"module_id": "career_fit"}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Career fit quiz not found")
    
    # Convert dates
    if isinstance(quiz.get('created_at'), str):
        quiz['created_at'] = datetime.fromisoformat(quiz['created_at'])
    
    return quiz

@api_router.post("/preliminary-quiz/career-fit/submit")
async def submit_career_fit_quiz(submission: QuizSubmission):
    """Submit career fit quiz (no authentication required - pre-registration)"""
    answers = submission.answers
    
    quiz = await db.quizzes.find_one({"module_id": "career_fit"})
    if not quiz:
        raise HTTPException(status_code=404, detail="Career fit quiz not found")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz["questions"])
    
    for question in quiz["questions"]:
        question_id = question["id"]
        user_answer = answers.get(question_id, -1)
        correct_answer = question["correct_answer"]
        
        if user_answer == correct_answer:
            correct_answers += 1
    
    score = (correct_answers / total_questions) * 100
    passed = score >= quiz["passing_score"]
    
    return {
        "score": score,
        "passed": passed,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "passing_score": quiz["passing_score"]
    }

@api_router.get("/preliminary-quiz/mechanical-knowledge")
async def get_mechanical_knowledge_quiz(current_user: User = Depends(get_current_user)):
    """Get the mechanical knowledge quiz (requires authentication, post-payment)"""
    quiz = await db.quizzes.find_one({"module_id": "mechanical_knowledge"}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Mechanical knowledge quiz not found")
    
    # Convert dates
    if isinstance(quiz.get('created_at'), str):
        quiz['created_at'] = datetime.fromisoformat(quiz['created_at'])
    
    return quiz

@api_router.post("/preliminary-quiz/mechanical-knowledge/submit")
async def submit_mechanical_knowledge_quiz(
    submission: QuizSubmission,
    current_user: User = Depends(get_current_user)
):
    """Submit mechanical knowledge quiz and determine if remedial module needed"""
    answers = submission.answers
    
    quiz = await db.quizzes.find_one({"module_id": "mechanical_knowledge"})
    if not quiz:
        raise HTTPException(status_code=404, detail="Mechanical knowledge quiz not found")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz["questions"])
    detailed_results = []
    
    for question in quiz["questions"]:
        question_id = question["id"]
        user_answer = answers.get(question_id, -1)
        correct_answer = question["correct_answer"]
        is_correct = user_answer == correct_answer
        
        if is_correct:
            correct_answers += 1
        
        detailed_results.append({
            "question_id": question_id,
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.get("explanation", "")
        })
    
    score = (correct_answers / total_questions) * 100
    passed = score >= 70  # 70% threshold for mechanical knowledge
    needs_remedial = score < 70
    
    # Save mechanical assessment
    assessment = MechanicalAssessment(
        user_id=current_user.id,
        answers=answers,
        score=score,
        passed=passed,
        needs_remedial_module=needs_remedial
    )
    
    doc = assessment.model_dump()
    doc['completed_at'] = doc['completed_at'].isoformat()
    
    await db.mechanical_assessments.insert_one(doc)
    
    # Update user's mechanical assessment status
    await db.users.update_one(
        {"id": current_user.id},
        {"$set": {
            "mechanical_assessment_completed": True,
            "needs_remedial_module": needs_remedial,
            "mechanical_assessment_score": score
        }}
    )
    
    return {
        "score": score,
        "passed": passed,
        "needs_remedial_module": needs_remedial,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "detailed_results": detailed_results
    }

@api_router.get("/preliminary-quiz/mechanical-knowledge/status")
async def get_mechanical_knowledge_status(current_user: User = Depends(get_current_user)):
    """Check if user has completed mechanical knowledge quiz"""
    assessment = await db.mechanical_assessments.find_one(
        {"user_id": current_user.id},
        {"_id": 0}
    )
    
    if not assessment:
        return {
            "completed": False,
            "needs_remedial_module": None,
            "score": None
        }
    
    return {
        "completed": True,
        "needs_remedial_module": assessment.get("needs_remedial_module", False),
        "score": assessment.get("score", 0)
    }

# Satisfaction Survey Routes
@api_router.post("/satisfaction-survey/submit")
async def submit_satisfaction_survey(
    ratings: Dict[str, int],
    open_feedback: str,
    current_user: User = Depends(get_current_user)
):
    """Submit satisfaction survey after completing training"""
    
    # Check if user has already submitted
    existing = await db.satisfaction_surveys.find_one({"user_id": current_user.id})
    if existing:
        raise HTTPException(status_code=400, detail="Survey already submitted")
    
    survey = SatisfactionSurvey(
        user_id=current_user.id,
        ratings=ratings,
        open_feedback=open_feedback
    )
    
    doc = survey.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.satisfaction_surveys.insert_one(doc)
    
    return {
        "message": "Merci pour votre retour !",
        "survey_id": survey.id
    }

@api_router.get("/satisfaction-survey/check")
async def check_satisfaction_survey(current_user: User = Depends(get_current_user)):
    """Check if user has submitted satisfaction survey"""
    survey = await db.satisfaction_surveys.find_one({"user_id": current_user.id})
    
    return {
        "submitted": survey is not None
    }

# Admin Messaging Routes
@api_router.post("/admin/messages/send")
async def send_admin_message(
    recipient_id: str,
    subject: str,
    message: str,
    current_user: User = Depends(require_admin)
):
    """Send message from admin to student(s)"""
    
    # If recipient_id is "all", it's a broadcast
    if recipient_id != "all":
        # Check if recipient exists
        recipient = await db.users.find_one({"id": recipient_id})
        if not recipient:
            raise HTTPException(status_code=404, detail="User not found")
    
    admin_message = AdminMessage(
        admin_id=current_user.id,
        recipient_id=recipient_id,
        subject=subject,
        message=message
    )
    
    doc = admin_message.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.admin_messages.insert_one(doc)
    
    return {
        "message": "Message sent successfully",
        "message_id": admin_message.id
    }

@api_router.get("/messages")
async def get_user_messages(current_user: User = Depends(get_current_user)):
    """Get all messages for current user"""
    messages = await db.admin_messages.find(
        {
            "$or": [
                {"recipient_id": current_user.id},
                {"recipient_id": "all"}
            ]
        },
        {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    
    for msg in messages:
        if isinstance(msg.get('created_at'), str):
            msg['created_at'] = datetime.fromisoformat(msg['created_at'])
    
    return messages

@api_router.patch("/messages/{message_id}/read")
async def mark_message_read(
    message_id: str,
    current_user: User = Depends(get_current_user)
):
    """Mark message as read"""
    result = await db.admin_messages.update_one(
        {"id": message_id, "recipient_id": current_user.id},
        {"$set": {"is_read": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return {"message": "Message marked as read"}

@api_router.get("/admin/messages")
async def get_all_messages(current_user: User = Depends(require_admin)):
    """Get all admin messages (admin only)"""
    messages = await db.admin_messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(500)
    
    for msg in messages:
        if isinstance(msg.get('created_at'), str):
            msg['created_at'] = datetime.fromisoformat(msg['created_at'])
        
        # Get recipient info
        if msg['recipient_id'] != "all":
            recipient = await db.users.find_one(
                {"id": msg['recipient_id']},
                {"_id": 0, "full_name": 1, "email": 1}
            )
            msg['recipient_info'] = recipient
        else:
            msg['recipient_info'] = {"full_name": "Tous les étudiants", "email": "broadcast"}
    
    return messages

# Admin Module Management Routes
class ModuleUpdate(BaseModel):
    title: str
    description: str
    content: str
    duration_minutes: int
    is_free: bool

@api_router.post("/admin/modules")
async def create_module(
    module_data: ModuleUpdate,
    current_user: User = Depends(require_admin)
):
    """Create new module (admin only)"""
    
    # Get the highest order_index
    modules = await db.modules.find().sort("order_index", -1).limit(1).to_list(1)
    next_order = 1 if not modules else modules[0].get("order_index", 0) + 1
    
    # Create new module
    new_module = Module(
        title=module_data.title,
        description=module_data.description,
        content=module_data.content,
        duration_minutes=module_data.duration_minutes,
        is_free=module_data.is_free,
        order_index=next_order
    )
    
    doc = new_module.model_dump()
    await db.modules.insert_one(doc)
    
    return {"message": "Module created successfully", "module_id": new_module.id, "order_index": next_order}

@api_router.put("/admin/modules/{module_id}")
async def update_module(
    module_id: str,
    module_data: ModuleUpdate,
    current_user: User = Depends(require_admin)
):
    """Update module content (admin only)"""
    
    # Check if module exists
    module = await db.modules.find_one({"id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Update module
    result = await db.modules.update_one(
        {"id": module_id},
        {"$set": {
            "title": module_data.title,
            "description": module_data.description,
            "content": module_data.content,
            "duration_minutes": module_data.duration_minutes,
            "is_free": module_data.is_free
        }}
    )
    
    if result.modified_count == 0:
        # Actually check if data is same
        return {"message": "Module already up to date", "module_id": module_id}
    
    return {"message": "Module updated successfully", "module_id": module_id}

@api_router.delete("/admin/modules/{module_id}")
async def delete_module(
    module_id: str,
    current_user: User = Depends(require_admin)
):
    """Delete module (admin only)"""
    
    # Check if module exists
    module = await db.modules.find_one({"id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Delete associated quiz
    await db.quizzes.delete_many({"module_id": module_id})
    
    # Delete module
    await db.modules.delete_one({"id": module_id})
    
    return {"message": "Module deleted successfully", "module_id": module_id}

# Admin Quiz Management
@api_router.post("/admin/quizzes")
async def create_quiz(
    quiz_data: dict,
    current_user: User = Depends(require_admin)
):
    """Create quiz for a module (admin only)"""
    
    module_id = quiz_data.get("module_id")
    
    # Check if module exists
    module = await db.modules.find_one({"id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Check if quiz already exists for this module
    existing_quiz = await db.quizzes.find_one({"module_id": module_id})
    if existing_quiz:
        raise HTTPException(status_code=400, detail="Quiz already exists for this module")
    
    # Create new quiz
    new_quiz = Quiz(
        module_id=module_id,
        title=quiz_data.get("title", f"Quiz - {module['title']}"),
        description=quiz_data.get("description", ""),
        passing_score=quiz_data.get("passing_score", 80),
        questions=quiz_data.get("questions", [])
    )
    
    doc = new_quiz.model_dump()
    await db.quizzes.insert_one(doc)
    
    return {"message": "Quiz created successfully", "quiz_id": new_quiz.id}

@api_router.put("/admin/quizzes/{quiz_id}")
async def update_quiz(
    quiz_id: str,
    quiz_data: dict,
    current_user: User = Depends(require_admin)
):
    """Update quiz (admin only)"""
    
    # Check if quiz exists
    quiz = await db.quizzes.find_one({"id": quiz_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Update quiz
    result = await db.quizzes.update_one(
        {"id": quiz_id},
        {"$set": {
            "title": quiz_data.get("title"),
            "description": quiz_data.get("description", ""),
            "passing_score": quiz_data.get("passing_score", 80),
            "questions": quiz_data.get("questions", [])
        }}
    )
    
    return {"message": "Quiz updated successfully", "quiz_id": quiz_id}

@api_router.delete("/admin/quizzes/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    current_user: User = Depends(require_admin)
):
    """Delete quiz (admin only)"""
    
    # Check if quiz exists
    quiz = await db.quizzes.find_one({"id": quiz_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Delete quiz
    await db.quizzes.delete_one({"id": quiz_id})
    
    return {"message": "Quiz deleted successfully", "quiz_id": quiz_id}

# Media Upload Routes (Admin only)
@api_router.post("/admin/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin)
):
    """Upload une image pour les modules (admin only)"""
    
    # Vérifier le type de fichier
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Utilisez JPG, PNG, GIF ou WebP")
    
    # Lire le contenu
    content = await file.read()
    
    # Vérifier la taille (max 5MB)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 5MB)")
    
    # Sauvegarder
    result = media_service.save_file(content, file.filename, "image")
    
    return result

@api_router.post("/admin/upload/video")
async def upload_video(
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin)
):
    """Upload une vidéo pour les modules (admin only)"""
    
    # Vérifier le type de fichier
    allowed_types = ["video/mp4", "video/webm", "video/ogg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Utilisez MP4, WebM ou OGG")
    
    # Lire le contenu
    content = await file.read()
    
    # Vérifier la taille (max 50MB)
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 50MB)")
    
    # Sauvegarder
    result = media_service.save_file(content, file.filename, "video")
    
    return result

@api_router.get("/admin/media/list")
async def list_media(
    file_type: str = None,
    current_user: User = Depends(require_admin)
):
    """Liste tous les médias uploadés (admin only)"""
    files = media_service.list_files(file_type)
    return {"files": files, "count": len(files)}

@api_router.delete("/admin/media/{file_type}/{filename}")
async def delete_media(
    file_type: str,
    filename: str,
    current_user: User = Depends(require_admin)
):
    """Supprime un média (admin only)"""
    success = media_service.delete_file(filename, file_type)
    
    if not success:
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return {"message": "Fichier supprimé avec succès"}

# AI Chat Routes
@api_router.post("/ai-chat")
async def ai_chat(
    message: str,
    current_user: User = Depends(get_current_user)
):
    """Send message to AI assistant and get response"""
    
    # Generate session ID for user (use user_id as session base)
    session_id = f"user_{current_user.id}"
    
    # Get AI response
    response = await ai_chat_service.get_response(message, session_id)
    
    # Save chat history
    chat_message = AIChatMessage(
        user_id=current_user.id,
        session_id=session_id,
        user_message=message,
        ai_response=response
    )
    
    doc = chat_message.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.ai_chat_messages.insert_one(doc)
    
    return {
        "message": message,
        "response": response,
        "message_id": chat_message.id
    }

@api_router.get("/ai-chat/history")
async def get_ai_chat_history(
    current_user: User = Depends(get_current_user),
    limit: int = 50
):
    """Get user's AI chat history"""
    
    messages = await db.ai_chat_messages.find(
        {"user_id": current_user.id},
        {"_id": 0}
    ).sort("created_at", -1).limit(limit).to_list(limit)
    
    # Reverse to get chronological order
    messages.reverse()
    
    for msg in messages:
        if isinstance(msg.get('created_at'), str):
            msg['created_at'] = datetime.fromisoformat(msg['created_at'])
    
    return messages

# Blog Management Routes
@api_router.get("/blog/posts")
async def get_blog_posts(published_only: bool = True):
    """Get all blog posts (public route)"""
    query = {"published": True} if published_only else {}
    
    posts = await db.blog_posts.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for post in posts:
        if isinstance(post.get('created_at'), str):
            post['created_at'] = datetime.fromisoformat(post['created_at'])
        if isinstance(post.get('updated_at'), str):
            post['updated_at'] = datetime.fromisoformat(post['updated_at'])
    
    return posts

# Landing Page Content Management
@api_router.get("/landing-page/content")
async def get_landing_page_content():
    """Get landing page content (public route)"""
    content = await db.landing_page_content.find_one({}, {"_id": 0})
    
    if not content:
        # Return default content if none exists
        default_content = LandingPageContent()
        return default_content.model_dump()
    
    if isinstance(content.get('updated_at'), str):
        content['updated_at'] = datetime.fromisoformat(content['updated_at'])
    
    return content

@api_router.put("/admin/landing-page/content")
async def update_landing_page_content(
    content_data: dict,
    current_user: User = Depends(require_admin)
):
    """Update landing page content (admin only)"""
    
    # Check if content exists
    existing = await db.landing_page_content.find_one({})
    
    # Update timestamp
    content_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    if existing:
        # Update existing
        await db.landing_page_content.update_one(
            {"id": existing["id"]},
            {"$set": content_data}
        )
    else:
        # Create new with default values merged
        default_content = LandingPageContent()
        merged_content = {**default_content.model_dump(), **content_data}
        await db.landing_page_content.insert_one(merged_content)
    
    return {"message": "Contenu de la landing page mis à jour avec succès"}

# AI Chatbot Configuration
@api_router.get("/admin/chatbot/config")
async def get_chatbot_config(current_user: User = Depends(require_admin)):
    """Get chatbot configuration (admin only)"""
    config = await db.ai_chatbot_config.find_one({}, {"_id": 0})
    
    if not config:
        # Return default config
        default_config = {
            "system_prompt": """Tu es un assistant virtuel expert pour la plateforme de formation "Inspecteur Auto". 

Tu aides les étudiants et visiteurs à comprendre la formation pour devenir inspecteur automobile certifié.

INFORMATIONS CLÉS SUR LA FORMATION:
- Durée: 11 heures de formation complète
- Prix: 297€ (paiement en 4x disponible)
- Certification officielle reconnue
- 8 modules de formation + quiz
- Taux de réussite: 97%
- Plus de 1200 diplômés

MODULES DE FORMATION:
1. Introduction à l'inspection automobile
2. Remise à niveau mécanique (si nécessaire)
3. Moteur et transmission
4. Systèmes électriques et électroniques
5. Freinage et suspension
6. ADAS (Systèmes d'aide à la conduite)
7. Aspects réglementaires et légaux
8. Carrosserie et châssis

REVENUS POTENTIELS:
- 50€ à 300€ par inspection
- Potentiel jusqu'à 4000€/mois
- Activité indépendante ou salariée

Tu dois:
1. Répondre de manière claire, pédagogique et professionnelle
2. Utiliser un ton encourageant et positif
3. Donner des exemples concrets quand pertinent
4. Si tu ne connais pas la réponse, le dire honnêtement
5. Suggérer de contacter le support pour questions administratives
6. Répondre en français

Sois concis (200-300 mots max) sauf si explication détaillée nécessaire.""",
            "formation_info": """Formation Inspecteur Automobile - Informations complètes

DURÉE: 11 heures
PRIX: 297€
CERTIFICATION: Officielle et reconnue
MODULES: 8 modules complets + quiz
TAUX DE RÉUSSITE: 97%""",
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        return default_config
    
    return config

@api_router.put("/admin/chatbot/config")
async def update_chatbot_config(
    config_data: dict,
    current_user: User = Depends(require_admin)
):
    """Update chatbot configuration (admin only)"""
    
    config_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    # Upsert (update or insert)
    await db.ai_chatbot_config.update_one(
        {},
        {"$set": config_data},
        upsert=True
    )
    
    # Recharger la configuration dans le service
    from ai_chat_service import ai_chat_service
    ai_chat_service.reload_config()
    
    return {"message": "Configuration du chatbot mise à jour avec succès"}

@api_router.get("/blog/posts/{slug}")
async def get_blog_post_by_slug(slug: str):
    """Get a single blog post by slug"""
    post = await db.blog_posts.find_one({"slug": slug, "published": True}, {"_id": 0})
    
    if not post:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if isinstance(post.get('created_at'), str):
        post['created_at'] = datetime.fromisoformat(post['created_at'])
    if isinstance(post.get('updated_at'), str):
        post['updated_at'] = datetime.fromisoformat(post['updated_at'])
    
    return post

@api_router.get("/admin/blog/posts")
async def get_all_blog_posts_admin(current_user: User = Depends(require_admin)):
    """Get all blog posts including unpublished (admin only)"""
    posts = await db.blog_posts.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for post in posts:
        if isinstance(post.get('created_at'), str):
            post['created_at'] = datetime.fromisoformat(post['created_at'])
        if isinstance(post.get('updated_at'), str):
            post['updated_at'] = datetime.fromisoformat(post['updated_at'])
    
    return posts

@api_router.post("/admin/blog/posts")
async def create_blog_post(
    post_data: BlogPost,
    current_user: User = Depends(require_admin)
):
    """Create a new blog post (admin only)"""
    
    # Check if slug already exists
    existing = await db.blog_posts.find_one({"slug": post_data.slug})
    if existing:
        raise HTTPException(status_code=400, detail="Un article avec ce slug existe déjà")
    
    doc = post_data.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    await db.blog_posts.insert_one(doc)
    
    return {"message": "Article créé avec succès", "post_id": post_data.id}

@api_router.put("/admin/blog/posts/{post_id}")
async def update_blog_post(
    post_id: str,
    post_data: BlogPost,
    current_user: User = Depends(require_admin)
):
    """Update a blog post (admin only)"""
    
    # Check if post exists
    existing = await db.blog_posts.find_one({"id": post_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Update timestamp
    doc = post_data.model_dump()
    doc['updated_at'] = datetime.now(timezone.utc).isoformat()
    doc['created_at'] = existing['created_at']  # Keep original creation date
    
    result = await db.blog_posts.update_one(
        {"id": post_id},
        {"$set": doc}
    )
    
    if result.modified_count == 0:
        return {"message": "Aucune modification apportée", "post_id": post_id}
    
    return {"message": "Article mis à jour avec succès", "post_id": post_id}

@api_router.delete("/admin/blog/posts/{post_id}")
async def delete_blog_post(
    post_id: str,
    current_user: User = Depends(require_admin)
):
    """Delete a blog post (admin only)"""
    
    result = await db.blog_posts.delete_one({"id": post_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return {"message": "Article supprimé avec succès"}

@api_router.patch("/admin/blog/posts/{post_id}/publish")
async def toggle_blog_post_publish(
    post_id: str,
    published: bool,
    current_user: User = Depends(require_admin)
):
    """Toggle publish status of a blog post (admin only)"""
    
    result = await db.blog_posts.update_one(
        {"id": post_id},
        {"$set": {"published": published, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return {"message": f"Article {'publié' if published else 'dépublié'} avec succès"}

# Health check
@api_router.get("/")
async def root():
    return {"message": "Inspecteur Auto API is running", "version": "2.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# SEO - Sitemap XML
@api_router.get("/sitemap.xml")
async def get_sitemap():
    """Generate sitemap.xml for SEO"""
    from fastapi.responses import Response
    
    # Get all blog posts
    blog_posts = await db.blog_posts.find({"published": True}, {"slug": 1, "updated_at": 1}).to_list(100)
    
    base_url = "https://autoedge.preview.emergentagent.com"  # À remplacer par le vrai domaine
    
    # Pages statiques
    static_pages = [
        {"loc": "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/register", "priority": "0.9", "changefreq": "monthly"},
        {"loc": "/pre-registration", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/programme", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/debouches-revenus", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/methode-autojust", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/certification", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/faq", "priority": "0.7", "changefreq": "weekly"},
        {"loc": "/blog", "priority": "0.8", "changefreq": "daily"},
        {"loc": "/contact", "priority": "0.6", "changefreq": "yearly"},
        {"loc": "/mentions-legales", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/confidentialite", "priority": "0.3", "changefreq": "yearly"},
    ]
    
    # Construire le XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Ajouter les pages statiques
    for page in static_pages:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}{page["loc"]}</loc>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += '  </url>\n'
    
    # Ajouter les articles de blog
    for post in blog_posts:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}/blog/{post["slug"]}</loc>\n'
        xml += '    <priority>0.7</priority>\n'
        xml += '    <changefreq>monthly</changefreq>\n'
        if post.get('updated_at'):
            updated = post['updated_at']
            if isinstance(updated, str):
                xml += f'    <lastmod>{updated[:10]}</lastmod>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return Response(content=xml, media_type="application/xml")

# Include the router in the main app
app.include_router(api_router)

# Mount static files for uploads
uploads_dir = Path(__file__).parent / "uploads"
uploads_dir.mkdir(exist_ok=True)
(uploads_dir / "images").mkdir(exist_ok=True)
(uploads_dir / "videos").mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

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