from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, Request, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
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

# Stripe integration
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

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
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    has_purchased: bool = False
    certificate_url: Optional[str] = None

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

class Quiz(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    module_id: str
    title: str
    questions: List[Dict[str, Any]]  # List of questions with options and correct answers
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

class PaymentTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    session_id: str
    amount: float
    currency: str = "EUR"
    payment_status: str = "pending"  # pending, completed, failed, expired
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ForumPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    content: str
    category: str = "general"  # general, questions, discussions, tips
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

# Certificate Generation Function
def generate_certificate(user_name: str, completion_date: str) -> str:
    """Generate a PDF certificate and return as base64 string"""
    
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = styles['Title']
    title_style.fontSize = 24
    title_style.spaceAfter = 30
    
    heading_style = styles['Heading1']
    heading_style.fontSize = 18
    heading_style.spaceAfter = 20
    
    normal_style = styles['Normal']
    normal_style.fontSize = 14
    normal_style.spaceAfter = 12
    
    # Build the certificate content
    story = []
    
    # Title
    title = Paragraph("CERTIFICAT DE FORMATION", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Formation title
    formation_title = Paragraph("Formation Inspecteur Automobile", heading_style)
    story.append(formation_title)
    story.append(Spacer(1, 30))
    
    # Certificate text
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
    
    # Signature section
    signature = Paragraph("Inspecteur Auto Formation", styles['Heading2'])
    story.append(signature)
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF data and encode it
    buffer.seek(0)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Convert to base64
    return base64.b64encode(pdf_data).decode('utf-8')

# Authentication Routes
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await db.users.find_one({"username": user_data.username})
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password and create user
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump(exclude={"password"})
    user_dict["password_hash"] = hashed_password
    
    user_obj = User(**user_dict)
    doc = user_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.users.insert_one(doc)
    
    # Create access token
    access_token = create_access_token(data={"sub": user_data.email})
    return Token(access_token=access_token, token_type="bearer", user=user_obj)

@api_router.post("/auth/login", response_model=Token)
async def login(login_data: UserLogin):
    user_doc = await db.users.find_one({"email": login_data.email}, {"_id": 0})
    if not user_doc or not verify_password(login_data.password, user_doc["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_doc.pop("password_hash", None)
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    user = User(**user_doc)
    access_token = create_access_token(data={"sub": login_data.email})
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Module Routes
@api_router.get("/modules", response_model=List[Module])
async def get_modules(current_user: Optional[User] = Depends(get_current_user_optional)):
    # If user is not authenticated or hasn't purchased, only show free modules
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
    
    # Check access permissions
    if not module.get("is_free", False):
        if not current_user or not current_user.has_purchased:
            raise HTTPException(status_code=403, detail="Purchase required to access this module")
    
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
    
    # Check access permissions
    if not module.get("is_free", False) and not current_user.has_purchased:
        raise HTTPException(status_code=403, detail="Purchase required to access this module")
    
    # Create or update progress
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
        
        await db.module_progress.insert_one(doc)
    
    # Check if all modules are completed to generate certificate
    if current_user.has_purchased:
        total_modules = await db.modules.count_documents({})
        completed_modules = await db.module_progress.count_documents({
            "user_id": current_user.id,
            "completed": True
        })
        
        if completed_modules >= total_modules and not current_user.certificate_url:
            # Generate certificate
            certificate_b64 = generate_certificate(
                current_user.full_name, 
                datetime.now().strftime('%d/%m/%Y')
            )
            
            # Save certificate URL (in real app, you'd upload to cloud storage)
            certificate_url = f"data:application/pdf;base64,{certificate_b64}"
            
            # Update user with certificate
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
    
    return progress

# Payment Routes
@api_router.post("/payments/checkout-session")
async def create_checkout_session(request: Request, current_user: User = Depends(get_current_user)):
    # Fixed formation package
    FORMATION_PACKAGE = {
        "name": "Formation Inspecteur Automobile Complète",
        "amount": 297.0,
        "currency": "EUR"
    }
    
    # Check if user already purchased
    if current_user.has_purchased:
        raise HTTPException(status_code=400, detail="Formation already purchased")
    
    try:
        # Get host URL from request
        host_url = str(request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/webhook/stripe"
        
        # Initialize Stripe checkout
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
        
        # Build URLs
        success_url = f"{host_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{host_url}/payment-cancel"
        
        # Create checkout request
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
        
        # Create session
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record
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
        # Get payment transaction
        payment_transaction = await db.payment_transactions.find_one({"session_id": session_id})
        if not payment_transaction or payment_transaction["user_id"] != current_user.id:
            raise HTTPException(status_code=404, detail="Payment transaction not found")
        
        # Check with Stripe
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
        checkout_status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Update payment status
        if checkout_status.payment_status == "paid" and payment_transaction["payment_status"] != "completed":
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {
                    "payment_status": "completed",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            # Update user purchase status
            await db.users.update_one(
                {"id": current_user.id},
                {"$set": {"has_purchased": True}}
            )
        
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
            
            # Update payment transaction
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {
                    "payment_status": "completed",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            # Update user purchase status
            if webhook_response.metadata and webhook_response.metadata.get("user_id"):
                user_id = webhook_response.metadata["user_id"]
                await db.users.update_one(
                    {"id": user_id},
                    {"$set": {"has_purchased": True}}
                )
        
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

# Forum Routes
@api_router.get("/forum/posts", response_model=List[Dict[str, Any]])
async def get_forum_posts(category: Optional[str] = None, current_user: User = Depends(get_current_user)):
    if not current_user.has_purchased:
        raise HTTPException(status_code=403, detail="Forum access requires course purchase")
    
    query = {}
    if category:
        query["category"] = category
    
    posts = await db.forum_posts.find(query, {"_id": 0}).sort("created_at", -1).to_list(50)
    
    # Get user info for each post
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
    
    # Get user info for each reply
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
    
    # Check if post exists
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
    
    # Update post reply count
    await db.forum_posts.update_one(
        {"id": post_id},
        {"$inc": {"replies_count": 1}}
    )
    
    return {"message": "Reply created successfully", "reply_id": reply.id}

# Health check
@api_router.get("/")
async def root():
    return {"message": "Inspecteur Auto API is running", "version": "2.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Include the router in the main app
app.include_router(api_router)

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