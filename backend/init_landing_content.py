#!/usr/bin/env python3
"""
Script to initialize default landing page content
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone

async def init_landing_content():
    # Connect to MongoDB
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client['inspecteur_auto']
    
    # Check if content already exists
    existing = await db.landing_page_content.find_one({})
    
    if existing:
        print("✅ Landing page content already exists!")
        return
    
    # Create default content
    default_content = {
        "id": "default",
        "hero_title": "Devenez Inspecteur Automobile Certifié",
        "hero_subtitle": "Maîtrisez l'art du diagnostic véhiculaire avec la méthode AutoJust. Formation complète en 11h pour générer jusqu'à 8000€/mois.",
        "stat_graduates": "1,200+",
        "stat_success_rate": "97%",
        "stat_duration": "11h",
        "stat_rating": "4.9/5",
        "price_amount": "297€",
        "price_description": "Formation complète + Certification",
        "cta_primary": "Commencer la formation",
        "cta_secondary": "Module gratuit",
        "feature_1_title": "Méthode AutoJust",
        "feature_1_description": "Système d'inspection révolutionnaire utilisé par plus de 500 professionnels en France.",
        "feature_2_title": "Certification Reconnue",
        "feature_2_description": "Obtenez votre certification officielle d'inspecteur automobile valorisée par l'industrie.",
        "feature_3_title": "Communauté Active",
        "feature_3_description": "Rejoignez une communauté de 1000+ inspecteurs et échangez sur vos expériences.",
        "feature_4_title": "Revenus Attractifs",
        "feature_4_description": "Générez 50 à 300€ par inspection avec un potentiel jusqu'à 4000€/mois.",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.landing_page_content.insert_one(default_content)
    print("✅ Default landing page content created successfully!")

if __name__ == "__main__":
    asyncio.run(init_landing_content())
