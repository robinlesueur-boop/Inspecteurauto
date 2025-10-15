#!/usr/bin/env python3
"""
Créer les quiz préliminaires :
1. Quiz d'adéquation au métier
2. Quiz de connaissances mécaniques
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

async def create_preliminary_quizzes():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🎯 Création des quiz préliminaires...\n")
    
    # Quiz 1 : Adéquation au Métier
    career_quiz = {
        "id": str(uuid.uuid4()),
        "module_id": "career_fit", # ID spécial
        "title": "Quiz d'Adéquation au Métier d'Inspecteur Automobile",
        "description": "Ce quiz évalue si votre profil et vos attentes correspondent au métier d'inspecteur automobile.",
        "passing_score": 0, # Pas de score minimum, juste informatif
        "is_preliminary": True,
        "quiz_type": "career_fit",
        "questions": [
            {
                "id": str(uuid.uuid4()),
                "question": "Pourquoi souhaitez-vous devenir inspecteur automobile ?",
                "type": "multiple_choice",
                "options": [
                    "Passion pour l'automobile et envie d'aider les acheteurs",
                    "Opportunité de revenus attractifs",
                    "Reconversion professionnelle rapide",
                    "Recommandation d'un proche"
                ],
                "correct_answer": 0,
                "points": 10,
                "explanation": "La passion automobile et l'envie d'aider sont les motivations les plus durables."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Combien d'heures par semaine êtes-vous prêt à consacrer à cette activité ?",
                "type": "multiple_choice",
                "options": [
                    "Moins de 10 heures (activité secondaire)",
                    "10 à 20 heures (mi-temps)",
                    "20 à 35 heures (temps partiel important)",
                    "Plus de 35 heures (temps plein)"
                ],
                "correct_answer": 3,
                "points": 8,
                "explanation": "Le temps plein permet de développer rapidement une clientèle stable."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quel est votre niveau actuel de connaissance automobile ?",
                "type": "multiple_choice",
                "options": [
                    "Débutant (je connais peu)",
                    "Amateur (j'entretiens ma voiture)",
                    "Passionné (je fais mes vidanges/freins)",
                    "Professionnel (mécanicien ou équivalent)"
                ],
                "correct_answer": 3,
                "points": 7,
                "explanation": "Toute base est utile, mais la formation vous apportera les compétences nécessaires."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Êtes-vous à l'aise pour échanger avec des clients et expliquer des problèmes techniques ?",
                "type": "multiple_choice",
                "options": [
                    "Non, je préfère éviter",
                    "Pas vraiment à l'aise",
                    "Oui, sans problème",
                    "Oui, c'est une de mes forces"
                ],
                "correct_answer": 3,
                "points": 10,
                "explanation": "La relation client est essentielle : 50% de votre métier consiste à expliquer et conseiller."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Êtes-vous prêt à investir dans du matériel professionnel (2000-5000€) ?",
                "type": "multiple_choice",
                "options": [
                    "Non, pas pour le moment",
                    "Oui, jusqu'à 2000€",
                    "Oui, jusqu'à 5000€",
                    "Oui, plus si nécessaire"
                ],
                "correct_answer": 2,
                "points": 8,
                "explanation": "Un investissement de 3000-5000€ en matériel est standard pour débuter professionnellement."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Comment réagiriez-vous si un client était mécontent de votre rapport ?",
                "type": "multiple_choice",
                "options": [
                    "Je serais très affecté et découragé",
                    "Je remettrais en question mon travail",
                    "J'écouterais et expliquerais calmement mes conclusions",
                    "J'argumenterais avec fermeté tout en restant professionnel"
                ],
                "correct_answer": 3,
                "points": 9,
                "explanation": "La gestion des clients difficiles fait partie du métier. Rester professionnel est crucial."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Êtes-vous prêt à travailler les week-ends et certains soirs ?",
                "type": "multiple_choice",
                "options": [
                    "Non, uniquement en semaine",
                    "Parfois si nécessaire",
                    "Oui, régulièrement",
                    "Oui, sans problème, c'est quand les clients sont disponibles"
                ],
                "correct_answer": 3,
                "points": 7,
                "explanation": "Les clients particuliers sont souvent disponibles le soir et le week-end."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quel revenu mensuel visez-vous la première année ?",
                "type": "multiple_choice",
                "options": [
                    "Complément de 500-1000€",
                    "1500-2500€",
                    "2500-4000€",
                    "Plus de 4000€"
                ],
                "correct_answer": 2,
                "points": 6,
                "explanation": "Un objectif réaliste la 1ère année : 2500-3500€ avec 15-20 inspections/mois."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Avez-vous une zone géographique définie pour votre activité ?",
                "type": "multiple_choice",
                "options": [
                    "Non, pas encore réfléchi",
                    "Ma ville uniquement",
                    "Ma ville + 20-30 km alentours",
                    "Large zone régionale (50+ km)"
                ],
                "correct_answer": 2,
                "points": 7,
                "explanation": "Une zone de 30-50 km permet d'avoir suffisamment de clients sans trop de déplacements."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Comment comptez-vous trouver vos premiers clients ?",
                "type": "multiple_choice",
                "options": [
                    "Je ne sais pas encore",
                    "Bouche-à-oreille uniquement",
                    "Réseaux sociaux et site web",
                    "Stratégie marketing complète (web + partenariats + publicité)"
                ],
                "correct_answer": 3,
                "points": 8,
                "explanation": "Une approche marketing complète accélère significativement le développement."
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Supprimer ancien si existe
    await db.quizzes.delete_one({"quiz_type": "career_fit"})
    await db.quizzes.insert_one(career_quiz)
    print(f"✅ Quiz Adéquation Métier créé : {len(career_quiz['questions'])} questions")
    
    # Quiz 2 : Connaissances Mécaniques
    mechanical_quiz = {
        "id": str(uuid.uuid4()),
        "module_id": "mechanical_knowledge", # ID spécial
        "title": "Évaluation des Connaissances Mécaniques",
        "description": "Ce quiz évalue vos connaissances de base en mécanique automobile. Un score inférieur à 80% vous orientera vers le module de remise à niveau.",
        "passing_score": 80,
        "is_preliminary": True,
        "quiz_type": "mechanical_knowledge",
        "questions": [
            {
                "id": str(uuid.uuid4()),
                "question": "Quel est le rôle principal du moteur dans un véhicule ?",
                "type": "multiple_choice",
                "options": [
                    "Transformer l'énergie électrique en mouvement",
                    "Transformer l'énergie chimique (carburant) en énergie mécanique",
                    "Refroidir le système de transmission",
                    "Alimenter les systèmes électriques"
                ],
                "correct_answer": 1,
                "explanation": "Le moteur thermique transforme l'énergie chimique du carburant en énergie mécanique via la combustion."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Combien de temps de fonctionnement représente un cycle à 4 temps dans un moteur essence ?",
                "type": "multiple_choice",
                "options": [
                    "1 tour de vilebrequin",
                    "2 tours de vilebrequin",
                    "4 tours de vilebrequin",
                    "Cela dépend du régime moteur"
                ],
                "correct_answer": 1,
                "explanation": "Un cycle complet (admission, compression, combustion, échappement) = 2 tours de vilebrequin = 720°."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quelle est la fonction de la courroie de distribution ?",
                "type": "multiple_choice",
                "options": [
                    "Entraîner l'alternateur",
                    "Synchroniser les soupapes avec les pistons",
                    "Refroidir le moteur",
                    "Transmettre la puissance aux roues"
                ],
                "correct_answer": 1,
                "explanation": "La courroie/chaîne de distribution synchronise l'ouverture des soupapes avec le mouvement des pistons."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Que signifie l'acronyme ABS ?",
                "type": "multiple_choice",
                "options": [
                    "Automatic Brake System",
                    "Anti-lock Braking System",
                    "Advanced Brake Security",
                    "Assisted Braking Solution"
                ],
                "correct_answer": 1,
                "explanation": "ABS = Anti-lock Braking System, système empêchant le blocage des roues au freinage."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quelle huile moteur choisir pour un moteur récent ?",
                "type": "multiple_choice",
                "options": [
                    "N'importe quelle huile 15W40",
                    "Celle recommandée par le constructeur (ex: 5W30)",
                    "La moins chère disponible",
                    "Toujours de la 10W40"
                ],
                "correct_answer": 1,
                "explanation": "Il faut TOUJOURS respecter la viscosité recommandée par le constructeur (ex: 5W30, 0W20...)."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "À quelle fréquence moyenne faut-il changer l'huile moteur ?",
                "type": "multiple_choice",
                "options": [
                    "Tous les 5 000 km",
                    "Tous les 10 000-15 000 km ou 1 an",
                    "Tous les 30 000 km",
                    "Quand le voyant s'allume"
                ],
                "correct_answer": 1,
                "explanation": "Selon constructeurs et type d'huile : 10 000-15 000 km ou 1 an maximum, même si peu roulé."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quel composant permet de changer la vitesse de rotation transmise aux roues ?",
                "type": "multiple_choice",
                "options": [
                    "L'embrayage",
                    "La boîte de vitesses",
                    "Le différentiel",
                    "Le volant moteur"
                ],
                "correct_answer": 1,
                "explanation": "La boîte de vitesses adapte le couple et la vitesse de rotation selon les besoins."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quelle est la pression normale des pneus d'une voiture de tourisme ?",
                "type": "multiple_choice",
                "options": [
                    "1,0 à 1,5 bar",
                    "2,0 à 2,5 bar",
                    "3,5 à 4,0 bar",
                    "5,0 bar"
                ],
                "correct_answer": 1,
                "explanation": "La pression standard varie de 2,0 à 2,5 bars selon le véhicule et la charge."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Que vérifie principalement le contrôle technique ?",
                "type": "multiple_choice",
                "options": [
                    "Les performances du moteur",
                    "La sécurité et la pollution",
                    "Le confort de conduite",
                    "L'état de la peinture"
                ],
                "correct_answer": 1,
                "explanation": "Le CT contrôle 131 points liés à la sécurité routière et aux émissions polluantes."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quelle est la fonction du radiateur ?",
                "type": "multiple_choice",
                "options": [
                    "Chauffer l'habitacle",
                    "Refroidir le liquide de refroidissement moteur",
                    "Filtrer l'air d'admission",
                    "Stocker l'huile moteur"
                ],
                "correct_answer": 1,
                "explanation": "Le radiateur dissipe la chaleur du liquide de refroidissement dans l'air ambiant."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Quel élément filtre l'air avant qu'il n'entre dans le moteur ?",
                "type": "multiple_choice",
                "options": [
                    "Le filtre à huile",
                    "Le filtre à air",
                    "Le filtre à carburant",
                    "Le filtre d'habitacle"
                ],
                "correct_answer": 1,
                "explanation": "Le filtre à air retient les impuretés avant l'admission dans les cylindres."
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Qu'est-ce que le 'parallélisme' des roues ?",
                "type": "multiple_choice",
                "options": [
                    "L'alignement des roues dans l'axe du véhicule",
                    "La distance entre les roues avant et arrière",
                    "L'angle d'inclinaison des roues",
                    "La pression identique dans tous les pneus"
                ],
                "correct_answer": 0,
                "explanation": "Le parallélisme est l'alignement horizontal des roues par rapport à l'axe longitudinal."
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.quizzes.delete_one({"quiz_type": "mechanical_knowledge"})
    await db.quizzes.insert_one(mechanical_quiz)
    print(f"✅ Quiz Connaissances Mécaniques créé : {len(mechanical_quiz['questions'])} questions")
    
    # Renommer Module 2
    result = await db.modules.update_one(
        {"order_index": 2},
        {"$set": {
            "title": "Remise à Niveau Mécanique - Les Fondamentaux",
            "description": "Module complet de remise à niveau sur les bases de la mécanique automobile. Idéal si vous avez obtenu moins de 80% au quiz de connaissances mécaniques.",
            "duration_minutes": 120
        }}
    )
    
    if result.modified_count > 0:
        print(f"✅ Module 2 renommé en 'Remise à Niveau Mécanique'")
    
    print(f"\n🎉 Quiz préliminaires créés avec succès!")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_preliminary_quizzes())
