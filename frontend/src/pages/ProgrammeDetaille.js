import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Helmet } from 'react-helmet-async';
import axios from "axios";
import { motion } from "framer-motion";
import { 
  BookOpen, 
  Clock, 
  CheckCircle, 
  Lock,
  Award,
  Users,
  Target,
  TrendingUp,
  Zap
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function ProgrammeDetaille() {
  const navigate = useNavigate();
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalModules: 0,
    totalDuration: 0,
    freeModules: 0
  });

  useEffect(() => {
    fetchModules();
  }, []);

  const fetchModules = async () => {
    try {
      // Récupérer tous les modules publiés pour la page de présentation
      const response = await axios.get(`${API}/modules/all-public`);
      const modulesData = response.data;
      
      setModules(modulesData);
      
      // Calculer les statistiques
      const totalDuration = modulesData.reduce((sum, mod) => sum + mod.duration_minutes, 0);
      const freeCount = modulesData.filter(mod => mod.is_free).length;
      
      setStats({
        totalModules: modulesData.length,
        totalDuration,
        freeModules: freeCount
      });
    } catch (error) {
      console.error('Erreur lors du chargement des modules:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0 && mins > 0) {
      return `${hours}h${mins}min`;
    } else if (hours > 0) {
      return `${hours}h`;
    } else {
      return `${mins}min`;
    }
  };

  // Structured data for SEO
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "Formation Inspecteur Automobile Certifié",
    "description": "Programme complet de formation pour devenir inspecteur automobile certifié avec la méthode d'inspection professionnelle. Formation en ligne complète avec certification reconnue.",
    "provider": {
      "@type": "Organization",
      "name": "Inspecteur Auto",
      "sameAs": "https://www.inspecteur-auto.fr"
    },
    "offers": {
      "@type": "Offer",
      "price": "297",
      "priceCurrency": "EUR",
      "availability": "https://schema.org/InStock",
      "url": "https://www.inspecteur-auto.fr/programme-detaille"
    },
    "hasCourseInstance": {
      "@type": "CourseInstance",
      "courseMode": "online",
      "duration": `PT${stats.totalDuration}M`
    },
    "numberOfCredits": modules.length,
    "educationalLevel": "Professional",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "187",
      "bestRating": "5"
    }
  };

  return (
    <>
      <Helmet>
        <title>Programme Détaillé - Formation Inspecteur Automobile | Inspecteur Auto</title>
        <meta 
          name="description" 
          content={`Découvrez le programme complet de notre formation d'inspecteur automobile. ${stats.totalModules} modules de formation, ${Math.floor(stats.totalDuration / 60)}h de contenu, certification reconnue. Devenez expert en diagnostic véhiculaire.`}
        />
        <meta name="keywords" content="formation inspecteur auto, programme formation, modules formation automobile, certification inspecteur, diagnostic véhiculaire, formation auto détaillée" />
        
        {/* Open Graph */}
        <meta property="og:title" content="Programme Détaillé - Formation Inspecteur Automobile" />
        <meta property="og:description" content={`Programme complet avec ${stats.totalModules} modules de formation pour devenir inspecteur automobile certifié.`} />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://www.inspecteur-auto.fr/programme-detaille" />
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Programme Détaillé - Formation Inspecteur Automobile" />
        <meta name="twitter:description" content={`Découvrez notre programme complet de ${stats.totalModules} modules de formation.`} />
        
        {/* Canonical URL */}
        <link rel="canonical" href="https://www.inspecteur-auto.fr/programme-detaille" />
        
        {/* Structured Data */}
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      </Helmet>

      <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="max-w-4xl mx-auto text-center"
            >
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
                Programme Détaillé de la Formation
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-blue-100">
                Découvrez le contenu complet de notre formation d'inspecteur automobile certifié
              </p>
              
              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
                  <BookOpen className="h-8 w-8 mb-3 mx-auto" />
                  <div className="text-3xl font-bold mb-2">{stats.totalModules}</div>
                  <div className="text-blue-100">Modules de formation</div>
                </div>
                <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
                  <Clock className="h-8 w-8 mb-3 mx-auto" />
                  <div className="text-3xl font-bold mb-2">{Math.floor(stats.totalDuration / 60)}h</div>
                  <div className="text-blue-100">de contenu vidéo</div>
                </div>
                <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
                  <Award className="h-8 w-8 mb-3 mx-auto" />
                  <div className="text-3xl font-bold mb-2">1</div>
                  <div className="text-blue-100">Certification reconnue</div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Programme Overview */}
        <section className="py-16 px-4">
          <div className="container mx-auto max-w-6xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-center mb-6 text-gray-900">
                Une Formation Complète et Structurée
              </h2>
              <p className="text-lg text-gray-600 text-center max-w-3xl mx-auto">
                Notre programme de formation est conçu pour vous transformer en expert du diagnostic automobile. 
                Chaque module vous apporte des compétences concrètes et immédiatement applicables.
              </p>
            </motion.div>

            {/* Key Benefits */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
              <Card>
                <CardContent className="pt-6 text-center">
                  <Target className="h-10 w-10 text-blue-600 mx-auto mb-3" />
                  <h3 className="font-semibold mb-2">Méthode d'inspection</h3>
                  <p className="text-sm text-gray-600">Système d'inspection éprouvé</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6 text-center">
                  <Users className="h-10 w-10 text-green-600 mx-auto mb-3" />
                  <h3 className="font-semibold mb-2">Support Expert</h3>
                  <p className="text-sm text-gray-600">Accompagnement personnalisé</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6 text-center">
                  <TrendingUp className="h-10 w-10 text-purple-600 mx-auto mb-3" />
                  <h3 className="font-semibold mb-2">Progression Suivie</h3>
                  <p className="text-sm text-gray-600">Tableau de bord détaillé</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6 text-center">
                  <Zap className="h-10 w-10 text-orange-600 mx-auto mb-3" />
                  <h3 className="font-semibold mb-2">Accès Immédiat</h3>
                  <p className="text-sm text-gray-600">Commencez dès maintenant</p>
                </CardContent>
              </Card>
            </div>

            {/* Modules List */}
            <div className="mb-12">
              <h2 className="text-3xl font-bold mb-8 text-gray-900">Contenu du Programme</h2>
              
              {loading ? (
                <div className="text-center py-12">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                  <p className="mt-4 text-gray-600">Chargement du programme...</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {modules.map((module, index) => (
                    <motion.div
                      key={module.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                    >
                      <Card className="hover:shadow-lg transition-shadow duration-300">
                        <CardHeader>
                          <div className="flex items-start justify-between">
                            <div className="flex-1" style={{ pointerEvents: 'none' }}>
                              <div className="flex items-center gap-3 mb-2">
                                <Badge variant="outline" className="text-lg px-3 py-1">
                                  Module {module.order_index}
                                </Badge>
                                {module.is_free ? (
                                  <Badge className="bg-green-500">
                                    <CheckCircle className="h-4 w-4 mr-1" />
                                    Gratuit
                                  </Badge>
                                ) : (
                                  <Badge variant="secondary">
                                    <Lock className="h-4 w-4 mr-1" />
                                    Premium
                                  </Badge>
                                )}
                              </div>
                              <CardTitle className="text-2xl mb-2">{module.title}</CardTitle>
                              <CardDescription className="text-base">
                                {module.description}
                              </CardDescription>
                            </div>
                            <div className="flex items-center gap-2 text-gray-600 ml-4">
                              <Clock className="h-5 w-5" />
                              <span className="font-medium">{formatDuration(module.duration_minutes)}</span>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          {/* On garde seulement le bouton, pas d'extrait de contenu */}
                          <div className="mt-6" style={{ pointerEvents: 'auto' }}>
                            {module.is_free ? (
                              <a
                                href="/register"
                                style={{
                                  display: 'block',
                                  width: '100%',
                                  padding: '20px 30px',
                                  backgroundColor: '#000000',
                                  color: '#ffffff',
                                  textAlign: 'center',
                                  textDecoration: 'none',
                                  borderRadius: '12px',
                                  fontWeight: '700',
                                  fontSize: '18px',
                                  cursor: 'pointer',
                                  userSelect: 'none',
                                  WebkitUserSelect: 'none',
                                  MozUserSelect: 'none',
                                  msUserSelect: 'none',
                                  boxShadow: '0 4px 6px rgba(0,0,0,0.3)',
                                  transition: 'all 0.2s',
                                  pointerEvents: 'auto'
                                }}
                                onMouseOver={(e) => {
                                  e.currentTarget.style.backgroundColor = '#1a1a1a';
                                  e.currentTarget.style.transform = 'scale(1.02)';
                                }}
                                onMouseOut={(e) => {
                                  e.currentTarget.style.backgroundColor = '#000000';
                                  e.currentTarget.style.transform = 'scale(1)';
                                }}
                              >
                                ✅ CLIQUEZ ICI - MODULE GRATUIT
                              </a>
                            ) : (
                              <a
                                href="/register"
                                style={{
                                  display: 'block',
                                  width: '100%',
                                  padding: '20px 30px',
                                  backgroundColor: '#2563eb',
                                  color: '#ffffff',
                                  textAlign: 'center',
                                  textDecoration: 'none',
                                  borderRadius: '12px',
                                  fontWeight: '700',
                                  fontSize: '18px',
                                  cursor: 'pointer',
                                  userSelect: 'none',
                                  WebkitUserSelect: 'none',
                                  MozUserSelect: 'none',
                                  msUserSelect: 'none',
                                  boxShadow: '0 4px 6px rgba(37,99,235,0.4)',
                                  transition: 'all 0.2s',
                                  pointerEvents: 'auto'
                                }}
                                onMouseOver={(e) => {
                                  e.currentTarget.style.backgroundColor = '#1d4ed8';
                                  e.currentTarget.style.transform = 'scale(1.02)';
                                }}
                                onMouseOut={(e) => {
                                  e.currentTarget.style.backgroundColor = '#2563eb';
                                  e.currentTarget.style.transform = 'scale(1)';
                                }}
                              >
                                🔓 CLIQUEZ ICI - S'INSCRIRE
                              </a>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              )}
            </div>

            {/* CTA Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-2xl p-8 md:p-12 text-center"
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Prêt à Commencer Votre Formation ?
              </h2>
              <p className="text-xl mb-8 text-blue-100">
                Rejoignez plus de 1,200 professionnels formés et certifiés
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/register">
                  <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                    Commencer la formation
                  </Button>
                </Link>
                <Link to="/contact">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto border-white text-white hover:bg-white/10">
                    Nous contacter
                  </Button>
                </Link>
              </div>
              <p className="mt-6 text-sm text-blue-100">
                <CheckCircle className="inline h-4 w-4 mr-1" />
                Module gratuit disponible • Certification reconnue • Garantie satisfait ou remboursé
              </p>
            </motion.div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-16 px-4 bg-white">
          <div className="container mx-auto max-w-4xl">
            <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Questions Fréquentes</h2>
            
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Quelle est la durée totale de la formation ?</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600">
                    La formation complète représente environ {Math.floor(stats.totalDuration / 60)} heures de contenu vidéo. 
                    Vous pouvez suivre les modules à votre rythme, selon votre disponibilité.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Les modules sont-ils accessibles à vie ?</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600">
                    Oui ! Une fois inscrit, vous avez un accès illimité à vie à tous les modules de formation 
                    et à toutes les mises à jour futures.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Y a-t-il des prérequis pour suivre la formation ?</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600">
                    Aucun prérequis technique n'est nécessaire. Notre formation est conçue pour vous accompagner 
                    depuis les bases jusqu'à l'expertise professionnelle.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>La certification est-elle reconnue ?</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600">
                    Oui, notre certification est délivrée après validation de tous les modules et quiz. 
                    Elle atteste de vos compétences en diagnostic automobile et est valorisée par les professionnels du secteur.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}

export default ProgrammeDetaille;
