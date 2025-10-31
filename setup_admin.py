#!/usr/bin/env python3
"""
Setup admin user for testing
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv('/app/backend/.env')
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def setup_admin():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    admin_email = "testadmin@test.com"
    admin_password = "Admin123456!"
    
    # Check if admin exists
    existing_admin = await db.users.find_one({"email": admin_email})
    
    if existing_admin:
        # Update existing user to be admin
        result = await db.users.update_one(
            {"email": admin_email},
            {"$set": {"is_admin": True}}
        )
        print(f"Updated existing user {admin_email} to admin: {result.modified_count} documents modified")
    else:
        # Create new admin user
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(admin_password)
        
        import uuid
        from datetime import datetime, timezone
        
        admin_user = {
            "id": str(uuid.uuid4()),
            "email": admin_email,
            "username": "testadmin",
            "full_name": "Test Admin",
            "is_active": True,
            "is_admin": True,
            "avatar_url": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "has_purchased": False,
            "certificate_url": None,
            "last_login": None,
            "registration_source": "website",
            "password_hash": hashed_password
        }
        
        await db.users.insert_one(admin_user)
        print(f"Created new admin user: {admin_email}")
    
    # Verify admin user
    admin_user = await db.users.find_one({"email": admin_email}, {"_id": 0, "email": 1, "is_admin": 1})
    print(f"Admin user verified: {admin_user}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(setup_admin())