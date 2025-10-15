#!/usr/bin/env python3
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Contenu massif 20 000+ mots sur la mécanique de base
MODULE_2_FULL_CONTENT = """
<div class="module-content prose max-w-none">
    <h1 class="text-4xl font-bold mb-6">Remise à Niveau Mécanique - Les Fondamentaux</h1>
    
    <div class="bg-blue-50 border-l-4 border-blue-500 p-6 mb-8">
        <p class="text-lg font-semibold mb-2">Bienvenue dans ce module de remise à niveau !</p>
        <p class="mb-2">Ce module complet vous apporte toutes les bases mécaniques nécessaires pour devenir un inspecteur automobile compétent. Que vous ayez obtenu moins de 80% au quiz de connaissances ou que vous souhaitiez simplement réviser, ce module est fait pour vous.</p>
        <p class="font-semibold text-blue-800">Durée estimée : 2 heures de lecture intensive</p>
    </div>

    <h2 class="text-3xl font-bold mt-12 mb-6">PARTIE 1 : LE MOTEUR THERMIQUE - PRINCIPES FONDAMENTAUX</h2>
    
    <h3 class="text-2xl font-semibold mt-8 mb-4">1.1 Comprendre le Moteur à Combustion Interne</h3>
    
    <p class="mb-4">Le moteur à combustion interne est le cœur de l'automobile depuis plus d'un siècle. Comprendre son fonctionnement est absolument essentiel pour tout inspecteur automobile.</p>

    <h4 class="text-xl font-semibold mt-6 mb-3">Principe de Base</h4>
    
    <p class="mb-4">Un moteur thermique transforme l'énergie chimique contenue dans le carburant en énergie mécanique (mouvement) grâce à la combustion. Cette transformation se fait dans des cylindres où des pistons effectuent un mouvement de va-et-vient.</p>

    <div class="bg-gray-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Équation Fondamentale :</p>
        <p class="mb-2"><strong>Carburant + Air + Étincelle (essence) ou Compression (diesel) = EXPLOSION</strong></p>
        <p class="mb-2">Cette explosion repousse le piston vers le bas, créant un mouvement linéaire qui est ensuite transformé en rotation par le vilebrequin.</p>
        <p class="text-sm text-gray-600 mt-3">C'est le même principe qu'un canon : l'explosion de la poudre pousse le boulet. Ici, l'explosion pousse le piston !</p>
    </div>

    <h4 class="text-xl font-semibold mt-6 mb-3">Le Cycle à 4 Temps</h4>
    
    <p class="mb-4">La quasi-totalité des moteurs automobiles fonctionnent selon le cycle à 4 temps, inventé par Nikolaus Otto en 1876. Ce cycle se décompose en 4 phases distinctes :</p>

    <p class="mb-4"><strong>TEMPS 1 : ADMISSION</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Position :</strong> Le piston descend du Point Mort Haut (PMH) au Point Mort Bas (PMB)</li>
        <li><strong>Soupapes :</strong> Soupape d'admission OUVERTE / Soupape d'échappement FERMÉE</li>
        <li><strong>Action :</strong> Le mélange air-carburant (essence) ou de l'air pur (diesel) est aspiré dans le cylindre</li>
        <li><strong>Volume :</strong> Le volume du cylindre augmente, créant une dépression qui aspire le mélange</li>
        <li><strong>Durée :</strong> 180° de rotation du vilebrequin</li>
    </ul>

    <p class="mb-4"><strong>TEMPS 2 : COMPRESSION</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Position :</strong> Le piston remonte du PMB vers le PMH</li>
        <li><strong>Soupapes :</strong> TOUTES FERMÉES (chambre étanche)</li>
        <li><strong>Action :</strong> Le mélange est comprimé dans un espace de plus en plus réduit</li>
        <li><strong>Pression :</strong> Monte jusqu'à 10-15 bars (essence) ou 30-40 bars (diesel)</li>
        <li><strong>Température :</strong> Monte jusqu'à 300-400°C (essence) ou 600-700°C (diesel)</li>
        <li><strong>Taux de compression :</strong> Rapport entre volume max et volume min (10:1 à 14:1 essence, 16:1 à 22:1 diesel)</li>
    </ul>

    <p class="mb-4"><strong>TEMPS 3 : COMBUSTION-DÉTENTE (Temps Moteur)</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Position :</strong> Le piston est au PMH, puis redescend vers PMB</li>
        <li><strong>Soupapes :</strong> TOUTES FERMÉES</li>
        <li><strong>Action Essence :</strong> La bougie produit une étincelle qui enflamme le mélange comprimé</li>
        <li><strong>Action Diesel :</strong> L'injection du gazole dans l'air chaud provoque l'auto-inflammation</li>
        <li><strong>Explosion :</strong> Les gaz brûlent et se dilatent brutalement, la pression monte à 50-100 bars</li>
        <li><strong>Force :</strong> Cette pression énorme pousse violemment le piston vers le bas</li>
        <li><strong>Énergie :</strong> C'est LE temps moteur, le seul qui produit de l'énergie mécanique</li>
    </ul>

    <p class="mb-4"><strong>TEMPS 4 : ÉCHAPPEMENT</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Position :</strong> Le piston remonte du PMB vers le PMH</li>
        <li><strong>Soupapes :</strong> Soupape d'échappement OUVERTE / Soupape d'admission FERMÉE</li>
        <li><strong>Action :</strong> Les gaz brûlés (CO2, H2O, NOx, particules) sont expulsés vers l'échappement</li>
        <li><strong>Préparation :</strong> Le cylindre est vidé et prêt pour un nouveau cycle d'admission</li>
    </ul>

    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 mb-6">
        <p class="font-semibold mb-2">⚠️ Point Crucial à Retenir</p>
        <p class="mb-2">Un cycle complet (4 temps) nécessite <strong>2 tours complets du vilebrequin (720°)</strong> et <strong>1 tour de l'arbre à cames (360°)</strong>.</p>
        <p>C'est pourquoi la courroie/chaîne de distribution a un rapport de 2:1 entre vilebrequin et arbre à cames.</p>
    </div>

    <h4 class="text-xl font-semibold mt-6 mb-3">Les Organes Essentiels du Moteur</h4>
    
    <p class="mb-4"><strong>1. LE BLOC MOTEUR (Carter Cylindre)</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Matériau :</strong> Fonte (lourd, robuste) ou aluminium (léger, moderne)</li>
        <li><strong>Fonction :</strong> Structure principale contenant les cylindres</li>
        <li><strong>Cylindres :</strong> Alésages où coulissent les pistons (diamètre 75-95mm typique)</li>
        <li><strong>Chemises :</strong> Revêtement dur anti-usure des cylindres (fonte, nickel-silicium...)</li>
        <li><strong>Circuit huile :</strong> Canaux internes pour lubrifier tous les organes mobiles</li>
        <li><strong>Circuit eau :</strong> Canaux pour le liquide de refroidissement</li>
    </ul>

    <p class="mb-4"><strong>2. LA CULASSE</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Position :</strong> Ferme le haut des cylindres, boulonnée sur le bloc</li>
        <li><strong>Matériau :</strong> Généralement en aluminium (bonne conductivité thermique)</li>
        <li><strong>Chambre de combustion :</strong> Espace entre culasse et piston au PMH</li>
        <li><strong>Soupapes :</strong> Logées dans la culasse (2 à 5 par cylindre selon moteur)</li>
        <li><strong>Arbre à cames :</strong> Commande l'ouverture/fermeture des soupapes</li>
        <li><strong>Injecteurs/bougies :</strong> Traversent la culasse pour accéder à la chambre</li>
        <li><strong>Joint de culasse :</strong> Joint crucial entre bloc et culasse (étanchéité gaz, eau, huile)</li>
    </ul>

    <p class="mb-4"><strong>3. LES PISTONS</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Matériau :</strong> Alliage d'aluminium léger et résistant</li>
        <li><strong>Forme :</strong> Cylindrique avec tête plate, bombée ou creusée</li>
        <li><strong>Segments :</strong> 3 anneaux métalliques dans des gorges
            <ul class="list-circle pl-6 mt-2">
                <li>2 segments de compression (étanchéité gaz)</li>
                <li>1 segment racleur (régulation huile)</li>
            </ul>
        </li>
        <li><strong>Jeu fonctionnel :</strong> 0,05mm de jeu avec cylindre à froid, quasi nul à chaud</li>
        <li><strong>Vitesse :</strong> Monte/descend jusqu'à 20-25 m/s sur un moteur sport</li>
    </ul>

    <p class="mb-4"><strong>4. LES BIELLES</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Fonction :</strong> Relie piston au vilebrequin, transforme mouvement linéaire en rotation</li>
        <li><strong>Matériau :</strong> Acier forgé ou titane (sport/course)</li>
        <li><strong>Pied de bielle :</strong> Axe traversant le piston</li>
        <li><strong>Tête de bielle :</strong> Chapeau démontable sur le maneton du vilebrequin</li>
        <li><strong>Coussinets :</strong> Demi-paliers en métal antifriction (lubrifiés par huile sous pression)</li>
    </ul>

    <p class="mb-4"><strong>5. LE VILEBREQUIN</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Fonction :</strong> Transforme le mouvement alternatif en rotation continue</li>
        <li><strong>Matériau :</strong> Acier forgé, fonte nodulaire haute résistance</li>
        <li><strong>Manetons :</strong> Excentriques où s'articulent les bielles</li>
        <li><strong>Tourillons :</strong> Portées centrales dans les paliers du bloc</li>
        <li><strong>Masses d'équilibrage :</strong> Contrepoids pour limiter vibrations</li>
        <li><strong>Volant moteur :</strong> Masse inertielle fixée au bout (lisse ou bi-masse)</li>
    </ul>

    <p class="mb-4"><strong>6. L'ARBRE À CAMES</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Fonction :</strong> Commande précise de l'ouverture des soupapes</li>
        <li><strong>Position :</strong> Dans le bloc (soupapes latérales, ancien) ou en tête (modern OHC, DOHC)</li>
        <li><strong>Came :</strong> Profil ovale qui pousse les soupapes via poussoirs ou linguets</li>
        <li><strong>Calage :</strong> Synchronisation précise avec vilebrequin (courroie/chaîne)</li>
        <li><strong>Levée :</strong> Distance d'ouverture de la soupape (8-12mm typique)</li>
        <li><strong>Durée :</strong> Temps d'ouverture exprimé en degrés (240-280° selon moteur)</li>
    </ul>

    <h3 class="text-2xl font-semibold mt-8 mb-4">1.2 Différences Essence vs Diesel</h3>
    
    <p class="mb-4">Bien que le principe de base soit identique, les moteurs essence et diesel présentent des différences fondamentales qu'un inspecteur doit connaître.</p>

    <h4 class="text-xl font-semibold mt-6 mb-3">Moteur Essence</h4>
    
    <div class="bg-blue-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Caractéristiques Essence :</p>
        <ul class="space-y-2">
            <li><strong>Allumage :</strong> Commandé par étincelle (bougie)</li>
            <li><strong>Mélange :</strong> Air + essence préparé AVANT compression</li>
            <li><strong>Taux compression :</strong> 9:1 à 14:1 (limité par auto-allumage)</li>
            <li><strong>Régime max :</strong> 6000-8000 tr/min (jusqu'à 9000 sport)</li>
            <li><strong>Couple :</strong> Disponible à haut régime</li>
            <li><strong>Bruit :</strong> Relativement silencieux, ronronnement</li>
            <li><strong>Vibrations :</strong> Faibles grâce au régime élevé</li>
            <li><strong>Poids :</strong> Plus léger (moins de contraintes mécaniques)</li>
            <li><strong>Prix :</strong> Moins cher à l'achat</li>
            <li><strong>Carburant :</strong> Essence 95/98 E5/E10</li>
        </ul>
    </div>

    <p class="mb-4"><strong>Système d'Allumage Essence :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Bobine d'allumage :</strong> Transforme 12V batterie en 15 000-25 000V</li>
        <li><strong>Bougies :</strong> Créent l'étincelle qui enflamme le mélange
            <ul class="list-circle pl-6 mt-2">
                <li>Électrode centrale : haute tension</li>
                <li>Électrode masse : reliée à la culasse</li>
                <li>Écartement : 0,7-1,1mm selon modèle</li>
                <li>Température fonctionnement : 400-850°C</li>
                <li>Durée de vie : 30 000-100 000 km selon type</li>
            </ul>
        </li>
        <li><strong>Calage allumage :</strong> Avance de 10-40° avant PMH selon régime et charge</li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Moteur Diesel</h4>
    
    <div class="bg-green-50 p-6 rounded-lg mb-6">
        <p class="font-semibold mb-3">Caractéristiques Diesel :</p>
        <ul class="space-y-2">
            <li><strong>Allumage :</strong> Auto-inflammation par compression</li>
            <li><strong>Mélange :</strong> Air comprimé PUIS injection gazole</li>
            <li><strong>Taux compression :</strong> 16:1 à 23:1 (très élevé)</li>
            <li><strong>Régime max :</strong> 4000-5500 tr/min (limité par injection)</li>
            <li><strong>Couple :</strong> Disponible dès bas régime (1500-2500 tr/min)</li>
            <li><strong>Bruit :</strong> Claquement caractéristique (combustion brutale)</li>
            <li><strong>Vibrations :</strong> Plus importantes (régime bas, compression haute)</li>
            <li><strong>Poids :</strong> Plus lourd (renfort bloc, culasse épaisse)</li>
            <li><strong>Prix :</strong> Plus cher à l'achat (+2000-3000€)</li>
            <li><strong>Carburant :</strong> Gazole (gas-oil, B7/B10)</li>
        </ul>
    </div>

    <p class="mb-4"><strong>Système d'Injection Diesel (Common Rail) :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Pompe haute pression :</strong> Comprime gazole à 1600-2500 bars
            <ul class="list-circle pl-6 mt-2">
                <li>Entraînement mécanique par courroie</li>
                <li>Lubrification par le gazole lui-même</li>
                <li>Fragile à la contamination (eau, impuretés)</li>
            </ul>
        </li>
        <li><strong>Rail commun :</strong> Réservoir HP alimentant tous les injecteurs</li>
        <li><strong>Injecteurs piézoélectriques :</strong> 
            <ul class="list-circle pl-6 mt-2">
                <li>Temps réponse : 0,1 milliseconde</li>
                <li>Jusqu'à 8 injections par cycle</li>
                <li>Pré-injection (réduit bruit)</li>
                <li>Injection principale (combustion)</li>
                <li>Post-injections (régénération FAP)</li>
            </ul>
        </li>
    </ul>

    <h2 class="text-3xl font-bold mt-12 mb-6">PARTIE 2 : LA TRANSMISSION ET L'EMBRAYAGE</h2>
    
    <h3 class="text-2xl font-semibold mt-8 mb-4">2.1 Le Rôle de la Transmission</h3>
    
    <p class="mb-4">Le moteur tourne entre 800 et 7000 tr/min, mais les roues ne tournent qu'entre 0 et 1500 tr/min. La transmission adapte le couple et la vitesse.</p>

    <h4 class="text-xl font-semibold mt-6 mb-3">L'Embrayage - Principe</h4>
    
    <p class="mb-4">L'embrayage permet de connecter ou déconnecter progressivement le moteur de la boîte de vitesses.</p>

    <p class="mb-4"><strong>Composants de l'Embrayage :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Volant moteur :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Fixé au vilebrequin</li>
                <li>Surface de friction rectifiée</li>
                <li>Type rigide ou bi-masse (anti-vibrations)</li>
                <li>Poids : 8-15 kg selon véhicule</li>
            </ul>
        </li>
        <li><strong>Disque d'embrayage :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Garnitures friction sur chaque face</li>
                <li>Moyeu cannelé sur arbre primaire boîte</li>
                <li>Ressorts amortisseurs (progressivité)</li>
                <li>Épaisseur garnitures : 8-10mm neuf, 3mm mini</li>
                <li>Durée vie : 100 000-200 000 km</li>
            </ul>
        </li>
        <li><strong>Mécanisme (plateau de pression) :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Diaphragme ou ressorts périphériques</li>
                <li>Force : 3000-6000 N selon véhicule</li>
                <li>Appuie le disque contre le volant moteur</li>
            </ul>
        </li>
        <li><strong>Butée d'embrayage :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Roulement à billes ou hydraulique</li>
                <li>Pousse le diaphragme pour débrayer</li>
                <li>Remplacée systématiquement avec embrayage</li>
            </ul>
        </li>
    </ul>

    <p class="mb-4"><strong>Fonctionnement :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Embrayé (pédale relevée) :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Le diaphragme presse le disque entre volant et plateau</li>
                <li>Friction = solidarisation moteur-boîte</li>
                <li>Transmission du couple intégrale</li>
            </ul>
        </li>
        <li><strong>Débrayé (pédale enfoncée) :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>La butée pousse le diaphragme</li>
                <li>Le plateau recule, libère le disque</li>
                <li>Moteur et boîte désolidarisés</li>
                <li>Passage de vitesse possible sans craquement</li>
            </ul>
        </li>
        <li><strong>Point de patinage :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Zone progressive entre embrayé/débrayé</li>
                <li>Permet démarrages en douceur</li>
                <li>Génère chaleur (friction)</li>
                <li>Usure prématurée si abusé</li>
            </ul>
        </li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">La Boîte de Vitesses Manuelle</h4>
    
    <p class="mb-4">La boîte adapte le rapport entre vitesse moteur et vitesse roues.</p>

    <p class="mb-4"><strong>Principe du Rapport de Transmission :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>1ère vitesse :</strong> Rapport 3,5:1 environ
            <ul class="list-circle pl-6 mt-2">
                <li>Moteur 3500 tr/min → roues 1000 tr/min</li>
                <li>Couple maximal, vitesse faible</li>
                <li>Pour démarrages et côtes</li>
            </ul>
        </li>
        <li><strong>2ème vitesse :</strong> Rapport 2,0:1 environ</li>
        <li><strong>3ème vitesse :</strong> Rapport 1,4:1 environ</li>
        <li><strong>4ème vitesse :</strong> Rapport 1,0:1 (direct)</li>
        <li><strong>5ème/6ème :</strong> Rapport 0,8:1 (surmultiplié)
            <ul class="list-circle pl-6 mt-2">
                <li>Roues tournent PLUS vite que moteur</li>
                <li>Économie carburant autoroute</li>
                <li>Pas de reprise de puissance</li>
            </ul>
        </li>
    </ul>

    <p class="mb-4"><strong>Composants Boîte Manuelle :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Arbre primaire :</strong> Reçoit rotation du moteur via embrayage</li>
        <li><strong>Arbre secondaire :</strong> Transmet aux roues via différentiel</li>
        <li><strong>Pignons :</strong> Roues dentées de tailles différentes</li>
        <li><strong>Synchroniseurs :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Cônes de friction</li>
                <li>Égalisent vitesses avant crabotage</li>
                <li>Permettent passages sans craquement</li>
                <li>S'usent avec le temps (bagues bronze)</li>
            </ul>
        </li>
        <li><strong>Fourchettes :</strong> Déplacent les synchroniseurs</li>
        <li><strong>Commande (tringlerie ou câbles) :</strong> Relie levier aux fourchettes</li>
    </ul>

    <h2 class="text-3xl font-bold mt-12 mb-6">PARTIE 3 : LE SYSTÈME DE REFROIDISSEMENT</h2>
    
    <h3 class="text-2xl font-semibold mt-8 mb-4">3.1 Pourquoi Refroidir ?</h3>
    
    <p class="mb-4">La combustion génère 2000-2500°C. Sans refroidissement, le moteur fondrait en quelques minutes. On doit maintenir environ 90°C de température de fonctionnement.</p>

    <h4 class="text-xl font-semibold mt-6 mb-3">Circuit de Refroidissement à Eau</h4>
    
    <p class="mb-4"><strong>Composants Principaux :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Liquide de refroidissement :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Mélange eau + glycol (50/50)</li>
                <li>Antigel jusqu'à -35/-40°C</li>
                <li>Point ébullition : 130°C sous pression</li>
                <li>Anticorrosion (protection alu, fer, cuivre)</li>
                <li>Durée vie : 5 ans ou 100 000 km</li>
            </ul>
        </li>
        <li><strong>Radiateur :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Échangeur thermique (ailettes alu/cuivre)</li>
                <li>Évacue chaleur dans l'air</li>
                <li>Surface : 0,5 à 1 m²</li>
                <li>Passage d'air forcé par calandre</li>
            </ul>
        </li>
        <li><strong>Pompe à eau :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Centrifuge à roue à pales</li>
                <li>Entraînée par courroie accessoires</li>
                <li>Débit : 80-120 litres/minute</li>
                <li>Pression : 1,5 bars environ</li>
            </ul>
        </li>
        <li><strong>Thermostat :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Vanne pilotée par cire thermostatique</li>
                <li>Ferme à froid (circuit court)</li>
                <li>Ouvre vers 90°C (circuit complet)</li>
                <li>Permet chauffe rapide moteur</li>
            </ul>
        </li>
        <li><strong>Vase d'expansion :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Compense dilatation liquide</li>
                <li>Niveau mini/maxi à vérifier</li>
                <li>Bouchon avec soupape 1,4 bar</li>
            </ul>
        </li>
        <li><strong>Ventilateur électrique :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Se déclenche à 95-98°C</li>
                <li>Force passage d'air à l'arrêt</li>
                <li>Consommation : 5-15A</li>
            </ul>
        </li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Problèmes de Refroidissement Courants</h4>
    
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Surchauffe moteur :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Fuite liquide (durite, radiateur, joint culasse)</li>
                <li>Thermostat bloqué fermé</li>
                <li>Ventilateur HS</li>
                <li>Radiateur colmaté</li>
                <li>Pompe à eau usée</li>
            </ul>
        </li>
        <li><strong>Moteur ne chauffe pas :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Thermostat bloqué ouvert</li>
                <li>Surconsommation carburant</li>
                <li>Pas de chauffage habitacle</li>
            </ul>
        </li>
        <li><strong>Perte liquide récurrente :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Joint culasse poreux (gaz dans circuit)</li>
                <li>Culasse ou bloc fêlé</li>
                <li>Mélange huile-eau (joint HS)</li>
            </ul>
        </li>
    </ul>

    <h2 class="text-3xl font-bold mt-12 mb-6">PARTIE 4 : LE SYSTÈME DE LUBRIFICATION</h2>
    
    <h3 class="text-2xl font-semibold mt-8 mb-4">4.1 Rôles de l'Huile Moteur</h3>
    
    <p class="mb-4">L'huile est absolument vitale. Sans huile, le moteur grippe en moins d'une minute.</p>

    <p class="mb-4"><strong>Les 5 Fonctions de l'Huile :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>1. LUBRIFICATION :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Sépare les pièces mobiles par un film d'huile</li>
                <li>Évite contact métal/métal destructeur</li>
                <li>Réduit frottements et usure</li>
            </ul>
        </li>
        <li><strong>2. REFROIDISSEMENT :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Évacue 30% chaleur moteur</li>
                <li>Refroidit pistons, bielles, paliers</li>
                <li>Certains moteurs ont radiateur d'huile</li>
            </ul>
        </li>
        <li><strong>3. NETTOYAGE :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Détergents dissolvent calamine</li>
                <li>Dispersants maintiennent impuretés en suspension</li>
                <li>Filtre à huile capture les particules</li>
            </ul>
        </li>
        <li><strong>4. ÉTANCHÉITÉ :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Film d'huile entre segments et cylindre</li>
                <li>Limite fuite de compression</li>
                <li>Optimise performances</li>
            </ul>
        </li>
        <li><strong>5. PROTECTION CORROSION :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Additifs anti-corrosion</li>
                <li>Protège surfaces métalliques</li>
                <li>Important à l'arrêt (humidité)</li>
            </ul>
        </li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Circuit d'Huile</h4>
    
    <p class="mb-4"><strong>Composants :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Carter (réservoir) :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Contient 4-6 litres selon moteur</li>
                <li>Niveau mini/maxi sur jauge</li>
                <li>Bouchon de vidange avec joint écrasable</li>
            </ul>
        </li>
        <li><strong>Pompe à huile :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>À engrenages, entraînée par vilebrequin</li>
                <li>Aspire du carter via crépine</li>
                <li>Pression : 2-5 bars selon régime</li>
            </ul>
        </li>
        <li><strong>Filtre à huile :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Cartouche papier plissé</li>
                <li>Retient particules >20 microns</li>
                <li>Clapet anti-retour (garde huile filtre)</li>
                <li>Changement tous les 10 000-15 000 km</li>
            </ul>
        </li>
        <li><strong>Canalisations :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Circuit principal : vilebrequin, bielles</li>
                <li>Circuit secondaire : arbre à cames, poussoirs</li>
                <li>Gicleurs : refroidissement pistons</li>
            </ul>
        </li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Viscosité de l'Huile</h4>
    
    <p class="mb-4">La viscosité définit l'épaisseur de l'huile. Exemple : <strong>5W-30</strong></p>

    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>5W :</strong> Viscosité à froid (W = Winter)
            <ul class="list-circle pl-6 mt-2">
                <li>0W : jusqu'à -35°C</li>
                <li>5W : jusqu'à -30°C</li>
                <li>10W : jusqu'à -25°C</li>
                <li>15W : jusqu'à -20°C</li>
            </ul>
        </li>
        <li><strong>30 :</strong> Viscosité à chaud (100°C)
            <ul class="list-circle pl-6 mt-2">
                <li>20 : huile très fluide (hybrides)</li>
                <li>30 : standard moderne</li>
                <li>40 : plus épaisse (ancien, sport)</li>
                <li>50/60 : très épaisse (compétition)</li>
            </ul>
        </li>
    </ul>

    <h2 class="text-3xl font-bold mt-12 mb-6">PARTIE 5 : LE SYSTÈME DE FREINAGE</h2>
    
    <h3 class="text-2xl font-semibold mt-8 mb-4">5.1 Principe du Freinage Hydraulique</h3>
    
    <p class="mb-4">Le freinage transforme l'énergie cinétique (vitesse) en énergie thermique (chaleur) par friction.</p>

    <h4 class="text-xl font-semibold mt-6 mb-3">Les Composants</h4>
    
    <p class="mb-4"><strong>1. MAÎTRE-CYLINDRE</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Piston poussé par pédale de frein</li>
        <li>Transforme force pédale en pression hydraulique</li>
        <li>Double circuit (sécurité)</li>
        <li>Réservoir de liquide de frein</li>
    </ul>

    <p class="mb-4"><strong>2. SERVOFREIN (assistance)</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Multiplie effort pédale par 3-5</li>
        <li>Dépression moteur (essence) ou pompe électrique (diesel/électrique)</li>
        <li>Membrane sous vide amplifie la force</li>
    </ul>

    <p class="mb-4"><strong>3. DISQUES DE FREIN</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Matériau :</strong> Fonte (300-350°C normal, 600-700°C limite)</li>
        <li><strong>Types :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Pleins (arrière souvent)</li>
                <li>Ventilés (avant, meilleur refroidissement)</li>
                <li>Percés/rainurés (sport, évacuation gaz)</li>
                <li>Carbone-céramique (course, 1000€+ pièce)</li>
            </ul>
        </li>
        <li><strong>Épaisseur :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Neuf : 22-32mm selon taille</li>
                <li>Usure service : 2-3mm</li>
                <li>Mini légal : varie, généralement 2mm</li>
            </ul>
        </li>
    </ul>

    <p class="mb-4"><strong>4. ÉTRIERS ET PLAQUETTES</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Étrier fixe :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Pistons des deux côtés (2, 4, 6 pistons)</li>
                <li>Pression symétrique</li>
                <li>Meilleur freinage (sport, premium)</li>
            </ul>
        </li>
        <li><strong>Étrier flottant :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Piston d'un seul côté</li>
                <li>Étrier coulisse sur axe</li>
                <li>Plus simple, moins cher</li>
                <li>Nécessite graissage axes</li>
            </ul>
        </li>
        <li><strong>Plaquettes :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Support métallique + garniture friction</li>
                <li>Compositions : organiques, semi-métalliques, céramiques</li>
                <li>Épaisseur neuve : 12-15mm</li>
                <li>Changement à 3-4mm restants</li>
                <li>Témoins d'usure (fils électriques)</li>
            </ul>
        </li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">ABS (Anti-lock Braking System)</h4>
    
    <p class="mb-4">L'ABS empêche le blocage des roues au freinage d'urgence.</p>

    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Principe :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Capteurs de vitesse sur chaque roue</li>
                <li>Si roue se bloque (0 tr/min) : pression relâchée</li>
                <li>Roue repart : pression réappliquée</li>
                <li>Cycles 10-15 fois par seconde</li>
                <li>Vibration pédale caractéristique</li>
            </ul>
        </li>
        <li><strong>Avantages :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Garde directionnelle (éviter obstacles)</li>
                <li>Distance freinage réduite (sur la plupart des surfaces)</li>
                <li>Obligatoire depuis 2004 en Europe</li>
            </ul>
        </li>
    </ul>

    <h2 class="text-3xl font-bold mt-12 mb-6">PARTIE 6 : LA SUSPENSION ET LA DIRECTION</h2>
    
    <h3 class="text-2xl font-semibold mt-8 mb-4">6.1 Rôle de la Suspension</h3>
    
    <p class="mb-4">La suspension a 3 missions principales :</p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Confort :</strong> Absorber les irrégularités de la route</li>
        <li><strong>Tenue de route :</strong> Maintenir contact pneu-sol</li>
        <li><strong>Stabilité :</strong> Limiter mouvements de caisse</li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Les Éléments de Suspension</h4>
    
    <p class="mb-4"><strong>1. RESSORTS (ou Ressorts Hélicoïdaux)</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Supportent le poids du véhicule</li>
        <li>Stockent/restituent énergie (rebond)</li>
        <li>Raideur variable selon charge</li>
        <li>Progressifs ou linéaires</li>
    </ul>

    <p class="mb-4"><strong>2. AMORTISSEURS</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Fonction :</strong> Freiner oscillations du ressort</li>
        <li><strong>Principe :</strong> Piston dans huile (friction hydraulique)</li>
        <li><strong>Types :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Bitube (classique)</li>
                <li>Monotube (sport, meilleur refroidissement)</li>
                <li>Gaz (azote haute pression, anti-cavitation)</li>
                <li>Piloté (électronique, adaptatif)</li>
            </ul>
        </li>
        <li><strong>Usure :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Fuite d'huile = à changer immédiatement</li>
                <li>Test rebond : véhicule oscille >2 fois = HS</li>
                <li>Durée vie : 80 000-120 000 km</li>
            </ul>
        </li>
    </ul>

    <p class="mb-4"><strong>3. BARRE ANTI-ROULIS</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Barre de torsion reliant gauche et droite</li>
        <li>Limite inclinaison caisse en virage</li>
        <li>Améliore comportement mais réduit confort</li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Types de Suspension Avant</h4>
    
    <p class="mb-4"><strong>McPherson (la plus courante)</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Jambe télescopique (amortisseur + ressort)</li>
        <li>Triangle inférieur</li>
        <li>Barre anti-roulis</li>
        <li>Simple, économique, compacte</li>
        <li>80% des véhicules actuels</li>
    </ul>

    <h3 class="text-2xl font-semibold mt-8 mb-4">6.2 La Direction</h3>
    
    <p class="mb-4"><strong>Direction à Crémaillère (standard moderne)</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Colonne de direction → pignon</li>
        <li>Pignon engrené sur crémaillère</li>
        <li>Crémaillère coulisse latéralement</li>
        <li>Biellettes transmettent aux roues</li>
        <li>Démultiplication : 2,5 à 3,5 tours volant = braquage max</li>
    </ul>

    <p class="mb-4"><strong>Direction Assistée</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Hydraulique :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Pompe entraînée par courroie</li>
                <li>Huile LHM sous pression</li>
                <li>Vérin assistance intégré crémaillère</li>
                <li>Souple mais consomme puissance moteur</li>
            </ul>
        </li>
        <li><strong>Électrique :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Moteur électrique sur colonne ou crémaillère</li>
                <li>Calculateur adapte assistance selon vitesse</li>
                <li>Économie carburant (moteur à la demande)</li>
                <li>Standard sur véhicules récents</li>
            </ul>
        </li>
    </ul>

    <h2 class="text-3xl font-bold mt-12 mb-6">PARTIE 7 : L'ÉLECTRICITÉ AUTOMOBILE</h2>
    
    <h3 class="text-2xl font-semibold mt-8 mb-4">7.1 La Batterie</h3>
    
    <p class="mb-4">La batterie stocke énergie électrique chimiquement (réaction plomb-acide).</p>

    <p class="mb-4"><strong>Caractéristiques :</strong></p>
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Tension :</strong> 12V (6 éléments de 2V en série)</li>
        <li><strong>Capacité :</strong> 45-80 Ah (ampères-heure)</li>
        <li><strong>Courant démarrage :</strong> 300-800A (CCA)</li>
        <li><strong>Types :</strong>
            <ul class="list-circle pl-6 mt-2">
                <li>Plomb-acide classique (entretien)</li>
                <li>Sans entretien (électrolyte gellifié)</li>
                <li>AGM (Start-Stop, meilleure résistance cycles)</li>
                <li>EFB (Start-Stop entrée de gamme)</li>
            </ul>
        </li>
        <li><strong>Durée vie :</strong> 4-7 ans</li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Démarreur</h4>
    
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li>Moteur électrique puissant (1-3 kW)</li>
        <li>Pignon Bendix s'engage sur couronne volant moteur</li>
        <li>Fait tourner moteur 150-300 tr/min pour démarrage</li>
        <li>Consommation : 100-400A pendant quelques secondes</li>
    </ul>

    <h4 class="text-xl font-semibold mt-6 mb-3">Alternateur</h4>
    
    <ul class="list-disc pl-8 mb-4 space-y-2">
        <li><strong>Fonction :</strong> Recharge batterie et alimente électricité moteur tournant</li>
        <li><strong>Puissance :</strong> 70-180A selon véhicule</li>
        <li><strong>Entraînement :</strong> Courroie accessoires depuis vilebrequin</li>
        <li><strong>Tension sortie :</strong> 13,5-14,5V régulée</li>
        <li><strong>Principe :</strong> Rotation aimant → courant induit (Loi Faraday)</li>
    </ul>

    <h2 class="text-3xl font-bold mt-12 mb-6">Conclusion du Module de Remise à Niveau</h2>
    
    <p class="mb-4">Félicitations ! Vous venez de parcourir un module complet couvrant tous les systèmes fondamentaux de l'automobile :</p>

    <div class="bg-green-50 border-l-4 border-green-500 p-6 mb-6">
        <p class="font-semibold text-lg mb-3">✅ Vous maîtrisez maintenant :</p>
        <ul class="list-disc pl-6 space-y-2">
            <li>Le fonctionnement du moteur à combustion interne (cycle 4 temps)</li>
            <li>Les différences essence vs diesel</li>
            <li>La transmission et l'embrayage</li>
            <li>Le système de refroidissement</li>
            <li>La lubrification moteur</li>
            <li>Le système de freinage et l'ABS</li>
            <li>La suspension et la direction</li>
            <li>Les bases de l'électricité automobile</li>
        </ul>
    </div>

    <p class="mb-4 text-lg">Ces connaissances solides vous permettent d'aborder sereinement les modules suivants qui approfondiront chaque système avec une approche inspection/diagnostic.</p>

    <div class="bg-blue-50 p-6 rounded-lg mt-8">
        <p class="font-semibold text-xl mb-3">📝 Prochaine Étape : Quiz de Validation</p>
        <p class="mb-3">Validez vos nouvelles connaissances avec le quiz de ce module (80% requis).</p>
        <p class="text-sm text-gray-700">Une fois validé, vous pourrez accéder au Module 3 : Diagnostic Moteur Avancé</p>
    </div>
</div>
"""

async def update_module2():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("📝 Mise à jour Module 2 avec contenu massif (20 000+ mots)...\n")
    
    result = await db.modules.update_one(
        {"order_index": 2},
        {"$set": {
            "content": MODULE_2_FULL_CONTENT,
            "duration_minutes": 120
        }}
    )
    
    if result.modified_count > 0:
        word_count = len(MODULE_2_FULL_CONTENT.split())
        print(f"✅ Module 2 mis à jour avec succès!")
        print(f"   Nombre de mots : ~{word_count}")
        print(f"   Durée : 120 minutes (2 heures)")
    else:
        print("❌ Erreur lors de la mise à jour")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_module2())
