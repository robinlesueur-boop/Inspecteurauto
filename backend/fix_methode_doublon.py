"""
Script pour corriger 'Méthode méthode d'inspection' -> 'Méthode d'inspection'
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

async def fix_all():
    """Corriger dans toutes les collections"""
    
    collections_to_check = [
        ('landing_page_content', None),
        ('modules', 'id'),
        ('blog_posts', 'id'),
        ('ai_config', 'type')
    ]
    
    for collection_name, id_field in collections_to_check:
        collection = db[collection_name]
        
        if id_field:
            documents = await collection.find({}).to_list(None)
        else:
            doc = await collection.find_one({})
            documents = [doc] if doc else []
        
        updated = 0
        for doc in documents:
            if not doc:
                continue
                
            updates = {}
            for key, value in doc.items():
                if isinstance(value, str) and "Méthode méthode d'inspection" in value:
                    new_value = value.replace("Méthode méthode d'inspection", "Méthode d'inspection")
                    updates[key] = new_value
            
            if updates:
                if id_field:
                    await collection.update_one(
                        {id_field: doc[id_field]},
                        {"$set": updates}
                    )
                else:
                    await collection.update_one(
                        {"_id": doc["_id"]},
                        {"$set": updates}
                    )
                updated += 1
                print(f"✅ {collection_name}: {list(updates.keys())}")
        
        if updated == 0:
            print(f"ℹ️  {collection_name}: Aucune correction nécessaire")
    
    client.close()
    print("\n✅ Terminé!")

if __name__ == "__main__":
    asyncio.run(fix_all())
