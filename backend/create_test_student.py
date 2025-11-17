#!/usr/bin/env python3
"""
Script to create a test student account with premium access
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import bcrypt
import uuid

async def create_test_student():
    # Connect to MongoDB
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client['inspecteur_auto']
    
    # Check if test student already exists
    existing = await db.users.find_one({"email": "eleve.test@inspecteur-auto.fr"})
    
    if existing:
        print("✅ Compte élève test existe déjà!")
        print(f"📧 Email: eleve.test@inspecteur-auto.fr")
        print(f"🔑 Mot de passe: Test123456!")
        print(f"💳 Accès Premium: {existing.get('has_purchased', False)}")
        
        # Update to premium if not already
        if not existing.get('has_purchased'):
            await db.users.update_one(
                {"email": "eleve.test@inspecteur-auto.fr"},
                {"$set": {
                    "has_purchased": True,
                    "purchase_date": datetime.now(timezone.utc).isoformat()
                }}
            )
            print("✅ Accès premium activé!")
        return
    
    # Create new test student with premium access
    password = "Test123456!"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    test_student = {
        "id": str(uuid.uuid4()),
        "email": "eleve.test@inspecteur-auto.fr",
        "username": "eleve_test",
        "full_name": "Élève Test Premium",
        "password": hashed_password.decode('utf-8'),
        "is_admin": False,
        "has_purchased": True,
        "purchase_date": datetime.now(timezone.utc).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.users.insert_one(test_student)
    print("✅ Compte élève test créé avec succès!")
    print("\n" + "="*50)
    print("🎓 COMPTE ÉLÈVE TEST - ACCÈS PREMIUM")
    print("="*50)
    print(f"📧 Email: eleve.test@inspecteur-auto.fr")
    print(f"🔑 Mot de passe: Test123456!")
    print(f"💳 Accès Premium: ✅ OUI")
    print(f"📅 Date d'achat: {datetime.now(timezone.utc).strftime('%d/%m/%Y')}")
    print("="*50)
    print("\n✨ Vous pouvez maintenant vous connecter avec ces identifiants")
    print("   pour voir l'expérience complète d'un élève premium!\n")

if __name__ == "__main__":
    asyncio.run(create_test_student())
