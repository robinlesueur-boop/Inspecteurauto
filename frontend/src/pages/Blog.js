import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Calendar, User, ArrowRight } from 'lucide-react';

const blogArticles = [
  {
    id: 1,
    title: "Comment devenir inspecteur automobile professionnel en 2025",
    slug: "devenir-inspecteur-automobile-2025",
    excerpt: "Découvrez les étapes essentielles pour démarrer votre carrière d'inspecteur automobile. Formation, équipement, réglementation... tout ce qu'il faut savoir.",
    author: "Équipe Inspecteur Auto",
    date: "15 janvier 2025",
    category: "Carrière",
    image: "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&q=80"
  },
  {
    id: 2,
    title: "Les 10 points de contrôle essentiels lors d'une inspection automobile",
    slug: "10-points-controle-inspection-automobile",
    excerpt: "Guide complet des vérifications indispensables pour une inspection automobile professionnelle. Carrosserie, mécanique, électronique...",
    author: "Expert AutoJust",
    date: "10 janvier 2025",
    category: "Technique",
    image: "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80"
  },
  {
    id: 3,
    title: "Marché de l'occasion : pourquoi l'inspection automobile est indispensable",
    slug: "marche-occasion-inspection-indispensable",
    excerpt: "Avec 5,5 millions de véhicules d'occasion vendus en France chaque année, l'inspection automobile devient un service incontournable pour les acheteurs.",
    author: "Équipe Inspecteur Auto",
    date: "5 janvier 2025",
    category: "Marché",
    image: "https://images.unsplash.com/photo-1563720360172-67b8f3dce741?w=800&q=80"
  },
  {
    id: 4,
    title: "Systèmes ADAS : le nouveau défi des inspecteurs automobiles",
    slug: "systemes-adas-defi-inspecteurs",
    excerpt: "Les systèmes d'aide à la conduite se multiplient. Comment les inspecter correctement ? Quels outils sont nécessaires ?",
    author: "Expert Technique",
    date: "28 décembre 2024",
    category: "Technologie",
    image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80"
  },
  {
    id: 5,
    title: "Tarifs inspection automobile 2025 : quel prix pratiquer ?",
    slug: "tarifs-inspection-automobile-2025",
    excerpt: "Analyse du marché et recommandations tarifaires pour les inspecteurs automobiles indépendants. De 150€ à 400€ selon les prestations.",
    author: "Équipe Inspecteur Auto",
    date: "20 décembre 2024",
    category: "Business",
    image: "https://images.unsplash.com/photo-1554224311-9f2c2170d17b?w=800&q=80"
  },
  {
    id: 6,
    title: "Fraude au kilométrage : comment la détecter efficacement",
    slug: "fraude-kilometrage-detection",
    excerpt: "35% des véhicules d'occasion présentent des anomalies. Apprenez les techniques pour détecter une fraude au compteur kilométrique.",
    author: "Expert AutoJust",
    date: "15 décembre 2024",
    category: "Technique",
    image: "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&q=80"
  }
];

