"""
Script pour remplacer toutes les références à 'AutoJust' par 'méthode d'inspection'
dans la base de données MongoDB
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

async def update_landing_page_content():
    """Mettre à jour le contenu de la landing page"""
    
    # Récupérer le contenu actuel
    content = await db.landing_page_content.find_one({})
    
    if content:
        # Remplacer dans tous les champs de texte
        updates = {}
        for key, value in content.items():
            if isinstance(value, str):
                # Remplacer AutoJust® et AutoJust
                new_value = value.replace('AutoJust®', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('AutoJust', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('méthode méthode d\'inspection', 'méthode d\'inspection professionnelle')
                
                if new_value != value:
                    updates[key] = new_value
                    print(f"✅ Mise à jour de {key}")
                    print(f"   Avant: {value[:100]}...")
                    print(f"   Après: {new_value[:100]}...")
        
        if updates:
            await db.landing_page_content.update_one(
                {"_id": content["_id"]},
                {"$set": updates}
            )
            print(f"\n✅ {len(updates)} champs mis à jour dans landing_page_content")
        else:
            print("ℹ️ Aucune mise à jour nécessaire dans landing_page_content")
    else:
        print("⚠️ Aucun contenu de landing page trouvé")

async def update_modules():
    """Mettre à jour les modules"""
    
    modules = await db.modules.find({}).to_list(None)
    updated_count = 0
    
    for module in modules:
        updates = {}
        
        # Vérifier tous les champs texte
        for field in ['title', 'description', 'content']:
            if field in module and isinstance(module[field], str):
                new_value = module[field].replace('AutoJust®', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('AutoJust', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('méthode méthode d\'inspection', 'méthode d\'inspection professionnelle')
                
                if new_value != module[field]:
                    updates[field] = new_value
        
        if updates:
            await db.modules.update_one(
                {"id": module["id"]},
                {"$set": updates}
            )
            updated_count += 1
            print(f"✅ Module mis à jour: {module.get('title', 'Sans titre')}")
    
    print(f"\n✅ {updated_count} modules mis à jour")

async def update_blog_posts():
    """Mettre à jour les articles de blog"""
    
    posts = await db.blog_posts.find({}).to_list(None)
    updated_count = 0
    
    for post in posts:
        updates = {}
        
        # Vérifier tous les champs texte
        for field in ['title', 'excerpt', 'content']:
            if field in post and isinstance(post[field], str):
                new_value = post[field].replace('AutoJust®', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('AutoJust', 'méthode d\'inspection professionnelle')
                new_value = new_value.replace('méthode méthode d\'inspection', 'méthode d\'inspection professionnelle')
                
                if new_value != post[field]:
                    updates[field] = new_value
        
        if updates:
            await db.blog_posts.update_one(
                {"id": post["id"]},
                {"$set": updates}
            )
            updated_count += 1
            print(f"✅ Article de blog mis à jour: {post.get('title', 'Sans titre')}")
    
    print(f"\n✅ {updated_count} articles de blog mis à jour")

async def update_ai_system_prompt():
    """Mettre à jour le prompt système de l'IA"""
    
    config = await db.ai_config.find_one({"type": "system_prompt"})
    
    if config and "prompt" in config:
        new_prompt = config["prompt"].replace('AutoJust®', 'méthode d\'inspection professionnelle')
        new_prompt = new_prompt.replace('AutoJust', 'méthode d\'inspection professionnelle')
        new_prompt = new_prompt.replace('méthode méthode d\'inspection', 'méthode d\'inspection professionnelle')
        
        if new_prompt != config["prompt"]:
            await db.ai_config.update_one(
                {"type": "system_prompt"},
                {"$set": {"prompt": new_prompt}}
            )
            print("✅ Prompt système de l'IA mis à jour")
        else:
            print("ℹ️ Prompt système de l'IA déjà à jour")
    else:
        print("⚠️ Aucun prompt système trouvé")

async def main():
    print("🔄 Mise à jour des références AutoJust dans la base de données...\n")
    
    await update_landing_page_content()
    print("\n" + "="*50 + "\n")
    
    await update_modules()
    print("\n" + "="*50 + "\n")
    
    await update_blog_posts()
    print("\n" + "="*50 + "\n")
    
    await update_ai_system_prompt()
    print("\n" + "="*50)
    
    print("\n✅ Mise à jour terminée!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
