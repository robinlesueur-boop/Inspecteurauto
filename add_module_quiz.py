#!/usr/bin/env python3
"""
Script to add quiz for the free module
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

async def add_module_quiz():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['inspecteur_auto_platform']
    
    # Get the free module ID
    free_module = await db.modules.find_one({"is_free": True})
    if not free_module:
        print("No free module found!")
        return
    
    module_id = free_module["id"]
    print(f"Found free module: {free_module['title']} (ID: {module_id})")
    
    # Create quiz for the free module
    module_quiz = {
        "id": str(uuid.uuid4()),
        "module_id": module_id,
        "title": "Quiz - Introduction à l'Inspection Automobile",
        "passing_score": 80,
        "questions": [
            {
                "id": "intro_q1",
                "question": "Quel est le volume approximatif de véhicules d'occasion vendus annuellement en France ?",
                "type": "multiple_choice",
                "options": [
                    "2,5 millions",
                    "3,8 millions", 
                    "5,5 millions",
                    "7,2 millions"
                ],
                "correct_answer": 2,
                "explanation": "Le marché français compte environ 5,5 millions de transactions de véhicules d'occasion par an."
            },
            {
                "id": "intro_q2",
                "question": "Quel pourcentage de véhicules d'occasion présenterait des anomalies non déclarées ?",
                "type": "multiple_choice",
                "options": [
                    "Environ 15%",
                    "Environ 25%",
                    "Environ 35%",
                    "Environ 45%"
                ],
                "correct_answer": 2,
                "explanation": "Environ 35% des véhicules d'occasion présentent des anomalies non déclarées lors de la vente."
            },
            {
                "id": "intro_q3",
                "question": "Quelle est la fourchette de tarif typique pour une inspection automobile professionnelle ?",
                "type": "multiple_choice",
                "options": [
                    "50 à 100 €",
                    "150 à 400 €",
                    "500 à 800 €",
                    "1000 € et plus"
                ],
                "correct_answer": 1,
                "explanation": "Une inspection automobile professionnelle se facture généralement entre 150 et 400 €."
            },
            {
                "id": "intro_q4",
                "question": "Combien de calculateurs électroniques peut contenir un véhicule moderne ?",
                "type": "multiple_choice",
                "options": [
                    "10 à 20",
                    "20 à 30",
                    "Plus de 50",
                    "Environ 100"
                ],
                "correct_answer": 2,
                "explanation": "Un véhicule moderne peut intégrer plus de 50 calculateurs électroniques gérant différentes fonctions."
            },
            {
                "id": "intro_q5",
                "question": "Combien de piliers composent la méthodologie AutoJust ?",
                "type": "multiple_choice",
                "options": [
                    "3 piliers",
                    "5 piliers",
                    "7 piliers",
                    "10 piliers"
                ],
                "correct_answer": 1,
                "explanation": "La méthodologie AutoJust repose sur 5 piliers : Systématisation, Technologie, Traçabilité, Transparence et Expertise."
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.quizzes.insert_one(module_quiz)
    print(f"✅ Quiz créé pour le module gratuit: {len(module_quiz['questions'])} questions")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_module_quiz())