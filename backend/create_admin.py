import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
from passlib.context import CryptContext
from datetime import datetime, timezone
import uuid

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin_user():
    """Create an admin user in the database"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Admin user details
    admin_data = {
        "id": str(uuid.uuid4()),
        "email": "admin@inspecteur-auto.fr",
        "username": "admin",
        "full_name": "Administrateur",
        "password_hash": pwd_context.hash("Admin123!"),
        "is_active": True,
        "is_admin": True,
        "avatar_url": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "has_purchased": True,  # Admin a accès à tout
        "certificate_url": None,
        "last_login": None,
        "registration_source": "admin_script"
    }
    
    # Check if admin already exists
    existing_admin = await db.users.find_one({"email": admin_data["email"]})
    
    if existing_admin:
        print("✅ Un compte admin existe déjà avec cet email!")
        print(f"   Email: {admin_data['email']}")
        print(f"   Mot de passe: Admin123!")
        
        # Update to make sure it's admin
        await db.users.update_one(
            {"email": admin_data["email"]},
            {"$set": {"is_admin": True, "has_purchased": True}}
        )
        print("   ✓ Droits admin confirmés")
    else:
        # Create new admin user
        await db.users.insert_one(admin_data)
        print("✅ Compte administrateur créé avec succès!")
        print(f"\n📧 Email: {admin_data['email']}")
        print(f"🔑 Mot de passe: Admin123!")
        print(f"\n⚠️  Veuillez changer ce mot de passe après la première connexion!")
    
    # Also create a regular test user with purchase
    test_user_data = {
        "id": str(uuid.uuid4()),
        "email": "user@test.fr",
        "username": "testuser",
        "full_name": "Utilisateur Test",
        "password_hash": pwd_context.hash("Test123!"),
        "is_active": True,
        "is_admin": False,
        "avatar_url": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "has_purchased": True,  # A déjà acheté la formation
        "certificate_url": None,
        "last_login": None,
        "registration_source": "test_script"
    }
    
    existing_test = await db.users.find_one({"email": test_user_data["email"]})
    
    if not existing_test:
        await db.users.insert_one(test_user_data)
        print("\n✅ Compte utilisateur test créé (avec formation achetée)")
        print(f"📧 Email: {test_user_data['email']}")
        print(f"🔑 Mot de passe: Test123!")
    
    client.close()
    print("\n🎉 Configuration terminée!")

if __name__ == "__main__":
    asyncio.run(create_admin_user())
