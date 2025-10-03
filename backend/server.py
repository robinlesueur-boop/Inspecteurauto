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

        <p>L'inspection automobile représente aujourd'hui l'un des métiers les plus prometteurs du secteur automotive. Avec plus de 5,2 millions de véhicules d'occasion échangés chaque année en France, et seulement 15% d'entre eux faisant l'objet d'une inspection professionnelle, le potentiel de développement est considérable.</p>

        <p>Cette formation « Devenir Inspecteur Automobile » a été conçue pour vous accompagner dans cette démarche professionnalisante. Elle s'appuie sur la méthodologie AutoJust, reconnue par plus de 300 inspecteurs certifiés et validée par 50+ partenaires B2B incluant des compagnies d'assurance, des sociétés de leasing et des plateformes de vente aux enchères.</p>

        <div class="info-box">
            <h4>🎯 Pourquoi le diagnostic est-il essentiel ?</h4>
            <p>Le diagnostic de positionnement constitue le fondement de votre parcours de formation. Il permet de :</p>
            <ul>
                <li><strong>Évaluer précisément</strong> vos compétences techniques actuelles</li>
                <li><strong>Identifier</strong> vos points forts et axes d'amélioration</li>
                <li><strong>Personnaliser</strong> votre parcours d'apprentissage</li>
                <li><strong>Définir</strong> des objectifs SMART et réalisables</li>
                <li><strong>Optimiser</strong> votre temps de formation</li>
            </ul>
        </div>

        <p>L'inspection automobile moderne exige une approche méthodique et rigoureuse. Un inspecteur professionnel doit maîtriser près de 200 points de contrôle répartis sur l'ensemble du véhicule, de la carrosserie aux systèmes électroniques les plus sophistiqués. Cette complexité nécessite une formation structurée et progressive, adaptée à votre profil et à vos objectifs.</p>

        <p>Le rôle du diagnostic initial est de cartographier vos connaissances actuelles pour construire un parcours optimisé. Contrairement à une formation généraliste, notre approche personnalisée vous permet de concentrer vos efforts sur les domaines où vous en avez le plus besoin, tout en consolidant vos acquis.</p>

        <img src="https://images.unsplash.com/photo-1498887960847-2a5e46312788?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Tableau de bord automobile moderne" class="module-image" />

        <p>L'évolution technologique des véhicules modernes rend cette formation d'autant plus nécessaire. Les systèmes embarqués, la multiplication des capteurs, l'émergence des véhicules hybrides et électriques transforment radicalement le métier d'inspecteur. Une BMW Série 3 de 2020 embarque plus de 100 calculateurs interconnectés, contre une dizaine pour un modèle équivalent de 2000.</p>

        <div class="success-box">
            <h4>💡 L'avantage concurrentiel de la formation</h4>
            <p>Un inspecteur formé à la méthodologie AutoJust dispose d'un avantage concurrentiel majeur :</p>
            <ul>
                <li><strong>Crédibilité renforcée</strong> grâce à la certification officielle</li>
                <li><strong>Méthodologie éprouvée</strong> et reconnue par les professionnels</li>
                <li><strong>Outils digitaux intégrés</strong> (WebApp, WeProov)</li>
                <li><strong>Réseau professionnel</strong> de 300+ inspecteurs</li>
                <li><strong>Formation continue</strong> pour rester à jour</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 2 : Présentation du parcours global et des attentes</h3>

        <p>Cette formation s'articule autour de 8 modules progressifs, conçus pour vous mener de l'initiation à l'expertise en 9h30 de contenu théorique enrichi d'exercices pratiques. Chaque module répond à un objectif pédagogique précis et s'appuie sur des cas concrets issus de notre base de données de plus de 10 000 inspections réalisées.</p>

        <div class="info-box">
            <h4>📚 Architecture de la formation</h4>
            <table>
                <tr>
                    <th>Module</th>
                    <th>Durée</th>
                    <th>Objectif principal</th>
                    <th>Livrables</th>
                </tr>
                <tr>
                    <td><strong>Module 1</strong><br/>Diagnostic et positionnement</td>
                    <td>30 min</td>
                    <td>Auto-évaluation et personnalisation</td>
                    <td>Plan de formation personnalisé</td>
                </tr>
                <tr>
                    <td><strong>Module 2</strong><br/>Fondamentaux de l'inspection</td>
                    <td>1h30</td>
                    <td>Rôle et missions de l'inspecteur</td>
                    <td>Code de déontologie</td>
                </tr>
                <tr>
                    <td><strong>Module 3</strong><br/>Remise à niveau mécanique</td>
                    <td>2h00</td>
                    <td>Bases techniques indispensables</td>
                    <td>Glossaire technique</td>
                </tr>
                <tr>
                    <td><strong>Module 4</strong><br/>Procédé d'inspection</td>
                    <td>2h15</td>
                    <td>Méthodologie 200+ points</td>
                    <td>Checklists opérationnelles</td>
                </tr>
                <tr>
                    <td><strong>Module 5</strong><br/>Avis sur le moteur</td>
                    <td>45 min</td>
                    <td>Expertise moteur approfondie</td>
                    <td>Grilles d'évaluation</td>
                </tr>
                <tr>
                    <td><strong>Module 6</strong><br/>Outils digitaux et rapports</td>
                    <td>1h15</td>
                    <td>Digitalisation et professionnalisation</td>
                    <td>Modèles de rapports</td>
                </tr>
                <tr>
                    <td><strong>Module 7</strong><br/>Aspects légaux et déontologie</td>
                    <td>35 min</td>
                    <td>Cadre juridique et responsabilités</td>
                    <td>Contrats types</td>
                </tr>
                <tr>
                    <td><strong>Module 8</strong><br/>Business et opérations</td>
                    <td>40 min</td>
                    <td>Développement d'activité</td>
                    <td>Business plan type</td>
                </tr>
            </table>
        </div>

        <h4>Attentes et prérequis</h4>

        <p>Cette formation s'adresse à un public diversifié, des professionnels de l'automobile souhaitant évoluer aux personnes en reconversion. Les attentes varient selon votre profil, mais certains éléments sont communs à tous les participants :</p>

        <p><strong>Engagement et assiduité :</strong> La formation demande un investissement personnel significatif. Chaque module doit être suivi intégralement, les quiz réussis avec un minimum de 70%, et l'examen final validé dans les mêmes conditions. La réussite dépend directement de votre implication.</p>

        <p><strong>Curiosité technique :</strong> L'automobile moderne est complexe et en évolution constante. Un bon inspecteur fait preuve de curiosité permanente, lit la presse spécialisée, suit les évolutions technologiques et n'hésite pas à se former régulièrement.</p>

        <p><strong>Rigueur méthodologique :</strong> L'inspection automobile ne tolère aucune approximation. Chaque point de contrôle doit être vérifié selon la procédure, chaque anomalie documentée, chaque conclusion justifiée. Cette rigueur s'apprend et se cultive.</p>

        <img src="https://images.unsplash.com/photo-1606577924006-27d39b132ae2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Véhicule moderne en inspection" class="module-image" />

        <div class="tip-box">
            <h4>⭐ Facteurs de réussite</h4>
            <p>L'analyse de nos 300+ inspecteurs certifiés révèle les facteurs clés de réussite :</p>
            <ul>
                <li><strong>Formation complète :</strong> 95% de réussite pour les participants suivant l'intégralité du parcours</li>
                <li><strong>Pratique terrain :</strong> Démarrage d'activité sous 3 mois pour 80% des certifiés</li>
                <li><strong>Réseau professionnel :</strong> Intégration dans la communauté AutoJust</li>
                <li><strong>Formation continue :</strong> Mise à jour des connaissances tous les 2 ans</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 3 : Quiz d'auto-évaluation et son rôle</h3>

        <p>Le quiz d'auto-évaluation constitue l'outil central de ce premier module. Contrairement à un simple test de connaissances, il s'agit d'un véritable instrument de diagnostic pédagogique, développé en collaboration avec des experts en ingénierie de formation et validé sur plusieurs centaines de profils.</p>

        <h4>Méthodologie du quiz</h4>

        <p>Le quiz comprend 50 questions réparties en 8 domaines de compétence, chacun étant évalué selon 3 niveaux de maîtrise. Cette approche granulaire permet une analyse fine de votre profil et l'identification précise des axes de développement prioritaires.</p>

        <div class="info-box">
            <h4>🔍 Domaines évalués</h4>
            <ol>
                <li><strong>Mécanique moteur (10 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : Fonctionnement 4 temps, composants de base</li>
                        <li>Niveau 2 : Diagnostic pannes courantes, lecture paramètres</li>
                        <li>Niveau 3 : Analyse approfondie, optimisation performances</li>
                    </ul>
                </li>
                <li><strong>Transmission (6 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : Différence manuelle/automatique, embrayage</li>
                        <li>Niveau 2 : Diagnostic usure, symptômes dysfonctionnements</li>
                        <li>Niveau 3 : Technologies avancées (CVT, double embrayage)</li>
                    </ul>
                </li>
                <li><strong>Électronique/Diagnostic (8 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : Utilisation multimètre, lecture codes OBD</li>
                        <li>Niveau 2 : Diagnostic réseau CAN, paramètres temps réel</li>
                        <li>Niveau 3 : Programmation calculateurs, multiplexage</li>
                    </ul>
                </li>
                <li><strong>Sécurité active/passive (6 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : ABS, airbags, ceintures de sécurité</li>
                        <li>Niveau 2 : ESP, aide au freinage d'urgence</li>
                        <li>Niveau 3 : Systèmes d'aide à la conduite (ADAS)</li>
                    </ul>
                </li>
                <li><strong>Carrosserie/Structure (5 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : Détection impacts, corrosion visible</li>
                        <li>Niveau 2 : Analyse géométrie, déformations structurelles</li>
                        <li>Niveau 3 : Matériaux composites, réparations invisibles</li>
                    </ul>
                </li>
                <li><strong>Relation client (5 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : Communication de base, présentation</li>
                        <li>Niveau 2 : Gestion objections, pédagogie</li>
                        <li>Niveau 3 : Négociation complexe, médiation</li>
                    </ul>
                </li>
                <li><strong>Réglementation (5 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : Code de la route, contrôle technique</li>
                        <li>Niveau 2 : Garanties légales, responsabilités</li>
                        <li>Niveau 3 : Évolutions réglementaires, normes européennes</li>
                    </ul>
                </li>
                <li><strong>Outils/Méthodes (5 questions) :</strong>
                    <ul>
                        <li>Niveau 1 : Outillage de base, check-lists papier</li>
                        <li>Niveau 2 : Outils digitaux, applications mobiles</li>
                        <li>Niveau 3 : Intégration CRM, automatisation</li>
                    </ul>
                </li>
            </ol>
        </div>

        <h4>Système de notation</h4>

        <p>Chaque question est pondérée selon sa complexité et son importance dans la pratique professionnelle. Le système de notation utilisé s'appuie sur l'échelle de Bloom revisitée, permettant d'évaluer non seulement les connaissances factuelles, mais aussi la capacité d'analyse, de synthèse et d'application pratique.</p>

        <ul>
            <li><strong>Questions niveau 1 (1 point) :</strong> Connaissances factuelles, définitions, procédures de base</li>
            <li><strong>Questions niveau 2 (2 points) :</strong> Compréhension, application, diagnostic simple</li>
            <li><strong>Questions niveau 3 (3 points) :</strong> Analyse, synthèse, résolution de problèmes complexes</li>
        </ul>

        <p>Le score total sur 100 points permet de situer votre niveau global, tandis que les scores par domaine révèlent vos points forts et axes d'amélioration. Cette granularité est essentielle pour personnaliser efficacement votre parcours de formation.</p>

        <div class="warning-box">
            <h4>⚠️ Importance de l'honnêteté</h4>
            <p>L'efficacité du diagnostic repose entièrement sur votre honnêteté lors de l'évaluation. Il ne s'agit pas d'un concours, mais d'un outil de personnalisation pédagogique. Une surévaluation de vos compétences pourrait vous orienter vers un parcours inadapté et compromettre votre réussite.</p>
            
            <p>N'hésitez pas à répondre "Je ne sais pas" aux questions qui dépassent vos connaissances actuelles. Cette information est précieuse pour adapter la formation à vos besoins réels.</p>
        </div>

        <img src="https://images.unsplash.com/photo-1746079074522-2b14240d932c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85" alt="Diagnostic automobile professionnel" class="module-image" />

        <div class="chapter-divider"></div>

        <h3>Chapitre 4 : Analyse des résultats et profils types</h3>

        <p>L'analyse de milliers d'évaluations réalisées depuis le lancement de la formation AutoJust a permis d'identifier 6 profils types d'apprenants, chacun présentant des caractéristiques spécifiques en termes de points forts, axes de développement et stratégies pédagogiques optimales.</p>

        <h4>Profil 1 : Le Technicien Expert (15% des apprenants)</h4>

        <p><strong>Caractéristiques :</strong> Mécaniciens expérimentés, chefs d'atelier, techniciens spécialisés avec 10+ années d'expérience. Score moyen : 75-85 points, avec excellence en mécanique moteur (90%+) et électronique (80%+).</p>

        <p><strong>Points forts :</strong> Diagnostic technique approfondi, maîtrise des outils de mesure, compréhension fine des systèmes complexes, capacité à identifier rapidement les dysfonctionnements.</p>

        <p><strong>Axes de développement :</strong> Relation client (souvent sous-évaluée), rédaction de rapports accessibles aux non-techniciens, aspects commerciaux et marketing, utilisation d'outils digitaux modernes.</p>

        <p><strong>Parcours recommandé :</strong> Focus sur les modules 2, 6, 7 et 8. Révision accélérée du module 3. Accent particulier sur la communication client et le développement business.</p>

        <h4>Profil 2 : Le Contrôleur Méthodique (20% des apprenants)</h4>

        <p><strong>Caractéristiques :</strong> Contrôleurs techniques, inspecteurs qualité, auditeurs automobiles. Score moyen : 65-75 points, avec excellence en réglementation (85%+) et méthodes (80%+).</p>

        <p><strong>Points forts :</strong> Rigueur méthodologique, respect des procédures, connaissance réglementaire approfondie, capacité de synthèse et de documentation.</p>

        <p><strong>Axes de développement :</strong> Expertise moteur spécifique, conseil personnalisé client, adaptation aux évolutions technologiques, diagnostic électronique avancé.</p>

        <p><strong>Parcours recommandé :</strong> Parcours standard avec renforcement du module 5 (avis moteur) et approfondissement du module 3 (électronique moderne).</p>

        <h4>Profil 3 : Le Commercial Relationnel (25% des apprenants)</h4>

        <p><strong>Caractéristiques :</strong> Vendeurs automobiles, conseillers clientèle, négociants. Score moyen : 45-60 points, avec excellence en relation client (80%+) mais faiblesse technique marquée.</p>

        <p><strong>Points forts :</strong> Communication exceptionnelle, capacité de persuasion, compréhension des enjeux commerciaux, réseau professionnel développé.</p>

        <p><strong>Axes de développement :</strong> Compétences techniques globales, crédibilité technique, utilisation d'outils de diagnostic, connaissance approfondie des systèmes automobiles.</p>

        <p><strong>Parcours recommandé :</strong> Parcours renforcé avec attention particulière aux modules 3, 4 et 5. Formation technique préalable recommandée.</p>

        <h4>Profil 4 : Le Passionné Autodidacte (20% des apprenants)</h4>

        <p><strong>Caractéristiques :</strong> Passionnés d'automobile, mécaniciens amateurs, collectionneurs. Score moyen : 50-65 points, avec des connaissances hétérogènes mais une motivation exceptionnelle.</p>

        <p><strong>Points forts :</strong> Passion authentique, curiosité technique, connaissance historique des modèles, capacité d'apprentissage autodidacte élevée.</p>

        <p><strong>Axes de développement :</strong> Professionnalisation des méthodes, structuration des connaissances, relation client professionnelle, aspects légaux et réglementaires.</p>

        <p><strong>Parcours recommandé :</strong> Parcours standard avec coaching personnalisé et focus sur la professionnalisation (modules 2, 6, 7 et 8).</p>

        <h4>Profil 5 : Le Reconverti Motivé (15% des apprenants)</h4>

        <p><strong>Caractéristiques :</strong> Professionnels d'autres secteurs en reconversion, demandeurs d'emploi, créateurs d'entreprise. Score moyen : 30-50 points, avec de grandes lacunes techniques mais une forte motivation.</p>

        <p><strong>Points forts :</strong> Motivation exceptionnelle, regard neuf sur le secteur, compétences transversales (gestion, communication), disponibilité pour la formation.</p>

        <p><strong>Axes de développement :</strong> Connaissances techniques complètes, codes du secteur automobile, réseau professionnel, crédibilité technique.</p>

        <p><strong>Parcours recommandé :</strong> Parcours renforcé avec préformation technique recommandée. Accompagnement personnalisé et mentorat par un inspecteur expérimenté.</p>

        <h4>Profil 6 : L'Entrepreneur Visionnaire (5% des apprenants)</h4>

        <p><strong>Caractéristiques :</strong> Dirigeants d'entreprise, investisseurs, consultants cherchant à développer une activité d'inspection. Score moyen : 40-60 points, avec focus sur les aspects stratégiques.</p>

        <p><strong>Points forts :</strong> Vision business, capacité de développement, réseau professionnel étendu, compréhension des enjeux économiques.</p>

        <p><strong>Axes de développement :</strong> Compétences techniques opérationnelles, crédibilité terrain, connaissance fine des processus d'inspection.</p>

        <p><strong>Parcours recommandé :</strong> Parcours personnalisé avec focus technique (modules 3, 4, 5) et développement business approfondi (module 8).</p>

        <div class="success-box">
            <h4>📊 Statistiques de réussite par profil</h4>
            <ul>
                <li><strong>Technicien Expert :</strong> 98% de réussite, démarrage activité sous 1 mois</li>
                <li><strong>Contrôleur Méthodique :</strong> 95% de réussite, excellente satisfaction client</li>
                <li><strong>Commercial Relationnel :</strong> 85% de réussite, développement réseau rapide</li>
                <li><strong>Passionné Autodidacte :</strong> 90% de réussite, forte spécialisation</li>
                <li><strong>Reconverti Motivé :</strong> 75% de réussite, persévérance exemplaire</li>
                <li><strong>Entrepreneur Visionnaire :</strong> 80% de réussite, croissance business élevée</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 5 : Définition des objectifs SMART</h3>

        <p>La définition d'objectifs SMART (Spécifique, Mesurable, Atteignable, Réaliste, Temporellement défini) constitue une étape cruciale de votre parcours de formation. Elle transforme votre projet vague de "devenir inspecteur automobile" en plan d'action concret et réalisable.</p>

        <h4>Spécifique : Préciser votre projet professionnel</h4>

        <p>Votre objectif doit être parfaitement défini. "Devenir inspecteur automobile" est trop vague. Il faut préciser :</p>

        <ul>
            <li><strong>Type de clientèle visée :</strong> Particuliers (B2C), professionnels (B2B), ou mixte</li>
            <li><strong>Zone géographique :</strong> Locale, régionale, ou nationale</li>
            <li><strong>Spécialisation éventuelle :</strong> Véhicules de collection, utilitaires, véhicules de luxe</li>
            <li><strong>Mode d'exercice :</strong> Indépendant, salarié, ou franchise</li>
            <li><strong>Objectif de revenus :</strong> Activité complémentaire ou principale</li>
        </ul>

        <div class="info-box">
            <h4>💡 Exemples d'objectifs spécifiques</h4>
            <ul>
                <li>"Devenir inspecteur automobile indépendant spécialisé dans les véhicules de collection pour une clientèle de particuliers passionnés en région Île-de-France"</li>
                <li>"Développer une activité d'inspection B2B pour les sociétés de leasing et compagnies d'assurance sur un périmètre national avec objectif de 200 inspections/mois"</li>
                <li>"Créer un service d'inspection intégré à mon garage existant pour sécuriser les ventes de véhicules d'occasion auprès de ma clientèle locale"</li>
            </ul>
        </div>

        <h4>Mesurable : Quantifier vos ambitions</h4>

        <p>Vos objectifs doivent être quantifiables pour permettre le suivi et l'évaluation de votre progression :</p>

        <table>
            <tr>
                <th>Indicateur</th>
                <th>Débutant</th>
                <th>Intermédiaire</th>
                <th>Expert</th>
            </tr>
            <tr>
                <td><strong>Nombre d'inspections/mois</strong></td>
                <td>5-10</td>
                <td>15-30</td>
                <td>40-60</td>
            </tr>
            <tr>
                <td><strong>Chiffre d'affaires mensuel</strong></td>
                <td>1 500-3 000€</td>
                <td>4 000-8 000€</td>
                <td>10 000-15 000€</td>
            </tr>
            <tr>
                <td><strong>Durée moyenne d'inspection</strong></td>
                <td>120 min</td>
                <td>90 min</td>
                <td>75 min</td>
            </tr>
            <tr>
                <td><strong>Taux de recommandation client</strong></td>
                <td>80%</td>
                <td>90%</td>
                <td>95%+</td>
            </tr>
            <tr>
                <td><strong>Délai de livraison rapport</strong></td>
                <td>48h</td>
                <td>24h</td>
                <td>12h</td>
            </tr>
        </table>

        <h4>Atteignable : Évaluer la faisabilité</h4>

        <p>Vos objectifs doivent être ambitieux mais réalisables compte tenu de vos contraintes personnelles et professionnelles :</p>

        <p><strong>Contraintes temporelles :</strong> Combien d'heures par semaine pouvez-vous consacrer à cette activité ? Une activité d'inspection à temps plein nécessite 35-40h/semaine, une activité complémentaire peut se limiter à 10-15h/semaine.</p>

        <p><strong>Contraintes financières :</strong> Quel budget pouvez-vous consacrer au démarrage (matériel, assurance, communication) ? L'investissement initial varie de 3 000€ (équipement de base) à 15 000€ (équipement professionnel complet).</p>

        <p><strong>Contraintes géographiques :</strong> Votre zone d'intervention doit être suffisamment dense en véhicules pour générer un volume d'activité viable. Une zone rurale nécessitera des déplacements plus importants.</p>

        <h4>Réaliste : S'appuyer sur le marché</h4>

        <p>Vos objectifs doivent s'appuyer sur une analyse réaliste du marché local :</p>

        <div class="warning-box">
            <h4>📈 Données de marché à considérer</h4>
            <ul>
                <li><strong>Taille du marché local :</strong> Nombre de transactions VO annuelles dans votre zone</li>
                <li><strong>Concurrence existante :</strong> Nombre d'inspecteurs actifs, leurs tarifs, leur positionnement</li>
                <li><strong>Demande potentielle :</strong> Enquêtes clients, partenariats possibles</li>
                <li><strong>Évolution du marché :</strong> Tendances, réglementation, nouveaux usages</li>
            </ul>
        </div>

        <h4>Temporellement défini : Planifier les étapes</h4>

        <p>Votre projet doit s'inscrire dans un calendrier précis avec des étapes intermédiaires :</p>

        <div class="success-box">
            <h4>🗓️ Planning type de déploiement</h4>
            <ul>
                <li><strong>Mois 1 :</strong> Formation complète + certification</li>
                <li><strong>Mois 2 :</strong> Création structure juridique + assurances</li>
                <li><strong>Mois 3 :</strong> Acquisition matériel + communication</li>
                <li><strong>Mois 4-6 :</strong> Démarrage activité + premiers clients</li>
                <li><strong>Mois 7-12 :</strong> Montée en puissance + fidélisation</li>
                <li><strong>Année 2 :</strong> Développement + spécialisation</li>
            </ul>
        </div>

        <div class="chapter-divider"></div>

        <h3>Chapitre 6 : Cas pratiques introductifs (annonce, mise en situation)</h3>

        <p>Pour conclure ce module de diagnostic et positionnement, nous vous proposons trois cas pratiques introductifs qui vous permettront de vous projeter concrètement dans les situations que vous rencontrerez en tant qu'inspecteur automobile certifié.</p>

        <h4>Cas pratique n°1 : Analyse d'une annonce suspecte</h4>

        <div class="tip-box">
            <h4>📄 Annonce Leboncoin</h4>
            <p><strong>Titre :</strong> "BMW 320d 2018, 45 000 km, état impeccable, cause déménagement"</p>
            <p><strong>Prix :</strong> 18 500€ (prix de marché : 22 000€)</p>
            <p><strong>Description :</strong> "Véhicule en parfait état, jamais accidenté, carnet d'entretien à jour, pneus neufs, révision récente. Vente rapide cause déménagement à l'étranger."</p>
            <p><strong>Photos :</strong> 4 photos extérieures prises par beau temps, aucune photo d'intérieur ni de compartiment moteur.</p>
        </div>

        <p><strong>Signaux d'alerte identifiés :</strong></p>
        <ul>
            <li>Prix significativement inférieur au marché (-15%)</li>
            <li>Justification émotionnelle ("cause déménagement")</li>
            <li>Photos limitées et orientées</li>
            <li>Absence de défauts mentionnés</li>
            <li>Profil vendeur : compte récent, peu d'évaluations</li>
        </ul>

        <p>Dans ce contexte, votre rôle d'inspecteur sera crucial pour rassurer l'acheteur potentiel et identifier les éventuels vices cachés justifiant ce prix attractif.</p>

        <h4>Cas pratique n°2 : Inspection pour compagnie d'assurance</h4>

        <p><strong>Contexte :</strong> Sinistre déclaré par un assuré - "collision avec un sanglier sur l'A6". La compagnie d'assurance suspecte une fraude car les dégâts déclarés semblent disproportionnés et le lieu de l'accident est inhabituel pour ce type de sinistre.</p>

        <p><strong>Véhicule :</strong> Audi Q5 2020, 25 000 km</p>
        <p><strong>Dégâts déclarés :</strong> Pare-chocs avant, phare droit, capot déformé</p>
        <p><strong>Montant estimé :</strong> 8 500€</p>

        <p><strong>Mission d'inspection :</strong></p>
        <ul>
            <li>Analyser la cohérence des dégâts avec l'accident déclaré</li>
            <li>Rechercher d'éventuels dégâts antérieurs masqués</li>
            <li>Vérifier l'authenticité des pièces endommagées</li>
            <li>Documenter l'état général du véhicule</li>
            <li>Produire un rapport d'expertise détaillé</li>
        </ul>

        <p>Ce type de mission nécessite une expertise technique pointue et une parfaite connaissance des techniques de fraude les plus courantes.</p>

        <h4>Cas pratique n°3 : Inspection pré-achat véhicule de collection</h4>

        <p><strong>Contexte :</strong> Un passionné souhaite acquérir une Porsche 911 Carrera de 1989 pour 65 000€. Il fait appel à vos services pour sécuriser cet investissement important.</p>

        <p><strong>Particularités :</strong></p>
        <ul>
            <li>Véhicule de 35 ans avec historique complexe</li>
            <li>Modifications non d'origine possibles</li>
            <li>Valeur élevée justifiant une expertise approfondie</li>
            <li>Marché spécialisé avec codes spécifiques</li>
            <li>Acheteur expert nécessitant un rapport de haut niveau</li>
        </ul>

        <p><strong>Défis spécifiques :</strong></p>
        <ul>
            <li>Authentification des éléments d'origine</li>
            <li>Évaluation de l'état de conservation</li>
            <li>Identification des restaurations antérieures</li>
            <li>Estimation du potentiel d'évolution de valeur</li>
            <li>Conseil sur les priorités de restauration</li>
        </ul>

        <img src="https://images.pexels.com/photos/4489749/pexels-photo-4489749.jpeg" alt="Inspection professionnelle en cours" class="module-image" />

        <div class="success-box">
            <h4>🎯 Objectifs pédagogiques atteints</h4>
            <p>À l'issue de ce premier module, vous devriez avoir :</p>
            <ul>
                <li>✅ Évalué précisément votre niveau actuel</li>
                <li>✅ Identifié votre profil d'apprenant</li>
                <li>✅ Défini vos objectifs SMART</li>
                <li>✅ Compris les enjeux de la profession</li>
                <li>✅ Anticipé les situations professionnelles futures</li>
            </ul>
        </div>

        <p><strong>Prochaine étape :</strong> Le Module 2 vous permettra d'approfondir les fondamentaux de l'inspection automobile et de comprendre précisément le rôle et les missions de l'inspecteur professionnel.</p>

        <p><em>Durée de lecture estimée : 30 minutes | Quiz de validation : 12 questions</em></p>
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
        
        <h3>🎯 Objectifs du Module</h3>
        <ul>
            <li>Maîtriser le rôle et les missions de l'inspecteur automobile</li>
            <li>Comprendre les principes de transparence et d'impartialité</li>
            <li>Connaître le cadre réglementaire français et européen</li>
            <li>Intégrer les responsabilités légales et la déontologie</li>
        </ul>

        <h3>👨‍🔧 Rôle et Missions de l'Inspecteur</h3>
        
        <h4>Définition du Métier</h4>
        <p>L'inspecteur automobile est un <strong>expert technique indépendant</strong> spécialisé dans l'évaluation complète de véhicules. Il intervient comme tiers de confiance dans les transactions automobiles.</p>
        
        <div style="background: #1e293b; padding: 20px; border-radius: 8px; margin: 16px 0;">
            <h5>🎯 Missions Principales</h5>
            <ul>
                <li><strong>Inspection technique complète :</strong> Évaluation de l'état mécanique, esthétique et sécuritaire</li>
                <li><strong>Rédaction de rapport détaillé :</strong> Document officiel avec photos et recommandations</li>
                <li><strong>Conseil expert :</strong> Accompagnement du client dans sa décision d'achat</li>
                <li><strong>Estimation de valeur :</strong> Évaluation du prix de marché selon l'état</li>
                <li><strong>Détection de vices cachés :</strong> Identification des défauts non apparents</li>
                <li><strong>Formation du client :</strong> Explication des enjeux techniques</li>
            </ul>
        </div>

        <h4>Contextes d'Intervention</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Type d'intervention</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Client</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Objectif</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Enjeu</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Achat particulier</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Acheteur privé</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Sécuriser l'achat</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">5 000 - 50 000€</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Expertise assurance</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Compagnie d'assurance</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Évaluer les dommages</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Remboursement sinistre</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Fin de leasing</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Société de leasing</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">État de restitution</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Facturation dégradations</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Vente aux enchères</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Maison de ventes</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Estimation préalable</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Prix de réserve</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Litige commercial</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Tribunal/Avocat</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Expertise judiciaire</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Dommages et intérêts</td>
            </tr>
        </table>

        <h3>⚖️ Principes de Transparence et Impartialité</h3>
        
        <h4>Transparence Absolue</h4>
        <p>La transparence constitue le fondement de la crédibilité professionnelle :</p>
        
        <ul>
            <li><strong>Méthodologie explicite :</strong> Explication claire du processus d'inspection</li>
            <li><strong>Critères objectifs :</strong> Grille de notation standardisée et publique</li>
            <li><strong>Photos systématiques :</strong> Documentation visuelle de tous les points contrôlés</li>
            <li><strong>Sources d'information :</strong> Référencement des bases de données utilisées</li>
            <li><strong>Limites de l'expertise :</strong> Clarification de ce qui n'est pas contrôlable</li>
        </ul>

        <div style="background: #065f46; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>📋 Checklist Transparence</h5>
            <ul>
                <li>✅ Présentation de la méthodologie avant intervention</li>
                <li>✅ Explication des outils utilisés</li>
                <li>✅ Durée prévisionnelle communiquée</li>
                <li>✅ Tarification claire et détaillée</li>
                <li>✅ Remise du rapport dans les 24h</li>
                <li>✅ Disponibilité pour questions post-inspection</li>
            </ul>
        </div>

        <h4>Impartialité Rigoureuse</h4>
        <p>L'impartialité garantit la fiabilité de l'évaluation :</p>
        
        <ul>
            <li><strong>Indépendance financière :</strong> Aucun lien commercial avec vendeur/acheteur</li>
            <li><strong>Neutralité émotionnelle :</strong> Évaluation basée uniquement sur les faits</li>
            <li><strong>Résistance aux pressions :</strong> Maintien des conclusions malgré les influences</li>
            <li><strong>Égalité de traitement :</strong> Même rigueur quel que soit le client</li>
        </ul>

        <h4>Gestion des Conflits d'Intérêts</h4>
        
        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🚫 Situations à Éviter Absolument</h5>
            <ul>
                <li>Inspection d'un véhicule que vous souhaitez acheter</li>
                <li>Recommandation d'un garage partenaire</li>
                <li>Commission sur une vente suite à votre expertise</li>
                <li>Pression pour modifier vos conclusions</li>
                <li>Double expertise pour le même véhicule (vendeur + acheteur)</li>
            </ul>
        </div>

        <h3>📜 Cadre Réglementaire de l'Inspection</h3>
        
        <h4>Réglementation Française</h4>
        
        <h5>Code de la Consommation</h5>
        <p>Articles L217-1 à L217-32 relatifs à la conformité et aux vices cachés :</p>
        <ul>
            <li><strong>Garantie de conformité :</strong> 2 ans pour défauts existants à la livraison</li>
            <li><strong>Garantie des vices cachés :</strong> Défauts rendant le bien impropre à l'usage</li>
            <li><strong>Obligation d'information :</strong> Devoir du vendeur professionnel</li>
        </ul>

        <h5>Code Civil</h5>
        <p>Articles 1641 à 1649 sur la garantie des défauts cachés :</p>
        <ul>
            <li>Défaut caché existant lors de la vente</li>
            <li>Défaut suffisamment grave</li>
            <li>Défaut inconnu de l'acheteur</li>
        </ul>

        <h4>Réglementation Européenne</h4>
        
        <h5>Directive 2011/83/UE (Droits des consommateurs)</h5>
        <ul>
            <li>Information précontractuelle obligatoire</li>
            <li>Droit de rétractation (14 jours pour vente à distance)</li>
            <li>Garantie légale de conformité (2 ans minimum)</li>
        </ul>

        <h5>Règlement RGPD (Protection des données)</h5>
        <ul>
            <li>Consentement explicite pour collecte de données</li>
            <li>Droit à l'effacement et à la portabilité</li>
            <li>Registre des traitements obligatoire</li>
        </ul>

        <h3>⚖️ Responsabilités Légales</h3>
        
        <h4>Responsabilité Civile Professionnelle</h4>
        
        <div style="background: #1e40af; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>💼 Assurance RC Professionnelle Obligatoire</h5>
            <p><strong>Montants de garantie recommandés :</strong></p>
            <ul>
                <li>Dommages corporels : 4 500 000€ minimum</li>
                <li>Dommages matériels : 1 500 000€ minimum</li>
                <li>Défense-recours : 300 000€ minimum</li>
                <li>Franchise : 500€ maximum</li>
            </ul>
        </div>

        <h4>Responsabilité Pénale</h4>
        <p>L'inspecteur peut engager sa responsabilité pénale en cas de :</p>
        <ul>
            <li><strong>Faux et usage de faux :</strong> Rapport mensonger (5 ans de prison, 75 000€ d'amende)</li>
            <li><strong>Escroquerie :</strong> Tromperie sur l'état du véhicule (5 ans, 375 000€)</li>
            <li><strong>Mise en danger d'autrui :</strong> Non-signalement d'un défaut de sécurité</li>
        </ul>

        <h4>Responsabilité Administrative</h4>
        <ul>
            <li>Respect des obligations déclaratives (URSSAF, impôts)</li>
            <li>Tenue des registres professionnels</li>
            <li>Formation continue obligatoire</li>
        </ul>

        <h3>🏛️ Code de Déontologie Professionnelle</h3>
        
        <h4>Principes Fondamentaux</h4>
        
        <div style="background: #581c87; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h5>🎯 Les 10 Commandements de l'Inspecteur</h5>
            <ol>
                <li><strong>Compétence :</strong> Maintenir et développer ses connaissances techniques</li>
                <li><strong>Intégrité :</strong> Honnêteté absolue dans les constats</li>
                <li><strong>Objectivité :</strong> Évaluation basée uniquement sur les faits</li>
                <li><strong>Confidentialité :</strong> Protection des informations clients</li>
                <li><strong>Indépendance :</strong> Liberté de jugement préservée</li>
                <li><strong>Responsabilité :</strong> Assume les conséquences de ses actes</li>
                <li><strong>Respect :</strong> Courtoisie envers tous les intervenants</li>
                <li><strong>Loyauté :</strong> Fidélité aux engagements pris</li>
                <li><strong>Diligence :</strong> Célérité dans l'exécution des missions</li>
                <li><strong>Formation :</strong> Mise à jour permanente des compétences</li>
            </ol>
        </div>

        <h4>Relations avec les Clients</h4>
        <ul>
            <li><strong>Information préalable :</strong> Explication claire de la prestation</li>
            <li><strong>Consentement éclairé :</strong> Validation de la compréhension client</li>
            <li><strong>Respect des délais :</strong> Tenue des engagements temporels</li>
            <li><strong>Confidentialité :</strong> Non-divulgation d'informations privées</li>
            <li><strong>Suivi post-intervention :</strong> Disponibilité pour explications</li>
        </ul>

        <h4>Relations avec les Confrères</h4>
        <ul>
            <li><strong>Respect mutuel :</strong> Pas de dénigrement de collègues</li>
            <li><strong>Partage d'expérience :</strong> Contribution à l'évolution métier</li>
            <li><strong>Tarification éthique :</strong> Pas de concurrence déloyale</li>
            <li><strong>Entraide professionnelle :</strong> Solidarité en cas de difficulté</li>
        </ul>

        <h3>📋 Obligations Administratives</h3>
        
        <h4>Statut Juridique</h4>
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="background: #374151;">
                <th style="padding: 12px; border: 1px solid #4b5563;">Statut</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Avantages</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">Inconvénients</th>
                <th style="padding: 12px; border: 1px solid #4b5563;">CA maxi</th>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>Micro-entreprise</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Simplicité, charges réduites</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Plafond CA, pas de TVA</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">72 600€</td>
            </tr>
            <tr style="background: #1f2937;">
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>EURL</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Flexibilité, protection</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Comptabilité, charges sociales</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Illimité</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #4b5563;"><strong>SASU</strong></td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Statut cadre, dividendes</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Charges élevées</td>
                <td style="padding: 12px; border: 1px solid #4b5563;">Illimité</td>
            </tr>
        </table>

        <h4>Obligations Déclaratives</h4>
        <ul>
            <li><strong>Déclaration d'activité :</strong> CFE dans les 15 jours</li>
            <li><strong>Immatriculation :</strong> RCS ou Répertoire des Métiers</li>
            <li><strong>Assurance :</strong> RC Pro + véhicule professionnel</li>
            <li><strong>Formation :</strong> Stage SPI (Stage de Préparation à l'Installation)</li>
        </ul>

        <h3>🔍 Cas Pratiques Déontologiques</h3>
        
        <h4>Situation 1 : Conflit d'Intérêt</h4>
        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <p><strong>Cas :</strong> Un ami vous demande d'inspecter un véhicule qu'il souhaite vendre.</p>
            <p><strong>Problème :</strong> Risque de complaisance, crédibilité compromise</p>
            <p><strong>Solution :</strong> Refuser poliment et orienter vers un confrère</p>
        </div>

        <h4>Situation 2 : Pression Commerciale</h4>
        <div style="background: #7c2d12; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <p><strong>Cas :</strong> Le vendeur vous propose une "prime" pour un rapport favorable.</p>
            <p><strong>Problème :</strong> Corruption, faux en écriture</p>
            <p><strong>Solution :</strong> Refus catégorique, documenter la tentative</p>
        </div>

        <h4>Situation 3 : Découverte Importante</h4>
        <div style="background: #065f46; padding: 16px; border-radius: 8px; margin: 16px 0;">
            <p><strong>Cas :</strong> Découverte d'un défaut de sécurité critique non déclaré.</p>
            <p><strong>Action :</strong> Signalement immédiat, refus de valider la transaction</p>
            <p><strong>Justification :</strong> Sécurité publique prioritaire</p>
        </div>

        <h3>📚 Points Clés à Retenir</h3>
        
        <ul>
            <li>L'inspecteur est un <strong>expert indépendant</strong> au service de la sécurité des transactions</li>
            <li>La <strong>transparence</strong> et l'<strong>impartialité</strong> sont les piliers de la crédibilité</li>
            <li>Le <strong>cadre légal</strong> protège autant qu'il engage la responsabilité</li>
            <li>La <strong>déontologie</strong> guide les décisions dans les situations complexes</li>
            <li>La <strong>formation continue</strong> est une obligation professionnelle et éthique</li>
        </ul>

        <p><em>Durée estimée : 90 minutes de lecture + 20 minutes pour le quiz</em></p>
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