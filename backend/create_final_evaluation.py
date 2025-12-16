#!/usr/bin/env python3
"""
Script to create final evaluation quiz
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
from pathlib import Path

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def create_final_evaluation():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Check if final evaluation already exists
    existing = await db.quizzes.find_one({"module_id": "final_evaluation"})
    if existing:
        print("Final evaluation quiz already exists!")
        client.close()
        return
    
    # Create comprehensive final evaluation quiz
    final_quiz = {
        "id": str(uuid.uuid4()),
        "module_id": "final_evaluation",  # Special module ID for final evaluation
        "title": "Évaluation Finale - Certification Inspecteur Automobile",
        "passing_score": 80,
        "questions": [
            {
                "id": "final_q1",
                "question": "Quelle est la première étape de la méthodologie méthode d'inspection ?",
                "type": "multiple_choice",
                "options": [
                    "Inspection visuelle extérieure",
                    "Analyse documentaire et vérification de l'identité du véhicule",
                    "Test routier",
                    "Diagnostic électronique"
                ],
                "correct_answer": 1,
                "explanation": "L'analyse documentaire et la vérification de l'identité du véhicule sont essentielles avant toute inspection physique."
            },
            {
                "id": "final_q2",
                "question": "Quel équipement est indispensable pour diagnostiquer les systèmes ADAS ?",
                "type": "multiple_choice",
                "options": [
                    "Multimètre simple",
                    "Valise de diagnostic OBD avec modules ADAS",
                    "Lampe torche LED",
                    "Manomètre de pression"
                ],
                "correct_answer": 1,
                "explanation": "Une valise de diagnostic spécialisée est nécessaire pour lire les codes défauts des systèmes ADAS."
            },
            {
                "id": "final_q3",
                "question": "Quelle est la profondeur minimale légale des sculptures de pneus en France ?",
                "type": "multiple_choice",
                "options": [
                    "1,0 mm",
                    "1,6 mm",
                    "2,0 mm",
                    "3,0 mm"
                ],
                "correct_answer": 1,
                "explanation": "La profondeur minimale légale des sculptures de pneus est de 1,6 mm en France."
            },
            {
                "id": "final_q4",
                "question": "Lors d'une inspection carrosserie, quel indice permet de détecter un repeint ?",
                "type": "multiple_choice",
                "options": [
                    "Différence de teinte sous différents angles",
                    "Peau d'orange visible",
                    "Traces de masquage sur joints",
                    "Toutes ces réponses"
                ],
                "correct_answer": 3,
                "explanation": "Tous ces éléments sont des indices de repeint et doivent être vérifiés lors de l'inspection."
            },
            {
                "id": "final_q5",
                "question": "Que signifie un code défaut de type 'P' en diagnostic OBD ?",
                "type": "multiple_choice",
                "options": [
                    "Problème de carrosserie (Paint)",
                    "Défaut du groupe motopropulseur (Powertrain)",
                    "Problème de pneus (Pneumatic)",
                    "Défaut de performance"
                ],
                "correct_answer": 1,
                "explanation": "Les codes P concernent le groupe motopropulseur (moteur, transmission)."
            },
            {
                "id": "final_q6",
                "question": "Quelle est la méthode recommandée pour tester l'efficacité du freinage ?",
                "type": "multiple_choice",
                "options": [
                    "Test visuel uniquement",
                    "Test routier + banc de freinage si disponible",
                    "Vérification de l'épaisseur des plaquettes uniquement",
                    "Test de la pédale de frein"
                ],
                "correct_answer": 1,
                "explanation": "Un test routier combiné à un passage au banc de freinage permet d'évaluer précisément l'efficacité."
            },
            {
                "id": "final_q7",
                "question": "Que doit contenir obligatoirement un rapport d'inspection méthode d'inspection ?",
                "type": "multiple_choice",
                "options": [
                    "Photos de tous les défauts constatés",
                    "Cotation précise de chaque élément inspecté",
                    "Recommandations client et estimation des réparations",
                    "Toutes ces réponses"
                ],
                "correct_answer": 3,
                "explanation": "Un rapport complet doit inclure photos, cotations, recommandations et estimations."
            },
            {
                "id": "final_q8",
                "question": "Comment vérifier l'authenticité du kilométrage d'un véhicule ?",
                "type": "multiple_choice",
                "options": [
                    "Consulter l'historique d'entretien",
                    "Vérifier les factures et le carnet",
                    "Consulter HistoVec et analyser l'usure",
                    "Toutes ces méthodes"
                ],
                "correct_answer": 3,
                "explanation": "Une vérification croisée de multiples sources permet de détecter une fraude au kilométrage."
            },
            {
                "id": "final_q9",
                "question": "Quel est le principal risque juridique pour un inspecteur automobile ?",
                "type": "multiple_choice",
                "options": [
                    "Non-détection d'un vice caché majeur",
                    "Retard dans la livraison du rapport",
                    "Erreur de prix dans le devis",
                    "Oubli de photos"
                ],
                "correct_answer": 0,
                "explanation": "La non-détection d'un vice caché majeur peut engager la responsabilité professionnelle de l'inspecteur."
            },
            {
                "id": "final_q10",
                "question": "Quelle assurance est indispensable pour exercer comme inspecteur automobile indépendant ?",
                "type": "multiple_choice",
                "options": [
                    "Assurance auto classique",
                    "Responsabilité civile professionnelle (RC Pro)",
                    "Assurance habitation",
                    "Protection juridique uniquement"
                ],
                "correct_answer": 1,
                "explanation": "La RC Pro est obligatoire pour couvrir les erreurs et omissions dans l'exercice professionnel."
            },
            {
                "id": "final_q11",
                "question": "Lors d'un test routier, quelle anomalie nécessite un arrêt immédiat ?",
                "type": "multiple_choice",
                "options": [
                    "Bruit de roulement léger",
                    "Vibration importante au freinage",
                    "Climatisation inefficace",
                    "Radio qui ne fonctionne pas"
                ],
                "correct_answer": 1,
                "explanation": "Une vibration importante au freinage peut indiquer un problème de sécurité critique."
            },
            {
                "id": "final_q12",
                "question": "Quelle est la durée de validité recommandée d'un rapport d'inspection ?",
                "type": "multiple_choice",
                "options": [
                    "1 semaine",
                    "15 jours",
                    "1 mois",
                    "3 mois"
                ],
                "correct_answer": 1,
                "explanation": "Un rapport d'inspection est généralement valable 15 jours, période pendant laquelle l'état du véhicule est censé rester stable."
            },
            {
                "id": "final_q13",
                "question": "Que signifie un liquide de refroidissement de couleur marron ou rouillé ?",
                "type": "multiple_choice",
                "options": [
                    "Liquide de refroidissement récent",
                    "Contamination ou oxydation du circuit",
                    "Liquide de refroidissement haute performance",
                    "Aucun problème"
                ],
                "correct_answer": 1,
                "explanation": "Un liquide marron ou rouillé indique une contamination ou une oxydation nécessitant une vidange du circuit."
            },
            {
                "id": "final_q14",
                "question": "Dans quelle situation devez-vous refuser une inspection ?",
                "type": "multiple_choice",
                "options": [
                    "Véhicule sale",
                    "Client pressé",
                    "Véhicule accidenté en attente d'expertise assurance",
                    "Mauvais temps"
                ],
                "correct_answer": 2,
                "explanation": "Un véhicule en cours d'expertise assurance ne doit pas être inspecté pour éviter tout conflit d'intérêt."
            },
            {
                "id": "final_q15",
                "question": "Quel est le premier réflexe avant de démarrer un véhicule inconnu ?",
                "type": "multiple_choice",
                "options": [
                    "Vérifier le niveau d'essence",
                    "Régler les rétroviseurs",
                    "Vérifier que le véhicule est au point mort et le frein à main serré",
                    "Allumer les phares"
                ],
                "correct_answer": 2,
                "explanation": "Pour des raisons de sécurité, toujours vérifier le point mort et le frein à main avant de démarrer."
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.quizzes.insert_one(final_quiz)
    print(f"✅ Quiz d'évaluation finale créé avec {len(final_quiz['questions'])} questions")
    print(f"   Score de passage: {final_quiz['passing_score']}%")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_final_evaluation())
