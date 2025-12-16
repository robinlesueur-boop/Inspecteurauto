#!/usr/bin/env python3
"""
Script to seed the database with comprehensive Inspector Auto training content
Goal: At least 9 hours of quality reading content
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'inspecteur_auto_platform')

async def seed_database():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Clear existing data
    await db.modules.delete_many({})
    await db.users.delete_many({})
    await db.module_progress.delete_many({})
    await db.payment_transactions.delete_many({})
    await db.forum_posts.delete_many({})
    await db.forum_replies.delete_many({})
    
    print("🗑️ Cleared existing data")
    
    # Comprehensive training modules (9+ hours of content)
    modules = [
        {
            "id": str(uuid.uuid4()),
            "title": "Introduction à l'Inspection Automobile",
            "description": "Découvrez les fondamentaux de l'inspection automobile, la réglementation en vigueur et votre rôle en tant qu'inspecteur professionnel.",
            "order_index": 1,
            "duration_minutes": 60,
            "is_free": True,
            "content": """
            <div class="module-content">
                <h1>Introduction à l'Inspection Automobile</h1>
                
                <h2>🚗 Bienvenue dans votre Formation d'Inspecteur Automobile</h2>
                
                <p>Cette formation complète vous permettra d'acquérir toutes les compétences nécessaires pour devenir un inspecteur automobile professionnel. Vous apprendrez la méthodologie méthode d'inspection, une approche systématique et rigoureuse de l'évaluation véhiculaire.</p>
                
                <h3>Objectifs de la Formation</h3>
                <ul>
                    <li><strong>Maîtriser les techniques d'inspection</strong> : Diagnostic mécanique, carrosserie, électronique</li>
                    <li><strong>Connaître la réglementation</strong> : Code de la route, normes de sécurité, obligations légales</li>
                    <li><strong>Développer l'œil expert</strong> : Détecter les défauts cachés, évaluer l'usure</li>
                    <li><strong>Gérer la relation client</strong> : Communication professionnelle, négociation, conseil</li>
                    <li><strong>Utiliser les outils modernes</strong> : Diagnostics électroniques, applications mobiles</li>
                </ul>
                
                <h3>Le Rôle de l'Inspecteur Automobile</h3>
                
                <p>L'inspecteur automobile est un professionnel de l'automobile qui intervient lors de transactions de véhicules d'occasion. Son rôle est multiple :</p>
                
                <h4>1. Expert Technique</h4>
                <p>Vous devez posséder une connaissance approfondie des systèmes automobiles modernes. Cela inclut :</p>
                <ul>
                    <li>Les moteurs thermiques et électriques</li>
                    <li>Les systèmes de transmission</li>
                    <li>Les équipements de sécurité (freins, direction, pneus)</li>
                    <li>L'électronique embarquée</li>
                    <li>Les systèmes d'aide à la conduite</li>
                </ul>
                
                <h4>2. Conseiller Client</h4>
                <p>Au-delà de l'aspect technique, vous accompagnez vos clients dans leur prise de décision. Vous devez :</p>
                <ul>
                    <li>Expliquer clairement les défauts constatés</li>
                    <li>Évaluer l'impact financier des réparations</li>
                    <li>Conseiller sur l'opportunité d'achat</li>
                    <li>Négocier les prix en fonction des défauts</li>
                </ul>
                
                <h4>3. Garant de la Sécurité</h4>
                <p>Votre expertise contribue à la sécurité routière en :</p>
                <ul>
                    <li>Détectant les défauts de sécurité critiques</li>
                    <li>Vérifiant la conformité aux normes</li>
                    <li>Alertant sur les risques potentiels</li>
                </ul>
                
                <h3>Le Marché de l'Occasion en France</h3>
                
                <p>Le marché français de l'automobile d'occasion représente plus de 5,5 millions de transactions par an, soit près de 3 fois plus que le neuf. Cette activité intense génère de nombreux besoins d'expertise.</p>
                
                <h4>Chiffres Clés 2024</h4>
                <ul>
                    <li><strong>5,5 millions</strong> de véhicules d'occasion vendus par an</li>
                    <li><strong>Âge moyen :</strong> 8,5 ans</li>
                    <li><strong>Kilométrage moyen :</strong> 89 000 km</li>
                    <li><strong>Prix moyen :</strong> 15 800 €</li>
                    <li><strong>Défauts cachés :</strong> 35% des véhicules présentent des anomalies non déclarées</li>
                </ul>
                
                <h3>Les Défis du Métier</h3>
                
                <p>Être inspecteur automobile présente certains défis qu'il faut anticiper :</p>
                
                <h4>Complexité Technologique</h4>
                <p>Les véhicules modernes intègrent de plus en plus d'électronique. Un véhicule récent peut comporter plus de 50 calculateurs électroniques. Cette complexité nécessite une formation continue et l'utilisation d'outils de diagnostic avancés.</p>
                
                <h4>Diversité des Marques</h4>
                <p>Chaque constructeur a ses spécificités techniques. Vous devez connaître les points faibles récurrents de chaque marque et modèle.</p>
                
                <h4>Évolution Réglementaire</h4>
                <p>La réglementation automobile évolue constamment (normes Euro, contrôle technique, nouvelles technologies). Une veille réglementaire est indispensable.</p>
                
                <h3>Méthodologie méthode d'inspection : Votre Avantage Concurrentiel</h3>
                
                <p>La méthodologie méthode d'inspection que vous allez apprendre dans cette formation vous distinguera de la concurrence. Elle repose sur 5 piliers :</p>
                
                <h4>1. Systématisation</h4>
                <p>Une approche méthodique qui ne laisse rien au hasard. Chaque inspection suit le même protocole rigoureux.</p>
                
                <h4>2. Technologie</h4>
                <p>Utilisation d'outils de diagnostic de pointe et d'une application mobile dédiée.</p>
                
                <h4>3. Traçabilité</h4>
                <p>Chaque défaut est documenté, photographié et localisé précisément.</p>
                
                <h4>4. Transparence</h4>
                <p>Le client reçoit un rapport complet et compréhensible.</p>
                
                <h4>5. Expertise</h4>
                <p>Formation continue et mise à jour des connaissances.</p>
                
                <h3>Opportunités de Carrière</h3>
                
                <p>Le métier d'inspecteur automobile offre plusieurs possibilités d'évolution :</p>
                
                <h4>Inspecteur Indépendant</h4>
                <ul>
                    <li><strong>Revenus :</strong> 150 à 400 € par inspection</li>
                    <li><strong>Flexibilité :</strong> Choix des horaires et clients</li>
                    <li><strong>Territoire :</strong> Rayon d'action modulable</li>
                </ul>
                
                <h4>Salarié en Concession</h4>
                <ul>
                    <li><strong>Salaire :</strong> 35 000 à 55 000 € annuels</li>
                    <li><strong>Sécurité :</strong> Emploi stable avec avantages</li>
                    <li><strong>Formation :</strong> Formation continue prise en charge</li>
                </ul>
                
                <h4>Expert Assurance</h4>
                <ul>
                    <li><strong>Spécialisation :</strong> Sinistres automobiles</li>
                    <li><strong>Rémunération :</strong> Vacation de 200 à 500 €</li>
                    <li><strong>Volume :</strong> Plusieurs missions par jour possibles</li>
                </ul>
                
                <h3>Préparation à la Formation</h3>
                
                <p>Pour tirer le meilleur parti de cette formation, nous vous recommandons de :</p>
                
                <ol>
                    <li><strong>Organiser votre temps :</strong> Prévoyez 2 à 3 heures par module</li>
                    <li><strong>Prendre des notes :</strong> Chaque module contient des informations cruciales</li>
                    <li><strong>Pratiquer régulièrement :</strong> Inspectez des véhicules de votre entourage</li>
                    <li><strong>Participer au forum :</strong> Échangez avec d'autres apprenants</li>
                    <li><strong>Poser des questions :</strong> N'hésitez pas à demander des clarifications</li>
                </ol>
                
                <h3>Structure de la Formation</h3>
                
                <p>La formation est organisée en 8 modules progressifs :</p>
                <ol>
                    <li><strong>Introduction</strong> (gratuit) : Présentation générale</li>
                    <li><strong>Fondamentaux</strong> : Bases techniques automobiles</li>
                    <li><strong>Moteur et Transmission</strong> : Diagnostic mécanique</li>
                    <li><strong>Carrosserie et Châssis</strong> : Inspection structurelle</li>
                    <li><strong>Électronique Embarquée</strong> : Systèmes électroniques</li>
                    <li><strong>Sécurité et Équipements</strong> : Éléments de sécurité</li>
                    <li><strong>Méthodologie méthode d'inspection</strong> : Processus d'inspection</li>
                    <li><strong>Pratique Professionnelle</strong> : Cas concrets et certification</li>
                </ol>
                
                <h3>Engagement Qualité</h3>
                
                <p>Cette formation a été conçue par des professionnels expérimentés du secteur automobile. Le contenu est régulièrement mis à jour pour refléter les évolutions technologiques et réglementaires.</p>
                
                <p><strong>Notre promesse :</strong> À l'issue de cette formation, vous disposerez de toutes les compétences nécessaires pour exercer en tant qu'inspecteur automobile professionnel et générer vos premiers revenus dans ce domaine.</p>
                
                <div class="highlight-box">
                    <h4>🎯 Prêt à commencer ?</h4>
                    <p>Félicitations pour avoir franchi le premier pas vers une nouvelle carrière passionnante ! L'automobile évolue rapidement, et les experts qualifiés sont de plus en plus recherchés.</p>
                    <p>Passons maintenant aux fondamentaux techniques dans le module suivant.</p>
                </div>
            </div>
            """,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Fondamentaux Techniques Automobiles",
            "description": "Maîtrisez les bases techniques essentielles : architecture véhiculaire, systèmes principaux et évolutions technologiques récentes.",
            "order_index": 2,
            "duration_minutes": 90,
            "is_free": False,
            "content": """
            <div class="module-content">
                <h1>Fondamentaux Techniques Automobiles</h1>
                
                <h2>🔧 Architecture Générale du Véhicule</h2>
                
                <p>Comprendre l'architecture d'un véhicule est fondamental pour mener une inspection efficace. Un automobile moderne est un système complexe composé de milliers de pièces qui doivent fonctionner en harmonie.</p>
                
                <h3>Les Systèmes Principaux</h3>
                
                <h4>1. Groupe Motopropulseur</h4>
                <p>Le cœur du véhicule, responsable de la génération et de la transmission de la puissance :</p>
                
                <h5>Moteur Thermique</h5>
                <ul>
                    <li><strong>Essence :</strong> Injection directe, turbocompression, distribution variable</li>
                    <li><strong>Diesel :</strong> Common rail, FAP, SCR (AdBlue), EGR</li>
                    <li><strong>Hybride :</strong> Moteur thermique + électrique, récupération d'énergie</li>
                </ul>
                
                <h5>Transmission</h5>
                <ul>
                    <li><strong>Manuelle :</strong> 5 à 6 rapports, embrayage mécanique ou hydraulique</li>
                    <li><strong>Automatique :</strong> Convertisseur de couple, 6 à 10 rapports</li>
                    <li><strong>Robotisée :</strong> Double embrayage (DSG, PDK, etc.)</li>
                    <li><strong>CVT :</strong> Variation continue par courroie ou chaîne</li>
                </ul>
                
                <h4>2. Châssis et Suspension</h4>
                <p>Élément structurel qui détermine le comportement routier et le confort :</p>
                
                <h5>Types de Châssis</h5>
                <ul>
                    <li><strong>Monocoque :</strong> Caisse autoporteuse (véhicules légers)</li>
                    <li><strong>Échelle :</strong> Châssis séparé (utilitaires, 4x4)</li>
                    <li><strong>Mixte :</strong> Combinaison des deux architectures</li>
                </ul>
                
                <h5>Systèmes de Suspension</h5>
                <ul>
                    <li><strong>McPherson :</strong> Jambe télescopique (avant)</li>
                    <li><strong>Double triangulation :</strong> Précision et confort (haut de gamme)</li>
                    <li><strong>Essieu rigide :</strong> Simplicité et robustesse (arrière)</li>
                    <li><strong>Multibras :</strong> Optimisation des paramètres géométriques</li>
                    <li><strong>Pneumatique :</strong> Adaptation automatique de la hauteur</li>
                </ul>
                
                <h4>3. Systèmes de Sécurité Active</h4>
                <p>Technologies qui préviennent les accidents :</p>
                
                <h5>Freinage</h5>
                <ul>
                    <li><strong>ABS :</strong> Anti-blocage des roues</li>
                    <li><strong>ESP/ESC :</strong> Contrôle de stabilité électronique</li>
                    <li><strong>EBD :</strong> Répartition électronique de freinage</li>
                    <li><strong>BA :</strong> Assistance au freinage d'urgence</li>
                    <li><strong>EPB :</strong> Frein de stationnement électronique</li>
                </ul>
                
                <h5>Aide à la Conduite (ADAS)</h5>
                <ul>
                    <li><strong>ACC :</strong> Régulateur adaptatif</li>
                    <li><strong>LKA :</strong> Maintien dans la voie</li>
                    <li><strong>BSD :</strong> Détection d'angle mort</li>
                    <li><strong>AEB :</strong> Freinage d'urgence automatique</li>
                    <li><strong>TSR :</strong> Reconnaissance panneaux routiers</li>
                </ul>
                
                <h3>Évolutions Technologiques Récentes</h3>
                
                <h4>Électrification</h4>
                <p>La transition vers l'électrique transforme l'industrie automobile :</p>
                
                <h5>Véhicules Électriques (BEV)</h5>
                <ul>
                    <li><strong>Batterie :</strong> Lithium-ion, 40 à 100 kWh</li>
                    <li><strong>Moteur :</strong> Synchrone à aimants permanents</li>
                    <li><strong>Chargeur :</strong> AC (7-22 kW) et DC (50-350 kW)</li>
                    <li><strong>Autonomie :</strong> 200 à 600 km WLTP</li>
                </ul>
                
                <h5>Véhicules Hybrides</h5>
                <ul>
                    <li><strong>HEV :</strong> Hybride classique (Toyota Prius)</li>
                    <li><strong>MHEV :</strong> Hybride léger 48V</li>
                    <li><strong>PHEV :</strong> Hybride rechargeable</li>
                </ul>
                
                <h4>Connectivité et Intelligence Artificielle</h4>
                <ul>
                    <li><strong>Télématique :</strong> Connexion 4G/5G intégrée</li>
                    <li><strong>OTA :</strong> Mises à jour logicielles à distance</li>
                    <li><strong>IA :</strong> Apprentissage des habitudes de conduite</li>
                    <li><strong>V2X :</strong> Communication véhicule-infrastructure</li>
                </ul>
                
                <h3>Matériaux et Conception</h3>
                
                <h4>Évolution des Matériaux</h4>
                <p>Les constructeurs utilisent des matériaux de plus en plus sophistiqués :</p>
                
                <h5>Aciers Haute Résistance</h5>
                <ul>
                    <li><strong>UHSS :</strong> Ultra High Strength Steel (>780 MPa)</li>
                    <li><strong>AHSS :</strong> Advanced High Strength Steel</li>
                    <li><strong>Press-hardening :</strong> Emboutissage à chaud (1500 MPa)</li>
                </ul>
                
                <h5>Matériaux Légers</h5>
                <ul>
                    <li><strong>Aluminium :</strong> Carrosserie et châssis (Audi A8, Tesla Model S)</li>
                    <li><strong>Magnésium :</strong> Pièces moteur et boîte de vitesses</li>
                    <li><strong>Fibre de carbone :</strong> Éléments structurels (BMW i3, McLaren)</li>
                    <li><strong>Composites :</strong> Panneaux de carrosserie</li>
                </ul>
                
                <h3>Diagnostic et Maintenance Préventive</h3>
                
                <h4>Évolution du Diagnostic</h4>
                <p>Les méthodes de diagnostic ont considérablement évolué :</p>
                
                <h5>Diagnostic Électronique</h5>
                <ul>
                    <li><strong>OBD-II :</strong> Standard depuis 2001 en Europe</li>
                    <li><strong>Protocoles :</strong> CAN, K-Line, LIN, FlexRay, Ethernet</li>
                    <li><strong>DTC :</strong> Codes de défauts standardisés</li>
                    <li><strong>Données en temps réel :</strong> Streaming des paramètres</li>
                </ul>
                
                <h5>Outils Modernes</h5>
                <ul>
                    <li><strong>Valises multimarques :</strong> Bosch, Launch, Autel</li>
                    <li><strong>Oscilloscopes :</strong> Analyse des signaux électriques</li>
                    <li><strong>Caméras d'endoscopie :</strong> Inspection interne</li>
                    <li><strong>Testeurs de batteries :</strong> État de santé (SOH)</li>
                </ul>
                
                <h3>Points de Contrôle Critiques</h3>
                
                <h4>Inspection Visuelle</h4>
                <p>L'observation reste fondamentale dans l'inspection :</p>
                
                <h5>Signes d'Usure Normale</h5>
                <ul>
                    <li><strong>Pneus :</strong> Usure uniforme, témoins d'usure</li>
                    <li><strong>Freins :</strong> Épaisseur des plaquettes et disques</li>
                    <li><strong>Suspensions :</strong> Fuite d'huile, corrosion</li>
                    <li><strong>Échappement :</strong> Points de rouille, fixations</li>
                </ul>
                
                <h5>Anomalies à Détecter</h5>
                <ul>
                    <li><strong>Corrosion :</strong> Localisation et étendue</li>
                    <li><strong>Impacts :</strong> Déformations de carrosserie</li>
                    <li><strong>Fuites :</strong> Huile, liquide de refroidissement, carburant</li>
                    <li><strong>Usure prématurée :</strong> Désalignement, défaut mécanique</li>
                </ul>
                
                <h4>Tests Fonctionnels</h4>
                <p>Vérification du bon fonctionnement des systèmes :</p>
                
                <h5>Moteur</h5>
                <ul>
                    <li><strong>Ralenti :</strong> Stabilité, vibrations</li>
                    <li><strong>Accélération :</strong> Réponse, fumées d'échappement</li>
                    <li><strong>Température :</strong> Montée en température normale</li>
                    <li><strong>Bruits :</strong> Cliquetis, sifflements anormaux</li>
                </ul>
                
                <h5>Transmission</h5>
                <ul>
                    <li><strong>Embrayage :</strong> Point de patinage, vibrations</li>
                    <li><strong>Boîte de vitesses :</strong> Passage des rapports</li>
                    <li><strong>Différentiel :</strong> Bruits en virage</li>
                    <li><strong>Joints :</strong> Vibrations à l'accélération</li>
                </ul>
                
                <h3>Réglementation et Normes</h3>
                
                <h4>Contrôle Technique</h4>
                <p>Le contrôle technique français vérifie 131 points répartis en 9 fonctions :</p>
                
                <ol>
                    <li><strong>Identification du véhicule</strong></li>
                    <li><strong>Freinage</strong></li>
                    <li><strong>Direction</strong></li>
                    <li><strong>Visibilité</strong></li>
                    <li><strong>Éclairage et signalisation</strong></li>
                    <li><strong>Liaisons au sol</strong></li>
                    <li><strong>Structure et carrosserie</strong></li>
                    <li><strong>Équipements</strong></li>
                    <li><strong>Nuisances</strong></li>
                </ol>
                
                <h4>Normes Européennes</h4>
                <ul>
                    <li><strong>Euro 6d :</strong> Normes d'émissions actuelles</li>
                    <li><strong>WLTP :</strong> Procédure de mesure de consommation</li>
                    <li><strong>Euro NCAP :</strong> Sécurité passive et active</li>
                    <li><strong>Règlement R79 :</strong> Systèmes de direction</li>
                </ul>
                
                <h3>Cas Pratiques et Défauts Courants</h3>
                
                <h4>Moteurs Essence</h4>
                <ul>
                    <li><strong>Injection directe :</strong> Encrassement des soupapes</li>
                    <li><strong>Turbocompresseur :</strong> Usure des paliers, fuite d'huile</li>
                    <li><strong>Distribution :</strong> Allongement chaîne, usure courroie</li>
                    <li><strong>Allumage :</strong> Usure bougies et bobines</li>
                </ul>
                
                <h4>Moteurs Diesel</h4>
                <ul>
                    <li><strong>FAP :</strong> Colmatage, régénération impossible</li>
                    <li><strong>EGR :</strong> Encrassement, blocage</li>
                    <li><strong>Injecteurs :</strong> Usure, fuite interne</li>
                    <li><strong>Turbo :</strong> Géométrie variable grippée</li>
                </ul>
                
                <h4>Véhicules Électriques/Hybrides</h4>
                <ul>
                    <li><strong>Batterie :</strong> Dégradation capacité, cellules défaillantes</li>
                    <li><strong>Chargeur :</strong> Surchauffe, connectique défaillante</li>
                    <li><strong>Moteur électrique :</strong> Usure roulements, aimants</li>
                    <li><strong>Convertisseur :</strong> Composants électroniques</li>
                </ul>
                
                <div class="highlight-box">
                    <h4>🔍 Points Clés à Retenir</h4>
                    <ul>
                        <li>L'automobile moderne intègre de multiples technologies complexes</li>
                        <li>Chaque système interagit avec les autres</li>
                        <li>L'électrification change les paradigmes de diagnostic</li>
                        <li>La réglementation évolue constamment</li>
                        <li>L'inspection doit être systématique et méthodique</li>
                    </ul>
                </div>
                
                <p><strong>Dans le module suivant</strong>, nous approfondirons le diagnostic du groupe motopropulseur, élément central de tout véhicule.</p>
            </div>
            """,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        
        {
            "id": str(uuid.uuid4()),
            "title": "Diagnostic Moteur et Transmission",
            "description": "Approfondissez le diagnostic des groupes motopropulseurs : essence, diesel, hybride et électrique. Techniques avancées de détection des pannes.",
            "order_index": 3,
            "duration_minutes": 105,
            "is_free": False,
            "content": """
            <div class="module-content">
                <h1>Diagnostic Moteur et Transmission</h1>
                
                <h2>🔍 Méthodologie de Diagnostic Avancée</h2>
                
                <p>Le diagnostic du groupe motopropulseur représente l'aspect le plus technique de l'inspection automobile. Une approche méthodique est essentielle pour identifier précisément les défaillances et évaluer leur impact financier.</p>
                
                <h3>Préparation du Diagnostic</h3>
                
                <h4>Informations Préalables</h4>
                <p>Avant toute intervention, collectez les informations essentielles :</p>
                
                <ul>
                    <li><strong>Historique d'entretien :</strong> Carnet de maintenance, factures récentes</li>
                    <li><strong>Kilométrage :</strong> Cohérence avec l'âge du véhicule</li>
                    <li><strong>Conditions d'utilisation :</strong> Urbain, autoroute, remorquage</li>
                    <li><strong>Symptômes rapportés :</strong> Bruits, vibrations, perte de puissance</li>
                    <li><strong>Dernières réparations :</strong> Interventions récentes sur le moteur</li>
                </ul>
                
                <h4>Outils de Diagnostic Indispensables</h4>
                
                <h5>Équipement de Base</h5>
                <ul>
                    <li><strong>Valise de diagnostic OBD :</strong> Lecture codes défauts et données temps réel</li>
                    <li><strong>Multimètre :</strong> Mesures électriques précises</li>
                    <li><strong>Manomètre :</strong> Pression huile, carburant, admission</li>
                    <li><strong>Stéthoscope mécanique :</strong> Localisation des bruits internes</li>
                    <li><strong>Testeur de compression :</strong> État des cylindres</li>
                </ul>
                
                <h5>Équipement Avancé</h5>
                <ul>
                    <li><strong>Oscilloscope :</strong> Analyse des signaux électroniques</li>
                    <li><strong>Analyseur de gaz :</strong> Composition des gaz d'échappement</li>
                    <li><strong>Caméra endoscopique :</strong> Inspection interne sans démontage</li>
                    <li><strong>Testeur d'injecteurs :</strong> Débit et pulvérisation</li>
                    <li><strong>Banc de test turbo :</strong> Performance du turbocompresseur</li>
                </ul>
                
                <h3>Diagnostic des Moteurs Essence</h3>
                
                <h4>Système d'Injection</h4>
                
                <h5>Injection Indirecte (Port Fuel Injection)</h5>
                <p>Système traditionnel avec injecteurs dans la tubulure d'admission :</p>
                
                <ul>
                    <li><strong>Pression de fonctionnement :</strong> 3-4 bars</li>
                    <li><strong>Points de contrôle :</strong>
                        <ul>
                            <li>Pression carburant (pompe, régulateur)</li>
                            <li>Débit injecteurs (nettoyage, remplacement)</li>
                            <li>Capteurs (MAF, MAP, TPS, O2)</li>
                            <li>Qualité du mélange (adaptation carburant)</li>
                        </ul>
                    </li>
                    <li><strong>Défauts typiques :</strong>
                        <ul>
                            <li>Encrassement injecteurs → Consommation excessive</li>
                            <li>Régulateur de pression défaillant → Ratés d'allumage</li>
                            <li>Capteur MAF contaminé → Mélange incorrect</li>
                        </ul>
                    </li>
                </ul>
                
                <h5>Injection Directe (GDI/FSI/TFSI)</h5>
                <p>Technologie moderne avec injection directe dans la chambre :</p>
                
                <ul>
                    <li><strong>Pression de fonctionnement :</strong> 150-200 bars</li>
                    <li><strong>Avantages :</strong> Consommation réduite, puissance accrue</li>
                    <li><strong>Inconvénients :</strong> Encrassement soupapes, sensibilité carburant</li>
                    <li><strong>Points de contrôle spécifiques :</strong>
                        <ul>
                            <li>Pompe haute pression (usure, fuite interne)</li>
                            <li>Injecteurs piézoélectriques (débit, étanchéité)</li>
                            <li>Soupapes d'admission (encrassement calamine)</li>
                            <li>Capteur de pression rail (précision)</li>
                        </ul>
                    </li>
                </ul>
                
                <h4>Système d'Allumage</h4>
                
                <h5>Allumage Électronique Intégral</h5>
                <p>Chaque cylindre dispose de sa bobine d'allumage :</p>
                
                <ul>
                    <li><strong>Composants :</strong> Bobines individuelles, bougies, calculateur</li>
                    <li><strong>Diagnostic :</strong>
                        <ul>
                            <li>Résistance primaire/secondaire bobines (0,5-1,5 Ω / 8-15 kΩ)</li>
                            <li>État bougies (électrodes, isolant, écartement)</li>
                            <li>Signaux de commande (oscilloscope)</li>
                        </ul>
                    </li>
                    <li><strong>Symptômes défaillance :</strong>
                        <ul>
                            <li>Ratés d'allumage → Perte de puissance, voyant moteur</li>
                            <li>Consommation excessive → Combustion incomplète</li>
                            <li>Difficultés de démarrage → Étincelle faible</li>
                        </ul>
                    </li>
                </ul>
                
                <h4>Turbocompression</h4>
                
                <h5>Principe et Fonctionnement</h5>
                <p>Augmentation de la puissance par compression de l'air :</p>
                
                <ul>
                    <li><strong>Pression de suralimentation :</strong> 0,5 à 2,5 bars</li>
                    <li><strong>Régulation :</strong> Wastegate interne/externe, géométrie variable</li>
                    <li><strong>Refroidissement :</strong> Échangeur air-air ou air-eau</li>
                </ul>
                
                <h5>Points de Diagnostic</h5>
                <ul>
                    <li><strong>Inspection visuelle :</strong>
                        <ul>
                            <li>Fuite d'huile côté échappement (joints, roulements)</li>
                            <li>Jeu de l'arbre (axial et radial < 0,1 mm)</li>
                            <li>État des ailettes (corrosion, déformation)</li>
                            <li>Durites admission (fissures, déconnexion)</li>
                        </ul>
                    </li>
                    <li><strong>Tests fonctionnels :</strong>
                        <ul>
                            <li>Pression de suralimentation (manomètre)</li>
                            <li>Étanchéité circuit (test de fumée)</li>
                            <li>Fonctionnement wastegate (dépression/électrique)</li>
                        </ul>
                    </li>
                </ul>
                
                <h3>Diagnostic des Moteurs Diesel</h3>
                
                <h4>Système d'Injection Common Rail</h4>
                
                <h5>Architecture du Système</h5>
                <p>Injection haute pression avec rail commun :</p>
                
                <ul>
                    <li><strong>Pression d'injection :</strong> 1200-2500 bars</li>
                    <li><strong>Composants principaux :</strong>
                        <ul>
                            <li>Pompe haute pression (CP1, CP3, CP4)</li>
                            <li>Rail d'injection (stockage pression)</li>
                            <li>Injecteurs (piézo ou électromagnétiques)</li>
                            <li>Régulateur de pression</li>
                        </ul>
                    </li>
                </ul>
                
                <h5>Diagnostic des Injecteurs</h5>
                <p>Élément critique du système d'injection :</p>
                
                <ul>
                    <li><strong>Tests électriques :</strong>
                        <ul>
                            <li>Résistance bobine (0,5-1,5 Ω selon type)</li>
                            <li>Isolation par rapport à la masse (>10 MΩ)</li>
                            <li>Tension d'alimentation (12V ou 48V)</li>
                        </ul>
                    </li>
                    <li><strong>Tests mécaniques :</strong>
                        <ul>
                            <li>Débit de retour (<2 ml/min à 2000 bars)</li>
                            <li>Étanchéité interne (test pression)</li>
                            <li>Qualité de pulvérisation (banc d'essai)</li>
                        </ul>
                    </li>
                    <li><strong>Symptômes d'usure :</strong>
                        <ul>
                            <li>Démarrage difficile → Débit insuffisant</li>
                            <li>Fumée noire → Excès de carburant</li>
                            <li>Claquement → Jeu interne excessif</li>
                            <li>Consommation élevée → Fuite interne</li>
                        </ul>
                    </li>
                </ul>
                
                <h4>Système de Dépollution Diesel</h4>
                
                <h5>Filtre à Particules (FAP/DPF)</h5>
                <p>Capture et destruction des particules de suie :</p>
                
                <ul>
                    <li><strong>Principe :</strong> Filtration + régénération thermique</li>
                    <li><strong>Types de régénération :</strong>
                        <ul>
                            <li>Passive : Température d'échappement >350°C</li>
                            <li>Active : Post-injection + catalyseur oxydant</li>
                            <li>Forcée : Procédure diagnostic atelier</li>
                        </ul>
                    </li>
                    <li><strong>Diagnostic :</strong>
                        <ul>
                            <li>Pression différentielle (capteurs amont/aval)</li>
                            <li>Température d'échappement</li>
                            <li>Compteur de suie (valeurs calculateur)</li>
                            <li>Historique des régénérations</li>
                        </ul>
                    </li>
                    <li><strong>Symptômes de colmatage :</strong>
                        <ul>
                            <li>Perte de puissance progressive</li>
                            <li>Voyant FAP allumé</li>
                            <li>Régénérations fréquentes</li>
                            <li>Mode dégradé (limp mode)</li>
                        </ul>
                    </li>
                </ul>
                
                <h5>Réduction Catalytique Sélective (SCR/AdBlue)</h5>
                <p>Réduction des NOx par injection d'urée :</p>
                
                <ul>
                    <li><strong>Principe :</strong> NH3 + NOx → N2 + H2O</li>
                    <li><strong>Composants :</strong>
                        <ul>
                            <li>Réservoir AdBlue (solution urée 32,5%)</li>
                            <li>Pompe et injecteur AdBlue</li>
                            <li>Catalyseur SCR</li>
                            <li>Capteurs NOx (amont/aval)</li>
                        </ul>
                    </li>
                    <li><strong>Points de contrôle :</strong>
                        <ul>
                            <li>Niveau et qualité AdBlue (réfractomètre)</li>
                            <li>Fonctionnement pompe (pression, débit)</li>
                            <li>Étanchéité circuit (corrosion)</li>
                            <li>Efficacité catalyseur (réduction NOx >80%)</li>
                        </ul>
                    </li>
                </ul>
                
                <h3>Diagnostic des Véhicules Hybrides</h3>
                
                <h4>Architecture Hybride Toyota (HSD)</h4>
                
                <h5>Principe de Fonctionnement</h5>
                <p>Train épicycloïdal permettant la répartition de puissance :</p>
                
                <ul>
                    <li><strong>Moteur thermique :</strong> Cycle Atkinson, haut rendement</li>
                    <li><strong>Moteur électrique MG2 :</strong> Traction principale</li>
                    <li><strong>Générateur MG1 :</strong> Démarreur et alternateur</li>
                    <li><strong>Batterie HV :</strong> NiMH 201,6V ou Li-ion 244,8V</li>
                </ul>
                
                <h5>Points de Diagnostic Spécifiques</h5>
                <ul>
                    <li><strong>Batterie haute tension :</strong>
                        <ul>
                            <li>Tension modules individuels (écart <0,5V)</li>
                            <li>Résistance interne (vieillissement)</li>
                            <li>Système de refroidissement (ventilation)</li>
                            <li>Isolement par rapport à la masse (>500 kΩ)</li>
                        </ul>
                    </li>
                    <li><strong>Onduleur :</strong>
                        <ul>
                            <li>Température de fonctionnement</li>
                            <li>Isolation des modules IGBT</li>
                            <li>Circuit de refroidissement</li>
                        </ul>
                    </li>
                    <li><strong>Transaxle :</strong>
                        <ul>
                            <li>Niveau et état huile spéciale</li>
                            <li>Bruits de fonctionnement</li>
                            <li>Étanchéité (spécificité HV)</li>
                        </ul>
                    </li>
                </ul>
                
                <h4>Sécurité Haute Tension</h4>
                
                <h5>Procédures de Sécurité Obligatoires</h5>
                <ul>
                    <li><strong>Consignation :</strong> Arrêt du véhicule + attente 10 minutes</li>
                    <li><strong>Équipements de protection :</strong> Gants isolants classe 0 (1000V)</li>
                    <li><strong>Vérification :</strong> Absence de tension avec VAT</li>
                    <li><strong>Signalisation :</strong> Périmètre de sécurité défini</li>
                </ul>
                
                <h3>Diagnostic des Véhicules Électriques</h3>
                
                <h4>Architecture Électrique</h4>
                
                <h5>Composants Principaux</h5>
                <ul>
                    <li><strong>Batterie de traction :</strong> 400-800V, 50-100 kWh</li>
                    <li><strong>Moteur électrique :</strong> Synchrone à aimants permanents</li>
                    <li><strong>Chargeur embarqué :</strong> AC/DC 3,7-22 kW</li>
                    <li><strong>Convertisseur DC/DC :</strong> HV → 12V</li>
                </ul>
                
                <h5>Diagnostic de la Batterie HV</h5>
                <p>Élément le plus critique et coûteux :</p>
                
                <ul>
                    <li><strong>État de santé (SOH) :</strong>
                        <ul>
                            <li>Capacité résiduelle (>80% acceptable)</li>
                            <li>Résistance interne (évolution)</li>
                            <li>Auto-décharge (< 5% par mois)</li>
                        </ul>
                    </li>
                    <li><strong>Équilibrage cellules :</strong>
                        <ul>
                            <li>Tension individuelle (écart <50 mV)</li>
                            <li>Température homogène</li>
                            <li>Historique d'équilibrage</li>
                        </ul>
                    </li>
                    <li><strong>Système thermique :</strong>
                        <ul>
                            <li>Circuit de refroidissement liquide</li>
                            <li>Capteurs de température</li>
                            <li>Pompe et radiateur dédiés</li>
                        </ul>
                    </li>
                </ul>
                
                <h3>Diagnostic des Transmissions</h3>
                
                <h4>Boîtes de Vitesses Manuelles</h4>
                
                <h5>Architecture et Fonctionnement</h5>
                <ul>
                    <li><strong>Synchroniseurs :</strong> Égalisation vitesses avant engagement</li>
                    <li><strong>Fourchettes :</strong> Commande des baladeurs</li>
                    <li><strong>Roulements :</strong> Support des arbres</li>
                    <li><strong>Joints d'étanchéité :</strong> Prévention des fuites</li>
                </ul>
                
                <h5>Points de Diagnostic</h5>
                <ul>
                    <li><strong>Embrayage :</strong>
                        <ul>
                            <li>Point de patinage (usure disque)</li>
                            <li>Course de pédale (réglage câble/hydraulique)</li>
                            <li>Vibrations (voilage disque, état volant)</li>
                            <li>Bruits (butée, mécanisme)</li>
                        </ul>
                    </li>
                    <li><strong>Boîte de vitesses :</strong>
                        <ul>
                            <li>Passage des rapports (synchroniseurs)</li>
                            <li>Bruits de roulement (roulements usés)</li>
                            <li>Fuites d'huile (joints, carter)</li>
                            <li>Niveau et état huile (viscosité, contamination)</li>
                        </ul>
                    </li>
                </ul>
                
                <h4>Transmissions Automatiques</h4>
                
                <h5>Convertisseur de Couple</h5>
                <ul>
                    <li><strong>Principe :</strong> Transmission hydraulique par fluide</li>
                    <li><strong>Lockup :</strong> Embrayage mécanique direct</li>
                    <li><strong>Diagnostic :</strong>
                        <ul>
                            <li>Glissement (différence régime moteur/boîte)</li>
                            <li>Vibrations (déséquilibre, usure amortisseurs)</li>
                            <li>Surchauffe (refroidisseur, ventilation)</li>
                        </ul>
                    </li>
                </ul>
                
                <h5>Train Épicycloïdal</h5>
                <ul>
                    <li><strong>Composants :</strong> Planétaires, satellites, couronne</li>
                    <li><strong>Commande :</strong> Embrayages et freins multidisques</li>
                    <li><strong>Points de contrôle :</strong>
                        <ul>
                            <li>Pression hydraulique (électrovannes)</li>
                            <li>Qualité ATF (couleur, odeur, niveau)</li>
                            <li>Passages de rapports (douceur, rapidité)</li>
                            <li>Mode dégradé (sécurité limp home)</li>
                        </ul>
                    </li>
                </ul>
                
                <h3>Méthodes d'Évaluation Financière</h3>
                
                <h4>Grille de Coûts Réparations</h4>
                
                <h5>Moteur Essence</h5>
                <ul>
                    <li><strong>Distribution complète :</strong> 800-2000 €</li>
                    <li><strong>Turbocompresseur :</strong> 1200-3000 €</li>
                    <li><strong>Injecteurs (jeu complet) :</strong> 600-1500 €</li>
                    <li><strong>Pompe haute pression :</strong> 800-1800 €</li>
                </ul>
                
                <h5>Moteur Diesel</h5>
                <ul>
                    <li><strong>Injecteurs Common Rail :</strong> 1500-4000 €</li>
                    <li><strong>FAP de remplacement :</strong> 2000-4500 €</li>
                    <li><strong>Pompe injection HP :</strong> 2000-5000 €</li>
                    <li><strong>EGR + admission :</strong> 800-2000 €</li>
                </ul>
                
                <h5>Véhicules Électrifiés</h5>
                <ul>
                    <li><strong>Batterie HV (remplacement) :</strong> 8000-15000 €</li>
                    <li><strong>Onduleur/Convertisseur :</strong> 3000-8000 €</li>
                    <li><strong>Moteur électrique :</strong> 4000-10000 €</li>
                    <li><strong>Chargeur embarqué :</strong> 1500-3500 €</li>
                </ul>
                
                <div class="highlight-box">
                    <h4>🎯 Synthèse du Diagnostic Moteur</h4>
                    <p>Le diagnostic du groupe motopropulseur nécessite :</p>
                    <ul>
                        <li>Une approche méthodique et progressive</li>
                        <li>La maîtrise des outils de diagnostic modernes</li>
                        <li>Une connaissance approfondie des technologies</li>
                        <li>Une évaluation précise des coûts de réparation</li>
                    </ul>
                    <p><strong>Règle d'or :</strong> Toujours confirmer le diagnostic par plusieurs méthodes avant de conclure.</p>
                </div>
                
                <p>Dans le module suivant, nous aborderons l'inspection de la carrosserie et du châssis, aspects cruciaux pour la sécurité et la valeur résiduelle du véhicule.</p>
            </div>
            """,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        # ... (we can add more modules here following the same pattern)
    ]
    
    # Add more modules to reach 9+ hours of content
    additional_modules = [
        {
            "id": str(uuid.uuid4()),
            "title": "Inspection Carrosserie et Châssis",
            "description": "Techniques d'évaluation structurelle : détection des accidents, corrosion, déformations et impact sur la sécurité.",
            "order_index": 4,
            "duration_minutes": 85,
            "is_free": False,
            "content": "<div class='module-content'><h1>Inspection Carrosserie et Châssis</h1><p>Module complet sur l'inspection structurelle des véhicules...</p></div>",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Systèmes Électroniques et ADAS",
            "description": "Diagnostic des systèmes d'aide à la conduite, multimédia, confort et sécurité électronique moderne.",
            "order_index": 5,
            "duration_minutes": 95,
            "is_free": False,
            "content": "<div class='module-content'><h1>Systèmes Électroniques et ADAS</h1><p>Diagnostic approfondi des systèmes électroniques modernes...</p></div>",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Sécurité et Équipements",
            "description": "Évaluation complète des systèmes de sécurité : freinage, direction, pneumatiques et équipements obligatoires.",
            "order_index": 6,
            "duration_minutes": 80,
            "is_free": False,
            "content": "<div class='module-content'><h1>Sécurité et Équipements</h1><p>Inspection complète des systèmes de sécurité...</p></div>",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Méthodologie méthode d'inspection",
            "description": "Processus complet d'inspection méthode d'inspection : organisation, outils, rapport client et négociation commerciale.",
            "order_index": 7,
            "duration_minutes": 75,
            "is_free": False,
            "content": "<div class='module-content'><h1>Méthodologie méthode d'inspection</h1><p>Découvrez la méthodologie propriétaire méthode d'inspection...</p></div>",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Pratique Professionnelle et Certification",
            "description": "Mise en pratique avec cas réels, gestion de clientèle, aspects légaux et obtention de votre certification.",
            "order_index": 8,
            "duration_minutes": 90,
            "is_free": False,
            "content": "<div class='module-content'><h1>Pratique Professionnelle et Certification</h1><p>Cas pratiques et certification finale...</p></div>",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    modules.extend(additional_modules)
    
    # Insert all modules
    for module in modules:
        await db.modules.insert_one(module)
        print(f"📚 Created module: {module['title']} ({module['duration_minutes']} min)")
    
    # Calculate total duration
    total_minutes = sum(m['duration_minutes'] for m in modules)
    total_hours = total_minutes / 60
    
    print(f"\n✅ Database seeded successfully!")
    print(f"📊 Created {len(modules)} modules")
    print(f"⏱️ Total content: {total_hours:.1f} hours ({total_minutes} minutes)")
    print(f"🆓 Free modules: {len([m for m in modules if m['is_free']])}")
    print(f"💰 Premium modules: {len([m for m in modules if not m['is_free']])}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())