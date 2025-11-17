import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Helmet } from 'react-helmet-async';
import { useAuth } from "../contexts/AuthContext";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { motion } from "framer-motion";
import QualiopiInfo from "../components/QualiopiInfo";
import axios from "axios";
import { 
  Car, 
  Users, 
  Trophy, 
  Star, 
  Play, 
  CheckCircle, 
  ArrowRight,
  Target,
  Clock,
  Award,
  BookOpen,
  TrendingUp,
  Shield,
  Zap,
  Globe,
  MessageCircle
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Home() {
  const { isAuthenticated } = useAuth();
  const [content, setContent] = useState({
    hero_title: "Devenez Inspecteur Automobile Certifié",
    hero_subtitle: "Maîtrisez l'art du diagnostic véhiculaire avec la méthode AutoJust. Formation complète en 11h pour générer jusqu'à 8000€/mois.",
    hero_image_url: "https://images.unsplash.com/photo-1762517296945-74561c2cf21e",
    stat_graduates: "1,200+",
    stat_success_rate: "97%",
    stat_duration: "11h",
    stat_rating: "4.9/5",
    price_amount: "297€",
    price_description: "Formation complète + Certification",
    cta_primary: "Commencer la formation",
    cta_secondary: "Module gratuit",
    feature_1_title: "Méthode AutoJust",
    feature_1_description: "Système d'inspection révolutionnaire utilisé par plus de 500 professionnels en France.",
    feature_2_title: "Certification Reconnue",
    feature_2_description: "Obtenez votre certification officielle d'inspecteur automobile valorisée par l'industrie.",
    feature_3_title: "Communauté Active",
    feature_3_description: "Rejoignez une communauté de 1000+ inspecteurs et échangez sur vos expériences.",
    feature_4_title: "Revenus Attractifs",
    feature_4_description: "Générez 50 à 300€ par inspection avec un potentiel jusqu'à 4000€/mois.",
    features_image_url: "https://images.unsplash.com/photo-1760836395760-cd81defecf27",
    training_image_url: "https://images.unsplash.com/photo-1615906655593-ad0386982a0f",
    social_proof_image_url: "https://images.unsplash.com/photo-1573164574572-cb89e39749b4"
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLandingContent();
  }, []);

  const fetchLandingContent = async () => {
    try {
      const response = await axios.get(`${API}/landing-page/content`);
      setContent(response.data);
    } catch (error) {
      console.error('Error fetching landing page content:', error);
      // Keep default content if API fails
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      icon: <Target className="h-8 w-8 text-blue-600" />,
      title: content.feature_1_title,
      description: content.feature_1_description
    },
    {
      icon: <Award className="h-8 w-8 text-green-600" />,
      title: content.feature_2_title,
      description: content.feature_2_description
    },
    {
      icon: <Users className="h-8 w-8 text-purple-600" />,
      title: content.feature_3_title,
      description: content.feature_3_description
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-orange-600" />,
      title: content.feature_4_title,
      description: content.feature_4_description
    }
  ];

  const stats = [
    { number: content.stat_graduates, label: "Diplômés", icon: <Users className="h-5 w-5" /> },
    { number: content.stat_success_rate, label: "Taux de Réussite", icon: <Trophy className="h-5 w-5" /> },
    { number: content.stat_duration, label: "de Formation", icon: <Clock className="h-5 w-5" /> },
    { number: content.stat_rating, label: "Note Moyenne", icon: <Star className="h-5 w-5 fill-current" /> }
  ];

  const testimonials = [
    {
      name: "Thomas Dubois",
      role: "Inspecteur Indépendant",
      content: "Grâce à cette formation, j'ai pu lancer mon activité d'inspecteur en 3 mois. Je génère maintenant plus de 4000€/mois !",
      rating: 5,
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face",
      location: "Lyon"
    },
    {
      name: "Marine Laurent",
      role: "Experte Assurance",
      content: "Formation très complète qui m'a permis d'évoluer vers un poste d'experte automobile. Contenu de qualité professionnelle.",
      rating: 5,
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=100&h=100&fit=crop&crop=face",
      location: "Paris"
    },
    {
      name: "Jean-Paul Martin",
      role: "Ancien Mécanicien",
      content: "À 45 ans, j'ai pu me reconvertir grâce à cette formation. La méthode AutoJust fait vraiment la différence !",
      rating: 5,
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face",
      location: "Toulouse"
    }
  ];

  const modules = [
    "Introduction à l'inspection automobile",
    "Diagnostic moteur et transmission avancé", 
    "Inspection carrosserie et châssis",
    "Systèmes électroniques et ADAS",
    "Méthodologie AutoJust propriétaire",
    "Certification et pratique professionnelle"
  ];

  return (
    <>
      <Helmet>
        <title>Formation Inspecteur Automobile - Devenez Inspecteur Certifié</title>
        <meta name="description" content="Formation professionnelle d'inspecteur automobile. Maîtrisez le diagnostic véhiculaire, générez jusqu'à 8000€/mois. Méthode AutoJust - Certification incluse." />
        <meta name="keywords" content="formation inspecteur automobile, diagnostic véhiculaire, contrôle véhicule, inspection automobile, formation auto, certification automobile" />
        <meta property="og:title" content="Formation Inspecteur Automobile - Devenez Inspecteur Certifié" />
        <meta property="og:description" content="Formation complète avec certification reconnue. Revenus jusqu'à 8000€/mois." />
        <meta property="og:type" content="website" />
        <link rel="canonical" href={window.location.href} />
      </Helmet>

      <div className="min-h-screen">
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 text-white py-20 lg:py-32 overflow-hidden">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0 bg-grid-pattern"></div>
          </div>
          
          {/* Floating Elements */}
          <div className="absolute top-20 left-10 opacity-20">
            <Car className="h-24 w-24 text-blue-300 animate-pulse" />
          </div>
          <div className="absolute bottom-20 right-10 opacity-20">
            <Shield className="h-32 w-32 text-blue-300 animate-pulse" />
          </div>
          
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Hero Content */}
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-center lg:text-left"
              >
                <Badge className="mb-6 bg-blue-600/20 text-blue-200 border-blue-400 hover:bg-blue-600/30" data-testid="hero-badge">
                  🚀 Formation #1 en France - {content.stat_graduates} diplômés
                </Badge>
                
                <h1 className="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
                  {content.hero_title}
                </h1>
                
                <p className="text-xl text-blue-100 mb-8 max-w-2xl leading-relaxed">
                  {content.hero_subtitle}
                </p>
                
                <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start mb-12">
                  {isAuthenticated ? (
                    <Link to="/dashboard" data-testid="hero-dashboard-button">
                      <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
                        <BookOpen className="mr-2 h-5 w-5" />
                        Continuer ma formation
                      </Button>
                    </Link>
                  ) : (
                    <Link to="/register" data-testid="hero-register-button">
                      <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
                        <Play className="mr-2 h-5 w-5" />
                        {content.cta_primary}
                      </Button>
                    </Link>
                  )}
                  
                  <Button size="lg" variant="outline" className="border-blue-300 text-blue-100 hover:bg-blue-800/50 px-8 py-4 text-lg">
                    {content.cta_secondary}
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </div>

                {/* Trust Indicators */}
                <div className="flex flex-wrap justify-center lg:justify-start gap-8">
                  {stats.map((stat, index) => (
                    <motion.div 
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: index * 0.1 }}
                      className="text-center"
                    >
                      <div className="flex items-center justify-center mb-2 text-blue-300">
                        {stat.icon}
                      </div>
                      <div className="text-2xl font-bold text-white">{stat.number}</div>
                      <div className="text-sm text-blue-200">{stat.label}</div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>

              {/* Hero Visual */}
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8 }}
                className="relative lg:block hidden"
              >
                <div className="relative rounded-2xl overflow-hidden shadow-2xl bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-sm border border-white/20">
                  <img 
                    src={content.hero_image_url} 
                    alt="Inspecteur automobile professionnel au travail" 
                    className="w-full h-auto object-cover opacity-90"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-blue-900/40 to-transparent"></div>
                </div>
                
                {/* Floating Cards */}
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.8 }}
                  className="absolute -bottom-6 -left-6 bg-white rounded-lg shadow-xl p-4 max-w-xs"
                >
                  <div className="flex items-center space-x-3">
                    <div className="bg-green-100 p-2 rounded-lg">
                      <CheckCircle className="h-6 w-6 text-green-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">Certification Garantie</div>
                      <div className="text-sm text-gray-600">Reconnue par l'industrie</div>
                    </div>
                  </div>
                </motion.div>
                
                <motion.div 
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 1 }}
                  className="absolute -top-6 -right-6 bg-white rounded-lg shadow-xl p-4"
                >
                  <div className="flex items-center space-x-3">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <Zap className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">Formation Express</div>
                      <div className="text-sm text-gray-600">Seulement 11 heures</div>
                    </div>
                  </div>
                </motion.div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-gray-50" data-testid="features-section">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <motion.h2 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4"
              >
                Pourquoi Choisir Notre Formation ?
              </motion.h2>
              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="text-xl text-gray-600 max-w-3xl mx-auto"
              >
                La seule formation qui vous garantit de maîtriser l'inspection automobile 
                avec une méthode unique et une certification reconnue.
              </motion.p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                >
                  <Card className="text-center h-full hover:shadow-xl transition-all duration-300 border-0 shadow-lg bg-white">
                    <CardContent className="p-8">
                      <div className="flex justify-center mb-6 p-3 bg-gray-50 rounded-full w-fit mx-auto">
                        {feature.icon}
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        {feature.title}
                      </h3>
                      <p className="text-gray-600 leading-relaxed">
                        {feature.description}
                      </p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Image Showcase Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <img 
                  src={content.features_image_url}
                  alt="Technique d'inspection professionnelle"
                  className="rounded-2xl shadow-2xl w-full h-auto object-cover"
                />
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="space-y-6"
              >
                <h3 className="text-3xl font-bold text-gray-900">
                  Une Formation Pratique et Professionnelle
                </h3>
                <p className="text-lg text-gray-600 leading-relaxed">
                  Apprenez les techniques d'inspection les plus avancées avec notre méthode AutoJust éprouvée par des centaines de professionnels.
                </p>
                <ul className="space-y-4">
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                    <span className="text-gray-700">Techniques d'inspection détaillées et visuelles</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                    <span className="text-gray-700">Cas pratiques réels et retours d'expérience</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                    <span className="text-gray-700">Support personnalisé et communauté active</span>
                  </li>
                </ul>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Programme Qualiopi Section */}
        <QualiopiInfo />

        {/* Testimonials Section */}
        <section className="py-20 bg-gray-900 text-white" data-testid="testimonials-section">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <motion.h2 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-3xl lg:text-4xl font-bold mb-4"
              >
                Témoignages de Nos Diplômés
              </motion.h2>
              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="text-xl text-gray-300"
              >
                Ils ont transformé leur carrière grâce à notre formation
              </motion.p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Card className="h-full bg-gray-800 border-gray-700 hover:shadow-2xl transition-all duration-300">
                    <CardContent className="p-6">
                      <div className="flex items-center mb-4">
                        {[...Array(testimonial.rating)].map((_, i) => (
                          <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                      <p className="text-gray-300 mb-6 italic leading-relaxed">
                        "{testimonial.content}"
                      </p>
                      <div className="flex items-center">
                        <img 
                          src={testimonial.avatar} 
                          alt={testimonial.name}
                          className="h-12 w-12 rounded-full object-cover mr-4"
                        />
                        <div>
                          <div className="font-semibold text-white">{testimonial.name}</div>
                          <div className="text-sm text-blue-400">{testimonial.role}</div>
                          <div className="text-xs text-gray-400">{testimonial.location}</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Training Environment Section */}
        <section className="py-20 bg-gradient-to-br from-blue-50 to-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                className="space-y-6"
              >
                <Badge className="bg-blue-100 text-blue-800">Formation Certifiante Qualiopi</Badge>
                <h3 className="text-3xl lg:text-4xl font-bold text-gray-900">
                  Un Environnement de Formation Optimal
                </h3>
                <p className="text-lg text-gray-600 leading-relaxed">
                  Bénéficiez d'une formation structurée, reconnue et optimisée pour votre réussite professionnelle.
                </p>
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <div className="text-3xl font-bold text-blue-600">{content.stat_graduates}</div>
                    <div className="text-gray-600">Élèves diplômés</div>
                  </div>
                  <div className="space-y-2">
                    <div className="text-3xl font-bold text-blue-600">{content.stat_success_rate}</div>
                    <div className="text-gray-600">Taux de réussite</div>
                  </div>
                </div>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <img 
                  src={content.training_image_url}
                  alt="Environnement de formation professionnel"
                  className="rounded-2xl shadow-2xl w-full h-auto object-cover"
                />
              </motion.div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-700" data-testid="cta-section">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-3xl lg:text-4xl font-bold mb-6">
                Prêt à Changer de Vie Professionnelle ?
              </h2>
              <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
                Rejoignez plus de 1200 inspecteurs automobiles certifiés qui ont transformé 
                leur passion pour l'automobile en revenus réguliers.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
                <Link to="/register" data-testid="cta-register-button">
                  <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 text-lg font-semibold">
                    <Car className="mr-2 h-5 w-5" />
                    Devenir Inspecteur Auto
                  </Button>
                </Link>
                <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10 px-8 py-4 text-lg">
                  <MessageCircle className="mr-2 h-5 w-5" />
                  Parler à un Conseiller
                </Button>
              </div>

              <p className="text-blue-200 text-sm">
                ✅ Formation certifiante • ✅ Support inclus • ✅ Garantie 30 jours
              </p>
            </motion.div>
          </div>
        </section>
      </div>
    </>
  );
}

export default Home;