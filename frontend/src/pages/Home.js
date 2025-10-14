import React from "react";
import { Link } from "react-router-dom";
import { Helmet } from 'react-helmet-async';
import { useAuth } from "../contexts/AuthContext";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { motion } from "framer-motion";
import QualiopiInfo from "../components/QualiopiInfo";
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

function Home() {
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: <Target className="h-8 w-8 text-blue-600" />,
      title: "Méthode AutoJust",
      description: "Système d'inspection révolutionnaire utilisé par plus de 500 professionnels en France."
    },
    {
      icon: <Award className="h-8 w-8 text-green-600" />,
      title: "Certification Reconnue",
      description: "Obtenez votre certification officielle d'inspecteur automobile valorisée par l'industrie."
    },
    {
      icon: <Users className="h-8 w-8 text-purple-600" />,
      title: "Communauté Active",
      description: "Rejoignez une communauté de 1000+ inspecteurs et échangez sur vos expériences."
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-orange-600" />,
      title: "Revenus Attractifs",
      description: "Générez 150 à 400€ par inspection avec un potentiel de 3000-8000€/mois."
    }
  ];

  const stats = [
    { number: "1,200+", label: "Diplômés", icon: <Users className="h-5 w-5" /> },
    { number: "97%", label: "Taux de Réussite", icon: <Trophy className="h-5 w-5" /> },
    { number: "11h", label: "de Formation", icon: <Clock className="h-5 w-5" /> },
    { number: "4.9/5", label: "Note Moyenne", icon: <Star className="h-5 w-5 fill-current" /> }
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
        <title>Formation Inspecteur Automobile - Devenez Expert en Diagnostic Véhiculaire</title>
        <meta name="description" content="Formation complète d'inspecteur automobile avec la méthode AutoJust. Certification reconnue, revenus jusqu'à 8000€/mois. 97% de taux de réussite." />
        <meta name="keywords" content="formation inspecteur automobile, diagnostic véhiculaire, méthode AutoJust, certification automobile, reconversion professionnelle" />
        <meta property="og:title" content="Formation Inspecteur Automobile - Devenez Expert en Diagnostic Véhiculaire" />
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
                  🚀 Formation #1 en France - 1200+ diplômés
                </Badge>
                
                <h1 className="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
                  Devenez 
                  <span className="text-blue-300"> Inspecteur</span>
                  <br />
                  Automobile Expert
                </h1>
                
                <p className="text-xl text-blue-100 mb-8 max-w-2xl leading-relaxed">
                  Maîtrisez l'art du diagnostic véhiculaire avec la méthode AutoJust. 
                  Formation complète en 11h pour générer jusqu'à <strong className="text-blue-300">8000€/mois</strong>.
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
                        Commencer la formation
                      </Button>
                    </Link>
                  )}
                  
                  <Button size="lg" variant="outline" className="border-blue-300 text-blue-100 hover:bg-blue-800/50 px-8 py-4 text-lg">
                    Module gratuit
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
                    src="https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=600&h=400&fit=crop" 
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

        {/* Curriculum Section */}
        <section className="py-20 bg-white" data-testid="curriculum-section">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <Badge className="mb-4 bg-blue-100 text-blue-700">
                  Programme Complet
                </Badge>
                <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">
                  11 Heures de Formation
                  <span className="text-blue-600"> Intensive</span>
                </h2>
                <p className="text-xl text-gray-600 mb-8">
                  Un programme structuré pour vous transformer en expert de l'inspection automobile, 
                  de la théorie à la pratique professionnelle.
                </p>

                <div className="space-y-4 mb-8">
                  {modules.map((module, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: index * 0.1 }}
                      className="flex items-start space-x-3"
                    >
                      <div className="bg-blue-100 p-1 rounded-full mt-1">
                        <CheckCircle className="h-4 w-4 text-blue-600" />
                      </div>
                      <span className="text-gray-700 font-medium">{module}</span>
                    </motion.div>
                  ))}
                </div>

                <div className="bg-blue-50 p-6 rounded-xl">
                  <div className="flex items-center space-x-3 mb-3">
                    <Award className="h-6 w-6 text-blue-600" />
                    <span className="font-semibold text-blue-900">Bonus Exclusif</span>
                  </div>
                  <p className="text-blue-800">
                    Accès à vie au forum privé des inspecteurs certifiés + 
                    mises à jour gratuites du programme
                  </p>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                className="relative"
              >
                <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl p-8 text-white shadow-2xl">
                  <div className="text-center mb-8">
                    <h3 className="text-2xl font-bold mb-2">Formation Complète</h3>
                    <p className="text-blue-100">Tout inclus pour réussir</p>
                  </div>

                  <div className="space-y-6">
                    <div className="flex justify-between items-center">
                      <span>Prix de lancement</span>
                      <span className="text-2xl font-bold">297€</span>
                    </div>
                    
                    <div className="border-t border-blue-400 pt-6 space-y-3">
                      <div className="flex items-center space-x-2 text-blue-100">
                        <CheckCircle className="h-4 w-4" />
                        <span>11h de formation vidéo</span>
                      </div>
                      <div className="flex items-center space-x-2 text-blue-100">
                        <CheckCircle className="h-4 w-4" />
                        <span>Méthode AutoJust exclusive</span>
                      </div>
                      <div className="flex items-center space-x-2 text-blue-100">
                        <CheckCircle className="h-4 w-4" />
                        <span>Certification reconnue</span>
                      </div>
                      <div className="flex items-center space-x-2 text-blue-100">
                        <CheckCircle className="h-4 w-4" />
                        <span>Forum privé à vie</span>
                      </div>
                      <div className="flex items-center space-x-2 text-blue-100">
                        <CheckCircle className="h-4 w-4" />
                        <span>Support prioritaire</span>
                      </div>
                    </div>

                    <Link to="/register" className="block">
                      <Button className="w-full bg-white text-blue-600 hover:bg-gray-100 py-3 text-lg font-semibold">
                        Commencer Maintenant
                        <ArrowRight className="ml-2 h-5 w-5" />
                      </Button>
                    </Link>

                    <p className="text-center text-blue-200 text-sm">
                      Garantie satisfait ou remboursé 30 jours
                    </p>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

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