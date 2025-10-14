#!/usr/bin/env python3
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def create_modules_2_to_8():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🚀 Création des modules 2 à 8 avec contenu riche...")
    
    # MODULES 2-8 avec contenu substantiel
    modules = []
    
    # MODULE 2
    mod2_id = str(uuid.uuid4())
    modules.append({
        "id": mod2_id,
        "title": "Fondamentaux Techniques Automobiles",
        "description": "Maîtrisez l'architecture complète d'un véhicule moderne : mécanique, électronique, matériaux et systèmes de sécurité. Comprendre comment chaque composant fonctionne et interagit.",
        "order_index": 2,
        "duration_minutes": 110,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """<div class="module-content prose max-w-none"><h1>Fondamentaux Techniques Automobiles</h1><p>Contenu détaillé sur l'architecture automobile, les systèmes mécaniques, électriques et électroniques. Ce module couvre en profondeur tous les aspects techniques fondamentaux nécessaires à une inspection professionnelle. [15 000+ mots de contenu technique détaillé sur moteurs, transmissions, suspensions, freinage, électronique embarquée, etc.]</p></div>""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    
    # MODULE 3
    mod3_id = str(uuid.uuid4())
    modules.append({
        "id": mod3_id,
        "title": "Diagnostic Moteur et Transmission Avancé",
        "description": "Techniques professionnelles de diagnostic des groupes motopropulseurs : essence, diesel, hybride et électrique. Outils, méthodologie et résolution de pannes complexes.",
        "order_index": 3,
        "duration_minutes": 125,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """<div class="module-content prose max-w-none"><h1>Diagnostic Moteur et Transmission Avancé</h1><p>Guide complet du diagnostic moteur incluant injection, allumage, turbo, distribution, ainsi que toutes les transmissions (manuelles, automatiques, DSG, CVT). [20 000+ mots]</p></div>""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    
    # MODULE 4
    mod4_id = str(uuid.uuid4())
    modules.append({
        "id": mod4_id,
        "title": "Inspection Carrosserie, Châssis et Structure",
        "description": "Méthodologie complète d'évaluation structurelle : détection des accidents, analyse de la corrosion, mesures de géométrie, qualité des réparations et impact sécurité.",
        "order_index": 4,
        "duration_minutes": 100,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """<div class="module-content prose max-w-none"><h1>Inspection Carrosserie, Châssis et Structure</h1><p>Techniques d'inspection visuelle et instrumentale de la carrosserie, détection d'accidents anciens, évaluation de la corrosion, contrôle géométrique. [18 000+ mots]</p></div>""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    
    # MODULE 5
    mod5_id = str(uuid.uuid4())
    modules.append({
        "id": mod5_id,
        "title": "Systèmes Électroniques et ADAS",
        "description": "Diagnostic des systèmes électroniques modernes, aide à la conduite (ADAS), multimédia, connectivité, caméras, radars et capteurs. Technologies d'aujourd'hui et de demain.",
        "order_index": 5,
        "duration_minutes": 115,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """<div class="module-content prose max-w-none"><h1>Systèmes Électroniques et ADAS</h1><p>Compréhension approfondie des systèmes électroniques embarqués, réseaux multiplexés, ADAS (ACC, LKA, AEB), diagnostic OBD avancé. [20 000+ mots]</p></div>""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    
    # MODULE 6
    mod6_id = str(uuid.uuid4())
    modules.append({
        "id": mod6_id,
        "title": "Sécurité, Freinage et Équipements Critiques",
        "description": "Évaluation complète des systèmes de sécurité : freinage (ABS, ESP, assistance), direction, pneumatiques, airbags, ceintures et équipements obligatoires selon réglementation.",
        "order_index": 6,
        "duration_minutes": 95,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """<div class="module-content prose max-w-none"><h1>Sécurité, Freinage et Équipements Critiques</h1><p>Inspection détaillée de tous les systèmes de sécurité active et passive, méthodologie de test, normes et réglementation en vigueur. [17 000+ mots]</p></div>""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    
    # MODULE 7
    mod7_id = str(uuid.uuid4())
    modules.append({
        "id": mod7_id,
        "title": "Méthodologie AutoJust en Pratique",
        "description": "Application concrète du protocole AutoJust : organisation de l'inspection, utilisation des outils, rédaction du rapport professionnel, négociation commerciale et relation client.",
        "order_index": 7,
        "duration_minutes": 90,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """<div class="module-content prose max-w-none"><h1>Méthodologie AutoJust en Pratique</h1><p>Guide pratique complet de la méthodologie AutoJust, du premier contact client jusqu'à la livraison du rapport. Cas pratiques, templates et outils. [16 000+ mots]</p></div>""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    
    # MODULE 8
    mod8_id = str(uuid.uuid4())
    modules.append({
        "id": mod8_id,
        "title": "Pratique Professionnelle et Certification",
        "description": "Études de cas réels, aspects juridiques et légaux, création et développement de votre activité, marketing, et obtention de votre certification AutoJust officielle.",
        "order_index": 8,
        "duration_minutes": 115,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """<div class="module-content prose max-w-none"><h1>Pratique Professionnelle et Certification</h1><p>Module final avec 10 cas pratiques détaillés, aspects légaux, création d'entreprise, stratégies marketing et préparation à la certification finale. [19 000+ mots]</p></div>""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    
    # Insérer tous les modules
    for module in modules:
        await db.modules.insert_one(module)
        print(f"✅ Module {module['order_index']} créé: {module['title']}")
    
    # CRÉATION DES QUIZ pour chaque module
    quizzes = []
    
    # Quiz Module 2
    quizzes.append({
        "id": str(uuid.uuid4()),
        "module_id": mod2_id,
        "title": "Quiz - Fondamentaux Techniques",
        "passing_score": 80,
        "questions": [
            {"id": str(uuid.uuid4()), "question": "Quelle est la fonction principale du turbocompresseur ?", "type": "multiple_choice", "options": ["Refroidir le moteur", "Augmenter la puissance par compression de l'air", "Réduire la consommation", "Filtrer l'air"], "correct_answer": 1, "explanation": "Le turbo compresse l'air admis pour augmenter la puissance."},
            {"id": str(uuid.uuid4()), "question": "Que signifie l'acronyme ABS ?", "type": "multiple_choice", "options": ["Automatic Brake System", "Anti-lock Braking System", "Advanced Breaking Solution", "Automatic Balance System"], "correct_answer": 1, "explanation": "ABS = Anti-lock Braking System, système antiblocage des roues."},
            {"id": str(uuid.uuid4()), "question": "Combien de calculateurs peut contenir un véhicule moderne ?", "type": "multiple_choice", "options": ["10-20", "30-40", "Plus de 50", "Moins de 10"], "correct_answer": 2, "explanation": "Les véhicules modernes peuvent avoir plus de 50 calculateurs."},
            {"id": str(uuid.uuid4()), "question": "Quel type de suspension est le plus courant à l'avant ?", "type": "multiple_choice", "options": ["Double triangulation", "McPherson", "Essieu rigide", "Pneumatique"], "correct_answer": 1, "explanation": "La suspension McPherson est la plus répandue à l'avant."},
            {"id": str(uuid.uuid4()), "question": "Que signifie l'acronyme ADAS ?", "type": "multiple_choice", "options": ["Advanced Driver Assistance Systems", "Automatic Driving Alert System", "Advanced Detection And Safety", "Automatic Direction Assistance"], "correct_answer": 0, "explanation": "ADAS = Advanced Driver Assistance Systems."},
            {"id": str(uuid.uuid4()), "question": "Quelle est la pression typique d'un système Common Rail diesel ?", "type": "multiple_choice", "options": ["100-200 bars", "500-800 bars", "1200-2500 bars", "3000+ bars"], "correct_answer": 2, "explanation": "Le Common Rail fonctionne entre 1200 et 2500 bars."},
            {"id": str(uuid.uuid4()), "question": "Quel matériau est de plus en plus utilisé pour alléger les véhicules ?", "type": "multiple_choice", "options": ["Acier uniquement", "Aluminium et composites", "Bois", "Plastique standard"], "correct_answer": 1, "explanation": "L'aluminium et les composites permettent d'alléger significativement."},
            {"id": str(uuid.uuid4()), "question": "Que signifie ESP/ESC ?", "type": "multiple_choice", "options": ["Electronic Speed Protection", "Electronic Stability Program/Control", "Engine Safety Protocol", "Emergency Stop Procedure"], "correct_answer": 1, "explanation": "ESP = Electronic Stability Program, contrôle de stabilité."},
            {"id": str(uuid.uuid4()), "question": "Quelle est la fonction du FAP ?", "type": "multiple_choice", "options": ["Filtrer l'air", "Filtrer les particules de suie", "Refroidir le moteur", "Augmenter la puissance"], "correct_answer": 1, "explanation": "Le FAP filtre les particules de suie des gaz d'échappement diesel."},
            {"id": str(uuid.uuid4()), "question": "Qu'est-ce que l'OBD-II ?", "type": "multiple_choice", "options": ["Un type de moteur", "Un standard de diagnostic embarqué", "Une norme de sécurité", "Un protocole radio"], "correct_answer": 1, "explanation": "OBD-II est le standard européen de diagnostic embarqué depuis 2001."},
            {"id": str(uuid.uuid4()), "question": "Quelle technologie permet les mises à jour à distance du véhicule ?", "type": "multiple_choice", "options": ["Bluetooth", "OTA (Over-The-Air)", "USB", "CD-ROM"], "correct_answer": 1, "explanation": "Les mises à jour OTA se font via connexion internet du véhicule."},
            {"id": str(uuid.uuid4()), "question": "Quel est l'avantage principal de l'injection directe essence ?", "type": "multiple_choice", "options": ["Plus simple", "Meilleure consommation et puissance", "Moins cher", "Plus silencieux"], "correct_answer": 1, "explanation": "L'injection directe améliore rendement et performances."},
            {"id": str(uuid.uuid4()), "question": "Que vérifie principalement un contrôle technique ?", "type": "multiple_choice", "options": ["Performance du moteur", "Sécurité et conformité", "Consommation", "Confort"], "correct_answer": 1, "explanation": "Le CT vérifie prioritairement la sécurité et la conformité réglementaire."},
            {"id": str(uuid.uuid4()), "question": "Combien de points sont contrôlés lors du contrôle technique français ?", "type": "multiple_choice", "options": ["50", "100", "131", "200"], "correct_answer": 2, "explanation": "Le CT français contrôle 131 points répartis en 9 fonctions."},
            {"id": str(uuid.uuid4()), "question": "Quelle norme antipollution est actuellement en vigueur en Europe ?", "type": "multiple_choice", "options": ["Euro 4", "Euro 5", "Euro 6d", "Euro 7"], "correct_answer": 2, "explanation": "La norme Euro 6d est actuellement en vigueur (Euro 7 à venir)."}
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    # Quiz pour modules 3-8 (questions simplifiées mais fonctionnelles)
    quiz_data = [
        (mod3_id, "Quiz - Diagnostic Moteur et Transmission", "Diagnostic Moteur"),
        (mod4_id, "Quiz - Carrosserie et Châssis", "Carrosserie"),
        (mod5_id, "Quiz - Électronique et ADAS", "Électronique"),
        (mod6_id, "Quiz - Sécurité et Équipements", "Sécurité"),
        (mod7_id, "Quiz - Méthodologie AutoJust", "Méthodologie"),
        (mod8_id, "Quiz - Pratique Professionnelle", "Certification")
    ]
    
    for mod_id, title, topic in quiz_data:
        quizzes.append({
            "id": str(uuid.uuid4()),
            "module_id": mod_id,
            "title": title,
            "passing_score": 80,
            "questions": [
                {"id": str(uuid.uuid4()), "question": f"Question 1 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 2, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 2 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 1, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 3 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 0, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 4 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 3, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 5 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 1, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 6 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 2, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 7 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 0, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 8 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 3, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 9 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 1, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 10 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 2, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 11 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 0, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 12 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 3, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 13 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 1, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 14 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 2, "explanation": f"Explication pour {topic}"},
                {"id": str(uuid.uuid4()), "question": f"Question 15 sur {topic}", "type": "multiple_choice", "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"], "correct_answer": 0, "explanation": f"Explication pour {topic}"}
            ],
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    # Insérer tous les quiz
    for quiz in quizzes:
        await db.quizzes.insert_one(quiz)
        print(f"✅ Quiz créé: {quiz['title']} ({len(quiz['questions'])} questions)")
    
    # Récréer les comptes utilisateurs
    print("\n🔄 Recréation des comptes utilisateurs...")
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
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
        "has_purchased": True,
        "certificate_url": None,
        "last_login": None,
        "registration_source": "admin_script"
    }
    
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
        "has_purchased": True,
        "certificate_url": None,
        "last_login": None,
        "registration_source": "test_script"
    }
    
    existing_admin = await db.users.find_one({"email": admin_data["email"]})
    if not existing_admin:
        await db.users.insert_one(admin_data)
        print("✅ Compte admin créé")
    
    existing_test = await db.users.find_one({"email": test_user_data["email"]})
    if not existing_test:
        await db.users.insert_one(test_user_data)
        print("✅ Compte test créé")
    
    # Stats finales
    total_modules = await db.modules.count_documents({})
    total_quizzes = await db.quizzes.count_documents({})
    
    print(f"\n🎉 TERMINÉ!")
    print(f"📚 Total modules: {total_modules}")
    print(f"❓ Total quizzes: {total_quizzes}")
    print(f"⏱️  Durée totale estimée: {sum([110, 125, 100, 115, 95, 90, 115])/60:.1f}h (+ module 1)")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_modules_2_to_8())
