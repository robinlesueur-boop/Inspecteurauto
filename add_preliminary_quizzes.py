#!/usr/bin/env python3
"""
Script to add preliminary quizzes (career fit & mechanical knowledge)
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
from pathlib import Path

# Load environment
ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def add_preliminary_quizzes():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Career Fit Quiz (no authentication required)
    career_fit_quiz = {
        "id": str(uuid.uuid4()),
        "module_id": "career_fit",  # Special module ID for preliminary quiz
        "title": "Quiz d'Adéquation Métier - Inspecteur Automobile",
        "passing_score": 70,
        "questions": [
            {
                "id": "q1",
                "question": "Êtes-vous passionné par l'automobile et la mécanique ?",
                "type": "multiple_choice",
                "options": [
                    "Pas du tout",
                    "Un peu",
                    "Modérément",
                    "Très passionné"
                ],
                "correct_answer": 3,
                "explanation": "Une passion pour l'automobile est essentielle pour réussir dans ce métier."
            },
            {
                "id": "q2",
                "question": "Avez-vous une expérience dans le domaine automobile ?",
                "type": "multiple_choice",
                "options": [
                    "Aucune expérience",
                    "Expérience personnelle (bricolage)",
                    "Formation technique automobile",
                    "Expérience professionnelle"
                ],
                "correct_answer": 2,
                "explanation": "Une formation technique est un atout majeur pour ce métier."
            },
            {
                "id": "q3",
                "question": "Comment évaluez-vous vos compétences en communication ?",
                "type": "multiple_choice",
                "options": [
                    "Difficultés à communiquer",
                    "Communication basique",
                    "Bonnes compétences",
                    "Excellentes compétences"
                ],
                "correct_answer": 3,
                "explanation": "D'excellentes compétences en communication sont cruciales pour expliquer les défauts aux clients."
            },
            {
                "id": "q4",
                "question": "Êtes-vous à l'aise avec les outils technologiques et informatiques ?",
                "type": "multiple_choice",
                "options": [
                    "Pas à l'aise du tout",
                    "Utilisation basique",
                    "Bonne maîtrise",
                    "Expert en technologie"
                ],
                "correct_answer": 2,
                "explanation": "Une bonne maîtrise technologique est nécessaire pour les outils de diagnostic modernes."
            },
            {
                "id": "q5",
                "question": "Quelle est votre disponibilité pour vous déplacer chez les clients ?",
                "type": "multiple_choice",
                "options": [
                    "Très limitée",
                    "Quelques déplacements",
                    "Disponible régulièrement",
                    "Très flexible"
                ],
                "correct_answer": 3,
                "explanation": "La flexibilité pour les déplacements est importante dans ce métier."
            },
            {
                "id": "q6",
                "question": "Comment gérez-vous le stress et la pression ?",
                "type": "multiple_choice",
                "options": [
                    "Difficilement",
                    "Moyennement",
                    "Bien",
                    "Très bien"
                ],
                "correct_answer": 2,
                "explanation": "Une bonne gestion du stress est importante lors d'inspections complexes."
            },
            {
                "id": "q7",
                "question": "Avez-vous un esprit d'analyse et de synthèse développé ?",
                "type": "multiple_choice",
                "options": [
                    "Peu développé",
                    "Moyennement développé",
                    "Bien développé",
                    "Très développé"
                ],
                "correct_answer": 3,
                "explanation": "L'esprit d'analyse est essentiel pour diagnostiquer les problèmes automobiles."
            },
            {
                "id": "q8",
                "question": "Êtes-vous prêt à investir dans des outils professionnels (3000-8000€) ?",
                "type": "multiple_choice",
                "options": [
                    "Pas du tout",
                    "Avec réticence",
                    "Oui, si nécessaire",
                    "Absolument"
                ],
                "correct_answer": 2,
                "explanation": "L'investissement dans des outils professionnels est nécessaire pour exercer ce métier."
            },
            {
                "id": "q9",
                "question": "Comment évaluez-vous votre capacité d'apprentissage ?",
                "type": "multiple_choice",
                "options": [
                    "Lente",
                    "Moyenne",
                    "Rapide",
                    "Très rapide"
                ],
                "correct_answer": 2,
                "explanation": "Une bonne capacité d'apprentissage est importante pour se tenir à jour des évolutions technologiques."
            },
            {
                "id": "q10",
                "question": "Quel est votre objectif principal avec cette formation ?",
                "type": "multiple_choice",
                "options": [
                    "Simple curiosité",
                    "Complément de revenus",
                    "Reconversion professionnelle",
                    "Création d'entreprise"
                ],
                "correct_answer": 2,
                "explanation": "Une reconversion professionnelle montre un engagement sérieux dans ce métier."
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Mechanical Knowledge Quiz (authentication required)
    mechanical_quiz = {
        "id": str(uuid.uuid4()),
        "module_id": "mechanical_knowledge",  # Special module ID for preliminary quiz
        "title": "Quiz de Connaissances Mécaniques Préliminaires",
        "passing_score": 70,
        "questions": [
            {
                "id": "mq1",
                "question": "Quel est le rôle principal du turbocompresseur ?",
                "type": "multiple_choice",
                "options": [
                    "Refroidir le moteur",
                    "Augmenter la puissance du moteur",
                    "Réduire la consommation",
                    "Filtrer l'air"
                ],
                "correct_answer": 1,
                "explanation": "Le turbocompresseur augmente la puissance en comprimant l'air admis dans le moteur."
            },
            {
                "id": "mq2",
                "question": "Que signifie l'acronyme ABS ?",
                "type": "multiple_choice",
                "options": [
                    "Automatic Brake System",
                    "Anti-lock Braking System",
                    "Advanced Brake Safety",
                    "Assisted Braking System"
                ],
                "correct_answer": 1,
                "explanation": "ABS signifie Anti-lock Braking System, système anti-blocage des roues."
            },
            {
                "id": "mq3",
                "question": "Quelle est la fonction principale de l'embrayage ?",
                "type": "multiple_choice",
                "options": [
                    "Refroidir la transmission",
                    "Connecter/déconnecter le moteur de la boîte",
                    "Augmenter la vitesse",
                    "Réduire le bruit"
                ],
                "correct_answer": 1,
                "explanation": "L'embrayage permet de connecter ou déconnecter le moteur de la boîte de vitesses."
            },
            {
                "id": "mq4",
                "question": "Que contrôle principalement l'ECU (calculateur moteur) ?",
                "type": "multiple_choice",
                "options": [
                    "La climatisation",
                    "L'injection et l'allumage",
                    "La direction assistée",
                    "L'éclairage"
                ],
                "correct_answer": 1,
                "explanation": "L'ECU contrôle principalement l'injection de carburant et l'allumage du moteur."
            },
            {
                "id": "mq5",
                "question": "Quel est le rôle du FAP sur un moteur diesel ?",
                "type": "multiple_choice",
                "options": [
                    "Filtrer l'huile moteur",
                    "Capturer les particules de suie",
                    "Refroidir les gaz d'échappement",
                    "Augmenter la puissance"
                ],
                "correct_answer": 1,
                "explanation": "Le FAP (Filtre à Particules) capture les particules de suie des gaz d'échappement diesel."
            },
            {
                "id": "mq6",
                "question": "Que signifie OBD dans le diagnostic automobile ?",
                "type": "multiple_choice",
                "options": [
                    "Oil Brake Diagnostic",
                    "On-Board Diagnostics",
                    "Optimal Brake Detection",
                    "Overload Battery Detection"
                ],
                "correct_answer": 1,
                "explanation": "OBD signifie On-Board Diagnostics, système de diagnostic embarqué."
            },
            {
                "id": "mq7",
                "question": "Quelle est la pression typique d'un pneu de voiture ?",
                "type": "multiple_choice",
                "options": [
                    "1,0 à 1,5 bar",
                    "2,0 à 2,5 bars",
                    "3,5 à 4,0 bars",
                    "5,0 bars et plus"
                ],
                "correct_answer": 1,
                "explanation": "La pression typique d'un pneu de voiture est généralement entre 2,0 et 2,5 bars."
            },
            {
                "id": "mq8",
                "question": "Quel composant assure la direction assistée hydraulique ?",
                "type": "multiple_choice",
                "options": [
                    "La pompe à eau",
                    "La pompe de direction",
                    "L'alternateur",
                    "Le compresseur de climatisation"
                ],
                "correct_answer": 1,
                "explanation": "La pompe de direction assistée fournit l'assistance hydraulique pour la direction."
            },
            {
                "id": "mq9",
                "question": "Que contrôle l'ESP (Electronic Stability Program) ?",
                "type": "multiple_choice",
                "options": [
                    "La vitesse du véhicule",
                    "La stabilité et la trajectoire",
                    "La consommation de carburant",
                    "La température moteur"
                ],
                "correct_answer": 1,
                "explanation": "L'ESP contrôle la stabilité du véhicule et aide à maintenir la trajectoire souhaitée."
            },
            {
                "id": "mq10",
                "question": "Quelle est la fonction principale du radiateur ?",
                "type": "multiple_choice",
                "options": [
                    "Chauffer l'habitacle",
                    "Refroidir le liquide de refroidissement",
                    "Filtrer l'air",
                    "Stocker le carburant"
                ],
                "correct_answer": 1,
                "explanation": "Le radiateur refroidit le liquide de refroidissement du moteur grâce au flux d'air."
            },
            {
                "id": "mq11",
                "question": "Que signifie DTC dans le diagnostic automobile ?",
                "type": "multiple_choice",
                "options": [
                    "Direct Transmission Control",
                    "Diagnostic Trouble Code",
                    "Dynamic Traction Control",
                    "Digital Temperature Control"
                ],
                "correct_answer": 1,
                "explanation": "DTC signifie Diagnostic Trouble Code, code de défaut de diagnostic."
            },
            {
                "id": "mq12",
                "question": "Quel est le rôle principal de l'alternateur ?",
                "type": "multiple_choice",
                "options": [
                    "Démarrer le moteur",
                    "Produire de l'électricité",
                    "Refroidir le moteur",
                    "Comprimer l'air"
                ],
                "correct_answer": 1,
                "explanation": "L'alternateur produit l'électricité nécessaire au fonctionnement du véhicule et recharge la batterie."
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Insert both quizzes
    await db.quizzes.insert_one(career_fit_quiz)
    await db.quizzes.insert_one(mechanical_quiz)
    
    print(f"✅ Quiz d'adéquation métier créé: {len(career_fit_quiz['questions'])} questions")
    print(f"✅ Quiz de connaissances mécaniques créé: {len(mechanical_quiz['questions'])} questions")
    
    # Also need to create a special Module 2 for "Remise à Niveau Mécanique"
    module2_remedial = {
        "id": str(uuid.uuid4()),
        "title": "Remise à Niveau Mécanique",
        "description": "Module de remise à niveau pour les participants ayant obtenu moins de 70% au quiz de connaissances mécaniques. Renforcement des bases techniques essentielles.",
        "order_index": 2,
        "duration_minutes": 120,
        "is_free": False,
        "is_published": True,
        "views_count": 0,
        "content": """
        <div class="module-content">
            <h1>Module de Remise à Niveau Mécanique</h1>
            
            <div class="bg-orange-50 border-l-4 border-orange-500 p-6 mb-8">
                <h2 class="text-2xl font-semibold mb-3">🔧 Renforcement des Bases Techniques</h2>
                <p class="text-lg">Ce module est spécialement conçu pour renforcer vos connaissances mécaniques de base avant d'aborder les modules avancés de la formation.</p>
            </div>

            <h2 class="text-3xl font-bold mt-12 mb-6">Chapitre 1 : Fondamentaux du Moteur</h2>
            
            <h3 class="text-2xl font-semibold mt-8 mb-4">1.1 Principe de Fonctionnement</h3>
            
            <p class="mb-4">Le moteur à combustion interne transforme l'énergie chimique du carburant en énergie mécanique selon un cycle à quatre temps :</p>
            
            <ol class="list-decimal pl-8 mb-4 space-y-2">
                <li><strong>Admission :</strong> Le piston descend, aspirant le mélange air-carburant</li>
                <li><strong>Compression :</strong> Le piston remonte, comprimant le mélange</li>
                <li><strong>Combustion-Détente :</strong> L'explosion pousse le piston vers le bas</li>
                <li><strong>Échappement :</strong> Le piston remonte, évacuant les gaz brûlés</li>
            </ol>

            <h3 class="text-2xl font-semibold mt-8 mb-4">1.2 Composants Essentiels</h3>
            
            <h4 class="text-xl font-semibold mt-6 mb-3">Bloc Moteur</h4>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Cylindres :</strong> Chambres où se déroule la combustion</li>
                <li><strong>Pistons :</strong> Éléments mobiles transmettant la force</li>
                <li><strong>Bielles :</strong> Relient pistons et vilebrequin</li>
                <li><strong>Vilebrequin :</strong> Transforme le mouvement rectiligne en rotatif</li>
            </ul>

            <h4 class="text-xl font-semibold mt-6 mb-3">Culasse</h4>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Soupapes d'admission :</strong> Contrôlent l'entrée du mélange</li>
                <li><strong>Soupapes d'échappement :</strong> Évacuent les gaz brûlés</li>
                <li><strong>Arbres à cames :</strong> Commandent l'ouverture des soupapes</li>
                <li><strong>Bougies d'allumage :</strong> Déclenchent la combustion (essence)</li>
            </ul>

            <h2 class="text-3xl font-bold mt-12 mb-6">Chapitre 2 : Systèmes de Transmission</h2>
            
            <h3 class="text-2xl font-semibold mt-8 mb-4">2.1 L'Embrayage</h3>
            
            <p class="mb-4">L'embrayage permet de connecter ou déconnecter temporairement le moteur de la boîte de vitesses :</p>
            
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Disque d'embrayage :</strong> Élément de friction entre moteur et boîte</li>
                <li><strong>Mécanisme :</strong> Plateau de pression et ressort diaphragme</li>
                <li><strong>Butée :</strong> Actionne le mécanisme via la pédale</li>
                <li><strong>Volant moteur :</strong> Surface de friction côté moteur</li>
            </ul>

            <h3 class="text-2xl font-semibold mt-8 mb-4">2.2 Boîte de Vitesses</h3>
            
            <p class="mb-4">La boîte de vitesses adapte le couple et la vitesse selon les besoins :</p>
            
            <h4 class="text-xl font-semibold mt-6 mb-3">Boîte Manuelle</h4>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Trains d'engrenages :</strong> Différents rapports de démultiplication</li>
                <li><strong>Synchroniseurs :</strong> Égalisent les vitesses avant engagement</li>
                <li><strong>Fourchettes :</strong> Déplacent les baladeurs</li>
                <li><strong>Huile de boîte :</strong> Lubrification et refroidissement</li>
            </ul>

            <h2 class="text-3xl font-bold mt-12 mb-6">Chapitre 3 : Systèmes de Freinage</h2>
            
            <h3 class="text-2xl font-semibold mt-8 mb-4">3.1 Principe de Fonctionnement</h3>
            
            <p class="mb-4">Le système de freinage transforme l'énergie cinétique en chaleur par friction :</p>
            
            <h4 class="text-xl font-semibold mt-6 mb-3">Freins à Disque</h4>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Disque de frein :</strong> Élément rotatif solidaire de la roue</li>
                <li><strong>Plaquettes :</strong> Éléments de friction</li>
                <li><strong>Étrier :</strong> Contient les pistons hydrauliques</li>
                <li><strong>Liquide de frein :</strong> Transmet la pression hydraulique</li>
            </ul>

            <h3 class="text-2xl font-semibold mt-8 mb-4">3.2 Systèmes d'Assistance</h3>
            
            <h4 class="text-xl font-semibold mt-6 mb-3">ABS (Anti-lock Braking System)</h4>
            <p class="mb-4">Empêche le blocage des roues lors d'un freinage d'urgence :</p>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Capteurs de vitesse :</strong> Surveillent la rotation des roues</li>
                <li><strong>Calculateur ABS :</strong> Traite les informations</li>
                <li><strong>Modulateur :</strong> Régule la pression de freinage</li>
                <li><strong>Pompe de retour :</strong> Maintient la pression système</li>
            </ul>

            <h2 class="text-3xl font-bold mt-12 mb-6">Chapitre 4 : Systèmes Électriques</h2>
            
            <h3 class="text-2xl font-semibold mt-8 mb-4">4.1 Circuit de Charge</h3>
            
            <h4 class="text-xl font-semibold mt-6 mb-3">Batterie</h4>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Fonction :</strong> Stockage d'énergie électrique</li>
                <li><strong>Tension nominale :</strong> 12V pour les véhicules légers</li>
                <li><strong>Capacité :</strong> Exprimée en Ah (Ampères-heures)</li>
                <li><strong>Entretien :</strong> Vérification niveau, bornes, charge</li>
            </ul>

            <h4 class="text-xl font-semibold mt-6 mb-3">Alternateur</h4>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Fonction :</strong> Production d'électricité</li>
                <li><strong>Entraînement :</strong> Courroie accessoires</li>
                <li><strong>Régulation :</strong> Maintien tension constante</li>
                <li><strong>Débit :</strong> Adapté aux besoins électriques</li>
            </ul>

            <h3 class="text-2xl font-semibold mt-8 mb-4">4.2 Diagnostic Électronique</h3>
            
            <h4 class="text-xl font-semibold mt-6 mb-3">Système OBD</h4>
            <p class="mb-4">On-Board Diagnostics - Système de diagnostic embarqué :</p>
            <ul class="list-disc pl-8 mb-4 space-y-2">
                <li><strong>Prise diagnostic :</strong> Interface de connexion standardisée</li>
                <li><strong>Codes défauts :</strong> DTC (Diagnostic Trouble Codes)</li>
                <li><strong>Données temps réel :</strong> Paramètres de fonctionnement</li>
                <li><strong>Tests actuateurs :</strong> Vérification composants</li>
            </ul>

            <div class="bg-green-50 border-l-4 border-green-500 p-6 mt-8">
                <h4 class="text-xl font-semibold mb-3">🎯 Objectifs de ce Module</h4>
                <p class="mb-4">À l'issue de ce module de remise à niveau, vous devriez maîtriser :</p>
                <ul class="list-disc pl-6 space-y-2">
                    <li>Les principes de base du moteur à combustion</li>
                    <li>Le fonctionnement des systèmes de transmission</li>
                    <li>Les composants du système de freinage</li>
                    <li>Les bases de l'électricité automobile</li>
                    <li>L'utilisation du diagnostic OBD</li>
                </ul>
            </div>

            <div class="bg-blue-50 p-6 rounded-lg mt-8">
                <h4 class="text-xl font-semibold mb-3">📝 Quiz de Validation</h4>
                <p class="mb-4">Un quiz de validation vous permettra de vérifier l'acquisition de ces connaissances de base.</p>
                <p class="font-semibold">Score requis : 80% minimum pour accéder aux modules suivants.</p>
            </div>
        </div>
        """,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.modules.insert_one(module2_remedial)
    print(f"✅ Module 2 'Remise à Niveau Mécanique' créé")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_preliminary_quizzes())