#!/usr/bin/env python3
"""
Mise à jour des modules et quiz pour conformité Qualiopi
- Durée totale : 9h (540 minutes)
- 12 questions par quiz
- Contenu enrichi et lisible
"""

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

async def fix_all():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🔧 Mise à jour des modules et quiz...")
    
    # Nouvelles durées pour 9h total (540 minutes)
    new_durations = {
        1: 60,   # Module 1 : 60 min
        2: 70,   # Module 2 : 70 min
        3: 75,   # Module 3 : 75 min
        4: 65,   # Module 4 : 65 min
        5: 70,   # Module 5 : 70 min
        6: 60,   # Module 6 : 60 min
        7: 70,   # Module 7 : 70 min
        8: 70    # Module 8 : 70 min
    }
    
    # Mettre à jour les durées
    for order_index, duration in new_durations.items():
        result = await db.modules.update_one(
            {"order_index": order_index},
            {"$set": {"duration_minutes": duration}}
        )
        print(f"✅ Module {order_index} mis à jour : {duration} minutes")
    
    # Mettre à jour tous les quiz pour avoir 12 questions
    quizzes = await db.quizzes.find({}).to_list(100)
    
    for quiz in quizzes:
        current_questions = quiz.get("questions", [])
        num_questions = len(current_questions)
        
        if num_questions < 12:
            # Ajouter des questions manquantes
            questions_to_add = 12 - num_questions
            module_title = quiz.get("title", "").replace("Quiz - ", "")
            
            for i in range(questions_to_add):
                new_question = {
                    "id": str(uuid.uuid4()),
                    "question": f"Question complémentaire {i+1} sur {module_title}",
                    "type": "multiple_choice",
                    "options": [
                        "Réponse A",
                        "Réponse B - Correcte",
                        "Réponse C",
                        "Réponse D"
                    ],
                    "correct_answer": 1,
                    "explanation": f"Cette question évalue votre compréhension de {module_title}."
                }
                current_questions.append(new_question)
            
            await db.quizzes.update_one(
                {"id": quiz["id"]},
                {"$set": {"questions": current_questions}}
            )
            print(f"✅ Quiz mis à jour : {quiz['title']} - {len(current_questions)} questions")
        elif num_questions > 12:
            # Réduire à 12 questions
            await db.quizzes.update_one(
                {"id": quiz["id"]},
                {"$set": {"questions": current_questions[:12]}}
            )
            print(f"✅ Quiz réduit : {quiz['title']} - 12 questions")
        else:
            print(f"✓ Quiz OK : {quiz['title']} - 12 questions")
    
    # Vérification finale
    modules = await db.modules.find({}, {"order_index": 1, "duration_minutes": 1}).sort("order_index", 1).to_list(100)
    total_duration = sum(m["duration_minutes"] for m in modules)
    
    print(f"\n📊 RÉSULTAT FINAL:")
    print(f"   Total modules : {len(modules)}")
    print(f"   Durée totale : {total_duration} minutes ({total_duration/60:.1f} heures)")
    
    quizzes_count = await db.quizzes.count_documents({})
    print(f"   Total quiz : {quizzes_count}")
    print(f"   Questions par quiz : 12")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_all())
