#!/usr/bin/env python3
"""
Script to create admin account
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
from pathlib import Path
import bcrypt

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def create_admin():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Admin credentials
    admin_email = "admin@inspecteur-auto.fr"
    admin_password = "Admin123!"
    
    # Check if admin exists
    existing = await db.users.find_one({"email": admin_email})
    if existing:
        print(f"✅ Admin déjà existant: {admin_email}")
        print(f"   Password: {admin_password}")
        client.close()
        return
    
    # Hash password
    password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create admin user
    admin_user = {
        "id": str(uuid.uuid4()),
        "email": admin_email,
        "username": "admin",
        "full_name": "Administrateur",
        "password_hash": password_hash,
        "is_active": True,
        "is_admin": True,
        "has_purchased": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "registration_source": "system"
    }
    
    await db.users.insert_one(admin_user)
    
    print("=" * 60)
    print("✅ COMPTE ADMINISTRATEUR CRÉÉ AVEC SUCCÈS")
    print("=" * 60)
    print(f"Email:    {admin_email}")
    print(f"Password: {admin_password}")
    print(f"Username: admin")
    print("=" * 60)
    print("⚠️  IMPORTANT: Changez ce mot de passe après la première connexion!")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