function Blog() {
  return (
    <>
      <Helmet>
        <title>Blog - Inspecteur Automobile | Conseils, Actualités & Guides</title>
        <meta name="description" content="Blog de la formation Inspecteur Automobile : guides professionnels, actualités du marché, conseils techniques et tout ce qu'il faut savoir sur l'inspection automobile." />
        <meta name="keywords" content="inspecteur automobile, blog automobile, inspection voiture, contrôle véhicule occasion, formation inspecteur auto, ADAS, diagnostic automobile" />
      </Helmet>

      <div className="min-h-screen bg-gray-50">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-4xl font-bold mb-4">
              Blog Inspecteur Automobile
            </h1>
            <p className="text-xl text-blue-100 max-w-3xl">
              Guides professionnels, actualités du secteur, conseils techniques et 
              tout ce qu'il faut savoir pour réussir dans l'inspection automobile.
            </p>
          </div>
        </div>

        {/* Articles Grid */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {blogArticles.map((article) => (
              <Card key={article.id} className="hover:shadow-lg transition-shadow">
                <div className="aspect-video w-full overflow-hidden">
                  <img
                    src={article.image}
                    alt={article.title}
                    className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  />
                </div>
                
                <CardHeader>
                  <div className="flex items-center space-x-4 text-sm text-gray-500 mb-2">
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">
                      {article.category}
                    </span>
                    <div className="flex items-center">
                      <Calendar className="w-3 h-3 mr-1" />
                      {article.date}
                    </div>
                  </div>
                  
                  <CardTitle className="text-xl hover:text-blue-600 transition-colors">
                    {article.title}
                  </CardTitle>
                  
                  <CardDescription className="text-sm mt-2">
                    {article.excerpt}
                  </CardDescription>
                </CardHeader>
                
                <CardContent>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center text-sm text-gray-600">
                      <User className="w-4 h-4 mr-1" />
                      {article.author}
                    </div>
                    
                    <button className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center">
                      Lire plus
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* SEO-optimized content section */}
          <div className="mt-16 prose max-w-none">
            <Card className="p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Pourquoi devenir inspecteur automobile en 2025 ?
              </h2>
              
              <div className="text-gray-700 space-y-4">
                <p>
                  Le métier d'<strong>inspecteur automobile</strong> connaît un essor considérable 
                  en France. Avec plus de 5,5 millions de véhicules d'occasion vendus chaque année 
                  et une méfiance croissante des acheteurs face aux arnaques, l'<strong>inspection 
                  automobile professionnelle</strong> devient un service indispensable.
                </p>
                
                <h3 className="text-xl font-semibold text-gray-900 mt-6 mb-3">
                  Le marché de l'inspection automobile
                </h3>
                <p>
                  Le marché français du véhicule d'occasion représente un secteur dynamique où 
                  environ 35% des véhicules présentent des anomalies non déclarées. Cette réalité 
                  crée une demande importante pour les <strong>inspecteurs automobiles qualifiés</strong> 
                  capables d'effectuer des <strong>contrôles techniques approfondis</strong>.
                </p>
                
                <h3 className="text-xl font-semibold text-gray-900 mt-6 mb-3">
                  Compétences requises pour l'inspection automobile
                </h3>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Maîtrise du <strong>diagnostic automobile électronique</strong> (valises OBD, ADAS)</li>
                  <li>Connaissance approfondie de la <strong>mécanique automobile</strong></li>
                  <li>Capacité d'analyse des systèmes de <strong>sécurité active et passive</strong></li>
                  <li>Expertise en <strong>inspection carrosserie et châssis</strong></li>
                  <li>Compétences en rédaction de <strong>rapports d'expertise automobile</strong></li>
                </ul>
                
                <h3 className="text-xl font-semibold text-gray-900 mt-6 mb-3">
                  Revenus et perspectives d'un inspecteur automobile
                </h3>
                <p>
                  Un <strong>inspecteur automobile indépendant</strong> peut facturer entre 150€ 
                  et 400€ par inspection selon la complexité et le type de véhicule. Avec une 
                  moyenne de 3 à 5 inspections par jour, le potentiel de revenus est attractif, 
                  surtout dans les zones urbaines où la demande est forte.
                </p>
                
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8">
                  <h3 className="text-lg font-semibold text-blue-900 mb-3">
                    Formez-vous avec notre programme certifiant
                  </h3>
                  <p className="text-blue-800 mb-4">
                    Notre <strong>formation inspecteur automobile</strong> vous prépare à tous 
                    les aspects du métier : diagnostic, méthodologie AutoJust, réglementation, 
                    gestion d'entreprise et bien plus encore.
                  </p>
                  <Link to="/register">
                    <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium">
                      Découvrir la formation
                    </button>
                  </Link>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </>
  );
}

export default Blog;
