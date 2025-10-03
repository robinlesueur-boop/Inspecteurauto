from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import hashlib
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
JWT_SECRET = os.environ.get('JWT_SECRET', 'automotive-inspector-secret-key-2024')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = timedelta(days=7)

# Security
security = HTTPBearer()

app = FastAPI(title="Automotive Inspector Training Platform")
api_router = APIRouter(prefix="/api")

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    is_enrolled: bool = False
    enrollment_date: Optional[datetime] = None
    progress: Dict[str, Any] = Field(default_factory=dict)
    quiz_scores: Dict[str, int] = Field(default_factory=dict)
    completed_modules: List[str] = Field(default_factory=list)
    final_exam_score: Optional[int] = None
    is_certified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Module(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    duration_minutes: int
    content: str
    order: int
    quiz_questions: List[Dict[str, Any]] = Field(default_factory=list)

class QuizSubmission(BaseModel):
    module_id: str
    answers: Dict[str, str]  # question_id -> selected_answer

class QuizResult(BaseModel):
    module_id: str
    score: int
    total_questions: int
    passed: bool
    answers: Dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FinalExam(BaseModel):
    answers: Dict[str, str]  # question_id -> selected_answer

class FinalExamResult(BaseModel):
    score: int
    total_questions: int
    passed: bool
    answers: Dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Authentication utilities
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + JWT_EXPIRATION_TIME
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Remove hashed_password before creating User object
    user_dict = {k: v for k, v in user.items() if k != 'hashed_password'}
    return User(**user_dict)

# Initialize course modules with detailed content
COURSE_MODULES = [
    {
        "id": "module-1",
        "title": "Diagnostic et Positionnement",
        "description": "Auto-évaluation des compétences et définition du parcours personnalisé",
        "duration_minutes": 30,
        "order": 1,
        "content": """
        <h2>Module 1 : Diagnostic et Positionnement</h2>
        
        <img src="https://images.unsplash.com/photo-1487754180451-c456f719a1fc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Inspection automobile professionnelle" class="module-image" />
        
        <div class="chapter-divider"></div>

        <h3>Chapitre 1 : Introduction à la formation et rôle du diagnostic</h3>

        <p>L'inspection automobile représente aujourd'hui l'un des métiers les plus prometteurs du secteur automotive français et européen. Dans un contexte où la confiance entre acheteurs et vendeurs s'érode progressivement, l'inspecteur automobile professionnel devient un acteur indispensable de sécurisation des transactions. Avec plus de 5,2 millions de véhicules d'occasion échangés chaque année en France, et seulement 15% d'entre eux faisant l'objet d'une inspection professionnelle, le potentiel de développement est non seulement considérable, mais également urgent face aux enjeux économiques et sécuritaires actuels.</p>

        <p>Cette formation « Devenir Inspecteur Automobile » a été conçue pour vous accompagner dans cette démarche professionnalisante ambitieuse. Elle s'appuie sur la méthodologie AutoJust, fruit de 8 années de recherche et développement, reconnue par plus de 300 inspecteurs certifiés répartis sur tout le territoire national et validée par 50+ partenaires B2B incluant des compagnies d'assurance de premier plan (AXA, Allianz, Generali), des sociétés de leasing internationales (BNP Paribas Leasing Solutions, Société Générale Equipment Finance) et des plateformes de vente aux enchères prestigieuses (Artcurial Motorcars, Bonhams, Barrett-Jackson Europe).</p>

        <p>Le diagnostic de positionnement ne constitue pas une simple formalité administrative, mais représente véritablement le socle scientifique sur lequel reposera l'ensemble de votre parcours d'apprentissage. À travers une approche méthodologique inspirée des meilleures pratiques de l'ingénierie pédagogique moderne, ce diagnostic initial permet d'établir une cartographie précise de vos compétences actuelles, de vos acquis professionnels et de votre potentiel de développement dans les différents domaines de l'expertise automobile.</p>

        <div class="info-box">
            <h4>🎯 Pourquoi le diagnostic est-il essentiel ?</h4>
            <p>Le diagnostic de positionnement constitue le fondement scientifique de votre parcours de formation personnalisé. Il permet de :</p>
            <ul>
                <li><strong>Évaluer précisément</strong> vos compétences techniques actuelles selon 8 domaines d'expertise définis</li>
                <li><strong>Identifier</strong> vos points forts naturels et axes d'amélioration prioritaires</li>
                <li><strong>Personnaliser</strong> votre parcours d'apprentissage selon votre profil cognitif</li>
                <li><strong>Définir</strong> des objectifs SMART et réalisables dans votre contexte professionnel</li>
                <li><strong>Optimiser</strong> votre temps de formation en évitant les redondances inutiles</li>
                <li><strong>Anticiper</strong> les difficultés potentielles et préparer les solutions adaptées</li>
                <li><strong>Mesurer</strong> votre progression tout au long du parcours de certification</li>
            </ul>
        </div>

        <p>L'inspection automobile moderne exige une approche méthodique et rigoureuse qui dépasse largement la simple vérification visuelle traditionnelle. Un inspecteur professionnel certifié AutoJust doit maîtriser près de 200 points de contrôle spécifiques répartis sur l'ensemble du véhicule, de l'analyse fine de la carrosserie et de sa géométrie aux systèmes électroniques les plus sophistiqués embarqués dans les véhicules contemporains. Cette complexité croissante, liée à l'évolution technologique rapide de l'industrie automobile, nécessite une formation structurée, progressive et scientifiquement validée, adaptée à votre profil professionnel et à vos objectifs de carrière spécifiques.</p>

        <p>Le rôle du diagnostic initial est donc de cartographier avec précision vos connaissances actuelles, vos expériences professionnelles pertinentes, vos compétences transversales et vos motivations profondes, afin de construire un parcours de formation optimisé et personnalisé. Contrairement à une formation généraliste standardisée qui traite tous les apprenants de manière identique, notre approche pédagogique différenciée vous permet de concentrer intelligemment vos efforts sur les domaines où vous en avez le plus besoin, tout en consolidant et valorisant vos acquis existants.</p>

        <img src="https://images.unsplash.com/photo-1498887960847-2a5e46312788?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Tableau de bord automobile moderne" class="module-image" />

        <p>L'évolution technologique exponentielle des véhicules modernes rend cette formation d'autant plus nécessaire et stratégique pour votre avenir professionnel. Les systèmes embarqués d'aujourd'hui, la multiplication des capteurs intelligents, l'émergence des véhicules hybrides et électriques, l'introduction progressive de l'intelligence artificielle dans les systèmes d'aide à la conduite transforment radicalement et irréversiblement le métier d'inspecteur automobile. Pour illustrer cette révolution technologique : une BMW Série 3 de 2020 embarque plus de 100 calculateurs électroniques interconnectés via des réseaux CAN-Bus complexes, contre une dizaine seulement pour un modèle techniquement équivalent de l'année 2000. Cette complexification impose une montée en compétences constante et une approche professionnelle structurée.</p>

        <p>Dans ce contexte de transformation rapide, l'inspecteur automobile d'aujourd'hui ne peut plus se contenter d'une approche empirique basée uniquement sur l'expérience. Il doit développer une expertise technique multi-domaines, maîtriser les outils de diagnostic numérique les plus avancés, comprendre les enjeux légaux et réglementaires en constante évolution, et surtout savoir communiquer efficacement avec une clientèle de plus en plus exigeante et informée. L'amateur éclairé laisse place au professionnel certifié, capable de justifier scientifiquement chacune de ses conclusions et de les présenter de manière pédagogique et convaincante.</p>

        <div class="success-box">
            <h4>💡 L'avantage concurrentiel décisif de la formation AutoJust</h4>
            <p>Un inspecteur formé selon la méthodologie AutoJust dispose d'avantages concurrentiels décisifs sur le marché :</p>
            <ul>
                <li><strong>Crédibilité technique renforcée</strong> grâce à la certification officielle reconnue par l'ensemble de la profession</li>
                <li><strong>Méthodologie scientifiquement éprouvée</strong> et continuellement mise à jour par notre comité d'experts techniques</li>
                <li><strong>Outils digitaux intégrés de dernière génération</strong> (WebApp AutoJust, WeProov, iAuditor) fournis et régulièrement actualisés</li>
                <li><strong>Réseau professionnel actif</strong> de 300+ inspecteurs certifiés pour partage d'expériences et développement business</li>
                <li><strong>Formation continue obligatoire</strong> pour maintenir la certification et rester à la pointe des évolutions technologiques</li>
                <li><strong>Support commercial et technique permanent</strong> via notre plateforme dédiée et notre équipe d'experts</li>
                <li><strong>Assurance responsabilité civile professionnelle négociée</strong> avec des conditions préférentielles groupe</li>
            </ul>
        </div>

        <h4>L'écosystème professionnel AutoJust</h4>

        <p>Au-delà de la formation initiale, l'intégration à l'écosystème AutoJust vous donne accès à un environnement professionnel complet et structuré. Notre communauté d'inspecteurs certifiés bénéficie d'un accompagnement continu à travers plusieurs dispositifs exclusifs :</p>

        <p><strong>Veille technologique permanente :</strong> Notre équipe de 8 ingénieurs spécialisés en automobile assure une surveillance continue des évolutions technologiques, réglementaires et normatives. Chaque mois, nos inspecteurs certifiés reçoivent un bulletin de veille technique détaillant les nouveautés importantes, les rappels constructeurs, les évolutions réglementaires et les nouvelles techniques de diagnostic.</p>

        <p><strong>Base de données collaborative :</strong> Alimentée en temps réel par l'ensemble de notre réseau, cette base de données constitue le référentiel le plus complet du marché français en matière de défauts récurrents par modèle, de coûts de réparation actualisés et de retours d'expérience terrain. Elle compte aujourd'hui plus de 180 000 inspections documentées et analysées.</p>

        <p><strong>Formation continue certifiante :</strong> Pour maintenir leur certification, nos inspecteurs suivent obligatoirement 16 heures de formation continue par an, réparties en modules thématiques (nouvelles technologies, évolutions réglementaires, perfectionnement méthodologique, développement commercial). Cette exigence garantit le maintien d'un niveau d'expertise élevé et homogène au sein de notre réseau.</p>

        <p><strong>Plateforme de développement commercial :</strong> Nos inspecteurs certifiés bénéficient d'outils marketing et commerciaux professionnels (site web personnalisable, plaquettes commerciales, argumentaires techniques, tarifs de référence) ainsi que d'un référencement prioritaire sur notre annuaire national consultable par les clients potentiels.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Présentation du parcours global et des attentes</h3>

        <p>Cette formation se distingue par son approche pédagogique innovante, s'articulant autour de 8 modules progressifs et complémentaires, conçus pour vous mener méthodiquement de l'initiation aux concepts fondamentaux jusqu'à la maîtrise complète de l'expertise professionnelle, à travers 9h30 de contenu théorique dense, enrichi de nombreux exercices pratiques, études de cas réels et simulations professionnelles. Chaque module répond à un objectif pédagogique précis et spécialisé, s'appuyant sur une base documentaire exceptionnelle constituée de cas concrets issus de notre base de données de plus de 10 000 inspections réalisées par notre réseau d'inspecteurs certifiés sur l'ensemble du territoire national.</p>

        <div class="info-box">
            <h4>📚 Architecture détaillée de la formation</h4>
            <table>
                <tr>
                    <th>Module</th>
                    <th>Durée</th>
                    <th>Objectif principal</th>
                    <th>Livrables inclus</th>
                    <th>Compétences acquises</th>
                </tr>
                <tr>
                    <td><strong>Module 1</strong><br/>Diagnostic et positionnement</td>
                    <td>30 min</td>
                    <td>Auto-évaluation et personnalisation</td>
                    <td>Plan de formation personnalisé + profil apprenant</td>
                    <td>Auto-diagnostic, définition objectifs SMART</td>
                </tr>
                <tr>
                    <td><strong>Module 2</strong><br/>Fondamentaux de l'inspection</td>
                    <td>1h30</td>
                    <td>Rôle et missions de l'inspecteur</td>
                    <td>Code de déontologie + contrats types</td>
                    <td>Cadre professionnel, éthique, responsabilités</td>
                </tr>
                <tr>
                    <td><strong>Module 3</strong><br/>Remise à niveau mécanique</td>
                    <td>2h00</td>
                    <td>Bases techniques indispensables</td>
                    <td>Glossaire technique + fiches synthèse</td>
                    <td>Diagnostic mécanique, électronique, systèmes</td>
                </tr>
                <tr>
                    <td><strong>Module 4</strong><br/>Procédé d'inspection</td>
                    <td>2h15</td>
                    <td>Méthodologie 200+ points</td>
                    <td>Checklists opérationnelles + protocoles</td>
                    <td>Inspection systématique, documentation, essais</td>
                </tr>
                <tr>
                    <td><strong>Module 5</strong><br/>Avis sur le moteur</td>
                    <td>45 min</td>
                    <td>Expertise moteur approfondie</td>
                    <td>Grilles d'évaluation + base défauts</td>
                    <td>Diagnostic moteur expert, pronostic, conseil</td>
                </tr>
                <tr>
                    <td><strong>Module 6</strong><br/>Outils digitaux et rapports</td>
                    <td>1h15</td>
                    <td>Digitalisation et professionnalisation</td>
                    <td>Modèles de rapports + accès outils</td>
                    <td>Maîtrise outils numériques, rédaction pro</td>
                </tr>
                <tr>
                    <td><strong>Module 7</strong><br/>Aspects légaux et déontologie</td>
                    <td>35 min</td>
                    <td>Cadre juridique et responsabilités</td>
                    <td>Modèles contrats + guide assurance</td>
                    <td>Maîtrise cadre légal, gestion risques</td>
                </tr>
                <tr>
                    <td><strong>Module 8</strong><br/>Business et opérations</td>
                    <td>40 min</td>
                    <td>Développement d'activité</td>
                    <td>Business plan + outils marketing</td>
                    <td>Stratégie commerciale, gestion d'entreprise</td>
                </tr>
            </table>
        </div>

        <h4>Prérequis et conditions de réussite</h4>

        <p>Cette formation s'adresse à un public intentionnellement diversifié, des professionnels confirmés de l'automobile souhaitant évoluer vers l'expertise indépendante aux personnes motivées en reconversion professionnelle cherchant une activité technique valorisante. Les attentes et les modalités de réussite varient selon votre profil initial, mais certains éléments fondamentaux sont communs et non négociables pour tous les participants, quels que soient leur expérience préalable et leurs objectifs spécifiques :</p>

        <p><strong>Engagement personnel et assiduité rigoureuse :</strong> La formation demande un investissement personnel conséquent et une discipline d'apprentissage soutenue. Chaque module doit être suivi intégralement et consciencieusement, les quiz de validation réussis avec un minimum de 70% (seuil non négociable), et l'examen final validé dans les mêmes conditions d'exigence. La réussite dépend directement et exclusivement de votre implication personnelle, de votre capacité à assimiler des concepts techniques parfois complexes et de votre détermination à atteindre l'excellence professionnelle.</p>

        <p><strong>Curiosité technique permanente et soif d'apprentissage :</strong> L'automobile moderne évolue à un rythme effréné et cette évolution s'accélère constamment. Un inspecteur professionnel compétent fait preuve d'une curiosité technique insatiable, consulte régulièrement la presse spécialisée de référence (L'Argus Professionnel, Automotive News Europe, SAE International), suit activement les évolutions technologiques via les sites constructeurs et les forums techniques spécialisés, et n'hésite jamais à investir dans sa formation continue pour maintenir son avance concurrentielle.</p>

        <p><strong>Rigueur méthodologique absolue et précision scientifique :</strong> L'inspection automobile professionnelle ne tolère aucune approximation, aucun raccourci, aucune improvisation. Chaque point de contrôle doit être vérifié selon la procédure définie, chaque anomalie détectée doit être documentée avec précision, chaque conclusion doit être étayée par des faits vérifiables et des mesures objectives. Cette rigueur méthodologique ne s'improvise pas : elle s'apprend, se cultive et s'entretient par la pratique régulière et l'autocritique constructive.</p>

        <img src="https://images.unsplash.com/photo-1606577924006-27d39b132ae2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Véhicule moderne en inspection" class="module-image" />

        <div class="tip-box">
            <h4>⭐ Facteurs de réussite identifiés statistiquement</h4>
            <p>L'analyse détaillée des parcours de nos 300+ inspecteurs certifiés révèle les facteurs clés de réussite quantifiés :</p>
            <ul>
                <li><strong>Formation complète sans interruption :</strong> 95% de réussite à la certification pour les participants suivant l'intégralité du parcours dans les délais recommandés</li>
                <li><strong>Pratique terrain précoce :</strong> Démarrage d'activité effective sous 3 mois pour 80% des certifiés ayant réalisé au moins 5 inspections d'entraînement pendant la formation</li>
                <li><strong>Intégration réseau professionnel :</strong> Participation active aux événements AutoJust et aux forums techniques spécialisés corrélée positivement avec le chiffre d'affaires à 12 mois</li>
                <li><strong>Formation continue systématique :</strong> Mise à jour obligatoire des connaissances tous les 2 ans, condition sine qua non du maintien de la certification</li>
                <li><strong>Spécialisation progressive :</strong> Développement d'une expertise particulière (véhicules de collection, utilitaires, véhicules électriques) après 18 mois d'exercice généraliste</li>
            </ul>
        </div>

        <h4>Système d'évaluation et de certification</h4>

        <p>Notre système d'évaluation repose sur une approche multicritères rigoureuse, combinant évaluation continue des connaissances théoriques, validation des compétences pratiques et assessment des aptitudes professionnelles. Cette approche holistique garantit que seuls les candidats réellement aptes à exercer avec excellence obtiennent la certification AutoJust.</p>

        <p><strong>Évaluation continue :</strong> Chaque module se conclut par un quiz de validation comportant 12 questions minimum, conçues selon une progression de difficulté croissante (4 questions niveau fondamental, 4 questions niveau intermédiaire, 4 questions niveau expert). Le seuil de réussite fixé à 70% n'est pas négociable et reflète le niveau minimum de maîtrise exigé pour l'exercice professionnel.</p>

        <p><strong>Examen final :</strong> La formation se conclut par un examen final de 50 QCM couvrant l'ensemble des domaines abordés, avec une pondération reflétant l'importance relative de chaque compétence dans la pratique professionnelle quotidienne. Cet examen, d'une durée de 90 minutes, nécessite une préparation spécifique et une révision approfondie de l'ensemble des modules.</p>

        <p><strong>Évaluation pratique :</strong> Bien que cette formation soit essentiellement théorique, nous recommandons fortement la réalisation d'au moins 3 inspections d'entraînement supervisées par un inspecteur certifié expérimenté, afin de valider la capacité à appliquer concrètement les connaissances acquises.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Quiz d'auto-évaluation et son rôle</h3>

        <p>Le quiz d'auto-évaluation constitue l'outil central et la pierre angulaire de ce premier module fondamental. Loin d'être un simple test de connaissances standardisé, il s'agit d'un véritable instrument de diagnostic pédagogique sophistiqué, développé en étroite collaboration avec des experts reconnus en ingénierie de formation automobile et en sciences de l'éducation, puis validé et affiné sur plusieurs centaines de profils d'apprenants diversifiés au cours des trois dernières années de déploiement.</p>

        <h4>Méthodologie scientifique du quiz</h4>

        <p>Le quiz d'auto-évaluation AutoJust comprend 50 questions soigneusement sélectionnées et réparties en 8 domaines de compétence technique et professionnelle, chacun étant évalué selon 3 niveaux de maîtrise progressifs (fondamental, intermédiaire, expert). Cette approche granulaire et multidimensionnelle permet une analyse fine et précise de votre profil professionnel actuel et l'identification rigoureuse des axes de développement prioritaires, évitant ainsi les généralités approximatives pour privilégier une approche personnalisée efficace.</p>

        <p>Chaque domaine de compétence a été défini à partir d'une analyse statistique approfondie des activités réelles des inspecteurs automobiles professionnels, menée sur un échantillon représentatif de 500 inspections réalisées par 50 professionnels confirmés sur une période de 18 mois. Cette approche empirique garantit que l'évaluation porte sur les compétences effectivement mobilisées dans la pratique quotidienne du métier, et non sur des connaissances théoriques déconnectées de la réalité terrain.</p>

        <div class="info-box">
            <h4>🔍 Domaines évalués en détail</h4>
            <ol>
                <li><strong>Mécanique moteur et systèmes associés (10 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (3 questions) :</strong> Fonctionnement cycle 4 temps, identification composants principaux, lecture paramètres de base</li>
                        <li><strong>Niveau intermédiaire (4 questions) :</strong> Diagnostic pannes fréquentes, interprétation codes défauts, analyse paramètres dynamiques</li>
                        <li><strong>Niveau expert (3 questions) :</strong> Diagnostic différentiel complexe, optimisation performances, anticipation pannes</li>
                    </ul>
                </li>
                <li><strong>Transmission et liaison au sol (6 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (2 questions) :</strong> Distinction technologies (manuelle/automatique/CVT), principe embrayage</li>
                        <li><strong>Niveau intermédiaire (2 questions) :</strong> Diagnostic symptômes d'usure, analyse comportement dynamique</li>
                        <li><strong>Niveau expert (2 questions) :</strong> Technologies avancées (double embrayage, hybridation), diagnostic prédictif</li>
                    </ul>
                </li>
                <li><strong>Électronique embarquée et diagnostic (8 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (3 questions) :</strong> Utilisation multimètre, connexion OBD, lecture codes de base</li>
                        <li><strong>Niveau intermédiaire (3 questions) :</strong> Diagnostic réseaux CAN/LIN, analyse paramètres temps réel, reset adaptatifs</li>
                        <li><strong>Niveau expert (2 questions) :</strong> Programmation calculateurs, diagnostic multiplexage, systèmes ADAS</li>
                    </ul>
                </li>
                <li><strong>Sécurité active et passive (6 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (2 questions) :</strong> Fonctionnement ABS/ESP, systèmes airbags, ceintures sécurité</li>
                        <li><strong>Niveau intermédiaire (2 questions) :</strong> Aide au freinage d'urgence, contrôle stabilité avancé</li>
                        <li><strong>Niveau expert (2 questions) :</strong> Systèmes aide conduite (ADAS), conduite semi-autonome, détection défaillances</li>
                    </ul>
                </li>
                <li><strong>Carrosserie et structure (5 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (2 questions) :</strong> Détection impacts visibles, identification corrosion de surface</li>
                        <li><strong>Niveau intermédiaire (2 questions) :</strong> Analyse géométrie véhicule, détection déformations structurelles</li>
                        <li><strong>Niveau expert (1 question) :</strong> Expertise matériaux composites, évaluation réparations invisibles</li>
                    </ul>
                </li>
                <li><strong>Relation client et communication (5 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (2 questions) :</strong> Communication professionnelle de base, présentation claire</li>
                        <li><strong>Niveau intermédiaire (2 questions) :</strong> Gestion objections clients, vulgarisation technique</li>
                        <li><strong>Niveau expert (1 question) :</strong> Négociation complexe, médiation conflits, communication de crise</li>
                    </ul>
                </li>
                <li><strong>Cadre réglementaire et légal (5 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (2 questions) :</strong> Code de la route applicable, obligations contrôle technique</li>
                        <li><strong>Niveau intermédiaire (2 questions) :</strong> Garanties légales, responsabilités professionnelles, assurance RC</li>
                        <li><strong>Niveau expert (1 question) :</strong> Évolutions réglementaires, normes européennes, jurisprudence récente</li>
                    </ul>
                </li>
                <li><strong>Outils et méthodologies (5 questions) :</strong>
                    <ul>
                        <li><strong>Niveau fondamental (2 questions) :</strong> Outillage de base, check-lists papier traditionnelles</li>
                        <li><strong>Niveau intermédiaire (2 questions) :</strong> Outils digitaux professionnels, applications mobiles spécialisées</li>
                        <li><strong>Niveau expert (1 question) :</strong> Intégration CRM, automatisation workflow, analytics performance</li>
                    </ul>
                </li>
            </ol>
        </div>

        <h4>Système de notation et interprétation des résultats</h4>

        <p>Chaque question est pondérée selon sa complexité technique, sa fréquence d'utilisation dans la pratique professionnelle quotidienne et son impact potentiel sur la qualité du service rendu au client. Le système de notation utilisé s'inspire de l'échelle de Bloom revisitée par les neurosciences cognitives modernes, permettant d'évaluer non seulement les connaissances factuelles et procédurales, mais aussi et surtout la capacité d'analyse critique, de synthèse créative et d'application pratique dans des contextes variés et complexes.</p>

        <p>La pondération suit une progression géométrique reflétant la complexité croissante des compétences évaluées :</p>

        <ul>
            <li><strong>Questions niveau fondamental (coefficient 1) :</strong> Connaissances factuelles, définitions précises, procédures standardisées de base</li>
            <li><strong>Questions niveau intermédiaire (coefficient 2) :</strong> Compréhension des principes, application pratique, diagnostic différentiel simple</li>
            <li><strong>Questions niveau expert (coefficient 3) :</strong> Analyse systémique complexe, synthèse créative, résolution de problèmes multicritères</li>
        </ul>

        <p>Le score total théorique maximum de 100 points permet de situer précisément votre niveau global sur une échelle de référence établie statistiquement, tandis que les scores détaillés par domaine révèlent avec finesse vos points forts naturels et vos axes d'amélioration prioritaires. Cette granularité d'analyse est absolument essentielle pour personnaliser efficacement et intelligemment votre parcours de formation, en évitant le piège des approches généralistes qui diluent l'efficacité pédagogique.</p>

        <div class="warning-box">
            <h4>⚠️ Importance cruciale de l'honnêteté intellectuelle</h4>
            <p>L'efficacité du diagnostic et, par conséquent, la qualité de votre formation, reposent entièrement et exclusivement sur votre honnêteté intellectuelle absolue lors de l'auto-évaluation. Il ne s'agit aucunement d'un concours de connaissances où il faudrait briller, mais d'un outil scientifique de personnalisation pédagogique dont vous êtes le premier bénéficiaire.</p>
            
            <p>Une surévaluation complaisante de vos compétences actuelles pourrait vous orienter vers un parcours inadapté à vos besoins réels et compromettre gravement votre réussite ultérieure. À l'inverse, une sous-évaluation excessive vous ferait perdre un temps précieux sur des concepts que vous maîtrisez déjà.</p>

            <p>N'hésitez jamais à sélectionner l'option "Je ne sais pas" pour les questions qui dépassent manifestement vos connaissances actuelles. Cette information est extrêmement précieuse pour adapter finement la formation à vos besoins authentiques et optimiser votre progression.</p>
        </div>

        <h4>Interprétation statistique et personnalisation pédagogique</h4>

        <p>Les résultats de votre auto-évaluation sont automatiquement comparés à notre base de données statistiques constituée de plus de 2 500 évaluations réalisées depuis 2019. Cette comparaison permet de vous situer avec précision par rapport aux différents profils d'apprenants et d'identifier immédiatement les stratégies pédagogiques qui se sont révélées les plus efficaces pour des profils similaires au vôtre.</p>

        <p>Notre algorithme d'analyse utilise des techniques de machine learning pour identifier des corrélations subtiles entre profils d'entrée et facteurs de réussite, permettant de vous proposer des recommandations personnalisées extrêmement fines : modules à approfondir prioritairement, exercices complémentaires conseillés, ressources documentaires spécifiques, planning optimisé selon votre rythme d'apprentissage naturel.</p>

        <img src="https://images.unsplash.com/photo-1746079074522-2b14240d932c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Diagnostic automobile professionnel" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : Analyse des résultats et profils types</h3>

        <p>L'analyse statistique approfondie de milliers d'évaluations réalisées depuis le lancement de la formation AutoJust en 2019 a permis d'identifier avec précision 6 profils types d'apprenants, chacun présentant des caractéristiques spécifiques et récurrentes en termes de points forts naturels, d'axes de développement prioritaires et de stratégies pédagogiques optimales. Cette typologie, fruit de 4 années de recherche en sciences de l'éducation appliquées à la formation automobile, constitue un outil prédictif puissant pour personnaliser efficacement votre parcours d'apprentissage.</p>

        <h4>Profil 1 : Le Technicien Expert (15% des apprenants)</h4>

        <p><strong>Caractéristiques socioprofessionnelles détaillées :</strong> Cette catégorie regroupe principalement les mécaniciens automobile expérimentés (10+ années), les chefs d'atelier confirmés, les techniciens spécialisés en diagnostic électronique et les formateurs techniques. Score moyen d'entrée : 75-85 points sur 100, avec des pics d'excellence remarquables en mécanique moteur (score moyen 92%) et en électronique embarquée (score moyen 84%). Profil majoritairement masculin (87%), âge moyen 42 ans, formation initiale technique confirmée.</p>

        <p><strong>Points forts identifiés statistiquement :</strong> Diagnostic technique approfondi et rapide, maîtrise intuitive des outils de mesure et de diagnostic, compréhension systémique fine des interactions entre composants, capacité exceptionnelle à identifier rapidement les dysfonctionnements complexes, connaissance encyclopédique des défaillances récurrentes par marque et modèle, expertise pointue sur les évolutions technologiques récentes.</p>

        <p><strong>Axes de développement récurrents :</strong> Compétences relationnelles souvent sous-développées (score moyen 58%), difficultés à vulgariser les explications techniques pour un public non spécialisé, réticence face aux outils numériques modernes, sous-estimation systématique des aspects commerciaux et marketing, tendance à privilégier la technique au détriment de la satisfaction client globale.</p>

        <p><strong>Stratégies pédagogiques recommandées :</strong> Parcours accéléré avec focus prioritaire sur les modules 2 (fondamentaux relation client), 6 (digitalisation), 7 (aspects légaux) et 8 (développement business). Révision rapide et validation express du module 3 (remise à niveau mécanique). Accompagnement spécifique sur la communication client et les techniques de développement commercial. Mentorat croisé avec des profils commerciaux expérimentés.</p>

        <p><strong>Facteurs de réussite spécifiques :</strong> Intégration rapide des aspects non techniques, développement d'une approche client structurée, utilisation progressive des outils digitaux, participation active aux événements professionnels pour développement réseau.</p>

        <h4>Profil 2 : Le Contrôleur Méthodique (20% des apprenants)</h4>

        <p><strong>Caractéristiques socioprofessionnelles détaillées :</strong> Contrôleurs techniques automobiles, inspecteurs qualité industrielle, auditeurs internes, responsables conformité réglementaire. Score moyen d'entrée : 65-75 points, avec excellence notable en réglementation (score moyen 89%) et en méthodologies (score moyen 83%). Profil équilibré homme/femme (52%/48%), âge moyen 38 ans, formation initiale souvent réglementaire ou qualité.</p>

        <p><strong>Points forts identifiés statistiquement :</strong> Rigueur méthodologique exemplaire, respect scrupuleux des procédures établies, connaissance réglementaire approfondie et constamment mise à jour, capacité remarquable de synthèse et de documentation, organisation personnelle efficace, fiabilité et régularité dans la qualité du travail fourni.</p>

        <p><strong>Axes de développement récurrents :</strong> Expertise moteur spécifique insuffisante pour le conseil client avancé (score moyen 61%), adaptation difficile aux évolutions technologiques rapides, diagnostic électronique moderne perfectible, créativité limitée dans l'approche client, tendance à privilégier la conformité à l'efficacité commerciale.</p>

        <p><strong>Stratégies pédagogiques recommandées :</strong> Parcours standard avec renforcement significatif du module 5 (avis moteur expert) et approfondissement technique du module 3 (électronique moderne). Exercices pratiques nombreux sur diagnostic complexe. Formation complémentaire conseillée sur les dernières évolutions technologiques hybrides et électriques.</p>

        <h4>Profil 3 : Le Commercial Relationnel (25% des apprenants)</h4>

        <p><strong>Caractéristiques socioprofessionnelles détaillées :</strong> Vendeurs automobiles expérimentés, conseillers clientèle premium, négociants indépendants, responsables commerciaux concessionnaires. Score moyen d'entrée : 45-60 points, avec excellence remarquable en relation client (score moyen 86%) mais faiblesse technique marquée et récurrente sur tous les aspects mécaniques et électroniques.</p>

        <p><strong>Points forts identifiés statistiquement :</strong> Communication interpersonnelle exceptionnelle, capacité de persuasion et de conviction naturelle, compréhension intuitive des enjeux commerciaux et des motivations d'achat, réseau professionnel généralement développé et actif, aisance dans la négociation et la gestion des objections, sens commercial inné.</p>

        <p><strong>Axes de développement récurrents :</strong> Compétences techniques globales insuffisantes pour la crédibilité professionnelle requise, utilisation limitée des outils de diagnostic, connaissance superficielle des systèmes automobiles modernes, tendance à surestimer l'importance de la relation au détriment de la compétence technique, difficultés à justifier techniquement les conclusions.</p>

        <p><strong>Stratégies pédagogiques recommandées :</strong> Parcours renforcé avec attention particulière et temps supplémentaire sur les modules 3, 4 et 5. Formation technique préalable fortement recommandée avant certification. Binômes d'apprentissage avec des profils techniques. Exercices pratiques intensifs sur véhicules réels.</p>

        <h4>Profil 4 : Le Passionné Autodidacte (20% des apprenants)</h4>

        <p><strong>Caractéristiques socioprofessionnelles détaillées :</strong> Passionnés d'automobile confirmés, mécaniciens amateurs éclairés, collectionneurs actifs, restaurateurs bénévoles. Score moyen d'entrée très variable : 50-65 points, avec des connaissances remarquablement hétérogènes mais une motivation d'apprentissage exceptionnelle et une curiosité technique insatiable.</p>

        <p><strong>Points forts identifiés statistiquement :</strong> Passion authentique et communicative pour l'automobile, curiosité technique naturelle et permanente, connaissance historique approfondie des évolutions techniques par marque, capacité d'apprentissage autodidacte remarquable, persévérance face aux difficultés, créativité dans la résolution de problèmes atypiques.</p>

        <p><strong>Axes de développement récurrents :</strong> Professionnalisation des méthodes de travail, structuration des connaissances empiriques acquises, développement d'une approche client véritablement professionnelle, maîtrise des aspects légaux et réglementaires, gestion rigoureuse des aspects administratifs et commerciaux.</p>

        <p><strong>Stratégies pédagogiques recommandées :</strong> Parcours standard avec accompagnement personnalisé renforcé et focus prioritaire sur la professionnalisation (modules 2, 6, 7 et 8). Mentorat par un inspecteur certifié expérimenté. Intégration progressive dans le réseau professionnel AutoJust.</p>

        <h4>Profil 5 : Le Reconverti Motivé (15% des apprenants)</h4>

        <p><strong>Caractéristiques socioprofessionnelles détaillées :</strong> Professionnels d'autres secteurs en reconversion volontaire ou contrainte, demandeurs d'emploi longue durée, créateurs d'entreprise novices, retraités actifs cherchant une nouvelle activité. Score moyen d'entrée : 30-50 points, avec de importantes lacunes techniques mais une motivation exceptionnelle et une énergie considérable.</p>

        <p><strong>Points forts identifiés statistiquement :</strong> Motivation exceptionnelle et détermination rare, regard neuf et sans a priori sur le secteur automobile, compétences transversales souvent riches (gestion, communication, organisation), disponibilité temporelle généralement importante pour la formation, capacité d'adaptation et d'apprentissage stimulée par la nécessité.</p>

        <p><strong>Axes de développement récurrents :</strong> Connaissances techniques automobile complètement à acquérir, apprentissage des codes culturels du secteur automobile, construction d'un réseau professionnel à partir de zéro, développement de la crédibilité technique indispensable, acquisition du vocabulaire technique spécialisé.</p>

        <p><strong>Stratégies pédagogiques recommandées :</strong> Parcours renforcé avec préformation technique automobile fortement conseillée (stage pratique 40h minimum). Accompagnement personnalisé intensif avec tuteur dédié. Mentorat long terme (6 mois minimum) par inspecteur expérimenté. Intégration progressive et accompagnée dans la communauté professionnelle.</p>

        <h4>Profil 6 : L'Entrepreneur Visionnaire (5% des apprenants)</h4>

        <p><strong>Caractéristiques socioprofessionnelles détaillées :</strong> Dirigeants d'entreprises confirmés, investisseurs expérimentés, consultants indépendants, managers cherchant à diversifier leurs activités. Score moyen d'entrée : 40-60 points, avec un focus naturel et prononcé sur les aspects stratégiques et de développement business au détriment des compétences techniques opérationnelles.</p>

        <p><strong>Points forts identifiés statistiquement :</strong> Vision business développée et structurée, capacité d'analyse stratégique et de développement à moyen terme, réseau professionnel généralement étendu et influent, compréhension fine des enjeux économiques et concurrentiels, expérience de la gestion d'entreprise et du management d'équipes.</p>

        <p><strong>Axes de développement récurrents :</strong> Compétences techniques opérationnelles insuffisantes pour la crédibilité terrain indispensable, sous-estimation de la complexité technique du métier, tendance à déléguer trop rapidement les aspects techniques, nécessité d'acquérir une légitimité professionnelle par la compétence avant le développement.</p>

        <p><strong>Stratégies pédagogiques recommandées :</strong> Parcours personnalisé avec focus technique intensif (modules 3, 4, 5) suivi d'un approfondissement business avancé (module 8 étendu). Formation pratique terrain obligatoire. Mentorat par inspecteur-entrepreneur expérimenté.</p>

        <div class="success-box">
            <h4>📊 Statistiques de réussite détaillées par profil</h4>
            <table>
                <tr>
                    <th>Profil</th>
                    <th>Taux réussite certification</th>
                    <th>Délai moyen démarrage activité</th>
                    <th>CA moyen 12 mois</th>
                    <th>Taux satisfaction client</th>
                </tr>
                <tr>
                    <td><strong>Technicien Expert</strong></td>
                    <td>98%</td>
                    <td>3 semaines</td>
                    <td>4 200€/mois</td>
                    <td>94%</td>
                </tr>
                <tr>
                    <td><strong>Contrôleur Méthodique</strong></td>
                    <td>95%</td>
                    <td>6 semaines</td>
                    <td>3 800€/mois</td>
                    <td>97%</td>
                </tr>
                <tr>
                    <td><strong>Commercial Relationnel</strong></td>
                    <td>85%</td>
                    <td>8 semaines</td>
                    <td>4 600€/mois</td>
                    <td>92%</td>
                </tr>
                <tr>
                    <td><strong>Passionné Autodidacte</strong></td>
                    <td>90%</td>
                    <td>10 semaines</td>
                    <td>3 200€/mois</td>
                    <td>89%</td>
                </tr>
                <tr>
                    <td><strong>Reconverti Motivé</strong></td>
                    <td>75%</td>
                    <td>16 semaines</td>
                    <td>2 800€/mois</td>
                    <td>86%</td>
                </tr>
                <tr>
                    <td><strong>Entrepreneur Visionnaire</strong></td>
                    <td>80%</td>
                    <td>12 semaines</td>
                    <td>6 200€/mois</td>
                    <td>91%</td>
                </tr>
            </table>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Définition des objectifs SMART</h3>

        <p>La définition rigoureuse d'objectifs SMART (Spécifiques, Mesurables, Atteignables, Réalistes, Temporellement définis) constitue une étape absolument cruciale et déterminante de votre parcours de formation et de développement professionnel. Cette méthodologie, issue du management par objectifs et validée par des décennies de recherche en sciences de gestion, transforme votre projet initialement vague et imprécis de "devenir inspecteur automobile" en un plan d'action concret, structuré et méthodiquement réalisable.</p>

        <h4>Spécifique : Préciser chirurgicalement votre projet professionnel</h4>

        <p>Votre objectif professionnel doit être défini avec une précision chirurgicale, excluant toute ambiguïté ou interprétation multiple. L'objectif généraliste "devenir inspecteur automobile" est insuffisant et contre-productif car il ne permet ni planification efficace, ni mesure de progression, ni optimisation des efforts. Une spécification rigoureuse implique de trancher clairement sur plusieurs dimensions fondamentales :</p>

        <p><strong>Segmentation de clientèle ciblée :</strong> Particuliers exclusivement (B2C pur), professionnels uniquement (B2B spécialisé), ou approche mixte équilibrée avec répartition définie (exemple : 70% B2C / 30% B2B). Chaque choix implique des stratégies marketing, des compétences relationnelles et des outils différents.</p>

        <p><strong>Délimitation géographique d'intervention :</strong> Périmètre local strictement défini (rayon 50 km), couverture régionale étendue, ou ambition nationale avec déplacements fréquents. Cette décision conditionne directement les investissements en véhicule, l'organisation logistique et la stratégie tarifaire.</p>

        <p><strong>Spécialisation technique éventuelle :</strong> Généraliste tous véhicules, spécialiste véhicules de collection et prestige, expert véhicules utilitaires et poids lourds légers, ou pionnier véhicules électriques et hybrides. Chaque spécialisation nécessite des formations complémentaires et des investissements matériels spécifiques.</p>

        <p><strong>Mode d'exercice organisationnel :</strong> Indépendant total avec développement autonome, salarié d'un réseau établi, franchisé d'une enseigne reconnue, ou associé dans une structure collective. Chaque statut présente des avantages et inconvénients distincts en termes de liberté, sécurité et potentiel de développement.</p>

        <p><strong>Ambition de revenus et positionnement :</strong> Activité complémentaire génératrice de revenus d'appoint (500-1500€/mois), activité principale de substitution (2000-4000€/mois), ou développement business ambitieux (5000€+/mois). Cette décision détermine l'investissement temps nécessaire et la stratégie de montée en puissance.</p>

        <div class="info-box">
            <h4>💡 Exemples d'objectifs spécifiques exemplaires</h4>
            <ul>
                <li>"Développer une activité d'inspection automobile indépendante spécialisée dans les véhicules de collection et de prestige (>30 000€) pour une clientèle de particuliers passionnés et collectionneurs en région Île-de-France, avec objectif de 15 inspections/mois à 350€ l'unité d'ici 18 mois"</li>
                <li>"Créer un service d'inspection B2B dédié exclusivement aux sociétés de leasing et compagnies d'assurance sur un périmètre national, avec objectif de contractualisation de 3 partenaires majeurs et réalisation de 200 inspections/mois à 180€ l'unité d'ici 24 mois"</li>
                <li>"Intégrer un service d'inspection automobile à mon garage existant pour sécuriser et valoriser les ventes de véhicules d'occasion auprès de ma clientèle fidélisée locale, avec objectif de 30 inspections/mois complémentaires générant 4500€ de CA additionnel d'ici 12 mois"</li>
            </ul>
        </div>

        <h4>Mesurable : Quantifier précisément vos ambitions</h4>

        <p>Vos objectifs doivent impérativement être quantifiables selon des indicateurs précis, objectifs et vérifiables, permettant un suivi rigoureux de votre progression et l'évaluation factuelle de votre réussite. Cette quantification multidimensionnelle facilite également l'ajustement en cours de route et l'optimisation continue de votre stratégie.</p>

        <table>
            <tr>
                <th>Indicateur de performance</th>
                <th>Inspecteur débutant (0-6 mois)</th>
                <th>Inspecteur confirmé (6-24 mois)</th>
                <th>Inspecteur expert (24+ mois)</th>
            </tr>
            <tr>
                <td><strong>Volume mensuel d'inspections</strong></td>
                <td>5-12 inspections</td>
                <td>15-35 inspections</td>
                <td>40-70 inspections</td>
            </tr>
            <tr>
                <td><strong>Chiffre d'affaires mensuel brut</strong></td>
                <td>1 200-2 800€</td>
                <td>3 500-7 500€</td>
                <td>8 500-16 000€</td>
            </tr>
            <tr>
                <td><strong>Durée moyenne d'inspection</strong></td>
                <td>110-130 minutes</td>
                <td>80-100 minutes</td>
                <td>70-85 minutes</td>
            </tr>
            <tr>
                <td><strong>Taux de recommandation client</strong></td>
                <td>75-85%</td>
                <td>88-94%</td>
                <td>95-98%</td>
            </tr>
            <tr>
                <td><strong>Délai moyen de livraison rapport</strong></td>
                <td>36-48 heures</td>
                <td>18-24 heures</td>
                <td>8-12 heures</td>
            </tr>
            <tr>
                <td><strong>Taux de conversion prospect</strong></td>
                <td>15-25%</td>
                <td>30-40%</td>
                <td>45-60%</td>
            </tr>
            <tr>
                <td><strong>Panier moyen par inspection</strong></td>
                <td>180-220€</td>
                <td>220-280€</td>
                <td>280-350€</td>
            </tr>
        </table>

        <h4>Atteignable : Évaluer rigoureusement la faisabilité</h4>

        <p>Vos objectifs doivent être suffisamment ambitieux pour constituer un défi motivant, tout en restant réalistiquement atteignables compte tenu de vos contraintes personnelles, professionnelles et environnementales spécifiques. Cette évaluation de faisabilité nécessite une analyse honnête et approfondie de votre situation actuelle.</p>

        <p><strong>Contraintes temporelles personnelles :</strong> Évaluez précisément le temps hebdomadaire que vous pouvez réalistement consacrer à cette nouvelle activité, en tenant compte de vos obligations familiales, professionnelles et personnelles incompressibles. Une activité d'inspection à temps plein exige 35-45 heures/semaine (inspection + rédaction + commercial + administratif), tandis qu'une activité complémentaire peut fonctionner avec 12-20 heures/semaine mais limitera mécaniquement les volumes atteignables.</p>

        <p><strong>Contraintes financières d'investissement :</strong> Chiffrez précisément le budget que vous pouvez mobiliser pour le démarrage, incluant matériel de diagnostic (1500-5000€), véhicule professionnel adapté (si nécessaire), assurance RC professionnelle (1200-2500€/an), communication et marketing (500-2000€), formation complémentaire éventuelle (500-1500€). L'investissement initial total varie généralement de 5000€ (démarrage minimal) à 20000€ (équipement professionnel complet).</p>

        <p><strong>Contraintes géographiques de marché :</strong> Analysez objectivement la densité de votre marché local : nombre de transactions automobiles annuelles, niveau socioéconomique de la population, présence concurrentielle, accessibilité géographique. Une zone rurale impose des déplacements plus longs et coûteux, limitant le nombre d'interventions quotidiennes possibles, tandis qu'une zone urbaine dense offre plus d'opportunités mais génère aussi plus de concurrence.</p>

        <h4>Réaliste : Ancrer dans l'analyse de marché</h4>

        <p>Vos objectifs doivent impérativement s'appuyer sur une analyse factuelle et rigoureuse du marché local et de ses dynamiques réelles, évitant tout optimisme béat ou pessimisme paralysant. Cette analyse de marché constitue le socle indispensable de votre stratégie de développement.</p>

        <div class="warning-box">
            <h4>📈 Données de marché indispensables à analyser</h4>
            <ul>
                <li><strong>Taille du marché local quantifiée :</strong> Nombre exact de transactions VO annuelles dans votre zone d'intervention (données préfecture + professionnels)</li>
                <li><strong>Analyse concurrentielle exhaustive :</strong> Identification de tous les inspecteurs actifs, analyse de leurs tarifs, positionnement, forces/faiblesses</li>
                <li><strong>Évaluation de la demande potentielle :</strong> Enquêtes directes auprès de clients potentiels, sondages professionnels, analyse des tendances</li>
                <li><strong>Projection d'évolution du marché :</strong> Tendances démographiques, évolutions réglementaires prévisibles, impact des nouveaux usages (électrique, autopartage)</li>
                <li><strong>Analyse des partenaires potentiels :</strong> Garages, concessions, mandataires, assureurs, plateformes digitales susceptibles de prescrire vos services</li>
            </ul>
        </div>

        <h4>Temporellement défini : Planifier méthodiquement les étapes</h4>

        <p>Votre projet doit s'inscrire dans un calendrier précis et réaliste, jalonné d'étapes intermédiaires mesurables permettant de suivre votre progression et d'ajuster votre stratégie en fonction des résultats obtenus. Cette planification temporelle structure votre démarche et maintient votre motivation par l'atteinte d'objectifs intermédiaires réguliers.</p>

        <div class="success-box">
            <h4>🗓️ Planning type de déploiement professionnel</h4>
            <ul>
                <li><strong>Mois 1 - Formation et certification :</strong> Suivi intégral formation AutoJust, réussite certification, acquisition connaissances fondamentales</li>
                <li><strong>Mois 2 - Structuration juridique :</strong> Création structure juridique optimisée, souscription assurances professionnelles, ouverture comptes dédiés</li>
                <li><strong>Mois 3 - Équipement et communication :</strong> Acquisition matériel diagnostic, création supports communication, développement présence digitale</li>
                <li><strong>Mois 4-6 - Démarrage commercial :</strong> Prospection intensive, premiers clients, rodage méthodologique, ajustements opérationnels</li>
                <li><strong>Mois 7-12 - Montée en puissance :</strong> Développement volume d'activité, fidélisation clientèle, optimisation processus, première rentabilité</li>
                <li><strong>Année 2 - Consolidation et spécialisation :</strong> Stabilisation activité, développement spécialisation éventuelle, expansion géographique ou diversification services</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 6 : Cas pratiques introductifs (annonces, mise en situation)</h3>

        <p>Pour conclure efficacement ce module fondamental de diagnostic et positionnement, nous vous proposons une série de cas pratiques introductifs soigneusement sélectionnés qui vous permettront de vous projeter concrètement et réalistement dans les situations professionnelles variées et complexes que vous rencontrerez quotidiennement en tant qu'inspecteur automobile certifié AutoJust. Ces cas, issus de notre base de données de plus de 10 000 inspections réelles, illustrent la diversité des missions et la richesse des défis techniques et relationnels du métier.</p>

        <h4>Cas pratique n°1 : Analyse d'une annonce suspecte en ligne</h4>

        <div class="tip-box">
            <h4>📄 Annonce Leboncoin analysée</h4>
            <p><strong>Titre accrocheur :</strong> "BMW 320d 2018, 45 000 km, état impeccable, cause déménagement urgent"</p>
            <p><strong>Prix attractif :</strong> 18 500€ (prix de marché Argus : 21 800€ - décote de 15%)</p>
            <p><strong>Description séduisante :</strong> "Véhicule en parfait état général, jamais accidenté, carnet d'entretien BMW intégralement respecté, pneumatiques Michelin neufs (4000€), révision complète récente (850€), toutes factures disponibles. Cause déménagement professionnel urgent à l'étranger, vente rapide souhaitée. Véhicule visible sur rendez-vous uniquement."</p>
            <p><strong>Documentation photographique :</strong> 4 photos extérieures prises par temps ensoleillé sous éclairage favorable, aucune photo d'intérieur, aucune vue du compartiment moteur, aucun détail des documents.</p>
            <p><strong>Profil vendeur :</strong> Compte créé récemment (3 semaines), 2 évaluations positives seulement, localisation approximative.</p>
        </div>

        <p><strong>Signaux d'alerte détaillés identifiés :</strong></p>

        <ul>
            <li><strong>Prix significativement sous-évalué :</strong> Décote de 15% par rapport au marché sans justification technique apparente, technique classique d'attraction commerciale</li>
            <li><strong>Justification émotionnelle non vérifiable :</strong> "Déménagement urgent" impossible à confirmer, crée une pression temporelle artificielle sur l'acheteur</li>
            <li><strong>Documentation photographique orientée :</strong> Photos limitées et soigneusement sélectionnées, absence volontaire de vues compromettantes</li>
            <li><strong>Absence systématique de défauts :</strong> Aucun véhicule de 5 ans n'est "parfait", cette présentation manque de crédibilité</li>
            <li><strong>Profil vendeur peu rassurant :</strong> Compte récent et peu d'historique, manque de références et de crédibilité</li>
            <li><strong>Disponibilité restrictive :</strong> Visite "sur rendez-vous uniquement" peut masquer une indisponibilité réelle du véhicule</li>
        </ul>

        <p><strong>Méthodologie d'investigation recommandée :</strong> Dans ce contexte à risque élevé, votre intervention d'inspecteur professionnel devient cruciale pour sécuriser la transaction. Vous devrez mener une investigation approfondie incluant vérification documentaire complète (carte grise, factures, historique), inspection technique exhaustive recherchant spécifiquement les signes d'accident ou de réparations masquées, et validation de la cohérence entre l'annonce et la réalité du véhicule.</p>

        <p><strong>Valeur ajoutée client :</strong> Votre expertise permettra soit de rassurer l'acheteur sur la qualité réelle du véhicule (si conforme), soit de lui éviter un achat risqué (si non conforme), soit de négocier un prix plus juste en fonction des défauts réellement identifiés.</p>

        <h4>Cas pratique n°2 : Expertise contradictoire pour assurance</h4>

        <p><strong>Contexte détaillé :</strong> Sinistre déclaré par M. Dubois, assuré depuis 8 ans sans antécédent - "Collision avec sanglier sur autoroute A6 sens Lyon-Paris, PK 345, le 15 novembre 2023 vers 22h30". La compagnie d'assurance AXA mandate une expertise contradictoire car plusieurs éléments éveillent ses soupçons : dégâts déclarés disproportionnés pour ce type d'accident, localisation inhabituelle pour la présence de sangliers, déclaration tardive (4 jours après l'événement prétendu).</p>

        <p><strong>Véhicule expertisé :</strong> Audi Q5 TDI 190 S-Line 2020, 28 500 km au compteur, valeur estimée 42 000€</p>
        <p><strong>Dégâts déclarés par l'assuré :</strong> Pare-chocs avant déformé, projecteur LED droit brisé, capot enfoncé côté droit, calandre cassée</p>
        <p><strong>Estimation réparateur agréé :</strong> 8 650€ TTC (pièces d'origine + main d'œuvre + peinture)</p>

        <p><strong>Mission d'expertise approfondie :</strong></p>
        <ul>
            <li><strong>Analyse de cohérence technique :</strong> Vérifier la compatibilité entre les dégâts observés et le type de collision déclarée (impact animal)</li>
            <li><strong>Investigation forensique :</strong> Rechercher les traces d'impacts antérieurs, analyser la géométrie des déformations, examiner les zones de corrosion suspectes</li>
            <li><strong>Expertise matériaux :</strong> Vérifier l'authenticité des pièces endommagées, détecter d'éventuels remplacements récents non déclarés</li>
            <li><strong>Documentation exhaustive :</strong> Photographier sous tous les angles, relever les numéros de série, noter toute anomalie</li>
            <li><strong>Rapport contradictoire :</strong> Produire une expertise technique détaillée susceptible d'être utilisée en procédure judiciaire</li>
        </ul>

        <p><strong>Enjeux professionnels :</strong> Ce type de mission exige une expertise technique de très haut niveau, une parfaite connaissance des techniques de fraude à l'assurance les plus sophistiquées, et une capacité de rédaction juridique rigoureuse. Les conclusions de votre expertise peuvent déclencher des poursuites pénales ou des remboursements de dizaines de milliers d'euros.</p>

        <p><strong>Rémunération spécialisée :</strong> Les expertises contradictoires pour assurances se facturent généralement entre 400 et 800€ selon la complexité, avec possibilité de facturation supplémentaire en cas de comparution devant un tribunal.</p>

        <h4>Cas pratique n°3 : Inspection pré-achat véhicule de collection</h4>

        <p><strong>Contexte passionné :</strong> M. Bertrand, collectionneur confirmé et président du club Porsche Île-de-France, souhaite acquérir une Porsche 911 Carrera 3.2 de 1989 proposée à 68 000€ par un marchand spécialisé de Reims. Cette acquisition représente un investissement patrimonial significatif dans le contexte d'un marché des youngtimers en forte croissance (+12% par an depuis 5 ans).</p>

        <p><strong>Spécificités techniques du véhicule :</strong></p>
        <ul>
            <li>Porsche 911 Carrera 3.2 G50, millésime 1989 (dernière année G50)</li>
            <li>134 000 km compteur, historique de 3 propriétaires successifs</li>
            <li>Teinte Guards Red classique, intérieur cuir noir</li>
            <li>Modifications déclarées : amortisseurs Bilstein, silencieux Supersprint</li>
            <li>Restauration moteur annoncée en 2018 (facture 12 000€)</li>
        </ul>

        <p><strong>Particularités d'expertise collection :</strong></p>
        <ul>
            <li><strong>Authentification historique :</strong> Vérification de la cohérence entre numéro de châssis, moteur, et boîte avec les registres Porsche</li>
            <li><strong>Évaluation des modifications :</strong> Impact sur la valeur et l'authenticité, réversibilité des transformations</li>
            <li><strong>État de conservation :</strong> Analyse fine de la corrosion (zones critiques connues), qualité des restaurations antérieures</li>
            <li><strong>Potentiel d'évolution :</strong> Estimation de la valorisation future selon l'état actuel et les tendances de marché</li>
            <li><strong>Conseil en restauration :</strong> Priorités d'intervention, budget prévisionnel, impact sur la valeur patrimoniale</li>
        </ul>

        <p><strong>Défis techniques spécifiques :</strong></p>
        <ul>
            <li>Maîtrise de l'historique technique des 911 G (évolutions annuelles, défauts récurrents, cotes de référence)</li>
            <li>Réseau professionnel spécialisé (experts Porsche, restaurateurs référencés, pièces d'origine)</li>
            <li>Connaissance du marché collection (évolutions de cotes, critères de valorisation, tendances futures)</li>
            <li>Capacité de conseil patrimonial (fiscalité collection, assurance valeur agréée, stockage optimal)</li>
        </ul>

        <p><strong>Rémunération spécialisée :</strong> Les inspections de véhicules de collection se facturent généralement entre 350 et 600€, avec possibilité de missions complémentaires (suivi de restauration, réévaluation périodique, conseil en acquisition).</p>

        <h4>Cas pratique n°4 : Audit de parc pour entreprise</h4>

        <p><strong>Contexte professionnel B2B :</strong> La société GEODIS (logistique), possédant un parc de 45 véhicules utilitaires légers, souhaite faire auditer l'état de son parc avant renouvellement partiel. Objectif : optimiser la stratégie de renouvellement en identifiant les véhicules à conserver, à réviser ou à remplacer prioritairement.</p>

        <p><strong>Enjeux économiques :</strong> Budget annuel de renouvellement 180 000€, possibilité d'économies substantielles par optimisation du planning de renouvellement basé sur l'état technique réel plutôt que sur l'âge comptable.</p>

        <p><strong>Méthodologie d'audit de parc :</strong></p>
        <ul>
            <li>Inspection standardisée de chaque véhicule (45 minutes/véhicule)</li>
            <li>Grille d'évaluation spécifique utilitaires (usure, sécurité, fiabilité)</li>
            <li>Chiffrage des interventions nécessaires par véhicule</li>
            <li>Classement par priorité de renouvellement</li>
            <li>Rapport de synthèse avec recommandations stratégiques</li>
        </ul>

        <p><strong>Rémunération mission :</strong> Facturation forfaitaire 4500€ pour l'audit complet du parc (45 véhicules), soit 100€/véhicule, réalisable sur 3 jours avec assistant.</p>

        <img src="https://images.pexels.com/photos/4489749/pexels-photo-4489749.jpeg" alt="Inspection professionnelle en cours" class="module-image" />

        <div class="success-box">
            <h4>🎯 Objectifs pédagogiques atteints à l'issue de ce module</h4>
            <p>À l'issue de ce premier module fondamental, vous devriez avoir acquis et maîtrisé :</p>
            <ul>
                <li>✅ <strong>Auto-évaluation précise</strong> de votre niveau technique actuel selon 8 domaines d'expertise</li>
                <li>✅ <strong>Identification claire</strong> de votre profil d'apprenant parmi les 6 profils types validés statistiquement</li>
                <li>✅ <strong>Définition rigoureuse</strong> d'objectifs SMART personnalisés et réalisables</li>
                <li>✅ <strong>Compréhension approfondie</strong> des enjeux économiques et techniques de la profession</li>
                <li>✅ <strong>Anticipation réaliste</strong> des situations professionnelles futures et de leur complexité</li>
                <li>✅ <strong>Vision stratégique</strong> de votre développement professionnel à moyen terme</li>
                <li>✅ <strong>Motivation renforcée</strong> par la compréhension du potentiel du métier</li>
            </ul>
        </div>

        <p><strong>Transition vers le module suivant :</strong> Fort de ce diagnostic personnalisé et de cette vision claire de vos objectifs, vous êtes maintenant prêt à aborder le Module 2 qui vous permettra d'approfondir considérablement les fondamentaux de l'inspection automobile et de comprendre avec précision le rôle, les missions et les responsabilités de l'inspecteur professionnel dans l'écosystème automobile moderne.</p>

        <p><em>Durée totale de lecture estimée : 45-60 minutes selon votre profil | Quiz de validation : 12 questions | Temps recommandé pour l'auto-évaluation : 20 minutes supplémentaires</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Combien de véhicules d'occasion sont vendus annuellement en France ?",
                "options": ["3,5 millions", "5,2 millions", "7,1 millions", "8,9 millions"],
                "correct_answer": "5,2 millions"
            },
            {
                "id": "q2",
                "question": "Quel pourcentage de véhicules d'occasion fait actuellement l'objet d'une inspection ?",
                "options": ["5%", "15%", "25%", "35%"],
                "correct_answer": "15%"
            },
            {
                "id": "q3",
                "question": "Quel est le tarif moyen d'une inspection automobile ?",
                "options": ["100-150€", "200-300€", "350-400€", "450-500€"],
                "correct_answer": "200-300€"
            },
            {
                "id": "q4",
                "question": "Combien de temps dure approximativement une inspection complète ?",
                "options": ["60 minutes", "90 minutes", "120 minutes", "150 minutes"],
                "correct_answer": "90 minutes"
            },
            {
                "id": "q5",
                "question": "Quelle est la première qualité d'un inspecteur automobile ?",
                "options": ["Rapidité", "Impartialité", "Convivialité", "Flexibilité"],
                "correct_answer": "Impartialité"
            },
            {
                "id": "q6",
                "question": "Le parcours 'Renforcé' est recommandé pour quel profil ?",
                "options": ["Mécaniciens expérimentés", "Contrôleurs techniques", "Débutants", "Commerciaux auto"],
                "correct_answer": "Débutants"
            },
            {
                "id": "q7",
                "question": "Combien de points de contrôle comprend la méthodologie AutoJust ?",
                "options": ["150+", "200+", "250+", "300+"],
                "correct_answer": "200+"
            },
            {
                "id": "q8",
                "question": "Quel est le seuil de réussite pour les quiz de modules ?",
                "options": ["60%", "70%", "80%", "90%"],
                "correct_answer": "70%"
            },
            {
                "id": "q9",
                "question": "La formation continue est-elle obligatoire pour un inspecteur ?",
                "options": ["Non, pas nécessaire", "Recommandée", "Indispensable", "Uniquement la première année"],
                "correct_answer": "Indispensable"
            },
            {
                "id": "q10",
                "question": "Quel niveau permet de diagnostiquer des pannes courantes ?",
                "options": ["Débutant", "Intermédiaire", "Avancé", "Expert"],
                "correct_answer": "Intermédiaire"
            },
            {
                "id": "q11",
                "question": "L'inspecteur doit-il résister aux pressions commerciales ?",
                "options": ["Non, il doit s'adapter", "Parfois", "Oui, absolument", "Cela dépend du client"],
                "correct_answer": "Oui, absolument"
            },
            {
                "id": "q12",
                "question": "Combien de questions comprend l'examen final ?",
                "options": ["30 questions", "40 questions", "50 questions", "60 questions"],
                "correct_answer": "50 questions"
            }
        ]
    },
    {
        "id": "module-2",
        "title": "Fondamentaux de l'Inspection",
        "description": "Rôle, missions, cadre réglementaire et déontologie de l'inspecteur automobile",
        "duration_minutes": 90,
        "order": 2,
        "content": """
        <h2>Module 2 : Fondamentaux de l'Inspection Automobile</h2>
        
        <img src="https://images.unsplash.com/photo-1487754180451-c456f719a1fc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Fondamentaux inspection automobile" class="module-image" />
        
        <div class="chapter-divider"></div>

        <h3>Chapitre 1 : Le rôle de l'inspecteur (différence avec expert judiciaire)</h3>

        <p>L'inspecteur automobile professionnel occupe une position unique et stratégique dans l'écosystème complexe des transactions automobiles contemporaines. Contrairement aux idées reçues qui tendent à confondre les différents acteurs de l'expertise automobile, l'inspecteur privé possède un statut juridique, des prérogatives et des responsabilités spécifiques qui le distinguent nettement de l'expert judiciaire, de l'expert d'assurance ou encore du contrôleur technique réglementaire.</p>

        <p>Cette distinction fondamentale n'est pas qu'une subtilité juridique : elle détermine concrètement la portée de votre intervention, la valeur probante de vos conclusions, les conditions de votre responsabilité professionnelle et, ultimement, la stratégie de développement de votre activité. Une compréhension imparfaite de ces nuances peut conduire à des erreurs de positionnement coûteuses et à des situations de responsabilité non maîtrisées.</p>

        <div class="info-box">
            <h4>🎯 L'inspecteur automobile privé : définition et prérogatives</h4>
            <p>L'inspecteur automobile privé est un <strong>expert technique indépendant</strong> mandaté par contrat privé pour évaluer l'état d'un véhicule selon des critères objectifs et une méthodologie standardisée. Ses prérogatives incluent :</p>
            <ul>
                <li><strong>Inspection technique non destructive :</strong> Examen complet sans démontage ni altération du véhicule</li>
                <li><strong>Diagnostic instrumental :</strong> Utilisation d'outils de mesure et de diagnostic électronique</li>
                <li><strong>Évaluation comparative :</strong> Positionnement par rapport aux standards de marché</li>
                <li><strong>Conseil personnalisé :</strong> Recommandations adaptées au profil et aux besoins du client</li>
                <li><strong>Documentation probante :</strong> Constitution d'un dossier photographique et technique détaillé</li>
                <li><strong>Formation du client :</strong> Explication pédagogique des constats techniques</li>
            </ul>
        </div>

        <h4>Distinction fondamentale avec l'expert judiciaire</h4>

        <p>La confusion entre inspecteur privé et expert judiciaire constitue l'une des erreurs les plus fréquentes et les plus préjudiciables dans la compréhension du métier. Cette confusion, entretenue parfois par certains praticiens peu scrupuleux, peut conduire à des situations de responsabilité délicate et compromettre la crédibilité professionnelle.</p>

        <table>
            <tr>
                <th>Critère de distinction</th>
                <th>Inspecteur automobile privé</th>
                <th>Expert judiciaire</th>
                <th>Conséquences pratiques</th>
            </tr>
            <tr>
                <td><strong>Base légale d'intervention</strong></td>
                <td>Contrat de droit privé librement négocié</td>
                <td>Ordonnance du juge, mission légale</td>
                <td>Liberté contractuelle vs contrainte judiciaire</td>
            </tr>
            <tr>
                <td><strong>Indépendance vis-à-vis des parties</strong></td>
                <td>Mandaté par l'une des parties</td>
                <td>Indépendant des deux parties</td>
                <td>Partialité assumée vs neutralité absolue</td>
            </tr>
            <tr>
                <td><strong>Valeur probante du rapport</strong></td>
                <td>Simple renseignement technique</td>
                <td>Présomption de validité renforcée</td>
                <td>Contestation aisée vs force probante</td>
            </tr>
            <tr>
                <td><strong>Procédure contradictoire</strong></td>
                <td>Non obligatoire, unilatérale</td>
                <td>Obligatoire, contradictoire</td>
                <td>Souplesse procédurale vs rigueur judiciaire</td>
            </tr>
            <tr>
                <td><strong>Serment professionnel</strong></td>
                <td>Code de déontologie privé</td>
                <td>Serment devant le tribunal</td>
                <td>Engagement moral vs engagement judiciaire</td>
            </tr>
            <tr>
                <td><strong>Délais d'intervention</strong></td>
                <td>Librement négociés (24-48h typique)</td>
                <td>Imposés par le tribunal (30-90 jours)</td>
                <td>Réactivité commerciale vs contrainte judiciaire</td>
            </tr>
        </table>

        <h4>Positionnement professionnel optimal</h4>

        <p>Cette distinction claire permet de définir un positionnement professionnel optimal qui exploite les avantages spécifiques de l'inspection privée : réactivité, personnalisation du service, proximité client, flexibilité méthodologique, tout en assumant les limites inhérentes : valeur probante limitée, partialité assumée, responsabilité contractuelle.</p>

        <p>L'inspecteur privé intelligent ne cherche pas à singer l'expert judiciaire, mais développe sa valeur ajoutée spécifique : rapidité d'intervention, conseil personnalisé, accompagnement dans la décision, formation technique du client, service après-vente. Cette approche différenciée permet de justifier une tarification premium et de fidéliser durablement la clientèle.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Valeur ajoutée pour le client (sécuriser, rassurer, anticiper)</h3>

        <p>La valeur ajoutée de l'inspecteur automobile ne se limite pas à la simple vérification technique du véhicule, mais englobe un ensemble de services à haute valeur ajoutée qui transforment l'expérience d'achat du client et sécurisent significativement son investissement. Cette valeur ajoutée multifacette justifie la tarification professionnelle et différencie nettement l'inspecteur certifié AutoJust des solutions alternatives (inspection amateur, vérification rapide, conseil gratuit).</p>

        <h4>Sécurisation technique et financière de l'investissement</h4>

        <p>La sécurisation technique constitue la mission première et la plus visible de l'inspecteur, mais sa portée dépasse largement la simple détection de pannes. Il s'agit d'une véritable évaluation prospective qui permet au client de prendre sa décision d'achat en connaissance de cause complète.</p>

        <div class="success-box">
            <h4>🛡️ Dimensions de la sécurisation technique</h4>
            <ul>
                <li><strong>Détection des vices cachés :</strong> Identification des défauts non visibles à l'œil nu mais susceptibles d'engendrer des coûts importants (joint de culasse, boîte de vitesses, électronique défaillante)</li>
                <li><strong>Évaluation de l'usure prévisionnelle :</strong> Anticipation des interventions d'entretien et de réparation nécessaires à court et moyen terme</li>
                <li><strong>Analyse de cohérence :</strong> Vérification de la cohérence entre kilométrage affiché, état d'usure, historique d'entretien et prix demandé</li>
                <li><strong>Identification des non-conformités :</strong> Détection des modifications non déclarées, des réparations non conformes, des équipements manquants</li>
                <li><strong>Évaluation de la sécurité :</strong> Contrôle rigoureux des équipements de sécurité active et passive</li>
                <li><strong>Chiffrage prévisionnel :</strong> Estimation budgétaire des interventions nécessaires sur 12, 24 et 36 mois</li>
            </ul>
        </div>

        <p>L'impact financier de cette sécurisation est considérable : nos statistiques démontrent que l'inspection professionnelle permet d'éviter en moyenne 3 200€ de coûts cachés par véhicule inspecté, soit un retour sur investissement de 16:1 par rapport au coût de l'inspection. Cette performance statistique, mesurée sur plus de 8 000 inspections suivies pendant 24 mois, constitue l'argument commercial le plus puissant de notre métier.</p>

        <h4>Réassurance psychologique et accompagnement décisionnel</h4>

        <p>Au-delà de l'aspect purement technique, l'inspecteur joue un rôle psychologique fondamental dans le processus d'achat automobile. L'achat d'un véhicule d'occasion génère naturellement stress et incertitude chez la plupart des acheteurs, particulièrement les non-spécialistes. L'intervention d'un professionnel neutre et compétent transforme cette angoisse en confiance et facilite grandement la prise de décision.</p>

        <p>Cette dimension psychologique, souvent sous-estimée par les inspecteurs focalisés sur la technique, représente pourtant une part significative de la valeur perçue par le client. Elle justifie un investissement particulier dans les compétences relationnelles et de communication, souvent négligées dans les formations techniques traditionnelles.</p>

        <div class="tip-box">
            <h4>💭 Mécanismes psychologiques de la réassurance</h4>
            <ul>
                <li><strong>Réduction de l'asymétrie d'information :</strong> L'inspecteur comble le déficit de connaissances techniques du client non spécialisé</li>
                <li><strong>Transfert de responsabilité :</strong> Le client partage la responsabilité de la décision avec un professionnel compétent</li>
                <li><strong>Validation externe :</strong> Confirmation par un tiers de la qualité de son choix</li>
                <li><strong>Anticipation des regrets :</strong> Prévention du sentiment de regret post-achat par une décision éclairée</li>
                <li><strong>Confiance en l'avenir :</strong> Sérénité concernant les évolutions futures du véhicule</li>
            </ul>
        </div>

        <img src="https://images.unsplash.com/photo-1498887960847-2a5e46312788?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Conseil expert et accompagnement" class="module-image" />

        <h4>Anticipation et conseil prospectif</h4>

        <p>L'inspecteur automobile moderne ne se contente plus de dresser un constat statique à l'instant T, mais développe une approche prospective qui anticipe l'évolution du véhicule et conseille le client sur la stratégie d'entretien optimale. Cette dimension prévisionnelle, s'appuyant sur une base de données de retours d'expérience considérable, constitue la différenciation majeure par rapport à une simple inspection ponctuelle.</p>

        <p>Cette approche anticipatrice nécessite une connaissance approfondie des défaillances récurrentes par marque et modèle, des coûts de réparation actualisés, des stratégies d'entretien préventif efficaces et des évolutions technologiques susceptibles d'impact sur la valeur de revente future.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Les qualités essentielles (rigueur, observation, impartialité, pédagogie)</h3>

        <p>Le métier d'inspecteur automobile exige un ensemble de qualités professionnelles et personnelles spécifiques, dont la maîtrise conditionne directement la qualité du service rendu et, par conséquent, la réussite commerciale et professionnelle. Ces qualités, identifiées par l'analyse comportementale de nos 300+ inspecteurs certifiés les plus performants, se développent par la formation, la pratique et l'auto-évaluation continue.</p>

        <h4>Rigueur méthodologique et systémique</h4>

        <p>La rigueur constitue la qualité cardinale de l'inspecteur professionnel. Elle se manifeste à tous les niveaux : préparation de l'intervention, application de la méthodologie, documentation des constats, rédaction des conclusions, respect des engagements temporels. Cette rigueur n'est pas innée : elle se cultive, se structure et se maintient par des habitudes professionnelles appropriées.</p>

        <div class="info-box">
            <h4>🔬 Manifestations de la rigueur professionnelle</h4>
            <ul>
                <li><strong>Préparation systématique :</strong> Check-list matériel, documentation du véhicule, briefing client, plan d'intervention</li>
                <li><strong>Application méthodologique stricte :</strong> Respect de la séquence AutoJust, contrôle exhaustif des 200+ points, temps minimum par phase</li>
                <li><strong>Documentation exhaustive :</strong> Photographie systématique, prise de notes détaillées, mesures précises, horodatage</li>
                <li><strong>Vérifications croisées :</strong> Validation de la cohérence entre différents indices, recoupement des informations</li>
                <li><strong>Auto-contrôle final :</strong> Relecture critique, vérification de l'exhaustivité, validation de la cohérence globale</li>
            </ul>
        </div>

        <p>Cette rigueur méthodologique se traduit concrètement par des résultats mesurables : nos inspecteurs les plus rigoureux présentent un taux de réclamation client 5 fois inférieur à la moyenne, un taux de recommandation supérieur de 15%, et une progression de chiffre d'affaires plus rapide de 25% par rapport aux inspecteurs moins structurés.</p>

        <h4>Capacité d'observation fine et analytique</h4>

        <p>L'observation constitue l'outil de travail fondamental de l'inspecteur automobile. Mais il ne s'agit pas d'une simple capacité visuelle : il s'agit d'une compétence complexe combinant acuité visuelle, expérience technique, connaissance des défaillances typiques et capacité d'analyse systémique pour transformer des observations partielles en diagnostic global cohérent.</p>

        <p>Cette capacité d'observation se développe progressivement à travers l'expérience, mais peut être considérablement accélérée par une formation structurée et des exercices ciblés. Elle s'appuie sur plusieurs dimensions complémentaires :</p>

        <div class="success-box">
            <h4>👁️ Dimensions de l'observation professionnelle</h4>
            <ul>
                <li><strong>Observation visuelle directe :</strong> Détection des anomalies de forme, couleur, alignement, usure, corrosion</li>
                <li><strong>Observation auditive :</strong> Identification des bruits anormaux, régularité du fonctionnement, variations suspectes</li>
                <li><strong>Observation tactile :</strong> Évaluation des vibrations, températures, résistances mécaniques</li>
                <li><strong>Observation olfactive :</strong> Détection des odeurs caractéristiques (brûlé, carburant, liquides)</li>
                <li><strong>Observation contextuelle :</strong> Analyse de l'environnement, cohérence globale, indices annexes</li>
                <li><strong>Observation comparative :</strong> Référencement par rapport aux standards connus du modèle</li>
            </ul>
        </div>

        <h4>Impartialité et objectivité scientifique</h4>

        <p>L'impartialité représente probablement la qualité la plus délicate à maintenir dans l'exercice quotidien du métier d'inspecteur. Contrairement à l'expert judiciaire qui bénéficie d'un cadre procédural protecteur, l'inspecteur privé évolue dans un environnement commercial où les pressions, tentations et conflits d'intérêts sont permanents et subtils.</p>

        <p>Cette impartialité ne se décrète pas : elle se construit par la mise en place de garde-fous procéduraux, la formation éthique continue et l'adhésion à un code de déontologie strict et contrôlé. Elle constitue également un avantage commercial décisif : les clients font confiance aux inspecteurs réputés impartiaux et les recommandent massivement.</p>

        <div class="warning-box">
            <h4>⚖️ Menaces récurrentes contre l'impartialité</h4>
            <ul>
                <li><strong>Pressions économiques directes :</strong> Propositions de commissions, primes à la complaisance, menaces de non-paiement</li>
                <li><strong>Pressions relationnelles :</strong> Sympathie pour le vendeur/acheteur, relations personnelles, recommandations d'amis</li>
                <li><strong>Pressions temporelles :</strong> Urgence artificielle, pression à la conclusion rapide, chantage aux délais</li>
                <li><strong>Pressions techniques :</strong> Remise en cause de la compétence, contest ation des méthodes, intimidation technique</li>
                <li><strong>Auto-persuasion :</strong> Rationalisation de conclusions orientées, biais de confirmation, évitement de conflits</li>
            </ul>
        </div>

        <h4>Pédagogie et vulgarisation technique</h4>

        <p>La capacité pédagogique distingue l'inspecteur professionnel accompli du simple technicien compétent. Face à une clientèle majoritairement non spécialisée, l'inspecteur doit savoir vulgariser des concepts techniques complexes, expliquer clairement ses constats et recommandations, et former le client aux bonnes pratiques d'entretien et d'utilisation.</p>

        <p>Cette dimension pédagogique nécessite des compétences spécifiques rarement enseignées dans les formations techniques traditionnelles : structuration du discours, adaptation au niveau de l'interlocuteur, utilisation d'analogies parlantes, support visuel efficace, vérification de la compréhension.</p>

        <img src="https://images.unsplash.com/photo-1606577924006-27d39b132ae2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Communication pédagogique client" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : Préparation et sécurité de l'inspecteur</h3>

        <p>La préparation de l'intervention d'inspection et la sécurité de l'inspecteur constituent des aspects fondamentaux trop souvent négligés dans les formations d'initiation. Ces éléments, qui peuvent paraître secondaires aux yeux du débutant, conditionnent pourtant directement la qualité de l'inspection, la sécurité juridique de l'intervention et, ultimement, la pérennité de l'activité professionnelle.</p>

        <h4>Préparation technique et logistique de l'intervention</h4>

        <p>Une intervention d'inspection réussie commence 24 heures avant la rencontre avec le client. Cette préparation minutieuse, chronophage initialement mais rapidement rentabilisée, comprend plusieurs phases distinctes et complémentaires :</p>

        <div class="info-box">
            <h4>📋 Check-list de préparation pré-intervention (24h avant)</h4>
            <ol>
                <li><strong>Recherche documentaire du véhicule :</strong>
                    <ul>
                        <li>Fiche technique constructeur complète</li>
                        <li>Défauts récurrents connus pour ce modèle/millésime</li>
                        <li>Bulletins de rappel constructeur éventuels</li>
                        <li>Cote Argus actualisée et historique des prix</li>
                        <li>Spécificités techniques de la version exacte</li>
                    </ul>
                </li>
                <li><strong>Préparation matérielle :</strong>
                    <ul>
                        <li>Vérification charge batteries des appareils</li>
                        <li>Test fonctionnel valise de diagnostic</li>
                        <li>Nettoyage et calibrage des instruments de mesure</li>
                        <li>Préparation des consommables (gants, lingettes, étiquettes)</li>
                        <li>Synchronisation applications mobiles</li>
                    </ul>
                </li>
                <li><strong>Planification logistique :</strong>
                    <ul>
                        <li>Itinéraire optimisé et temps de trajet calculé</li>
                        <li>Coordonnées client vérifiées et confirmées</li>
                        <li>Lieu d'inspection validé (éclairage, sécurité, accessibilité)</li>
                        <li>Conditions météorologiques vérifiées</li>
                        <li>Planning de la journée optimisé</li>
                    </ul>
                </li>
            </ol>
        </div>

        <h4>Sécurité physique et juridique de l'inspecteur</h4>

        <p>L'activité d'inspection automobile expose l'inspecteur à des risques multiples qu'une préparation appropriée permet de minimiser significativement. Ces risques, souvent sous-évalués par les débutants, peuvent avoir des conséquences graves sur la santé, la sécurité et la responsabilité professionnelle.</p>

        <table>
            <tr>
                <th>Type de risque</th>
                <th>Manifestations courantes</th>
                <th>Mesures préventives</th>
                <th>Équipement requis</th>
            </tr>
            <tr>
                <td><strong>Risques mécaniques</strong></td>
                <td>Coupures, pincements, chutes</td>
                <td>EPI adaptés, gestes sécurisés</td>
                <td>Gants, chaussures sécurité</td>
            </tr>
            <tr>
                <td><strong>Risques chimiques</strong></td>
                <td>Contact liquides, vapeurs toxiques</td>
                <td>Ventilation, protection individuelle</td>
                <td>Gants nitrile, lunettes</td>
            </tr>
            <tr>
                <td><strong>Risques routiers</strong></td>
                <td>Accident lors essai routier</td>
                <td>Vérifications préalables, prudence</td>
                <td>Assurance étendue</td>
            </tr>
            <tr>
                <td><strong>Risques juridiques</strong></td>
                <td>Mise en cause responsabilité</td>
                <td>RC Pro, documentation rigoureuse</td>
                <td>Contrats, assurance</td>
            </tr>
            <tr>
                <td><strong>Risques commerciaux</strong></td>
                <td>Impayés, contestations abusives</td>
                <td>Contrat écrit, acompte</td>
                <td>Conditions générales</td>
            </tr>
        </table>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Outils indispensables (lampe, OBD-II, carnet numérique)</h3>

        <p>L'évolution technologique de l'automobile moderne impose une mise à niveau constante de l'outillage professionnel de l'inspecteur. Les outils d'hier, suffisants pour les véhicules des années 1990-2000, deviennent rapidement obsolètes face à la sophistication croissante des systèmes embarqués. Cette section détaille les outils indispensables, leurs caractéristiques techniques recommandées et leurs modalités d'utilisation optimales.</p>

        <h4>Éclairage professionnel et inspection visuelle</h4>

        <p>L'éclairage constitue l'outil le plus fondamental et le plus universellement utilisé de l'inspecteur automobile. Paradoxalement, c'est aussi l'un des plus négligés par les inspecteurs débutants, qui sous-estiment son impact sur la qualité de l'inspection et la détection des défauts subtils.</p>

        <div class="success-box">
            <h4>💡 Spécifications techniques éclairage professionnel</h4>
            <ul>
                <li><strong>Lampe torche principale :</strong> LED 2000+ lumens, température couleur 6000K, autonomie 4h minimum, résistance IP67</li>
                <li><strong>Lampe d'inspection fine :</strong> LED 500 lumens, faisceau focalisé, autonomie 8h, résistance chocs</li>
                <li><strong>Projecteur de zone :</strong> LED 5000+ lumens, éclairage large, support stable, alimentation 12V/220V</li>
                <li><strong>Lampe UV (optionnel) :</strong> Détection liquides invisibles, vérification peinture, authentification</li>
            </ul>
        </div>

        <h4>Diagnostic électronique : valises OBD-II et évolutions</h4>

        <p>Le diagnostic électronique représente le domaine d'évolution le plus rapide et le plus critique pour l'inspecteur moderne. La multiplication des calculateurs, l'interconnexion des systèmes via les réseaux CAN/LIN/Ethernet, l'émergence de l'intelligence artificielle embarquée transforment radicalement les méthodes de diagnostic et les exigences en matière d'outillage.</p>

        <table>
            <tr>
                <th>Catégorie d'outil</th>
                <th>Équipement de base</th>
                <th>Équipement professionnel</th>
                <th>Équipement expert</th>
                <th>Coût approximatif</th>
            </tr>
            <tr>
                <td><strong>Valise OBD générique</strong></td>
                <td>ELM327 Bluetooth</td>
                <td>Autel MP808 / Launch CRP919</td>
                <td>Bosch KTS / Texa Navigator</td>
                <td>25€ à 8 000€</td>
            </tr>
            <tr>
                <td><strong>Mesures électriques</strong></td>
                <td>Multimètre basique</td>
                <td>Fluke 117 / Metrix MX58</td>
                <td>Oscilloscope automobile</td>
                <td>30€ à 2 500€</td>
            </tr>
            <tr>
                <td><strong>Tests spécialisés</strong></td>
                <td>Testeur batterie simple</td>
                <td>Testeur batterie/alternateur</td>
                <td>Analyseur réseau électrique</td>
                <td>50€ à 1 200€</td>
            </tr>
            <tr>
                <td><strong>Documentation</strong></td>
                <td>Smartphone + app gratuite</td>
                <td>Tablette + app professionnelle</td>
                <td>Système intégré + CRM</td>
                <td>0€ à 3 000€</td>
            </tr>
        </table>

        <h4>Digitalisation et carnet numérique</h4>

        <p>La transition vers le numérique représente une révolution méthodologique qui transforme fondamentalement l'efficacité, la traçabilité et la professionnalisation de l'inspection automobile. Cette digitalisation, initialement optionnelle, devient progressivement incontournable face aux exigences croissantes de qualité, rapidité et traçabilité des clients modernes.</p>

        <div class="tip-box">
            <h4>📱 Écosystème numérique AutoJust</h4>
            <ul>
                <li><strong>WebApp AutoJust mobile :</strong> Check-lists interactives, géolocalisation, synchronisation cloud automatique</li>
                <li><strong>WeProov constat :</strong> Photographie horodatée, géolocalisée et blockchainée juridiquement incontestable</li>
                <li><strong>iAuditor SafetyCulture :</strong> Check-lists intelligentes, scoring automatique, génération rapport instantané</li>
                <li><strong>CRM intégré :</strong> Gestion client, planning, facturation, suivi commercial automatisé</li>
                <li><strong>Base de données technique :</strong> Fiches véhicules, défauts récurrents, coûts de réparation actualisés</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 6 : Transparence et communication</h3>

        <p>La transparence et la communication constituent les piliers fondamentaux de la relation client moderne et les facteurs différenciants majeurs dans un marché de plus en plus concurrentiel. L'inspecteur automobile qui maîtrise ces dimensions développe un avantage concurrentiel durable et génère une fidélisation client exceptionnelle, source de développement commercial naturel et pérenne.</p>

        <h4>Transparence procédurale et méthodologique</h4>

        <p>La transparence dépasse largement la simple honnêteté : elle constitue une stratégie professionnelle globale qui vise à rendre totalement compréhensible et vérifiable l'ensemble du processus d'inspection. Cette approche, initialement plus chronophage, génère une confiance client exceptionnelle et prévient efficacement les contestations ultérieures.</p>

        <div class="info-box">
            <h4>🔍 Checklist transparence absolue</h4>
            <ul>
                <li><strong>Présentation méthodologique préalable :</strong> Explication détaillée des 200+ points AutoJust avant début d'inspection</li>
                <li><strong>Démonstration des outils :</strong> Présentation et test des appareils de diagnostic devant le client</li>
                <li><strong>Communication temporelle :</strong> Annonce préalable de la durée de chaque phase et respect scrupuleux</li>
                <li><strong>Tarification détaillée :</strong> Devis précis avec décomposition des prestations incluses/exclues</li>
                <li><strong>Engagement de délai :</strong> Promesse écrite de remise du rapport dans le délai annoncé</li>
                <li><strong>Disponibilité post-inspection :</strong> Engagement de réponse aux questions pendant 30 jours</li>
                <li><strong>Traçabilité complète :</strong> Horodatage de chaque phase, géolocalisation, photos datées</li>
            </ul>
        </div>

        <h4>Communication adaptée et personnalisée</h4>

        <p>La communication efficace s'adapte systématiquement au profil du client, à ses connaissances techniques, à ses préoccupations spécifiques et à son style de décision. Cette personnalisation, basée sur une écoute active et une observation fine du comportement client, multiplie l'impact des recommandations et facilite l'acceptation des conclusions défavorables.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 7 : Exercices pratiques (analyse d'annonce, observation terrain)</h3>

        <p>L'apprentissage théorique des fondamentaux doit impérativement être complété par des exercices pratiques qui permettent l'appropriation concrète des concepts étudiés et le développement des réflexes professionnels indispensables. Cette section propose une série d'exercices progressifs, du plus simple au plus complexe, calibrés selon les différents profils d'apprenants identifiés.</p>

        <h4>Exercice 1 : Analyse critique d'annonces en ligne</h4>

        <p>Cet exercice fondamental développe votre capacité à détecter les signaux d'alerte dans les annonces de vente, compétence essentielle pour orienter efficacement vos investigations et optimiser votre temps d'inspection.</p>

        <div class="tip-box">
            <h4>🕵️ Grille d'analyse des annonces</h4>
            <table>
                <tr>
                    <th>Élément d'analyse</th>
                    <th>Signal positif</th>
                    <th>Signal neutre</th>
                    <th>Signal d'alerte</th>
                </tr>
                <tr>
                    <td><strong>Prix vs marché</strong></td>
                    <td>±5% de l'Argus</td>
                    <td>±10% justifié</td>
                    <td>>15% d'écart</td>
                </tr>
                <tr>
                    <td><strong>Justification vente</strong></td>
                    <td>Renouvellement, évolution besoins</td>
                    <td>Changement professionnel</td>
                    <td>Urgence, déménagement</td>
                </tr>
                <tr>
                    <td><strong>Photographies</strong></td>
                    <td>8+ photos variées, détails</td>
                    <td>4-6 photos standards</td>
                    <td><4 photos, angles choisis</td>
                </tr>
                <tr>
                    <td><strong>Description technique</strong></td>
                    <td>Détaillée, défauts mentionnés</td>
                    <td>Correcte, équilibrée</td>
                    <td>Élogieuse, "parfait état"</td>
                </tr>
                <tr>
                    <td><strong>Historique vendeur</strong></td>
                    <td>Profil établi, évaluations positives</td>
                    <td>Quelques ventes, correct</td>
                    <td>Nouveau compte, anonyme</td>
                </tr>
            </table>
        </div>

        <img src="https://images.unsplash.com/photo-1746079074522-2b14240d932c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Analyse d'annonce professionnelle" class="module-image" />

        <div class="success-box">
            <h4>🎯 Objectifs pédagogiques du module</h4>
            <p>À l'issue de ce module fondamental, vous maîtriserez :</p>
            <ul>
                <li>✅ <strong>Rôle et missions</strong> de l'inspecteur automobile professionnel</li>
                <li>✅ <strong>Distinction claire</strong> avec les autres acteurs de l'expertise</li>
                <li>✅ <strong>Principes déontologiques</strong> et leur application pratique</li>
                <li>✅ <strong>Cadre réglementaire</strong> français et européen applicable</li>
                <li>✅ <strong>Préparation rigoureuse</strong> des interventions</li>
                <li>✅ <strong>Communication professionnelle</strong> adaptée aux clients</li>
                <li>✅ <strong>Analyse critique</strong> des situations d'inspection</li>
            </ul>
        </div>

        <p><strong>Transition vers le module suivant :</strong> Ces fondamentaux solidement acquis, le Module 3 vous permettra d'approfondir les aspects techniques indispensables avec une remise à niveau mécanique complète adaptée aux véhicules modernes.</p>

        <p><em>Durée totale de lecture estimée : 90 minutes | Quiz de validation : 12 questions | Exercices pratiques recommandés : 30 minutes supplémentaires</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quel est le rôle principal d'un inspecteur automobile ?",
                "options": ["Vendre des véhicules", "Expert technique indépendant", "Réparateur automobile", "Commercial auto"],
                "correct_answer": "Expert technique indépendant"
            },
            {
                "id": "q2",
                "question": "Dans quels contextes l'inspecteur peut-il intervenir ?",
                "options": ["Uniquement vente particuliers", "Assurance et leasing uniquement", "Ventes, assurance, leasing, expertises", "Uniquement litiges"],
                "correct_answer": "Ventes, assurance, leasing, expertises"
            },
            {
                "id": "q3",
                "question": "Quelle est la durée de la garantie de conformité selon le Code de la Consommation ?",
                "options": ["1 an", "2 ans", "3 ans", "5 ans"],
                "correct_answer": "2 ans"
            },
            {
                "id": "q4",
                "question": "Le montant minimum recommandé pour l'assurance RC Pro en dommages corporels est :",
                "options": ["1 500 000€", "3 000 000€", "4 500 000€", "6 000 000€"],
                "correct_answer": "4 500 000€"
            },
            {
                "id": "q5",
                "question": "En cas de faux et usage de faux, l'inspecteur risque :",
                "options": ["Amende uniquement", "5 ans de prison + 75 000€", "Interdiction d'exercer", "Blâme professionnel"],
                "correct_answer": "5 ans de prison + 75 000€"
            },
            {
                "id": "q6",
                "question": "Quel est le premier principe du code de déontologie ?",
                "options": ["Rapidité", "Compétence", "Rentabilité", "Convivialité"],
                "correct_answer": "Compétence"
            },
            {
                "id": "q7",
                "question": "Le plafond de CA pour une micro-entreprise de services est :",
                "options": ["36 800€", "72 600€", "176 200€", "Illimité"],
                "correct_answer": "72 600€"
            },
            {
                "id": "q8",
                "question": "L'inspecteur doit-il refuser d'inspecter le véhicule d'un ami ?",
                "options": ["Non, pas de problème", "Oui, conflit d'intérêt", "Ça dépend du prix", "Avec une remise"],
                "correct_answer": "Oui, conflit d'intérêt"
            },
            {
                "id": "q9",
                "question": "La formation continue est-elle obligatoire ?",
                "options": ["Non", "Recommandée", "Obligatoire", "Uniquement les 3 premières années"],
                "correct_answer": "Obligatoire"
            },
            {
                "id": "q10",
                "question": "En cas de défaut de sécurité critique, l'inspecteur doit :",
                "options": ["L'ignorer si le client insiste", "Le mentionner discrètement", "Signaler immédiatement", "Négocier un arrangement"],
                "correct_answer": "Signaler immédiatement"
            },
            {
                "id": "q11",
                "question": "Le délai de remise du rapport doit être :",
                "options": ["Immédiat", "24h maximum", "48h maximum", "1 semaine"],
                "correct_answer": "24h maximum"
            },
            {
                "id": "q12",
                "question": "L'indépendance de l'inspecteur signifie :",
                "options": ["Travailler seul", "Pas de lien commercial avec vendeur/acheteur", "Choisir ses horaires", "Fixer ses tarifs"],
                "correct_answer": "Pas de lien commercial avec vendeur/acheteur"
            }
        ]
    },
    {
        "id": "module-3",
        "title": "Remise à Niveau Mécanique",
        "description": "Bases essentielles : moteur, transmission, freinage, électronique embarquée",
        "duration_minutes": 120,
        "order": 3,
        "content": """
        <h2>Module 3 : Remise à Niveau Mécanique</h2>
        
        <h3>🎯 Objectifs du Module</h3>
        <ul>
            <li>Maîtriser les bases du moteur thermique et hybride</li>
            <li>Comprendre les systèmes de transmission</li>
            <li>Connaître les circuits de freinage et de direction</li>
            <li>Appréhender l'électronique embarquée moderne</li>
        </ul>

        <h3>🔧 Le Moteur Thermique : Fonctionnement et Diagnostic</h3>
        
        <h4>Principe des 4 Temps</h4>
        <p>Le moteur à 4 temps est le cœur de la plupart des véhicules. Comprendre son fonctionnement est essentiel pour l'inspection.</p>
        
        <div style="background: #1e293b; padding: 20px; border-radius: 8px; margin: 16px 0;">
            <h5>🔄 Cycle Complet du Moteur</h5>
            <ol>
                <li><strong>1er Temps - Admission :</strong>
                    <ul>
                        <li>Piston descend, dépression créée</li>
                        <li>Soupape d'admission ouvre</li>
                        <li>Mélange air/carburant aspiré</li>
                        <li>Volume : de 0 à cylindrée totale</li>
                    </ul>
                </li>
                <li><strong>2ème Temps - Compression :</strong>
                    <ul>
                        <li>Toutes soupapes fermées</li>
                        <li>Piston remonte, comprime le mélange</li>
                        <li>Ratio de compression : 8:1 à 12:1</li>
                        <li>Température monte à 400-500°C</li>
                    </ul>
                </li>
                <li><strong>3ème Temps - Combustion/Détente :</strong>
                    <ul>
                        <li>Allumage du mélange par bougie</li>
                        <li>Explosion repousse le piston</li>
                        <li>Force transmise au vilebrequin</li>
                        <li>Temps moteur (seul productif)</li>
                    </ul>
                </li>
                <li><strong>4ème Temps - Échappement :</strong>
                    <ul>
                        <li>Soupape d'échappement ouvre</li>
                        <li>Piston expulse gaz brûlés</li>
                        <li>Nettoyage de la chambre</li>
                        <li>Préparation cycle suivant</li>
                    </ul>
                </li>
            </ol>
        </div>

        <h4>Architecture Moteur</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Composant</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Fonction</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Signes d'usure</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Impact inspection</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Pistons</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Transmission force explosion</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Claquements, fumée bleue</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Révision majeure nécessaire</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Soupapes</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Contrôle admission/échappement</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Bruit métallique, perte puissance</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Réglage ou remplacement</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Vilebrequin</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Transformation mouvement linéaire/rotatif</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Vibrations anormales</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Moteur HS, remplacement</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Arbre à cames</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Commande ouverture soupapes</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Décalage distribution</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Réparation coûteuse</td>
            </tr>
        </table>

        <h4>Systèmes Annexes du Moteur</h4>
        
        <h5>💧 Circuit de Refroidissement</h5>
        <ul>
            <li><strong>Radiateur :</strong> Évacuation chaleur, vérifier encrassement</li>
            <li><strong>Pompe à eau :</strong> Circulation liquide, écouter bruits</li>
            <li><strong>Thermostat :</strong> Régulation température, test ouverture</li>
            <li><strong>Liquide de refroidissement :</strong> Niveau, couleur, antigel</li>
        </ul>

        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>⚠️ Points de Vigilance Refroidissement</h5>
            <ul>
                <li>Fuite = surchauffe = casse moteur</li>
                <li>Mélange huile/liquide = joint culasse</li>
                <li>Corrosion = radiateur à remplacer</li>
                <li>Thermostat grippé = surconsommation</li>
            </ul>
        </div>

        <h5>🛢️ Circuit de Lubrification</h5>
        <ul>
            <li><strong>Huile moteur :</strong> Niveau, viscosité, contamination</li>
            <li><strong>Filtre à huile :</strong> État, périodicité changement</li>
            <li><strong>Pompe à huile :</strong> Pression, débit</li>
            <li><strong>Carter :</strong> Étanchéité, pas de fissures</li>
        </ul>

        <h3>⚙️ Transmission : Boîte, Embrayage, Différentiel</h3>
        
        <h4>Types de Transmission</h4>
        
        <div style="background: #065f46; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🔧 Boîte de Vitesses Manuelle</h5>
            <p><strong>Fonctionnement :</strong></p>
            <ul>
                <li>Engrenages de différents diamètres</li>
                <li>Modification du rapport de démultiplication</li>
                <li>Passage manuel des vitesses</li>
                <li>Embrayage pour désolidariser moteur/boîte</li>
            </ul>
            <p><strong>Points de contrôle :</strong></p>
            <ul>
                <li>Fluidité du passage de vitesses</li>
                <li>Absence de craquements</li>
                <li>Point d'embrayage correct</li>
                <li>Niveau d'huile de boîte</li>
            </ul>
        </div>

        <div style="background: #1e40af; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🔄 Boîte de Vitesses Automatique</h5>
            <p><strong>Fonctionnement :</strong></p>
            <ul>
                <li>Convertisseur de couple hydraulique</li>
                <li>Train épicycloïdal</li>
                <li>Passage automatique des rapports</li>
                <li>Gestion électronique</li>
            </ul>
            <p><strong>Points de contrôle :</strong></p>
            <ul>
                <li>Douceur des passages de rapports</li>
                <li>Absence de à-coups</li>
                <li>Réactivité en mode manuel</li>
                <li>Couleur et odeur de l'huile ATF</li>
            </ul>
        </div>

        <h4>L'Embrayage (Boîtes Manuelles)</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Composant</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Symptômes d'usure</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Test inspection</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Disque d'embrayage</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Patinage, point haut</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Test en côte, démarrage 3ème</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Mécanisme</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Durcissement pédale</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Force d'appui, progressivité</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Butée</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Grincement débrayage</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Bruit pédale enfoncée</td>
            </tr>
        </table>

        <h3>🛑 Système de Freinage</h3>
        
        <h4>Circuit Hydraulique</h4>
        <p>Le freinage repose sur la transmission de pression hydraulique :</p>
        
        <ul>
            <li><strong>Maître-cylindre :</strong> Génération pression (pédale)</li>
            <li><strong>Servo-frein :</strong> Assistance au freinage</li>
            <li><strong>Répartiteur :</strong> Distribution pression AV/AR</li>
            <li><strong>Flexibles :</strong> Acheminement fluide sous pression</li>
            <li><strong>Étriers/Cylindres :</strong> Transformation pression en force</li>
        </ul>

        <h4>Éléments de Friction</h4>
        
        <div style="background: #581c87; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🔍 Contrôles Obligatoires</h5>
            <p><strong>Plaquettes de frein :</strong></p>
            <ul>
                <li>Épaisseur minimum : 3mm de garniture</li>
                <li>Usure régulière (pas de biais)</li>
                <li>Absence de fissures ou délaminage</li>
                <li>Témoins d'usure fonctionnels</li>
            </ul>
            <p><strong>Disques de frein :</strong></p>
            <ul>
                <li>Épaisseur selon constructeur</li>
                <li>Surface lisse, pas de rayures profondes</li>
                <li>Absence de voilage</li>
                <li>Pas de fissures radiaires</li>
            </ul>
        </div>

        <h4>Systèmes d'Aide au Freinage</h4>
        
        <ul>
            <li><strong>ABS (Anti Blocage) :</strong> Empêche blocage roues</li>
            <li><strong>ESP (Contrôle stabilité) :</strong> Correction trajectoire</li>
            <li><strong>AFU (Aide au freinage d'urgence) :</strong> Détection panique</li>
            <li><strong>EBD (Répartition électronique) :</strong> Optimisation freinage</li>
        </ul>

        <h3>🔧 Direction et Train Roulant</h3>
        
        <h4>Système de Direction</h4>
        
        <h5>Direction à Crémaillère</h5>
        <p>Standard sur véhicules modernes :</p>
        <ul>
            <li><strong>Colonne de direction :</strong> Transmission mouvement volant</li>
            <li><strong>Crémaillère :</strong> Transformation rotation/translation</li>
            <li><strong>Biellettes :</strong> Liaison avec roues</li>
            <li><strong>Assistance :</strong> Hydraulique ou électrique</li>
        </ul>

        <h5>Points de Contrôle Direction</h5>
        <ul>
            <li><strong>Jeu au volant :</strong> Maximum 30° sans réaction roues</li>
            <li><strong>Centrage :</strong> Véhicule va droit, volant centré</li>
            <li><strong>Effort :</strong> Manœuvre à l'arrêt possible sans forcer</li>
            <li><strong>Bruits :</strong> Pas de claquements en braquage</li>
        </ul>

        <h4>Suspension</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Type</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Composants</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Défauts courants</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Test</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Amortisseur</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Piston, huile, ressort</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Fuite, perte efficacité</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Test rebonds, fuites</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Ressort</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Spirale acier</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Cassure, affaissement</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Hauteur caisse, symétrie</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Rotule</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Articulation sphérique</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Jeu, déchirure soufflet</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Test jeu, inspection visuelle</td>
            </tr>
        </table>

        <h3>🔌 Électronique Embarquée</h3>
        
        <h4>Architecture Électrique Moderne</h4>
        
        <div style="background: #1e293b; padding: 20px; border-radius: 8px; margin: 16px 0;">
            <h5>📱 Systèmes Embarqués</h5>
            <ul>
                <li><strong>Calculateur moteur (UCE) :</strong> Gestion injection, allumage</li>
                <li><strong>Calculateur ABS/ESP :</strong> Sécurité active</li>
                <li><strong>BCM (Body Control Module) :</strong> Confort, éclairage</li>
                <li><strong>Airbag :</strong> Sécurité passive</li>
                <li><strong>Climatisation :</strong> Confort thermique</li>
                <li><strong>Multimédia :</strong> Info-divertissement</li>
            </ul>
        </div>

        <h4>Diagnostic OBD (On-Board Diagnostic)</h4>
        
        <p>Norme obligatoire depuis 2001 (essence) et 2004 (diesel) :</p>
        
        <ul>
            <li><strong>Prise OBD :</strong> Accès aux calculateurs</li>
            <li><strong>Codes défauts :</strong> P (moteur), B (carrosserie), C (châssis), U (réseau)</li>
            <li><strong>Données temps réel :</strong> Paramètres moteur</li>
            <li><strong>Tests actifs :</strong> Activation composants</li>
        </ul>

        <div style="background: #065f46; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🔍 Procédure Diagnostic OBD</h5>
            <ol>
                <li>Connexion valise sur prise OBD</li>
                <li>Identification véhicule (VIN)</li>
                <li>Lecture codes défauts mémorisés</li>
                <li>Consultation données temps réel</li>
                <li>Tests actifs si nécessaire</li>
                <li>Effacement codes après réparation</li>
            </ol>
        </div>

        <h4>Capteurs et Actionneurs</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Capteur</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Fonction</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Défaillance</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Symptôme</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Débit d'air</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Mesure air aspiré</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Encrassement</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Perte puissance</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Sonde lambda</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Richesse mélange</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Vieillissement</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Surconsommation</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Position vilebrequin</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Synchronisation</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Panne complète</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Moteur ne démarre pas</td>
            </tr>
        </table>

        <h3>🔋 Batterie et Alternateur</h3>
        
        <h4>Circuit de Charge</h4>
        
        <ul>
            <li><strong>Batterie :</strong> Stockage énergie, démarrage moteur</li>
            <li><strong>Alternateur :</strong> Production électricité, charge batterie</li>
            <li><strong>Régulateur :</strong> Contrôle tension (≈14,4V)</li>
            <li><strong>Démarreur :</strong> Lancement moteur</li>
        </ul>

        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>⚡ Tests Électriques Essentiels</h5>
            <ul>
                <li><strong>Tension batterie :</strong> 12,6V moteur arrêté</li>
                <li><strong>Tension charge :</strong> 14,2-14,8V moteur tournant</li>
                <li><strong>Courant de fuite :</strong> <50mA contact coupé</li>
                <li><strong>Démarreur :</strong> Chute tension <2V au démarrage</li>
            </ul>
        </div>

        <h3>📚 Glossaire Technique Simplifié</h3>
        
        <div style="background: #1e293b; padding: 20px; border-radius: 8px; margin: 16px 0;">
            <h5>🔧 Termes Essentiels</h5>
            <ul>
                <li><strong>Cylindrée :</strong> Volume balayé par pistons (ex: 2.0L = 2000cm³)</li>
                <li><strong>Couple :</strong> Force rotative moteur (Nm), détermine reprises</li>
                <li><strong>Puissance :</strong> Travail par unité de temps (Ch/kW), vitesse max</li>
                <li><strong>Taux de compression :</strong> Rapport volume maxi/mini cylindre</li>
                <li><strong>PMH/PMB :</strong> Point Mort Haut/Bas du piston</li>
                <li><strong>Avance allumage :</strong> Timing explosion avant PMH</li>
                <li><strong>Richesse :</strong> Rapport air/carburant (14,7:1 = stœchiométrique)</li>
            </ul>
        </div>

        <h3>🎯 Points Clés pour l'Inspection</h3>
        
        <ul>
            <li>Un moteur sain tourne rond et régulier au ralenti</li>
            <li>Les transmissions usées génèrent bruits et à-coups</li>
            <li>Le freinage doit être progressif et sans vibrations</li>
            <li>L'électronique moderne simplifie le diagnostic mais complexifie les pannes</li>
            <li>L'entretien préventif évite 80% des pannes</li>
        </ul>

        <p><em>Durée estimée : 120 minutes de lecture + 25 minutes pour le quiz</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Combien de temps producteur d'énergie y a-t-il dans un cycle 4 temps ?",
                "options": ["1 temps", "2 temps", "3 temps", "4 temps"],
                "correct_answer": "1 temps"
            },
            {
                "id": "q2",
                "question": "À quel moment les soupapes sont-elles toutes fermées ?",
                "options": ["Admission", "Compression", "Combustion", "Échappement"],
                "correct_answer": "Compression"
            },
            {
                "id": "q3",
                "question": "Quelle est l'épaisseur minimum des plaquettes de frein ?",
                "options": ["2mm", "3mm", "4mm", "5mm"],
                "correct_answer": "3mm"
            },
            {
                "id": "q4",
                "question": "Le jeu maximum au volant sans réaction des roues est de :",
                "options": ["15°", "30°", "45°", "60°"],
                "correct_answer": "30°"
            },
            {
                "id": "q5",
                "question": "La tension normale d'une batterie moteur arrêté est :",
                "options": ["12,0V", "12,6V", "13,2V", "14,4V"],
                "correct_answer": "12,6V"
            },
            {
                "id": "q6",
                "question": "Depuis quand l'OBD est-il obligatoire sur les moteurs essence ?",
                "options": ["1998", "2001", "2004", "2007"],
                "correct_answer": "2001"
            },
            {
                "id": "q7",
                "question": "Que signifie un code défaut commençant par P ?",
                "options": ["Carrosserie", "Moteur", "Châssis", "Réseau"],
                "correct_answer": "Moteur"
            },
            {
                "id": "q8",
                "question": "La richesse stœchiométrique air/carburant est de :",
                "options": ["12,5:1", "14,7:1", "16,2:1", "18,1:1"],
                "correct_answer": "14,7:1"
            },
            {
                "id": "q9",
                "question": "L'ABS empêche :",
                "options": ["Le dérapage", "Le blocage des roues", "La perte de puissance", "La surchauffe"],
                "correct_answer": "Le blocage des roues"
            },
            {
                "id": "q10",
                "question": "Un embrayage qui patine se teste en :",
                "options": ["Marche arrière", "1ère vitesse", "3ème vitesse", "Point mort"],
                "correct_answer": "3ème vitesse"
            },
            {
                "id": "q11",
                "question": "La tension de charge normale de l'alternateur est :",
                "options": ["12-13V", "14,2-14,8V", "15-16V", "16-17V"],
                "correct_answer": "14,2-14,8V"
            },
            {
                "id": "q12",
                "question": "Un courant de fuite normal sur une batterie est :",
                "options": ["<20mA", "<50mA", "<100mA", "<200mA"],
                "correct_answer": "<50mA"
            }
        ]
    },
    {
        "id": "module-4",
        "title": "Procédé d'Inspection : 200+ Points de Contrôle",
        "description": "Méthodologie complète d'inspection terrain avec checklists détaillées et outils de diagnostic",
        "duration_minutes": 135,
        "order": 4,
        "content": """
        <h2>Module 4 : Procédé d'Inspection - 200+ Points de Contrôle</h2>
        
        <img src="https://images.unsplash.com/photo-1487754180451-c456f719a1fc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Inspection automobile professionnelle" class="module-image" />
        
        <div class="chapter-divider"></div>

        <h3>Chapitre 1 : Préparation et méthodologie (sécurité, matériel, briefing client)</h3>

        <p>L'inspection automobile professionnelle commence bien avant l'examen du véhicule lui-même. Une préparation minutieuse conditionne la qualité, l'efficacité et la sécurité de toute l'intervention. Cette phase préparatoire, souvent négligée par les inspecteurs débutants, représente pourtant 15% du temps total d'inspection mais conditionne 80% de la réussite de la mission.</p>

        <div class="info-box">
            <h4>🛡️ Priorité Absolue : La Sécurité</h4>
            <p>Avant toute intervention, l'inspecteur doit s'assurer que les conditions de sécurité sont réunies :</p>
            <ul>
                <li><strong>Équipements de protection individuelle :</strong> Gants nitrile, lunettes de protection, chaussures de sécurité</li>
                <li><strong>Environnement d'inspection :</strong> Sol stable, éclairage suffisant, aération si en local fermé</li>
                <li><strong>État du véhicule :</strong> Moteur refroidi, frein à main serré, véhicule sur terrain plat</li>
                <li><strong>Assurance professionnelle :</strong> Vérification validité RC Pro et extension géographique</li>
            </ul>
        </div>

        <h4>Matériel professionnel requis</h4>

        <p>L'inspecteur moderne dispose d'un arsenal technologique qui s'est considérablement enrichi ces dernières années. L'investissement initial varie de 2 500€ (équipement de base) à 8 000€ (équipement professionnel complet), mais cette différence se ressent immédiatement sur la qualité des inspections et la crédibilité professionnelle.</p>

        <table>
            <tr>
                <th>Catégorie</th>
                <th>Équipement de base</th>
                <th>Équipement professionnel</th>
                <th>Coût approximatif</th>
            </tr>
            <tr>
                <td><strong>Diagnostic électronique</strong></td>
                <td>Valise OBD générique</td>
                <td>Valise multi-marques Launch/Autel</td>
                <td>300€ à 2 000€</td>
            </tr>
            <tr>
                <td><strong>Mesures électriques</strong></td>
                <td>Multimètre basique</td>
                <td>Multimètre automobile + pince ampèremétrique</td>
                <td>50€ à 400€</td>
            </tr>
            <tr>
                <td><strong>Éclairage</strong></td>
                <td>Lampe LED portable</td>
                <td>Projecteur LED rechargeable + lampe d'inspection</td>
                <td>30€ à 200€</td>
            </tr>
            <tr>
                <td><strong>Mesures mécaniques</strong></td>
                <td>Règle, jauge de profondeur</td>
                <td>Comparateur, testeur compression, manomètre</td>
                <td>100€ à 800€</td>
            </tr>
            <tr>
                <td><strong>Documentation</strong></td>
                <td>Smartphone + app</td>
                <td>Tablette durcie + app pro + imprimante portable</td>
                <td>200€ à 1 000€</td>
            </tr>
        </table>

        <div class="tip-box">
            <h4>💡 Optimisation du matériel</h4>
            <p>L'expérience de nos 300+ inspecteurs certifiés révèle les investissements prioritaires :</p>
            <ol>
                <li><strong>Valise de diagnostic :</strong> 40% d'amélioration de la détection des défauts</li>
                <li><strong>Éclairage professionnel :</strong> 60% de gain de temps en inspection moteur</li>
                <li><strong>Application mobile dédiée :</strong> 50% de réduction du temps de rédaction</li>
                <li><strong>Appareil photo dédié :</strong> 80% d'amélioration de la qualité visuelle des rapports</li>
            </ol>
        </div>

        <h4>Briefing client et gestion des attentes</h4>

        <p>Le briefing initial conditionne la satisfaction client finale. Cette phase de 10-15 minutes permet d'établir la confiance, de clarifier les attentes mutuelles et de prévenir les malentendus post-inspection.</p>

        <div class="success-box">
            <h4>📋 Trame de briefing client</h4>
            <ol>
                <li><strong>Présentation personnelle :</strong> Certification, expérience, assurance</li>
                <li><strong>Méthodologie :</strong> Explication des 200+ points de contrôle</li>
                <li><strong>Durée :</strong> 90 minutes d'inspection + 24h pour le rapport</li>
                <li><strong>Limites :</strong> Inspection non destructive, pas de démontage</li>
                <li><strong>Livrables :</strong> Rapport détaillé + photos + avis moteur</li>
                <li><strong>Modalités :</strong> Accompagnement souhaitable, questions encouragées</li>
            </ol>
        </div>

        <img src="https://images.unsplash.com/photo-1498887960847-2a5e46312788?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Outils de diagnostic automobile" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Inspection extérieure (carrosserie, corrosion, alignements)</h3>

        <p>L'inspection extérieure constitue le premier contact visuel avec le véhicule et détermine souvent la première impression du client. Cette phase, d'une durée de 25-30 minutes, couvre 68 points de contrôle spécifiques répartis selon une méthodologie éprouvée par plus de 10 000 inspections réalisées.</p>

        <h4>Méthodologie de tour de véhicule</h4>

        <p>L'inspection extérieure suit un parcours codifié garantissant l'exhaustivité et la répétabilité. Cette approche systémique, inspirée des méthodes aéronautiques, élimine les oublis et optimise le temps d'intervention.</p>

        <div class="info-box">
            <h4>🔄 Séquence d'inspection extérieure (25 minutes)</h4>
            <ol>
                <li><strong>Vue d'ensemble (2 min) :</strong> Position générale, première impression, anomalies évidentes</li>
                <li><strong>Face avant (5 min) :</strong> Pare-chocs, calandre, phares, capot, pare-brise</li>
                <li><strong>Côté conducteur (6 min) :</strong> Portières, vitres, rétroviseurs, passages de roues</li>
                <li><strong>Arrière (4 min) :</strong> Pare-chocs, feux, coffre, échappement, plaque</li>
                <li><strong>Côté passager (6 min) :</strong> Symétrie avec côté conducteur, comparaisons</li>
                <li><strong>Toit et parties hautes (2 min) :</strong> Pavillon, gouttières, antennes, rails</li>
            </ol>
        </div>

        <h4>Détection et analyse de la corrosion</h4>

        <p>La corrosion représente l'un des défauts les plus critiques et les plus coûteux à traiter. Sa détection précoce peut faire la différence entre une réparation de 500€ et un véhicule économiquement irréparable. L'inspecteur doit maîtriser les différents types de corrosion et leur évolution.</p>

        <table>
            <tr>
                <th>Type de corrosion</th>
                <th>Localisation typique</th>
                <th>Signes visuels</th>
                <th>Criticité</th>
                <th>Coût de réparation</th>
            </tr>
            <tr>
                <td><strong>Corrosion superficielle</strong></td>
                <td>Rayures, impacts</td>
                <td>Points de rouille isolés</td>
                <td>Faible</td>
                <td>50-200€</td>
            </tr>
            <tr>
                <td><strong>Corrosion par piqûres</strong></td>
                <td>Bas de caisse, seuils</td>
                <td>Petits trous multiples</td>
                <td>Moyenne</td>
                <td>300-800€</td>
            </tr>
            <tr>
                <td><strong>Corrosion galvanique</strong></td>
                <td>Jonctions métaux différents</td>
                <td>Décoloration, boursouflures</td>
                <td>Élevée</td>
                <td>800-2000€</td>
            </tr>
            <tr>
                <td><strong>Corrosion structurelle</strong></td>
                <td>Longerons, montants</td>
                <td>Déformation, perforation</td>
                <td>Critique</td>
                <td>2000€+</td>
            </tr>
        </table>

        <h4>Analyse des défauts de carrosserie</h4>

        <p>L'évaluation des défauts de carrosserie nécessite un œil exercé et une méthodologie rigoureuse. L'inspecteur doit différencier les dommages esthétiques des dommages structurels, évaluer leur origine (accident, usure, négligence) et estimer leur impact sur la valeur et la sécurité du véhicule.</p>

        <div class="warning-box">
            <h4>⚠️ Signaux d'alerte majeurs</h4>
            <ul>
                <li><strong>Teintes différentes :</strong> Indication de repeinte, possible accident</li>
                <li><strong>Jeux inégaux :</strong> Déformation de structure ou mauvais remontage</li>
                <li><strong>Ondulations :</strong> Travaux de carrosserie, mastic mal poncé</li>
                <li><strong>Soudures atypiques :</strong> Réparation structurelle, accident grave</li>
                <li><strong>Corrosion active :</strong> Évolution rapide, intervention urgente</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Inspection intérieure (électronique, airbags, habitacle)</h3>

        <p>L'inspection intérieure révèle souvent l'usage réel du véhicule et peut dévoiler des défauts cachés non visibles à l'extérieur. Cette phase de 20 minutes couvre 45 points de contrôle et nécessite une attention particulière aux systèmes de sécurité et aux équipements électroniques.</p>

        <h4>Contrôle des systèmes de sécurité</h4>

        <p>Les systèmes de sécurité moderne (airbags, prétensionneurs, assistance au freinage) représentent des enjeux vitaux. Leur défaillance peut avoir des conséquences dramatiques, et leur réparation coûte généralement entre 1 500€ et 5 000€. L'inspecteur doit maîtriser leur fonctionnement et leurs modes de défaillance.</p>

        <div class="info-box">
            <h4>🛡️ Check-list sécurité passive</h4>
            <ul>
                <li><strong>Témoins airbag :</strong> Extinction après démarrage (6 secondes max)</li>
                <li><strong>Ceintures de sécurité :</strong> Enroulement correct, verrouillage fonctionnel</li>
                <li><strong>Prétensionneurs :</strong> Pas de déclenchement intempestif visible</li>
                <li><strong>Sièges enfants :</strong> Points d'ancrage ISOFIX présents et fonctionnels</li>
                <li><strong>Appuis-tête :</strong> Réglage et verrouillage corrects</li>
            </ul>
        </div>

        <h4>Évaluation de l'usure intérieure</h4>

        <p>L'usure de l'habitacle révèle l'usage réel du véhicule et peut contredire le kilométrage affiché. L'inspecteur expérimenté sait décrypter ces indices pour détecter les anomalies et évaluer la cohérence globale.</p>

        <img src="https://images.unsplash.com/photo-1606577924006-27d39b132ae2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Intérieur véhicule moderne" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : Compartiment moteur (contrôles visuels et mécaniques)</h3>

        <p>Le compartiment moteur concentre la complexité technique maximale du véhicule moderne. Cette phase d'inspection de 25-30 minutes couvre 52 points de contrôle et nécessite l'expertise la plus poussée de l'inspecteur. C'est également la zone où se cachent les défauts les plus coûteux.</p>

        <h4>Diagnostic moteur approfondi</h4>

        <p>L'évaluation moteur combine l'analyse visuelle, auditive, olfactive et instrumentale. Cette approche multi-sensorielle, complétée par le diagnostic électronique, permet de détecter 95% des dysfonctionnements, y compris ceux en phase d'amorçage.</p>

        <div class="success-box">
            <h4>🔧 Protocole de diagnostic moteur</h4>
            <ol>
                <li><strong>Inspection visuelle à froid (5 min) :</strong> Fuites, corrosion, modifications</li>
                <li><strong>Contrôle des niveaux (3 min) :</strong> Huile, liquide refroidissement, frein</li>
                <li><strong>Démarrage et écoute (5 min) :</strong> Temps démarrage, bruits anormaux</li>
                <li><strong>Diagnostic OBD (8 min) :</strong> Codes défauts, paramètres temps réel</li>
                <li><strong>Test en charge (5 min) :</strong> Accélérations, montée température</li>
            </ol>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Essai routier (démarrage, moteur, boîte, direction, freins)</h3>

        <p>L'essai routier représente l'épreuve de vérité de l'inspection. C'est le moment où tous les systèmes fonctionnent en conditions réelles et où se révèlent les défauts impossible à détecter à l'arrêt. Cette phase de 15-20 minutes nécessite une grande expérience et une parfaite maîtrise des techniques de conduite d'évaluation.</p>

        <h4>Sécurité et responsabilité</h4>

        <p>L'essai routier engage la responsabilité civile et pénale de l'inspecteur. Une préparation rigoureuse et le respect de protocoles stricts sont indispensables pour limiter les risques tout en maintenant l'efficacité du diagnostic.</p>

        <div class="warning-box">
            <h4>⚠️ Protocole de sécurité essai routier</h4>
            <ul>
                <li><strong>Vérifications préalables :</strong> Freinage, direction, niveaux, pneus</li>
                <li><strong>Accompagnement :</strong> Propriétaire ou mandataire présent obligatoirement</li>
                <li><strong>Parcours :</strong> Sélectionné à l'avance, sécurisé, représentatif</li>
                <li><strong>Assurance :</strong> Extension conduite professionnelle vérifiée</li>
                <li><strong>Météo :</strong> Conditions compatibles avec sécurité</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 6 : Documentation (photos, carnet, factures, historique)</h3>

        <p>La documentation constitue la mémoire de l'inspection et la base légale du rapport. Une documentation rigoureuse protège autant l'inspecteur que le client et constitue souvent l'élément décisif en cas de litige. La révolution numérique a transformé cette phase, permettant une traçabilité et une qualité inégalées.</p>

        <img src="https://images.unsplash.com/photo-1746079074522-2b14240d932c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Documentation inspection" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 7 : Checklists types et exercices de simulation</h3>

        <p>La check-list constitue l'épine dorsale de l'inspection professionnelle. Elle garantit l'exhaustivité, la répétabilité et la traçabilité de chaque intervention. Les check-lists AutoJust, développées et affinées sur plus de 10 000 inspections, constituent la référence professionnelle du secteur.</p>

        <div class="tip-box">
            <h4>📊 Répartition des 200+ points de contrôle</h4>
            <ul>
                <li><strong>Carrosserie et esthétique :</strong> 68 points (34%)</li>
                <li><strong>Mécanique et motorisation :</strong> 52 points (26%)</li>
                <li><strong>Sécurité et équipements :</strong> 45 points (22,5%)</li>
                <li><strong>Intérieur et confort :</strong> 25 points (12,5%)</li>
                <li><strong>Essai routier :</strong> 20 points (10%)</li>
            </ul>
        </div>

        <p><em>Durée de lecture estimée : 135 minutes | Quiz de validation : 12 questions</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quelle est la durée recommandée pour la phase de préparation d'une inspection ?",
                "options": ["5-8 minutes", "10-15 minutes", "15-20 minutes", "20-25 minutes"],
                "correct_answer": "10-15 minutes"
            },
            {
                "id": "q2",
                "question": "Combien de points de contrôle couvre l'inspection extérieure ?",
                "options": ["55 points", "68 points", "72 points", "85 points"],
                "correct_answer": "68 points"
            },
            {
                "id": "q3",
                "question": "Quel est l'investissement minimum pour un équipement d'inspection de base ?",
                "options": ["1 500€", "2 500€", "3 500€", "4 500€"],
                "correct_answer": "2 500€"
            },
            {
                "id": "q4",
                "question": "La corrosion structurelle nécessite généralement un budget de réparation de :",
                "options": ["500-800€", "800-1500€", "1500-2000€", "2000€ et plus"],
                "correct_answer": "2000€ et plus"
            },
            {
                "id": "q5",
                "question": "Combien de temps doit s'écouler maximum pour l'extinction du témoin airbag ?",
                "options": ["3 secondes", "6 secondes", "10 secondes", "15 secondes"],
                "correct_answer": "6 secondes"
            },
            {
                "id": "q6",
                "question": "L'inspection du compartiment moteur couvre combien de points de contrôle ?",
                "options": ["45 points", "52 points", "60 points", "68 points"],
                "correct_answer": "52 points"
            },
            {
                "id": "q7",
                "question": "Quelle est la durée standard d'un essai routier d'inspection ?",
                "options": ["10-12 minutes", "15-20 minutes", "20-25 minutes", "25-30 minutes"],
                "correct_answer": "15-20 minutes"
            },
            {
                "id": "q8",
                "question": "Le briefing client représente quel pourcentage du temps total d'inspection ?",
                "options": ["10%", "15%", "20%", "25%"],
                "correct_answer": "15%"
            },
            {
                "id": "q9",
                "question": "Une valise de diagnostic améliore la détection des défauts de :",
                "options": ["25%", "30%", "35%", "40%"],
                "correct_answer": "40%"
            },
            {
                "id": "q10",
                "question": "Combien d'inspections ont servi à développer la méthodologie AutoJust ?",
                "options": ["5 000", "8 000", "10 000+", "15 000"],
                "correct_answer": "10 000+"
            },
            {
                "id": "q11",
                "question": "La réparation d'un système airbag coûte généralement entre :",
                "options": ["500-1000€", "1000-1500€", "1500-5000€", "5000-8000€"],
                "correct_answer": "1500-5000€"
            },
            {
                "id": "q12",
                "question": "Quelle est la répartition en pourcentage des points carrosserie/esthétique ?",
                "options": ["30%", "34%", "38%", "42%"],
                "correct_answer": "34%"
            }
        ]
    },
    {
        "id": "module-5",
        "title": "Avis sur le Moteur : Expertise Approfondie",
        "description": "Analyse spécifique du moteur selon kilométrage, modèle et techniques d'évaluation avancées",
        "duration_minutes": 45,
        "order": 5,
        "content": """
        <h2>Module 5 : Avis sur le Moteur - Expertise Approfondie</h2>
        
        <img src="https://images.pexels.com/photos/4489749/pexels-photo-4489749.jpeg" alt="Expertise moteur professionnelle" class="module-image" />
        
        <div class="chapter-divider"></div>

        <h3>Chapitre 1 : Pourquoi l'avis moteur est central</h3>

        <p>L'avis sur le moteur constitue le cœur de l'expertise automobile et la valeur ajoutée principale de l'inspecteur professionnel. Contrairement à une inspection généraliste, cet avis spécialisé exige une connaissance approfondie des motorisations, de leurs évolutions technologiques et de leurs défaillances spécifiques selon les modèles et kilométrages.</p>

        <p>Dans un marché de l'occasion où 78% des acheteurs redoutent prioritairement les pannes moteur, et où ces dernières représentent 45% du coût total de possession d'un véhicule d'occasion, l'avis moteur expert devient l'élément différenciant majeur de l'inspection professionnelle.</p>

        <div class="info-box">
            <h4>🔬 Spécificité de l'avis moteur</h4>
            <p>L'avis moteur AutoJust se distingue par :</p>
            <ul>
                <li><strong>Analyse contextualisée :</strong> Prise en compte du modèle, millésime, kilométrage</li>
                <li><strong>Base de données :</strong> Référentiel de 150 000+ moteurs analysés</li>
                <li><strong>Prédictibilité :</strong> Estimation des évolutions à 12, 24 et 36 mois</li>
                <li><strong>Chiffrage :</strong> Évaluation des coûts d'entretien prévisionnels</li>
                <li><strong>Recommandations :</strong> Plan d'action priorisé pour l'acquéreur</li>
            </ul>
        </div>

        <h4>Impact économique de l'avis moteur</h4>

        <p>Les statistiques de nos 300+ inspecteurs certifiés démontrent l'impact économique direct de l'avis moteur :</p>

        <table>
            <tr>
                <th>Type d'avis</th>
                <th>Impact sur décision achat</th>
                <th>Économies moyennes client</th>
                <th>Satisfaction post-achat</th>
            </tr>
            <tr>
                <td><strong>Avis favorable</strong></td>
                <td>85% de concrétisation</td>
                <td>Négociation -8%</td>
                <td>96% satisfaction</td>
            </tr>
            <tr>
                <td><strong>Avis réservé</strong></td>
                <td>45% de concrétisation</td>
                <td>Négociation -15%</td>
                <td>88% satisfaction</td>
            </tr>
            <tr>
                <td><strong>Avis défavorable</strong></td>
                <td>12% de concrétisation</td>
                <td>Évitement perte 3000€+</td>
                <td>98% satisfaction</td>
            </tr>
        </table>

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Analyse visuelle et auditive (bruits, vibrations, fumées)</h3>

        <p>L'expertise moteur commence par l'analyse sensorielle, technique ancestrale enrichie par l'expérience et la connaissance des spécificités techniques. Cette phase de diagnostic non-intrusif révèle 70% des dysfonctionnements moteur avant même l'utilisation d'instruments.</p>

        <h4>Diagnostic par l'écoute</h4>

        <p>Chaque moteur possède sa "signature sonore" caractéristique. L'inspecteur expérimenté développe une bibliothèque auditive lui permettant d'identifier instantanément les anomalies et leur localisation.</p>

        <div class="success-box">
            <h4>🎵 Cartographie sonore moteur</h4>
            <ul>
                <li><strong>Claquement métallique :</strong> Usure coussinets, jeu excessif vilebrequin</li>
                <li><strong>Sifflement aigu :</strong> Fuite dépression, joint turbo défaillant</li>
                <li><strong>Ronflement grave :</strong> Roulement défaillant, poulie endommagée</li>
                <li><strong>Grincement intermittent :</strong> Courroie détendue ou encrassée</li>
                <li><strong>Cognement synchrone :</strong> Avance allumage incorrecte, carburant inadapté</li>
            </ul>
        </div>

        <h4>Analyse des vibrations</h4>

        <p>Les vibrations moteur révèlent l'état des supports, l'équilibrage des masses tournantes et la qualité de la combustion. L'analyse vibratoire permet de détecter préventivement des défaillances majeures.</p>

        <img src="https://images.pexels.com/photos/7715199/pexels-photo-7715199.jpeg" alt="Diagnostic moteur approfondi" class="module-image" />

        <h4>Interprétation des fumées d'échappement</h4>

        <p>La couleur, la densité et l'odeur des fumées d'échappement constituent un indicateur précieux de l'état interne du moteur et de ses systèmes annexes.</p>

        <table>
            <tr>
                <th>Couleur fumée</th>
                <th>Origine probable</th>
                <th>Diagnostic</th>
                <th>Coût réparation</th>
            </tr>
            <tr>
                <td><strong>Blanche épaisse</strong></td>
                <td>Liquide refroidissement</td>
                <td>Joint de culasse</td>
                <td>1500-3000€</td>
            </tr>
            <tr>
                <td><strong>Bleue continue</strong></td>
                <td>Combustion d'huile</td>
                <td>Segments, guides soupapes</td>
                <td>2000-5000€</td>
            </tr>
            <tr>
                <td><strong>Noire dense</strong></td>
                <td>Surenrichissement</td>
                <td>Injection, filtration</td>
                <td>300-800€</td>
            </tr>
            <tr>
                <td><strong>Grise persistante</strong></td>
                <td>Combustion incomplète</td>
                <td>Allumage, compression</td>
                <td>200-600€</td>
            </tr>
        </table>

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Défauts connus par modèle/kilométrage (base de données)</h3>

        <p>Chaque motorisation présente des défaillances récurrentes liées à sa conception, aux matériaux utilisés ou aux évolutions techniques. La base de données AutoJust, enrichie continuellement par le retour d'expérience terrain, référence plus de 2 500 défauts types répartis sur 850 motorisations différentes.</p>

        <div class="info-box">
            <h4>📊 Exemples de défauts récurrents par marque</h4>
            
            <h5>Groupe PSA (Peugeot, Citroën, DS)</h5>
            <ul>
                <li><strong>1.6 THP :</strong> Chaîne de distribution (80 000-120 000 km)</li>
                <li><strong>2.0 HDi :</strong> Injecteurs (150 000-200 000 km)</li>
                <li><strong>1.2 PureTech :</strong> Courroie de distribution humide (100 000 km)</li>
            </ul>
            
            <h5>Groupe Renault-Nissan</h5>
            <ul>
                <li><strong>1.5 dCi :</strong> Vanne EGR (120 000-150 000 km)</li>
                <li><strong>2.0 TCe :</strong> Turbocompresseur (100 000-130 000 km)</li>
                <li><strong>1.6 dCi :</strong> Pompe haute pression (180 000 km)</li>
            </ul>
            
            <h5>Groupe VAG (Volkswagen, Audi, Skoda, Seat)</h5>
            <ul>
                <li><strong>1.4 TSI :</strong> Chaîne de distribution (100 000 km)</li>
                <li><strong>2.0 TDI :</strong> Géométrie variable turbo (150 000 km)</li>
                <li><strong>1.6 TDI :</strong> Volant moteur bi-masse (180 000 km)</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : Rédiger un avis clair, objectif et utile</h3>

        <p>La rédaction de l'avis moteur constitue l'exercice le plus délicat de l'inspection. Il s'agit de transformer une analyse technique complexe en recommandations claires et actionnables pour le client, tout en maintenant l'objectivité et la précision scientifique.</p>

        <div class="tip-box">
            <h4>✍️ Structure type de l'avis moteur</h4>
            <ol>
                <li><strong>État général (2-3 lignes) :</strong> Synthèse de l'évaluation globale</li>
                <li><strong>Points positifs :</strong> Éléments rassurants identifiés</li>
                <li><strong>Points d'attention :</strong> Éléments à surveiller ou maintenir</li>
                <li><strong>Points critiques :</strong> Défauts nécessitant intervention</li>
                <li><strong>Prévisions d'évolution :</strong> 12, 24, 36 mois</li>
                <li><strong>Budget prévisionnel :</strong> Estimation coûts entretien/réparation</li>
                <li><strong>Recommandation finale :</strong> Achat conseillé/déconseillé/conditionné</li>
            </ol>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Cas concrets et exercices pratiques</h3>

        <p>Pour maîtriser l'art de l'avis moteur, rien ne remplace l'analyse de cas concrets. Voici trois exemples représentatifs des situations les plus fréquemment rencontrées par l'inspecteur professionnel.</p>

        <div class="warning-box">
            <h4>📋 Cas pratique n°1 : BMW 320d F30 - 150 000 km</h4>
            <p><strong>Contexte :</strong> Véhicule de 2015, entretien BMW jusqu'à 100 000 km, puis garage indépendant</p>
            <p><strong>Observations :</strong> Léger claquement démarrage à froid, fumée grise intermittente, consommation d'huile 1L/1000km</p>
            <p><strong>Diagnostic :</strong> Début d'usure chaîne de distribution, injecteurs encrassés</p>
            <p><strong>Avis :</strong> "Moteur globalement sain mais présentant des signes d'usure cohérents avec le kilométrage. Chaîne de distribution à surveiller (remplacement préventif recommandé avant 180 000 km - budget 2 000€). Décalaminage conseillé sous 6 mois (300€). Achat recommandé avec négociation -1 500€ pour anticiper ces interventions."</p>
        </div>

        <p><em>Durée de lecture estimée : 45 minutes | Quiz de validation : 12 questions</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Quel pourcentage des acheteurs d'occasion redoutent prioritairement les pannes moteur ?",
                "options": ["68%", "73%", "78%", "83%"],
                "correct_answer": "78%"
            },
            {
                "id": "q2",
                "question": "Les pannes moteur représentent quel pourcentage du coût total de possession ?",
                "options": ["35%", "40%", "45%", "50%"],
                "correct_answer": "45%"
            },
            {
                "id": "q3",
                "question": "Combien de moteurs sont référencés dans la base de données AutoJust ?",
                "options": ["100 000+", "120 000+", "150 000+", "180 000+"],
                "correct_answer": "150 000+"
            },
            {
                "id": "q4",
                "question": "L'analyse sensorielle révèle quel pourcentage des dysfonctionnements moteur ?",
                "options": ["60%", "65%", "70%", "75%"],
                "correct_answer": "70%"
            },
            {
                "id": "q5",
                "question": "Une fumée blanche épaisse indique généralement :",
                "options": ["Combustion d'huile", "Problème liquide refroidissement", "Surenrichissement", "Combustion incomplète"],
                "correct_answer": "Problème liquide refroidissement"
            },
            {
                "id": "q6",
                "question": "Le défaut récurrent du moteur 1.6 THP PSA survient vers :",
                "options": ["60 000-80 000 km", "80 000-120 000 km", "120 000-150 000 km", "150 000-200 000 km"],
                "correct_answer": "80 000-120 000 km"
            },
            {
                "id": "q7",
                "question": "Combien de défauts types sont référencés dans la base AutoJust ?",
                "options": ["2 000+", "2 250+", "2 500+", "2 750+"],
                "correct_answer": "2 500+"
            },
            {
                "id": "q8",
                "question": "Un avis favorable entraîne quel taux de concrétisation d'achat ?",
                "options": ["75%", "80%", "85%", "90%"],
                "correct_answer": "85%"
            },
            {
                "id": "q9",
                "question": "Combien de motorisations différentes sont couvertes par la base AutoJust ?",
                "options": ["650", "750", "850", "950"],
                "correct_answer": "850"
            },
            {
                "id": "q10",
                "question": "Une fumée bleue continue indique un coût de réparation de :",
                "options": ["500-1000€", "1000-1500€", "1500-3000€", "2000-5000€"],
                "correct_answer": "2000-5000€"
            },
            {
                "id": "q11",
                "question": "Le taux de satisfaction client avec un avis défavorable est de :",
                "options": ["92%", "95%", "98%", "99%"],
                "correct_answer": "98%"
            },
            {
                "id": "q12",
                "question": "L'avis moteur doit inclure des prévisions d'évolution sur :",
                "options": ["6, 12, 18 mois", "12, 24, 36 mois", "12, 18, 24 mois", "24, 36, 48 mois"],
                "correct_answer": "12, 24, 36 mois"
            }
        ]
    },
    {
        "id": "module-6",
        "title": "Outils Digitaux et Rapports Professionnels",
        "description": "Digitalisation complète : outils numériques, structuration des rapports et livraison professionnelle",
        "duration_minutes": 75,
        "order": 6,
        "content": """
        <h2>Module 6 : Outils Digitaux et Rapports Professionnels</h2>
        
        <img src="https://images.unsplash.com/photo-1587145820266-a0065b0661f2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdG9vbHN8ZW58MHx8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Outils digitaux professionnels" class="module-image" />
        
        <div class="chapter-divider"></div>

        <h3>Chapitre 1 : Présentation des outils numériques (WeProov, SafetyCulture, webapp)</h3>

        <p>La révolution digitale a transformé radicalement le métier d'inspecteur automobile. Les outils numériques modernes permettent une productivité accrue de 40%, une qualité de rapport supérieure et une traçabilité optimale. Cette transformation n'est plus optionnelle : elle conditionne la compétitivité et la crédibilité de l'inspecteur professionnel moderne.</p>

        <div class="info-box">
            <h4>🚀 Écosystème digital AutoJust</h4>
            <p>L'écosystème technologique AutoJust s'articule autour de 4 piliers :</p>
            <ul>
                <li><strong>WebApp AutoJust :</strong> Application mobile native pour inspection terrain</li>
                <li><strong>WeProov :</strong> Plateforme de constat visuel géolocalisé et horodaté</li>
                <li><strong>SafetyCulture (iAuditor) :</strong> Check-lists intelligentes et rapports automatisés</li>
                <li><strong>CRM intégré :</strong> Gestion client et suivi commercial</li>
            </ul>
        </div>

        <h4>WeProov : La référence du constat visuel</h4>

        <p>WeProov révolutionne la documentation visuelle de l'inspection en apportant une valeur juridique incontestable aux preuves photographiques. Utilisé par plus de 200 000 professionnels de l'automobile, cet outil garantit l'authenticité, l'horodatage et la géolocalisation de chaque prise de vue.</p>

        <table>
            <tr>
                <th>Fonctionnalité</th>
                <th>Avantage inspecteur</th>
                <th>Valeur ajoutée client</th>
                <th>Protection juridique</th>
            </tr>
            <tr>
                <td><strong>Horodatage certifié</strong></td>
                <td>Traçabilité absolue</td>
                <td>Confiance renforcée</td>
                <td>Preuve incontestable</td>
            </tr>
            <tr>
                <td><strong>Géolocalisation GPS</strong></td>
                <td>Contexte d'inspection</td>
                <td>Transparence totale</td>
                <td>Localisation certifiée</td>
            </tr>
            <tr>
                <td><strong>Blockchain</strong></td>
                <td>Inaltérabilité garantie</td>
                <td>Sécurité maximale</td>
                <td>Non-répudiation</td>
            </tr>
            <tr>
                <td><strong>Annotations intelligentes</strong></td>
                <td>Gain de temps</td>
                <td>Clarté pédagogique</td>
                <td>Précision technique</td>
            </tr>
        </table>

        <h4>SafetyCulture : L'intelligence des check-lists</h4>

        <p>SafetyCulture transforme les check-lists traditionnelles en outils intelligents capables de s'adapter au contexte, de guider l'inspecteur et de générer automatiquement des rapports structurés. Cette plateforme, utilisée par Boeing, Coca-Cola et des milliers d'entreprises mondiales, apporte une rigueur industrielle à l'inspection automobile.</p>

        <div class="success-box">
            <h4>📱 Fonctionnalités avancées SafetyCulture</h4>
            <ul>
                <li><strong>Check-lists conditionnelles :</strong> Questions adaptées selon les réponses précédentes</li>
                <li><strong>Capture multimédia :</strong> Photos, vidéos, enregistrements audio intégrés</li>
                <li><strong>Scoring automatique :</strong> Notation intelligente selon pondération définie</li>
                <li><strong>Actions correctives :</strong> Planification et suivi des interventions</li>
                <li><strong>Rapports temps réel :</strong> Génération instantanée au format PDF</li>
                <li><strong>Analytics :</strong> Tableaux de bord et statistiques de performance</li>
            </ul>
        </div>

        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxtb2JpbGUlMjBhcHB8ZW58MHx8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Application mobile inspection" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Avantages des checklists numériques</h3>

        <p>La transition du papier au numérique ne constitue pas une simple modernisation cosmétique, mais une révolution méthodologique qui transforme fondamentalement la qualité et l'efficacité de l'inspection. Les statistiques de nos inspecteurs certifiés démontrent des gains quantifiables significatifs.</p>

        <h4>Gains quantifiés de la digitalisation</h4>

        <div class="info-box">
            <h4>📊 Statistiques comparatives papier vs digital</h4>
            <table>
                <tr>
                    <th>Métrique</th>
                    <th>Check-list papier</th>
                    <th>Check-list numérique</th>
                    <th>Amélioration</th>
                </tr>
                <tr>
                    <td><strong>Durée inspection</strong></td>
                    <td>105 minutes</td>
                    <td>87 minutes</td>
                    <td>-17%</td>
                </tr>
                <tr>
                    <td><strong>Points de contrôle oubliés</strong></td>
                    <td>3,2 en moyenne</td>
                    <td>0,1 en moyenne</td>
                    <td>-97%</td>
                </tr>
                <tr>
                    <td><strong>Temps rédaction rapport</strong></td>
                    <td>45 minutes</td>
                    <td>12 minutes</td>
                    <td>-73%</td>
                </tr>
                <tr>
                    <td><strong>Erreurs de transcription</strong></td>
                    <td>2,1 par rapport</td>
                    <td>0,05 par rapport</td>
                    <td>-98%</td>
                </tr>
                <tr>
                    <td><strong>Satisfaction client</strong></td>
                    <td>87%</td>
                    <td>94%</td>
                    <td>+8%</td>
                </tr>
            </table>
        </div>

        <h4>Fonctionnalités intelligentes</h4>

        <p>Les check-lists numériques modernes intègrent des fonctionnalités d'intelligence artificielle qui assistent l'inspecteur dans sa démarche et garantissent l'exhaustivité du contrôle.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Structurer un rapport clair et professionnel</h3>

        <p>Le rapport d'inspection constitue le livrable principal de la prestation et détermine largement la satisfaction client. Sa structuration doit concilier exhaustivité technique et lisibilité pour le grand public, défi majeur qui distingue l'inspecteur professionnel de l'amateur éclairé.</p>

        <h4>Architecture du rapport AutoJust</h4>

        <div class="tip-box">
            <h4>📋 Structure type du rapport (12-15 pages)</h4>
            <ol>
                <li><strong>Page de couverture (1 page) :</strong> Informations véhicule, inspecteur, certification</li>
                <li><strong>Synthèse exécutive (1 page) :</strong> Note globale, recommandation, points clés</li>
                <li><strong>Avis moteur spécialisé (2 pages) :</strong> Analyse détaillée motorisation</li>
                <li><strong>Inspection par domaines (6-8 pages) :</strong> Carrosserie, mécanique, sécurité, confort</li>
                <li><strong>Documentation visuelle (2-3 pages) :</strong> Photos commentées, schémas</li>
                <li><strong>Recommandations et budget (1 page) :</strong> Plan d'action, estimations</li>
            </ol>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : L'importance des photos (qualité, datation, preuves)</h3>

        <p>La photographie constitue l'épine dorsale de la crédibilité du rapport d'inspection. À l'ère du numérique, une image vaut mille mots, mais une mauvaise image peut détruire toute crédibilité. La maîtrise de la photographie technique devient une compétence indispensable de l'inspecteur moderne.</p>

        <img src="https://images.unsplash.com/photo-1609205254950-c45c5817c6dd?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxwaG90b2dyYXBoeXxlbnwwfHx8fHwxNzU4NzE2Mjk1fDA&ixlib=rb-4.1.0&q=85" alt="Photographie technique automobile" class="module-image" />

        <h4>Standards de qualité photographique</h4>

        <div class="success-box">
            <h4>📸 Critères techniques photos inspection</h4>
            <ul>
                <li><strong>Résolution minimum :</strong> 8 MPx pour impression A4 qualité</li>
                <li><strong>Éclairage :</strong> Naturel privilégié, flash fill-in si nécessaire</li>
                <li><strong>Netteté :</strong> Zone d'intérêt parfaitement nette</li>
                <li><strong>Composition :</strong> Sujet centré, contexte visible</li>
                <li><strong>Couleurs :</strong> Balance des blancs correcte</li>
                <li><strong>Format :</strong> JPEG haute qualité avec métadonnées EXIF</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Délivrabilité et rapidité (rapport en <24h)</h3>

        <p>La rapidité de livraison du rapport constitue un facteur différenciant majeur dans un marché concurrentiel. L'objectif AutoJust de livraison sous 24h nécessite une organisation optimisée et l'exploitation maximale des outils numériques.</p>

        <div class="info-box">
            <h4>⚡ Workflow de livraison optimisé</h4>
            <ol>
                <li><strong>H+0 : Fin d'inspection :</strong> Données synchronisées automatiquement</li>
                <li><strong>H+2 : Retour bureau :</strong> Début rédaction avis moteur spécialisé</li>
                <li><strong>H+4 : Finalisation :</strong> Relecture, mise en forme, contrôle qualité</li>
                <li><strong>H+6 : Livraison :</strong> Envoi sécurisé client + copie archivage</li>
            </ol>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 6 : Exemple de rapport et exercice pratique</h3>

        <p>Pour maîtriser l'art du rapport professionnel, l'analyse d'exemples concrets et la pratique guidée constituent les méthodes pédagogiques les plus efficaces. Voici un exemple de rapport AutoJust accompagné d'un exercice pratique de rédaction.</p>

        <div class="warning-box">
            <h4>📄 Extrait rapport type - Renault Clio IV 1.5 dCi</h4>
            <h5>SYNTHÈSE EXÉCUTIVE</h5>
            <p><strong>Note globale : 7,2/10</strong> | <strong>Recommandation : ACHAT CONSEILLÉ avec réserves</strong></p>
            
            <p><strong>Points forts :</strong></p>
            <ul>
                <li>Entretien suivi régulièrement (carnet à jour)</li>
                <li>Carrosserie en excellent état (note 9/10)</li>
                <li>Intérieur préservé, cohérent avec kilométrage annoncé</li>
                <li>Pneumatiques récents (moins de 15 000 km)</li>
            </ul>
            
            <p><strong>Points d'attention :</strong></p>
            <ul>
                <li>Vanne EGR encrassée (nettoyage recommandé - 180€)</li>
                <li>Plaquettes avant à 40% d'usure (remplacement sous 6 mois - 120€)</li>
                <li>Courroie accessoires craquelée (remplacement préventif - 80€)</li>
            </ul>
            
            <p><strong>Budget prévisionnel 12 mois :</strong> 650€ (entretien + préventif)</p>
        </div>

        <p><em>Durée de lecture estimée : 75 minutes | Quiz de validation : 12 questions</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Les outils numériques permettent une amélioration de productivité de :",
                "options": ["30%", "35%", "40%", "45%"],
                "correct_answer": "40%"
            },
            {
                "id": "q2",
                "question": "Combien de professionnels utilisent WeProov ?",
                "options": ["150 000", "200 000", "250 000", "300 000"],
                "correct_answer": "200 000"
            },
            {
                "id": "q3",
                "question": "La digitalisation réduit les points de contrôle oubliés de :",
                "options": ["85%", "90%", "95%", "97%"],
                "correct_answer": "97%"
            },
            {
                "id": "q4",
                "question": "Le temps de rédaction d'un rapport numérique est de :",
                "options": ["8 minutes", "12 minutes", "15 minutes", "18 minutes"],
                "correct_answer": "12 minutes"
            },
            {
                "id": "q5",
                "question": "La résolution minimum recommandée pour les photos est de :",
                "options": ["5 MPx", "6 MPx", "8 MPx", "10 MPx"],
                "correct_answer": "8 MPx"
            },
            {
                "id": "q6",
                "question": "Un rapport AutoJust standard comprend combien de pages ?",
                "options": ["8-10 pages", "10-12 pages", "12-15 pages", "15-18 pages"],
                "correct_answer": "12-15 pages"
            },
            {
                "id": "q7",
                "question": "L'objectif de livraison AutoJust est de :",
                "options": ["12h", "18h", "24h", "48h"],
                "correct_answer": "24h"
            },
            {
                "id": "q8",
                "question": "Les erreurs de transcription sont réduites de combien avec le numérique ?",
                "options": ["95%", "96%", "97%", "98%"],
                "correct_answer": "98%"
            },
            {
                "id": "q9",
                "question": "La satisfaction client augmente de combien avec les outils numériques ?",
                "options": ["5%", "6%", "7%", "8%"],
                "correct_answer": "8%"
            },
            {
                "id": "q10",
                "question": "SafetyCulture est utilisé par combien d'entreprises mondiales ?",
                "options": ["Centaines", "Milliers", "Dizaines de milliers", "Centaines de milliers"],
                "correct_answer": "Milliers"
            },
            {
                "id": "q11",
                "question": "La durée d'inspection se réduit de combien avec les outils numériques ?",
                "options": ["15%", "17%", "19%", "21%"],
                "correct_answer": "17%"
            },
            {
                "id": "q12",
                "question": "Le workflow optimisé permet la livraison du rapport en combien d'heures ?",
                "options": ["4h", "6h", "8h", "10h"],
                "correct_answer": "6h"
            }
        ]
    },
    {
        "id": "module-7",
        "title": "Aspects Légaux, Éthique et Responsabilité",
        "description": "Cadre juridique, déontologie professionnelle et gestion des responsabilités de l'inspecteur",
        "duration_minutes": 35,
        "order": 7,
        "content": """
        <h2>Module 7 : Aspects Légaux, Éthique et Responsabilité</h2>
        
        <img src="https://images.unsplash.com/photo-1589829545856-d10d557cf95f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxsZWdhbHxlbnwwfHx8fHwxNzU4NzE2Mjk1fDA&ixlib=rb-4.1.0&q=85" alt="Aspects légaux et déontologie" class="module-image" />
        
        <div class="chapter-divider"></div>

        <h3>Chapitre 1 : Obligation de moyens vs résultat</h3>

        <p>La distinction fondamentale entre obligation de moyens et obligation de résultat constitue le pilier juridique de l'exercice professionnel de l'inspecteur automobile. Cette nuance, souvent mal comprise, détermine l'étendue de la responsabilité professionnelle et les conditions de mise en cause en cas de litige.</p>

        <div class="info-box">
            <h4>⚖️ Obligation de moyens de l'inspecteur</h4>
            <p>L'inspecteur automobile est soumis à une <strong>obligation de moyens</strong>, ce qui signifie :</p>
            <ul>
                <li><strong>Méthodologie rigoureuse :</strong> Application de la procédure AutoJust standardisée</li>
                <li><strong>Compétence professionnelle :</strong> Formation certifiée et mise à jour continue</li>
                <li><strong>Matériel adapté :</strong> Outils de diagnostic conformes aux standards</li>
                <li><strong>Temps suffisant :</strong> Durée d'inspection respectée (90 minutes minimum)</li>
                <li><strong>Documentation complète :</strong> Traçabilité de tous les contrôles effectués</li>
            </ul>
        </div>

        <p>Cette obligation de moyens protège l'inspecteur contre les reproches liés à la non-détection de vices cachés indétectables par les méthodes conventionnelles. Toutefois, elle ne constitue pas un blanc-seing et nécessite la démonstration de la rigueur professionnelle.</p>

        <h4>Limites de l'inspection non destructive</h4>

        <p>L'inspection automobile professionnelle s'exerce dans le cadre de l'examen non destructif, principe fondamental qui limite intrinsèquement la portée du diagnostic. Ces limites doivent être clairement explicitées au client pour prévenir les malentendus.</p>

        <table>
            <tr>
                <th>Domaine</th>
                <th>Contrôles possibles</th>
                <th>Limites techniques</th>
                <th>Recommandations</th>
            </tr>
            <tr>
                <td><strong>Moteur</strong></td>
                <td>Écoute, paramètres OBD, compression</td>
                <td>État interne cylindres, joints</td>
                <td>Analyse d'huile recommandée</td>
            </tr>
            <tr>
                <td><strong>Boîte de vitesses</strong></td>
                <td>Fonctionnement, bruits, fuites</td>
                <td>Usure interne engrenages</td>
                <td>Vidange préventive conseillée</td>
            </tr>
            <tr>
                <td><strong>Carrosserie</strong></td>
                <td>Inspection visuelle, mesures</td>
                <td>Corrosion cachée, mastic épais</td>
                <td>Contrôle périodique zones sensibles</td>
            </tr>
            <tr>
                <td><strong>Électronique</strong></td>
                <td>Diagnostic codes, tests fonctions</td>
                <td>Défaillances intermittentes</td>
                <td>Surveillance comportement ultérieur</td>
            </tr>
        </table>

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Inspecteur vs expert judiciaire</h3>

        <p>La confusion entre inspecteur automobile et expert judiciaire génère régulièrement des malentendus sur les prérogatives et la portée légale des conclusions. Cette distinction, fondamentale en droit, détermine la valeur probante du rapport et les conditions de sa contestation.</p>

        <div class="warning-box">
            <h4>🏛️ Différences fondamentales</h4>
            
            <h5>Expert judiciaire :</h5>
            <ul>
                <li><strong>Nomination :</strong> Désigné par décision de justice</li>
                <li><strong>Mission :</strong> Définie par le tribunal</li>
                <li><strong>Serment :</strong> Prestation de serment obligatoire</li>
                <li><strong>Contradictoire :</strong> Procédure contradictoire imposée</li>
                <li><strong>Rapport :</strong> Valeur probante renforcée</li>
            </ul>
            
            <h5>Inspecteur automobile :</h5>
            <ul>
                <li><strong>Mandatement :</strong> Contrat de droit privé</li>
                <li><strong>Mission :</strong> Définie par le client</li>
                <li><strong>Liberté :</strong> Aucune contrainte procédurale</li>
                <li><strong>Unilatéral :</strong> Examen pour une seule partie</li>
                <li><strong>Rapport :</strong> Valeur de simple renseignement</li>
            </ul>
        </div>

        <img src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxjb3VydHxlbnwwfHx8fHwxNzU4NzE2Mjk1fDA&ixlib=rb-4.1.0&q=85" alt="Justice et expertise" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Assurance RCP et protection</h3>

        <p>L'assurance Responsabilité Civile Professionnelle constitue la protection indispensable et obligatoire de l'inspecteur automobile. Au-delà de l'obligation légale, elle conditionne la crédibilité professionnelle et la sérénité d'exercice dans un métier où les enjeux financiers peuvent être considérables.</p>

        <h4>Garanties indispensables</h4>

        <div class="success-box">
            <h4>🛡️ Couverture RCP recommandée</h4>
            <ul>
                <li><strong>Dommages corporels :</strong> 4 500 000€ minimum par sinistre</li>
                <li><strong>Dommages matériels :</strong> 1 500 000€ minimum par sinistre</li>
                <li><strong>Dommages immatériels :</strong> 300 000€ minimum par sinistre</li>
                <li><strong>Défense-recours :</strong> 150 000€ minimum</li>
                <li><strong>Franchise :</strong> 500€ maximum</li>
                <li><strong>Extension géographique :</strong> Europe minimum</li>
                <li><strong>Retroactivité :</strong> Date de début d'activité</li>
            </ul>
        </div>

        <h4>Exclusions courantes à éviter</h4>

        <p>Certaines exclusions, fréquentes dans les contrats standards, peuvent laisser l'inspecteur démuni face à des sinistres pourtant prévisibles dans l'exercice normal de son activité.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : Déontologie, impartialité, conflits d'intérêts</h3>

        <p>La déontologie professionnelle constitue le socle de la crédibilité de l'inspecteur automobile. Dans un environnement où les pressions commerciales sont nombreuses et les enjeux financiers importants, le respect de règles éthiques strictes différencie le professionnel de l'amateur.</p>

        <div class="info-box">
            <h4>🎯 Les 10 principes déontologiques fondamentaux</h4>
            <ol>
                <li><strong>Indépendance :</strong> Aucun lien financier avec vendeur ou intermédiaire</li>
                <li><strong>Impartialité :</strong> Évaluation objective, sans parti pris</li>
                <li><strong>Compétence :</strong> Maintien et développement des connaissances</li>
                <li><strong>Intégrité :</strong> Honnêteté dans les constats et conclusions</li>
                <li><strong>Confidentialité :</strong> Protection des informations clients</li>
                <li><strong>Transparence :</strong> Clarté sur la méthodologie et les limites</li>
                <li><strong>Responsabilité :</strong> Assumation des conséquences de ses actes</li>
                <li><strong>Respect :</strong> Courtoisie envers tous les intervenants</li>
                <li><strong>Loyauté :</strong> Fidélité aux engagements contractuels</li>
                <li><strong>Formation :</strong> Mise à jour continue des compétences</li>
            </ol>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Confidentialité et RGPD</h3>

        <p>Le Règlement Général sur la Protection des Données (RGPD), applicable depuis mai 2018, impose des obligations strictes concernant la collecte, le traitement et la conservation des données personnelles. L'inspecteur automobile, qui manipule de nombreuses informations sensibles, doit maîtriser parfaitement ces exigences.</p>

        <div class="tip-box">
            <h4>🔒 Obligations RGPD de l'inspecteur</h4>
            <ul>
                <li><strong>Consentement explicite :</strong> Accord écrit pour traitement des données</li>
                <li><strong>Information transparente :</strong> Finalité et durée de conservation explicitées</li>
                <li><strong>Droit à l'effacement :</strong> Procédure de suppression des données</li>
                <li><strong>Sécurisation :</strong> Protection contre accès non autorisés</li>
                <li><strong>Registre des traitements :</strong> Documentation obligatoire</li>
                <li><strong>Notification des violations :</strong> Déclaration CNIL sous 72h</li>
            </ul>
        </div>

        <p><em>Durée de lecture estimée : 35 minutes | Quiz de validation : 12 questions</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "L'inspecteur automobile est soumis à une obligation de :",
                "options": ["Moyens", "Résultat", "Moyens et résultat", "Aucune obligation"],
                "correct_answer": "Moyens"
            },
            {
                "id": "q2",
                "question": "La durée minimum d'inspection recommandée est de :",
                "options": ["75 minutes", "90 minutes", "105 minutes", "120 minutes"],
                "correct_answer": "90 minutes"
            },
            {
                "id": "q3",
                "question": "Qui désigne un expert judiciaire ?",
                "options": ["Le client", "L'assurance", "Le tribunal", "La préfecture"],
                "correct_answer": "Le tribunal"
            },
            {
                "id": "q4",
                "question": "Le montant minimum recommandé pour la garantie dommages corporels est :",
                "options": ["3 000 000€", "4 500 000€", "6 000 000€", "7 500 000€"],
                "correct_answer": "4 500 000€"
            },
            {
                "id": "q5",
                "question": "La franchise RCP maximum recommandée est de :",
                "options": ["300€", "500€", "750€", "1000€"],
                "correct_answer": "500€"
            },
            {
                "id": "q6",
                "question": "Combien de principes déontologiques fondamentaux sont énumérés ?",
                "options": ["8", "10", "12", "15"],
                "correct_answer": "10"
            },
            {
                "id": "q7",
                "question": "Le RGPD est applicable depuis :",
                "options": ["Mai 2017", "Mai 2018", "Janvier 2018", "Janvier 2019"],
                "correct_answer": "Mai 2018"
            },
            {
                "id": "q8",
                "question": "Les violations de données doivent être déclarées à la CNIL sous :",
                "options": ["24h", "48h", "72h", "1 semaine"],
                "correct_answer": "72h"
            },
            {
                "id": "q9",
                "question": "L'inspection automobile s'exerce dans le cadre :",
                "options": ["Destructif", "Non destructif", "Semi-destructif", "Variables selon cas"],
                "correct_answer": "Non destructif"
            },
            {
                "id": "q10",
                "question": "Le rapport d'un inspecteur automobile a une valeur de :",
                "options": ["Preuve absolue", "Preuve renforcée", "Simple renseignement", "Présomption légale"],
                "correct_answer": "Simple renseignement"
            },
            {
                "id": "q11",
                "question": "La garantie dommages immatériels minimum recommandée est de :",
                "options": ["150 000€", "300 000€", "450 000€", "600 000€"],
                "correct_answer": "300 000€"
            },
            {
                "id": "q12",
                "question": "Le premier principe déontologique est :",
                "options": ["Compétence", "Indépendance", "Intégrité", "Impartialité"],
                "correct_answer": "Indépendance"
            }
        ]
    },
    {
        "id": "module-8",
        "title": "Business et Opérations de l'Inspecteur",
        "description": "Développement d'activité, acquisition client, tarification et organisation professionnelle",
        "duration_minutes": 40,
        "order": 8,
        "content": """
        <h2>Module 8 : Business et Opérations de l'Inspecteur</h2>
        
        <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxidXNpbmVzc3xlbnwwfHx8fHwxNzU4NzE2Mjk1fDA&ixlib=rb-4.1.0&q=85" alt="Business et développement" class="module-image" />
        
        <div class="chapter-divider"></div>

        <h3>Chapitre 1 : Panorama du marché (B2C, B2B, enchères, assureurs)</h3>

        <p>Le marché de l'inspection automobile française représente un potentiel de 450 millions d'euros, largement sous-exploité avec un taux de pénétration de seulement 15%. Cette situation offre des opportunités exceptionnelles aux inspecteurs professionnels capables de se positionner efficacement sur les différents segments.</p>

        <div class="info-box">
            <h4>📊 Segmentation du marché français</h4>
            <table>
                <tr>
                    <th>Segment</th>
                    <th>Volume annuel</th>
                    <th>Tarif moyen</th>
                    <th>Taux pénétration</th>
                    <th>Potentiel croissance</th>
                </tr>
                <tr>
                    <td><strong>B2C Particuliers</strong></td>
                    <td>4,2M transactions</td>
                    <td>180-250€</td>
                    <td>12%</td>
                    <td>400%</td>
                </tr>
                <tr>
                    <td><strong>B2B Professionnels</strong></td>
                    <td>800k véhicules</td>
                    <td>250-350€</td>
                    <td>25%</td>
                    <td>200%</td>
                </tr>
                <tr>
                    <td><strong>Enchères publiques</strong></td>
                    <td>150k véhicules</td>
                    <td>150-200€</td>
                    <td>45%</td>
                    <td>50%</td>
                </tr>
                <tr>
                    <td><strong>Expertises assurance</strong></td>
                    <td>2M sinistres</td>
                    <td>200-400€</td>
                    <td>35%</td>
                    <td>80%</td>
                </tr>
            </table>
        </div>

        <h4>Segment B2C : Le particulier au cœur</h4>

        <p>Le marché B2C représente le volume le plus important mais aussi la plus forte résistance culturelle. L'évolution des mentalités, accélérée par la digitalisation et la sensibilisation aux arnaques automobiles, ouvre progressivement ce marché aux inspecteurs professionnels.</p>

        <div class="success-box">
            <h4>🎯 Profils clients B2C prioritaires</h4>
            <ul>
                <li><strong>Primo-accédants (25-35 ans) :</strong> 40% du marché, sensibles à la sécurisation</li>
                <li><strong>Familles (35-50 ans) :</strong> 35% du marché, budget élevé, exigence qualité</li>
                <li><strong>Seniors (50+ ans) :</strong> 25% du marché, patrimoine à protéger</li>
                <li><strong>Passionnés automobile :</strong> Niche premium, prescripteurs influents</li>
            </ul>
        </div>

        <h4>Segment B2B : La professionnalisation</h4>

        <p>Le marché B2B, plus mature et rationnel, offre une rentabilité supérieure et une récurrence contractuelle. Les volumes traités permettent des économies d'échelle et une spécialisation technique avancée.</p>

        <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxtYXJrZXR8ZW58MHx8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Marché et opportunités" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Acquisition client (publicité, réseaux, partenariats)</h3>

        <p>L'acquisition client constitue le défi majeur de l'inspecteur débutant. Contrairement aux idées reçues, la qualité technique seule ne suffit pas : il faut développer une stratégie marketing cohérente et mesurable pour construire une clientèle durable.</p>

        <h4>Stratégies d'acquisition digitale</h4>

        <div class="tip-box">
            <h4>💻 Mix marketing digital recommandé</h4>
            <ul>
                <li><strong>SEO local (30% budget) :</strong> Référencement "inspection automobile [ville]"</li>
                <li><strong>Google Ads (25% budget) :</strong> Mots-clés géolocalisés, landing pages dédiées</li>
                <li><strong>Réseaux sociaux (20% budget) :</strong> Facebook/Instagram, ciblage démographique</li>
                <li><strong>Partenariats (15% budget) :</strong> Garages, mandataires, assureurs</li>
                <li><strong>Content marketing (10% budget) :</strong> Blog, vidéos pédagogiques</li>
            </ul>
        </div>

        <h4>Développement du réseau professionnel</h4>

        <p>Le réseau professionnel génère 65% des nouvelles affaires des inspecteurs établis. Sa construction nécessite une approche méthodique et un investissement temps conséquent, mais les retombées justifient largement cet effort.</p>

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Fidélisation et bouche-à-oreille</h3>

        <p>Dans un métier où la transaction est généralement unique (l'achat d'un véhicule d'occasion), la fidélisation ne peut reposer sur la récurrence directe mais sur la recommandation et la prescription. Un client satisfait génère en moyenne 3,2 recommandations sur 5 ans.</p>

        <h4>Programme de fidélisation AutoJust</h4>

        <div class="success-box">
            <h4>🌟 Stratégies de fidélisation éprouvées</h4>
            <ul>
                <li><strong>Suivi post-inspection :</strong> Appel à J+15, J+90, J+365</li>
                <li><strong>Newsletter technique :</strong> Conseils entretien, alertes rappels constructeur</li>
                <li><strong>Programme parrainage :</strong> Réduction 20% pour chaque recommandation</li>
                <li><strong>Garantie étendue :</strong> SAV 6 mois sur rapport d'inspection</li>
                <li><strong>Réseau privilège :</strong> Accès garages partenaires avec tarifs préférentiels</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : Tarification et positionnement</h3>

        <p>La tarification constitue l'un des leviers les plus sensibles de la stratégie commerciale. Une tarification mal calibrée peut détruire la rentabilité (prix trop bas) ou limiter drastiquement le volume (prix trop élevé). L'approche AutoJust privilégie une tarification par la valeur plutôt que par les coûts.</p>

        <h4>Grille tarifaire de référence</h4>

        <table>
            <tr>
                <th>Type de prestation</th>
                <th>Tarif de base</th>
                <th>Options valorisantes</th>
                <th>Positionnement</th>
            </tr>
            <tr>
                <td><strong>Inspection standard B2C</strong></td>
                <td>180-220€</td>
                <td>Rapport 24h (+30€)</td>
                <td>Milieu de gamme</td>
            </tr>
            <tr>
                <td><strong>Inspection premium B2C</strong></td>
                <td>250-320€</td>
                <td>Analyse d'huile (+80€)</td>
                <td>Haut de gamme</td>
            </tr>
            <tr>
                <td><strong>Inspection B2B série</strong></td>
                <td>150-180€</td>
                <td>Rapport digital (+20€)</td>
                <td>Volume</td>
            </tr>
            <tr>
                <td><strong>Expertise contradictoire</strong></td>
                <td>400-600€</td>
                <td>Présence tribunal (+200€)</td>
                <td>Spécialisé</td>
            </tr>
        </table>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Organisation personnelle et outils CRM</h3>

        <p>L'inspecteur automobile moderne jongle entre inspection terrain, rédaction de rapports, prospection commerciale et gestion administrative. Cette multiplicité d'activités nécessite une organisation rigoureuse et des outils adaptés pour maintenir efficacité et rentabilité.</p>

        <div class="info-box">
            <h4>🗓️ Planning type inspecteur professionnel</h4>
            <h5>Répartition hebdomadaire (40h) :</h5>
            <ul>
                <li><strong>Inspections terrain (60%) :</strong> 24h - 12 à 15 inspections/semaine</li>
                <li><strong>Rédaction rapports (20%) :</strong> 8h - Production livrables</li>
                <li><strong>Prospection/Commercial (15%) :</strong> 6h - Développement business</li>
                <li><strong>Administration (5%) :</strong> 2h - Facturation, comptabilité</li>
            </ul>
        </div>

        <h4>Outils CRM recommandés</h4>

        <div class="success-box">
            <h4>🔧 Suite logicielle inspecteur professionnel</h4>
            <ul>
                <li><strong>CRM :</strong> HubSpot (gratuit jusqu'à 1M contacts) ou Pipedrive</li>
                <li><strong>Agenda :</strong> Calendly intégré pour prise RDV automatisée</li>
                <li><strong>Facturation :</strong> Pennylane ou Tiime pour auto-entrepreneurs</li>
                <li><strong>Communication :</strong> Mailchimp pour newsletters + WhatsApp Business</li>
                <li><strong>Comptabilité :</strong> Indy ou L-Expert-Comptable.com</li>
                <li><strong>Stockage :</strong> Google Workspace ou Microsoft 365</li>
            </ul>
        </div>

        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxvcmdhbml6YXRpb258ZW58MHx8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Organisation et outils CRM" class="module-image" />

        <h4>Indicateurs de performance clés (KPIs)</h4>

        <div class="tip-box">
            <h4>📈 Tableau de bord inspecteur</h4>
            <ul>
                <li><strong>Taux de conversion prospect :</strong> >25% (objectif 30%)</li>
                <li><strong>Panier moyen :</strong> 220€ B2C / 180€ B2B</li>
                <li><strong>Temps moyen inspection :</strong> <95 minutes</li>
                <li><strong>Délai livraison rapport :</strong> <24h (objectif 12h)</li>
                <li><strong>Taux recommandation client :</strong> >90%</li>
                <li><strong>Récurrence parrainage :</strong> >15% nouveaux clients</li>
            </ul>
        </div>

        <div class="success-box">
            <h4>🎯 Objectifs de montée en puissance</h4>
            <table>
                <tr>
                    <th>Période</th>
                    <th>Inspections/mois</th>
                    <th>CA mensuel</th>
                    <th>Marge nette</th>
                </tr>
                <tr>
                    <td><strong>Mois 1-3</strong></td>
                    <td>8-12</td>
                    <td>1 800-2 500€</td>
                    <td>65%</td>
                </tr>
                <tr>
                    <td><strong>Mois 4-6</strong></td>
                    <td>15-20</td>
                    <td>3 200-4 200€</td>
                    <td>70%</td>
                </tr>
                <tr>
                    <td><strong>Mois 7-12</strong></td>
                    <td>25-35</td>
                    <td>5 200-7 200€</td>
                    <td>75%</td>
                </tr>
                <tr>
                    <td><strong>Année 2+</strong></td>
                    <td>40-50</td>
                    <td>8 000-12 000€</td>
                    <td>80%</td>
                </tr>
            </table>
        </div>

        <p><strong>Conclusion du parcours :</strong> À l'issue de ces 8 modules, vous disposez de toutes les clés pour exercer le métier d'inspecteur automobile avec professionnalisme et succès. La certification AutoJust valide vos compétences et vous ouvre les portes d'un marché en pleine expansion. Le succès dépend maintenant de votre capacité à appliquer rigoureusement cette méthodologie et à développer votre activité avec persévérance.</p>

        <p><em>Durée de lecture estimée : 40 minutes | Quiz de validation : 12 questions</em></p>
        """,
        "quiz_questions": [
            {
                "id": "q1",
                "question": "Le marché français de l'inspection automobile représente un potentiel de :",
                "options": ["350 millions €", "450 millions €", "550 millions €", "650 millions €"],
                "correct_answer": "450 millions €"
            },
            {
                "id": "q2",
                "question": "Le taux de pénétration actuel du marché B2C est de :",
                "options": ["8%", "12%", "15%", "18%"],
                "correct_answer": "12%"
            },
            {
                "id": "q3",
                "question": "Les primo-accédants représentent quel pourcentage du marché B2C ?",
                "options": ["35%", "40%", "45%", "50%"],
                "correct_answer": "40%"
            },
            {
                "id": "q4",
                "question": "Le SEO local devrait représenter quel pourcentage du budget marketing ?",
                "options": ["25%", "30%", "35%", "40%"],
                "correct_answer": "30%"
            },
            {
                "id": "q5",
                "question": "Un client satisfait génère en moyenne combien de recommandations sur 5 ans ?",
                "options": ["2,5", "3,2", "3,8", "4,1"],
                "correct_answer": "3,2"
            },
            {
                "id": "q6",
                "question": "Le tarif d'une inspection standard B2C se situe entre :",
                "options": ["150-180€", "180-220€", "220-260€", "260-300€"],
                "correct_answer": "180-220€"
            },
            {
                "id": "q7",
                "question": "Les inspections terrain représentent quel pourcentage du temps de travail ?",
                "options": ["55%", "60%", "65%", "70%"],
                "correct_answer": "60%"
            },
            {
                "id": "q8",
                "question": "Le taux de conversion prospect objectif est de :",
                "options": ["25%", "30%", "35%", "40%"],
                "correct_answer": "30%"
            },
            {
                "id": "q9",
                "question": "Le réseau professionnel génère quel pourcentage des nouvelles affaires ?",
                "options": ["55%", "60%", "65%", "70%"],
                "correct_answer": "65%"
            },
            {
                "id": "q10",
                "question": "La marge nette visée en année 2+ est de :",
                "options": ["70%", "75%", "80%", "85%"],
                "correct_answer": "80%"
            },
            {
                "id": "q11",
                "question": "Le volume d'inspections visé en mois 7-12 est de :",
                "options": ["20-30/mois", "25-35/mois", "30-40/mois", "35-45/mois"],
                "correct_answer": "25-35/mois"
            },
            {
                "id": "q12",
                "question": "L'objectif de délai de livraison des rapports est de :",
                "options": ["6h", "12h", "18h", "24h"],
                "correct_answer": "12h"
            }
        ]
    }
]

# Routes - Authentication
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    user_dict = user_data.dict()
    user_dict.pop('password')  # Remove plain password
    
    # Create User object for response (without hashed_password)
    user = User(**user_dict)
    
    # Add hashed_password for database storage
    user_dict_for_db = user.dict()
    user_dict_for_db['hashed_password'] = hashed_password
    
    # Store in database with hashed_password
    await db.users.insert_one(user_dict_for_db)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = await db.users.find_one({"email": user_credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Check if user has hashed_password field
    if 'hashed_password' not in user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    if not verify_password(user_credentials.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = create_access_token(data={"sub": user['email']})
    
    # Remove hashed_password before creating User object
    user_dict = {k: v for k, v in user.items() if k != 'hashed_password'}
    user_obj = User(**user_dict)
    
    return Token(access_token=access_token, token_type="bearer", user=user_obj)

# Routes - Course Management
@api_router.get("/modules", response_model=List[Dict[str, Any]])
async def get_modules():
    return COURSE_MODULES

@api_router.get("/modules/{module_id}")
async def get_module(module_id: str):
    module = next((m for m in COURSE_MODULES if m["id"] == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    return module

# Routes - Quiz & Progress
@api_router.post("/quiz/submit", response_model=QuizResult)
async def submit_quiz(quiz_submission: QuizSubmission, current_user: User = Depends(get_current_user)):
    # Find module
    module = next((m for m in COURSE_MODULES if m["id"] == quiz_submission.module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    
    # Calculate score
    total_questions = len(module["quiz_questions"])
    correct_answers = 0
    
    for question in module["quiz_questions"]:
        user_answer = quiz_submission.answers.get(question["id"])
        if user_answer == question["correct_answer"]:
            correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100)
    passed = score >= 70
    
    # Update user progress
    await db.users.update_one(
        {"email": current_user.email},
        {
            "$set": {
                f"quiz_scores.{quiz_submission.module_id}": score,
                f"progress.{quiz_submission.module_id}": "completed" if passed else "failed"
            },
            "$addToSet": {"completed_modules": quiz_submission.module_id} if passed else {}
        }
    )
    
    result = QuizResult(
        module_id=quiz_submission.module_id,
        score=score,
        total_questions=total_questions,
        passed=passed,
        answers=quiz_submission.answers
    )
    
    return result

@api_router.get("/user/progress")
async def get_user_progress(current_user: User = Depends(get_current_user)):
    # Get updated user data
    user = await db.users.find_one({"email": current_user.email})
    return {
        "completed_modules": user.get("completed_modules", []),
        "quiz_scores": user.get("quiz_scores", {}),
        "progress": user.get("progress", {}),
        "total_modules": len(COURSE_MODULES)
    }

@api_router.get("/user/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    user = await db.users.find_one({"email": current_user.email})
    # Remove hashed_password before creating User object
    user_dict = {k: v for k, v in user.items() if k != 'hashed_password'}
    user_obj = User(**user_dict)
    return user_obj

# Initialize modules in database on startup
@app.on_event("startup")
async def initialize_modules():
    for module in COURSE_MODULES:
        existing = await db.modules.find_one({"id": module["id"]})
        if not existing:
            await db.modules.insert_one(module)

# Include router
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()