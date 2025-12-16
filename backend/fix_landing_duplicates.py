"""
Script pour corriger les doublons dans le contenu de la landing page
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def fix_duplicates():
    """Corriger les doublons"""
    
    content = await db.landing_page_content.find_one({})
    
    if content:
        updates = {}
        for key, value in content.items():
            if isinstance(value, str):
                # Corriger les différents types de doublons
                new_value = value.replace('méthode d\'inspection professionnelle professionnelle', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('méthode méthode d\'inspection professionnelle', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('Méthode méthode d\'inspection professionnelle', 'Méthode d\'inspection professionnelle')
                
                if new_value != value:
                    updates[key] = new_value
                    print(f"✅ Correction de {key}")
                    print(f"   {value[:150]}")
                    print(f"   → {new_value[:150]}\n")
        
        if updates:
            await db.landing_page_content.update_one(
                {"_id": content["_id"]},
                {"$set": updates}
            )
            print(f"✅ {len(updates)} champs corrigés")
        else:
            print("ℹ️ Aucune correction nécessaire")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_duplicates())
