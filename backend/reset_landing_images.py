#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone

async def reset_landing_images():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client['inspecteur_auto']
    
    # Supprimer l'ancien document
    await db.landing_page_content.delete_many({})
    
    # Créer un nouveau document propre
    new_content = {
        'id': 'default',
        'hero_title': 'Devenez Inspecteur Automobile Certifié',
        'hero_subtitle': "Maîtrisez l'art du diagnostic véhiculaire avec la méthode AutoJust. Formation complète en 11h pour générer jusqu'à 8000€/mois.",
        'hero_image_url': 'https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=1200&q=80',
        'stat_graduates': '1,200+',
        'stat_success_rate': '97%',
        'stat_duration': '11h',
        'stat_rating': '4.9/5',
        'price_amount': '297€',
        'price_description': 'Formation complète + Certification',
        'cta_primary': 'Commencer la formation',
        'cta_secondary': 'Module gratuit',
        'feature_1_title': 'Méthode AutoJust',
        'feature_1_description': "Système d'inspection révolutionnaire utilisé par plus de 500 professionnels en France.",
        'feature_2_title': 'Certification Reconnue',
        'feature_2_description': "Obtenez votre certification officielle d'inspecteur automobile valorisée par l'industrie.",
        'feature_3_title': 'Communauté Active',
        'feature_3_description': "Rejoignez une communauté de 1000+ inspecteurs et échangez sur vos expériences.",
        'feature_4_title': 'Revenus Attractifs',
        'feature_4_description': "Générez 50 à 300€ par inspection avec un potentiel jusqu'à 4000€/mois.",
        'features_image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=1200&q=80',
        'training_image_url': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=1200&q=80',
        'social_proof_image_url': 'https://images.unsplash.com/photo-1573164574572-cb89e39749b4?w=1200&q=80',
        'updated_at': datetime.now(timezone.utc).isoformat()
    }
    
    await db.landing_page_content.insert_one(new_content)
    
    print('✅ Landing page réinitialisée avec 3 belles images Unsplash!')
    print('')
    print('📸 Images installées:')
    print('  1. Hero: Inspecteur automobile professionnel')
    print('  2. Features: Mécanicien au travail') 
    print('  3. Training: Diagnostic automobile')
    print('')
    print('Rafraîchissez la landing page pour voir les images!')

if __name__ == "__main__":
    asyncio.run(reset_landing_images())
