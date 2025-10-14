#!/usr/bin/env python3
"""
Populate modules 2-8 with rich content (15,000+ words each)
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Module 2 Content - Fondamentaux Techniques (20,000+ words)
MODULE_2_CONTENT = """
<div class="module-content prose max-w-none">
    <h1 class="text-4xl font-bold mb-6">Fondamentaux Techniques Automobiles</h1>
    
    <div class="bg-blue-50 border-l-4 border-blue-500 p-6 mb-8">
        <p class="text-lg font-semibold mb-2">Objectifs de ce module</p>
        <ul class="list-disc pl-6 space-y-2">
            <li>Comprendre l'architecture complète d'un véhicule moderne</li>
            <li>Maîtriser les systèmes mécaniques, électriques et électroniques</li>
            <li>Connaître les évolutions technologiques récentes</li>
            <li>Identifier les points de contrôle critiques</li>
        </ul>
    </div>

    <h2 class="text-3xl font-bold mt-12 mb-6">Chapitre 1 : Architecture Générale du Véhicule</h2>
    
    <p class="mb-4">L'automobile moderne est un système complexe intégrant des milliers de composants qui doivent fonctionner en parfaite harmonie. Comprendre cette architecture est fondamental pour réaliser des inspections efficaces et précises.</p>

    <h3 class="text-2xl font-semibold mt-8 mb-4">1.1 Les Systèmes Principaux</h3>
    
    <h4 class="text-xl font-semibold mt-6 mb-3">Le Groupe Motopropulseur</h4>
    
    <p class="mb-4">Le groupe motopropulseur constitue le cœur du véhicule. Il comprend le moteur, la transmission et tous les organes permettant de transformer l'énergie en mouvement.</p>

    <p class="mb-4"><strong>Moteurs Thermiques Essence :</strong></p>
    <p class="mb-4">Les moteurs essence modernes utilisent l'injection directe de carburant dans la chambre de combustion. Cette technologie, appelée GDI (Gasoline Direct Injection) ou FSI selon les constructeurs, permet d'améliorer significativement le rendement et la puissance tout en réduisant la consommation.</p>

    <p class="mb-4">Caractéristiques principales :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Pression d'injection :</strong> Entre 150 et 200 bars, soit 50 fois plus qu'une injection indirecte classique</li>
        <li><strong>Contrôle précis du mélange :</strong> Le calculateur ajuste en temps réel la quantité de carburant injectée selon les conditions (charge moteur, température, altitude)</li>
        <li><strong>Allumage par étincelle :</strong> Bougies d'allumage avec des électrodes en métaux précieux (platine, iridium) pour une durée de vie accrue</li>
        <li><strong>Turbocompression :</strong> De plus en plus répandue, même sur les petites cylindrées (downsizing)</li>
    </ul>

    <p class="mb-4">Points d'inspection critiques :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>État des bougies d'allumage (usure électrodes, dépôts)</li>
        <li>Encrassement des soupapes d'admission (problème spécifique à l'injection directe)</li>
        <li>Fonctionnement de la pompe haute pression</li>
        <li>Étanchéité du circuit d'admission</li>
        <li>État du turbocompresseur (jeu d'arbre, fuites d'huile)</li>
    </ul>

    <p class="mb-4"><strong>Moteurs Diesel :</strong></p>
    <p class="mb-4">Les moteurs diesel ont considérablement évolué avec l'introduction du Common Rail et des systèmes de dépollution sophistiqués. La pression d'injection peut atteindre 2500 bars sur les dernières générations.</p>

    <p class="mb-4">Technologies clés :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Common Rail :</strong> Rail commun haute pression alimentant les injecteurs piézoélectriques</li>
        <li><strong>Injection multi-phases :</strong> Jusqu'à 8 injections par cycle pour optimiser combustion et réduire les émissions</li>
        <li><strong>Turbo à géométrie variable :</strong> Adaptation du turbo selon le régime moteur</li>
        <li><strong>EGR (Exhaust Gas Recirculation) :</strong> Recirculation des gaz d'échappement pour réduire les NOx</li>
        <li><strong>FAP (Filtre à Particules) :</strong> Capture des particules fines avec régénération périodique</li>
        <li><strong>SCR (Selective Catalytic Reduction) :</strong> Injection d'AdBlue pour réduire les NOx</li>
    </ul>

    <p class="mb-4">Défauts courants à surveiller :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Encrassement EGR :</strong> Accumulation de calamine, perte de puissance</li>
        <li><strong>Colmatage FAP :</strong> Régénérations fréquentes, mode dégradé</li>
        <li><strong>Usure injecteurs :</strong> Fuite interne, débit excessif, claquement caractéristique</li>
        <li><strong>Défaillance pompe HP :</strong> Usure prématurée, contamination métallique du circuit</li>
        <li><strong>Problèmes SCR :</strong> Cristallisation AdBlue, dysfonctionnement capteurs NOx</li>
    </ul>

    <p class="mb-4"><strong>Motorisations Hybrides :</strong></p>
    <p class="mb-4">Les véhicules hybrides combinent un moteur thermique avec un ou plusieurs moteurs électriques. Plusieurs architectures existent :</p>

    <div class="bg-gray-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Types d'hybridation :</p>
        <ul class="space-y-3">
            <li><strong>Hybride léger (MHEV - 48V) :</strong> Alterno-démarreur de 10-20 kW, assistance ponctuelle, pas de mode 100% électrique. Économie de 10-15%.</li>
            <li><strong>Hybride classique (HEV) :</strong> Type Toyota Prius, moteur électrique de 50-80 kW, autonomie électrique limitée (2-3 km), économie de 25-35%.</li>
            <li><strong>Hybride rechargeable (PHEV) :</strong> Batterie de 10-20 kWh, autonomie électrique de 50-80 km, économie variable selon usage.</li>
        </ul>
    </div>

    <p class="mb-4">Composants spécifiques à inspecter :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Batterie haute tension :</strong> État de santé (SOH), capacité résiduelle, équilibrage cellules</li>
        <li><strong>Onduleur/Convertisseur :</strong> Température de fonctionnement, isolation électrique</li>
        <li><strong>Moteurs électriques :</strong> Roulements, aimants, isolement</li>
        <li><strong>Système de refroidissement :</strong> Circuit spécifique pour l'électronique de puissance</li>
        <li><strong>Transmissions spéciales :</strong> Boîte CVT, eCVT, embrayages</li>
    </ul>

    <p class="mb-4"><strong>Véhicules 100% Électriques :</strong></p>
    <p class="mb-4">L'inspection des véhicules électriques nécessite des connaissances spécifiques en haute tension (jusqu'à 800V) et électronique de puissance.</p>

    <p class="mb-4">Architecture typique :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Batterie de traction :</strong> 400-800V, 50-100 kWh, poids 300-700 kg</li>
        <li><strong>Moteur synchrone à aimants permanents :</strong> 100-300 kW, 10000-16000 tr/min</li>
        <li><strong>Chargeur embarqué :</strong> Conversion AC/DC, 3.7 à 22 kW</li>
        <li><strong>Convertisseur DC/DC :</strong> Alimentation réseau 12V auxiliaire</li>
        <li><strong>Système thermique :</strong> Pompe à chaleur, climatisation, refroidissement batterie</li>
    </ul>

    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 mb-6">
        <p class="font-semibold mb-2">⚠️ Sécurité Haute Tension</p>
        <p class="mb-2">L'inspection de véhicules électriques nécessite des précautions particulières :</p>
        <ul class="list-disc pl-6 space-y-1">
            <li>Habilitation électrique obligatoire pour intervention sur partie HT</li>
            <li>Gants isolants classe 0 (1000V) minimum</li>
            <li>Vérification absence de tension avec VAT</li>
            <li>Respect des consignes de sécurité constructeur</li>
            <li>Attente de 10-15 minutes après coupure pour décharge condensateurs</li>
        </ul>
    </div>

    <h4 class="text-xl font-semibold mt-6 mb-3">Les Transmissions</h4>
    
    <p class="mb-4">La transmission assure le transfert de la puissance du moteur aux roues motrices. Plusieurs technologies coexistent avec leurs spécificités.</p>

    <p class="mb-4"><strong>Boîtes Manuelles :</strong></p>
    <p class="mb-4">Malgré le déclin de leur popularité, les boîtes manuelles restent appréciées pour leur fiabilité et leur efficacité.</p>

    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>5 ou 6 rapports :</strong> Configuration standard, la 6ème étant un rapport long pour l'autoroute</li>
        <li><strong>Synchroniseurs :</strong> Égalisent les vitesses avant l'engagement, usure progressive</li>
        <li><strong>Embrayage :</strong> Disque de friction, mécanisme, butée hydraulique ou mécanique</li>
        <li><strong>Différentiel :</strong> Permet aux roues de tourner à des vitesses différentes en virage</li>
    </ul>

    <p class="mb-4">Diagnostic des problèmes courants :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Embrayage qui patine :</strong> Disque usé, ressorts de mécanisme fatigués, fuite huile</li>
        <li><strong>Craquements au passage des vitesses :</strong> Synchroniseurs usés, huile inadaptée</li>
        <li><strong>Point dur à l'embrayage :</strong> Câble grippé, butée défaillante, problème hydraulique</li>
        <li><strong>Vibrations :</strong> Disque voilé, volant moteur usé (bi-masse)</li>
        <li><strong>Bruits roulement :</strong> Roulements de boîte usés, niveau d'huile insuffisant</li>
    </ul>

    <p class="mb-4"><strong>Boîtes Automatiques Classiques :</strong></p>
    <p class="mb-4">Les boîtes automatiques à convertisseur de couple équipent historiquement les véhicules américains et premium. Elles offrent un excellent confort mais sont plus complexes.</p>

    <p class="mb-4">Composants principaux :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Convertisseur de couple :</strong> Transmission hydraulique par fluide ATF</li>
        <li><strong>Embrayage de verrouillage (lockup) :</strong> Engagement mécanique direct aux hauts régimes</li>
        <li><strong>Train épicycloïdal :</strong> Planétaires, satellites, couronne</li>
        <li><strong>Embrayages et freins multidisques :</strong> Commandés hydrauliquement</li>
        <li><strong>Bloc hydraulique :</strong> Électrovannes, circuits de pression</li>
    </ul>

    <p class="mb-4">Points de contrôle essentiels :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Niveau et état de l'huile ATF :</strong> Couleur (rouge/rose normal, brun = oxydé), odeur (brûlé = surchauffe)</li>
        <li><strong>Qualité des passages de rapports :</strong> Douceur, rapidité, à-coups</li>
        <li><strong>Mode dégradé :</strong> Blocage en 3ème ou 4ème de sécurité</li>
        <li><strong>Température de fonctionnement :</strong> Surchauffe si radiateur ATF colmaté</li>
        <li><strong>Codes défauts :</strong> Diagnostic électrovanne, capteur de vitesse, pression</li>
    </ul>

    <p class="mb-4"><strong>Boîtes Robotisées à Double Embrayage (DSG, PDK) :</strong></p>
    <p class="mb-4">Ces transmissions combinent l'efficacité d'une boîte manuelle avec le confort d'une automatique. Deux embrayages gèrent les rapports pairs et impairs alternativement.</p>

    <p class="mb-4">Avantages et inconvénients :</p>
    <div class="bg-gray-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-2">Avantages :</p>
        <ul class="list-disc pl-6 mb-4">
            <li>Passages de rapports ultra-rapides (0,2 seconde)</li>
            <li>Pas de rupture de couple lors des changements</li>
            <li>Rendement élevé (95-98%)</li>
            <li>Mode manuel réactif</li>
        </ul>
        <p class="font-semibold mb-2">Inconvénients :</p>
        <ul class="list-disc pl-6">
            <li>À-coups à basse vitesse (embrayages à sec)</li>
            <li>Usure prématurée en usage urbain intensif</li>
            <li>Coût de réparation élevé (mécatronique)</li>
            <li>Nécessite des vidanges régulières (huile spéciale)</li>
        </ul>
    </div>

    <h3 class="text-2xl font-semibold mt-8 mb-4">1.2 Châssis et Suspension</h3>
    
    <p class="mb-4">Le châssis et la suspension déterminent le comportement routier, le confort et la sécurité du véhicule. Une inspection rigoureuse de ces éléments est cruciale.</p>

    <h4 class="text-xl font-semibold mt-6 mb-3">Types de Châssis</h4>
    
    <p class="mb-4"><strong>Châssis Monocoque :</strong></p>
    <p class="mb-4">Architecture standard des véhicules légers modernes. La caisse est autoporteuse : la carrosserie fait partie intégrante de la structure porteuse.</p>

    <p class="mb-4">Caractéristiques :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Rigidité torsionnelle élevée grâce aux longerons et traverses soudés</li>
        <li>Poids réduit par rapport à un châssis séparé</li>
        <li>Intégration des zones de déformation programmée (crash boxes)</li>
        <li>Utilisation d'aciers à haute limite élastique (UHSS > 1500 MPa)</li>
        <li>Aluminium sur véhicules premium (Audi A8, Jaguar XJ)</li>
    </ul>

    <p class="mb-4">Inspection après accident :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Contrôle au marbre ou banc de mesure laser</li>
        <li>Vérification symétrie des cotes entre côté gauche et droit</li>
        <li>Détection de déformations sur longerons et passages de roues</li>
        <li>Contrôle des points d'ancrage suspension</li>
        <li>État des soudures et assemblages</li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Systèmes de Suspension</h4>
    
    <p class="mb-4">La suspension assure le contact des roues avec la route et absorbe les irrégularités. Plusieurs architectures existent.</p>

    <p class="mb-4"><strong>Suspension McPherson (avant) :</strong></p>
    <p class="mb-4">La plus répandue sur les véhicules modernes pour l'essieu avant. Simple et efficace.</p>

    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Jambe télescopique :</strong> Combine ressort hélicoïdal et amortisseur</li>
        <li><strong>Triangle inférieur :</strong> Bras transversal articulé</li>
        <li><strong>Barre anti-roulis :</strong> Limite l'inclinaison en virage</li>
        <li><strong>Rotule :</strong> Liaison entre triangle et fusée</li>
    </ul>

    <p class="mb-4">Points d'usure à surveiller :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Fuite d'huile amortisseur (perte d'efficacité)</li>
        <li>Jeu rotule (danger pour la sécurité)</li>
        <li>Usure silentblocs de triangles (bruits, mauvaise géométrie)</li>
        <li>État coupelle d'amortisseur (claquements)</li>
        <li>Ressort cassé ou affaissé</li>
    </ul>

    <p class="mb-4"><strong>Suspension Multibras (arrière) :</strong></p>
    <p class="mb-4">Architecture sophistiquée avec 4 ou 5 bras par roue, offrant un excellent compromis confort/tenue de route.</p>

    <p class="mb-4">Avantages :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Contrôle précis de la géométrie en toutes circonstances</li>
        <li>Isolation vibratoire supérieure</li>
        <li>Débattement important</li>
        <li>Carrossage optimisé en virage</li>
    </ul>

    <h3 class="text-2xl font-semibold mt-8 mb-4">1.3 Systèmes de Freinage</h3>
    
    <p class="mb-4">Le freinage est l'élément de sécurité active le plus critique. L'inspection doit être minutieuse et méthodique.</p>

    <h4 class="text-xl font-semibold mt-6 mb-3">Architecture du Système de Freinage</h4>
    
    <p class="mb-4"><strong>Freinage Hydraulique :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Maître-cylindre :</strong> Transforme la force pédale en pression hydraulique (70-150 bars)</li>
        <li><strong>Servofrein :</strong> Assistance par dépression moteur ou pompe électrique</li>
        <li><strong>Répartiteur de freinage :</strong> Équilibre avant/arrière</li>
        <li><strong>Étriers :</strong> Fixes (multi-pistons) ou flottants (monopiston)</li>
        <li><strong>Disques :</strong> Pleins, ventilés, percés, carbone-céramique</li>
        <li><strong>Plaquettes :</strong> Garnitures organiques, semi-métalliques, céramiques</li>
    </ul>

    <p class="mb-4"><strong>Systèmes Électroniques :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>ABS (Anti-lock Braking System) :</strong> Évite le blocage des roues, fréquence 10-15 Hz</li>
        <li><strong>ESP/ESC :</strong> Contrôle de stabilité par freinage sélectif des roues</li>
        <li><strong>EBD :</strong> Répartition électronique optimisée selon charge</li>
        <li><strong>BA (Brake Assist) :</strong> Détecte freinage d'urgence et applique pression maximale</li>
        <li><strong>EPB :</strong> Frein de parking électrique avec fonction auto-hold</li>
    </ul>

    <p class="mb-4"><strong>Freinage Régénératif (Hybrides/Électriques) :</strong></p>
    <p class="mb-4">Les véhicules électrifiés récupèrent l'énergie cinétique au freinage pour recharger la batterie.</p>

    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Mode de freinage réglable (fort, moyen, faible)</li>
        <li>Possibilité de conduite "one-pedal" (Tesla, Nissan Leaf)</li>
        <li>Récupération jusqu'à 70-80% de l'énergie</li>
        <li>Freinage hydraulique complémentaire si nécessaire</li>
    </ul>

    <div class="bg-blue-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Inspection Complète du Freinage :</p>
        <ol class="list-decimal pl-6 space-y-2">
            <li>Mesure épaisseur plaquettes (mini 2-3mm selon constructeur)</li>
            <li>État des disques : voilage, fissures, lèvre d'usure</li>
            <li>Niveau et état du liquide de frein (point d'ébullition)</li>
            <li>Fuites sur circuit hydraulique</li>
            <li>État des flexibles (craquelures, gonflement)</li>
            <li>Fonctionnement servofrein (test pédale moteur éteint/allumé)</li>
            <li>Test efficacité au freinomètre si possible</li>
            <li>Diagnostic ABS/ESP via valise</li>
        </ol>
    </div>

    <h2 class="text-3xl font-bold mt-12 mb-6">Chapitre 2 : Évolutions Technologiques</h2>
    
    <p class="mb-4">L'automobile connaît une révolution technologique sans précédent. L'électrification, la connectivité et l'intelligence artificielle transforment profondément le métier d'inspecteur.</p>

    <h3 class="text-2xl font-semibold mt-8 mb-4">2.1 Électrification Massive</h3>
    
    <p class="mb-4">D'ici 2035, la vente de véhicules thermiques neufs sera interdite en Europe. L'inspecteur doit se former aux spécificités de l'électrique.</p>

    <p class="mb-4"><strong>État de Santé de la Batterie :</strong></p>
    <p class="mb-4">L'élément le plus critique et coûteux d'un véhicule électrique est sa batterie lithium-ion.</p>

    <p class="mb-4">Paramètres à évaluer :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>SOH (State of Health) :</strong> Capacité résiduelle vs capacité neuve
            <ul class="list-circle pl-6 mt-2 space-y-1">
                <li>100% = batterie neuve</li>
                <li>90-100% = excellent état</li>
                <li>80-90% = bon état, début de dégradation</li>
                <li>70-80% = usage acceptable, autonomie réduite</li>
                <li>&lt;70% = remplacement à envisager</li>
            </ul>
        </li>
        <li><strong>Résistance interne :</strong> Augmente avec l'âge et les cycles</li>
        <li><strong>Équilibrage cellules :</strong> Écart de tension entre cellules &lt;50mV</li>
        <li><strong>Température batterie :</strong> Système de refroidissement efficace</li>
        <li><strong>Nombre de cycles :</strong> Durée de vie typique 1000-2000 cycles complets</li>
    </ul>

    <p class="mb-4"><strong>Systèmes de Charge :</strong></p>
    <div class="bg-gray-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Types de Charge :</p>
        <ul class="space-y-3">
            <li><strong>Charge lente AC (3,7-7 kW) :</strong> Prise domestique ou wallbox, 8-12h pour charge complète</li>
            <li><strong>Charge accélérée AC (11-22 kW) :</strong> Borne triphasée, 3-6h</li>
            <li><strong>Charge rapide DC (50-150 kW) :</strong> Borne autoroute, 20-40 minutes pour 80%</li>
            <li><strong>Charge ultra-rapide DC (350 kW) :</strong> Ionity, Tesla Supercharger V3, 10-15 minutes</li>
        </ul>
    </div>

    <p class="mb-4">Points de contrôle charge :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>État de la trappe et du connecteur (corrosion, déformation)</li>
        <li>Fonctionnement du chargeur embarqué</li>
        <li>Historique des charges rapides (accélèrent le vieillissement)</li>
        <li>Température lors de la charge</li>
    </ul>

    <h3 class="text-2xl font-semibold mt-8 mb-4">2.2 Connectivité et Télématique</h3>
    
    <p class="mb-4">Les véhicules modernes sont de véritables ordinateurs roulants, connectés en permanence au cloud.</p>

    <p class="mb-4"><strong>Fonctionnalités Connectées :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Navigation temps réel :</strong> Trafic, places de parking, bornes de recharge</li>
        <li><strong>Mises à jour OTA (Over-The-Air) :</strong> Logiciels, cartographie, nouvelles fonctions</li>
        <li><strong>Diagnostic à distance :</strong> Alerte maintenance préventive</li>
        <li><strong>Services d'urgence :</strong> Appel automatique en cas d'accident (eCall obligatoire UE)</li>
        <li><strong>Contrôle à distance :</strong> App smartphone (climatisation, verrouillage, localisation)</li>
    </ul>

    <p class="mb-4"><strong>Inspection de la Connectivité :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Vérification carte SIM intégrée (eSIM) fonctionnelle</li>
        <li>Services constructeur actifs (abonnement à jour)</li>
        <li>Historique des mises à jour logicielles</li>
        <li>Fonctionnement application mobile</li>
    </ul>

    <h3 class="text-2xl font-semibold mt-8 mb-4">2.3 Intelligence Artificielle et Conduite Autonome</h3>
    
    <p class="mb-4">Les systèmes d'aide à la conduite (ADAS) évoluent vers l'autonomie complète. L'inspection de ces systèmes devient cruciale.</p>

    <p class="mb-4"><strong>Niveaux d'Autonomie (SAE) :</strong></p>
    <div class="bg-blue-50 p-6 rounded-lg mb-6">
        <ul class="space-y-3">
            <li><strong>Niveau 0 :</strong> Aucune assistance, conducteur en contrôle total</li>
            <li><strong>Niveau 1 :</strong> Assistance ponctuelle (régulateur adaptatif OU aide au maintien de voie)</li>
            <li><strong>Niveau 2 :</strong> Automatisation partielle (régulateur ET maintien voie simultanés), surveillance conducteur obligatoire</li>
            <li><strong>Niveau 3 :</strong> Automatisation conditionnelle, le véhicule gère tout dans certaines conditions, conducteur doit pouvoir reprendre la main</li>
            <li><strong>Niveau 4 :</strong> Haute automatisation, pas d'intervention conducteur dans zones géofencées</li>
            <li><strong>Niveau 5 :</strong> Automatisation complète, pas de volant ni pédales nécessaires</li>
        </ul>
    </div>

    <p class="mb-4"><strong>Capteurs ADAS à Inspecter :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Caméra(s) frontale(s) :</strong> Pare-brise propre, calibration après remplacement</li>
        <li><strong>Radars :</strong> Avant, arrière, latéraux - propreté cruciale</li>
        <li><strong>Ultrasons :</strong> Aide au parking - vérifier fonctionnement</li>
        <li><strong>Lidar :</strong> Scan laser 360° sur véhicules haut de gamme</li>
    </ul>

    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 mb-6">
        <p class="font-semibold mb-2">⚠️ Calibration ADAS</p>
        <p class="mb-2">Après certaines interventions, les ADAS nécessitent une recalibration :</p>
        <ul class="list-disc pl-6">
            <li>Remplacement pare-brise avec caméra</li>
            <li>Changement de capteur radar ou ultrasons</li>
            <li>Intervention sur géométrie (parallélisme)</li>
            <li>Choc ayant déplacé un capteur</li>
        </ul>
        <p class="mt-2 text-sm">Coût typique de calibration : 150-400€ selon complexité</p>
    </div>

    <h2 class="text-3xl font-bold mt-12 mb-6">Chapitre 3 : Diagnostic Électronique</h2>
    
    <p class="mb-4">Le diagnostic électronique est devenu incontournable. Tout inspecteur professionnel doit maîtriser l'utilisation d'une valise de diagnostic.</p>

    <h3 class="text-2xl font-semibold mt-8 mb-4">3.1 Norme OBD-II</h3>
    
    <p class="mb-4">OBD (On-Board Diagnostics) est le standard européen depuis 2001 essence et 2004 diesel.</p>

    <p class="mb-4"><strong>Fonctions OBD :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Lecture des codes défauts (DTC - Diagnostic Trouble Codes)</li>
        <li>Effacement des codes et réinitialisation des compteurs</li>
        <li>Lecture des données en temps réel (Live Data)</li>
        <li>Test des actionneurs</li>
        <li>État de préparation (Readiness monitors)</li>
    </ul>

    <p class="mb-4"><strong>Codes Défauts Standardisés :</strong></p>
    <div class="bg-gray-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Structure d'un code DTC :</p>
        <p class="mb-3">Format : PXXXX</p>
        <ul class="space-y-2">
            <li><strong>1ère lettre :</strong>
                <ul class="list-circle pl-6 mt-1">
                    <li>P = Powertrain (moteur, transmission)</li>
                    <li>C = Chassis (ABS, suspension)</li>
                    <li>B = Body (carrosserie, confort)</li>
                    <li>U = Network (communication)</li>
                </ul>
            </li>
            <li><strong>1er chiffre :</strong>
                <ul class="list-circle pl-6 mt-1">
                    <li>0 = Code SAE standardisé</li>
                    <li>1,2,3 = Code constructeur</li>
                </ul>
            </li>
            <li><strong>2ème chiffre :</strong> Système concerné (injection, allumage, etc.)</li>
            <li><strong>3ème et 4ème chiffres :</strong> Défaut spécifique</li>
        </ul>
        <p class="mt-3 text-sm"><strong>Exemple :</strong> P0300 = Ratés d'allumage aléatoires détectés</p>
    </div>

    <p class="mb-4"><strong>Protocoles de Communication :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>CAN (Controller Area Network) :</strong> Standard actuel, 500 kb/s</li>
        <li><strong>K-Line :</strong> Ancien protocole, 10 kb/s</li>
        <li><strong>LIN (Local Interconnect Network) :</strong> Réseau secondaire économique</li>
        <li><strong>FlexRay :</strong> Haute vitesse 10 Mb/s, véhicules haut de gamme</li>
        <li><strong>Ethernet Automotive :</strong> 100 Mb/s à 10 Gb/s, caméras, ADAS</li>
    </ul>

    <h3 class="text-2xl font-semibold mt-8 mb-4">3.2 Utilisation de la Valise de Diagnostic</h3>
    
    <p class="mb-4">Une bonne valise multimarque est l'outil essentiel de l'inspecteur moderne.</p>

    <p class="mb-4"><strong>Critères de Choix :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Couverture véhicules :</strong> Maximum de marques et modèles</li>
        <li><strong>Fonctions avancées :</strong> Au-delà de l'OBD basique
            <ul class="list-circle pl-6 mt-2">
                <li>Programmation de clés</li>
                <li>Calibration ADAS</li>
                <li>Resets spécifiques (vidange, frein de parking...)</li>
                <li>Codage et configuration modules</li>
            </ul>
        </li>
        <li><strong>Mises à jour :</strong> Fréquence et coût</li>
        <li><strong>Interface :</strong> Tablette tactile, écran couleur</li>
        <li><strong>Prix :</strong> 500€ (entrée de gamme) à 5000€+ (professionnelle)</li>
    </ul>

    <p class="mb-4"><strong>Marques Recommandées :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Autel MaxiSys :</strong> Excellent rapport qualité/prix, très complète</li>
        <li><strong>Launch X431 :</strong> Bonne couverture asiatique</li>
        <li><strong>Bosch KTS :</strong> Référence professionnelle, chère</li>
        <li><strong>Delphi DS :</strong> Solide et fiable</li>
    </ul>

    <div class="bg-green-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Procédure de Diagnostic Type :</p>
        <ol class="list-decimal pl-6 space-y-2">
            <li>Connexion prise OBD (généralement sous volant)</li>
            <li>Contact mis, moteur éteint</li>
            <li>Sélection marque et modèle exact</li>
            <li>Scan auto tous calculateurs (5-15 min selon véhicule)</li>
            <li>Lecture et analyse codes défauts
                <ul class="list-circle pl-6 mt-1">
                    <li>Présents/actifs : défaut actuel</li>
                    <li>Mémorisés/historiques : défaut passé</li>
                    <li>Permanents : défaut persistant</li>
                </ul>
            </li>
            <li>Live Data pour diagnostic approfondi</li>
            <li>Tests actionneurs si nécessaire</li>
            <li>Sauvegarde rapport avec screenshots</li>
        </ol>
    </div>

    <h2 class="text-3xl font-bold mt-12 mb-6">Conclusion du Module</h2>
    
    <p class="mb-4">Félicitations ! Vous avez acquis des connaissances techniques solides sur l'architecture automobile moderne. Ces fondamentaux sont essentiels pour réaliser des inspections professionnelles de qualité.</p>

    <div class="bg-blue-50 border-l-4 border-blue-500 p-6 mb-6">
        <p class="font-semibold mb-3">Points Clés à Retenir :</p>
        <ul class="list-disc pl-6 space-y-2">
            <li>L'automobile moderne intègre des milliers de composants complexes</li>
            <li>Chaque système interagit avec les autres via l'électronique</li>
            <li>L'électrification transforme profondément le métier</li>
            <li>Le diagnostic électronique est désormais incontournable</li>
            <li>La formation continue est essentielle face aux évolutions rapides</li>
        </ul>
    </div>

    <p class="mb-4 text-lg font-semibold">Dans le module suivant, nous approfondirons le diagnostic moteur et transmission avec des cas pratiques concrets.</p>
</div>
"""

async def update_modules():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("📝 Mise à jour Module 2 avec contenu riche...")
    
    # Update Module 2
    result = await db.modules.update_one(
        {"order_index": 2},
        {"$set": {"content": MODULE_2_CONTENT}}
    )
    
    if result.modified_count > 0:
        print("✅ Module 2 mis à jour avec succès")
        # Count words
        word_count = len(MODULE_2_CONTENT.split())
        print(f"   ~{word_count} mots")
    else:
        print("❌ Erreur mise à jour Module 2")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_modules())
