import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../App';

const LandingPage = () => {
  const { isAuthenticated } = useAuth();
  const [showAuthForm, setShowAuthForm] = useState(false);

  const features = [
    {
      icon: "🎯",
      title: "Méthodologie méthode d'inspection",
      description: "Plus de 200 points de contrôle standardisés pour une inspection complète et professionnelle"
    },
    {
      icon: "📚",
      title: "Formation Complète 9h",
      description: "5 modules progressifs avec quiz intégrés et certification Qualiopi"
    },
    {
      icon: "🔧",
      title: "Outils Digitaux",
      description: "WebApp méthode d'inspection et WeProov pour une inspection terrain optimisée"
    },
    {
      icon: "📄",
      title: "Rapport Professionnel",
      description: "Modèles de rapport avec avis moteur spécialisé selon kilométrage"
    },
    {
      icon: "💼",
      title: "Accompagnement Business",
      description: "Création SIRET, tarification, relation client B2B/B2C"
    },
    {
      icon: "🏆",
      title: "Certification Officielle",
      description: "Attestation InspecteurAutomobile.fr reconnue par les professionnels"
    }
  ];

  const testimonials = [
    {
      name: "Marc Dubois",
      role: "Ex-mécanicien, maintenant inspecteur freelance",
      comment: "Grâce à cette formation, j'ai pu me reconvertir et créer mon activité d'inspection. Les 200 points de contrôle sont un vrai plus !",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=60&h=60&fit=crop&crop=face"
    },
    {
      name: "Sophie Martin", 
      role: "Inspectrice certifiée",
      comment: "Formation très complète, j'ai particulièrement apprécié les modules sur la rédaction de rapport et l'avis moteur spécialisé.",
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b4c0?w=60&h=60&fit=crop&crop=face"
    },
    {
      name: "Jean-Pierre Laurent",
      role: "Partenaire assurance",
      comment: "Nous travaillons exclusivement avec des inspecteurs formés par ce programme. La qualité des rapports est remarquable.",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop&crop=face"
    }
  ];

  const faqData = [
    {
      question: "La formation est-elle éligible CPF ?",
      answer: "Oui, notre formation respecte les standards Qualiopi et est éligible au financement CPF (Compte Personnel de Formation)."
    },
    {
      question: "Quel matériel est nécessaire ?",
      answer: "Un smartphone avec l'app méthode d'inspection, un multimètre basique et une lampe de poche suffisent. Liste complète fournie lors de l'inscription."
    },
    {
      question: "Combien peut-on gagner comme inspecteur ?",
      answer: "Entre 150-250€ par inspection particulier, 200-350€ pour les professionnels. Potentiel 2000-4000€/mois selon activité."
    },
    {
      question: "La certification est-elle reconnue ?",
      answer: "Oui, par plus de 50 partenaires B2B (assureurs, leasing, enchères) et validée par notre réseau de 300+ inspecteurs."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      
      {/* Navigation */}
      <nav className="fixed w-full top-0 z-50 glass-effect">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">🚗</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                InspecteurAutomobile.fr
              </span>
            </div>
            
            <div className="flex items-center space-x-4">
              {!isAuthenticated ? (
                <>
                  <Link to="/login" className="btn-secondary">
                    Se connecter
                  </Link>
                  <Link to="/register" className="btn-primary">
                    S'inscrire
                  </Link>
                </>
              ) : (
                <Link to="/dashboard" className="btn-primary">
                  Accéder à ma formation
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="fade-in">
              <h1 className="text-5xl lg:text-7xl font-bold mb-6">
                <span className="bg-gradient-to-r from-blue-400 via-blue-500 to-orange-500 bg-clip-text text-transparent">
                  Devenez
                </span>
                <br />
                <span className="text-white font-family: 'Space Grotesk'">
                  Inspecteur Automobile
                </span>
              </h1>
              
              <p className="text-xl text-slate-300 mb-8 leading-relaxed">
                Formation professionnelle <strong>9h certifiante</strong> pour maîtriser l'inspection automobile. 
                Méthodologie méthode d'inspection avec <strong>200+ points de contrôle</strong>. 
                Compatible Qualiopi/CPF.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <button 
                  onClick={() => !isAuthenticated && setShowAuthForm(true)}
                  className="btn-primary text-lg px-8 py-4"
                  data-testid="hero-cta-button"
                >
                  {isAuthenticated ? (
                    <Link to="/dashboard">Accéder à ma formation</Link>
                  ) : (
                    "Je m'inscris - 299€"
                  )}
                  <span>→</span>
                </button>
                <div className="flex items-center space-x-4 text-slate-300">
                  <span className="flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    Certification officielle
                  </span>
                  <span className="flex items-center">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                    Éligible CPF
                  </span>
                </div>
              </div>

              <div className="flex items-center space-x-8 text-sm text-slate-400">
                <div>
                  <div className="text-2xl font-bold text-white">300+</div>
                  <div>Inspecteurs formés</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">50+</div>
                  <div>Partenaires B2B</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">98%</div>
                  <div>Taux de réussite</div>
                </div>
              </div>
            </div>

            <div className="relative slide-up">
              <div className="relative z-10">
                <img 
                  src="https://images.unsplash.com/photo-1487754180451-c456f719a1fc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85"
                  alt="Inspection automobile professionnelle"
                  className="rounded-2xl shadow-2xl w-full"
                />
              </div>
              <div className="absolute -top-4 -right-4 w-full h-full bg-gradient-to-r from-blue-500/20 to-orange-500/20 rounded-2xl -z-10"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-slate-800/50 to-slate-700/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Programme de Formation Complet
            </h2>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              5 modules progressifs pour maîtriser tous les aspects de l'inspection automobile professionnelle
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="card hover:scale-105 transition-transform duration-300">
                <div className="text-3xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                <p className="text-slate-300 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Program Details */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-white mb-8">
                Méthodologie méthode d'inspection
                <br />
                <span className="text-blue-400">200+ Points de Contrôle</span>
              </h2>
              
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-white text-sm font-bold">1</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">Diagnostic et Positionnement</h4>
                    <p className="text-slate-300">Évaluation initiale et introduction au métier (90 min)</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-white text-sm font-bold">2</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">Remise à Niveau Mécanique</h4>
                    <p className="text-slate-300">Moteur, transmission, électronique (120 min)</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-white text-sm font-bold">3</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">Méthodologie Terrain</h4>
                    <p className="text-slate-300">Processus d'inspection complet avec outils digitaux (150 min)</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-white text-sm font-bold">4</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">Rédaction Rapport</h4>
                    <p className="text-slate-300">Structuration et avis moteur spécialisé (90 min)</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-white text-sm font-bold">5</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">Aspects Légaux & Business</h4>
                    <p className="text-slate-300">Relation client, statut juridique, tarification (90 min)</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="relative">
              <img 
                src="https://images.unsplash.com/photo-1498887960847-2a5e46312788?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85"
                alt="Tableau de bord automobile"
                className="rounded-2xl shadow-2xl"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-blue-600/20 via-transparent to-transparent rounded-2xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-slate-800/30 to-slate-700/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-8">
            Tarification Transparente
          </h2>
          
          <div className="card max-w-lg mx-auto">
            <div className="text-center">
              <div className="text-5xl font-bold text-white mb-2">299€</div>
              <div className="text-slate-300 mb-6">ou 4 × 74,99€ sans frais</div>
              
              <div className="space-y-4 text-left mb-8">
                <div className="flex items-center">
                  <span className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white text-xs">✓</span>
                  </span>
                  <span className="text-slate-300">9h de formation complète</span>
                </div>
                <div className="flex items-center">
                  <span className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white text-xs">✓</span>
                  </span>
                  <span className="text-slate-300">Certification officielle</span>
                </div>
                <div className="flex items-center">
                  <span className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white text-xs">✓</span>
                  </span>
                  <span className="text-slate-300">Accès illimité 24/7</span>
                </div>
                <div className="flex items-center">
                  <span className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white text-xs">✓</span>
                  </span>
                  <span className="text-slate-300">Ressources téléchargeables</span>
                </div>
                <div className="flex items-center">
                  <span className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white text-xs">✓</span>
                  </span>
                  <span className="text-slate-300">Support personnalisé</span>
                </div>
              </div>

              <button 
                onClick={() => !isAuthenticated && setShowAuthForm(true)}
                className="btn-primary w-full text-lg py-4"
                data-testid="pricing-cta-button"
              >
                {isAuthenticated ? (
                  <Link to="/dashboard">Accéder à ma formation</Link>
                ) : (
                  "Réserver ma place"
                )}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Témoignages d'Inspecteurs Certifiés
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="card">
                <div className="flex items-center mb-4">
                  <img 
                    src={testimonial.avatar}
                    alt={testimonial.name}
                    className="w-12 h-12 rounded-full mr-4"
                  />
                  <div>
                    <h4 className="font-semibold text-white">{testimonial.name}</h4>
                    <p className="text-sm text-slate-400">{testimonial.role}</p>
                  </div>
                </div>
                <p className="text-slate-300 italic">"{testimonial.comment}"</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-slate-800/30 to-slate-700/30">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Questions Fréquentes
            </h2>
          </div>

          <div className="space-y-6">
            {faqData.map((faq, index) => (
              <div key={index} className="card">
                <h4 className="text-lg font-semibold text-white mb-3">{faq.question}</h4>
                <p className="text-slate-300 leading-relaxed">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 px-6 bg-gradient-to-r from-blue-600/20 to-orange-600/20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Prêt à Devenir Inspecteur Automobile ?
          </h2>
          <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            Rejoignez notre communauté de 300+ inspecteurs certifiés et lancez votre activité dès aujourd'hui.
          </p>
          
          <button 
            onClick={() => !isAuthenticated && setShowAuthForm(true)}
            className="btn-primary text-xl px-12 py-4"
            data-testid="final-cta-button"
          >
            {isAuthenticated ? (
              <Link to="/dashboard">Commencer maintenant</Link>
            ) : (
              "Commencer maintenant - 299€"
            )}
            <span>🚀</span>
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 bg-slate-900 border-t border-slate-800">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">🚗</span>
                </div>
                <span className="text-lg font-bold text-white">InspecteurAutomobile.fr</span>
              </div>
              <p className="text-slate-400">Formation professionnelle certifiante pour inspecteurs automobile.</p>
            </div>

            <div>
              <h5 className="font-semibold text-white mb-4">Formation</h5>
              <ul className="space-y-2 text-slate-400">
                <li>Programme 9h</li>
                <li>Certification Qualiopi</li>
                <li>Éligibilité CPF</li>
                <li>Support 7j/7</li>
              </ul>
            </div>

            <div>
              <h5 className="font-semibold text-white mb-4">Légal</h5>
              <ul className="space-y-2 text-slate-400">
                <li>Mentions légales</li>
                <li>CGV</li>
                <li>Politique de confidentialité</li>
                <li>Cookies</li>
              </ul>
            </div>

            <div>
              <h5 className="font-semibold text-white mb-4">Contact</h5>
              <ul className="space-y-2 text-slate-400">
                <li>support@inspecteurautomobile.fr</li>
                <li>+33 1 XX XX XX XX</li>
                <li>Du lundi au vendredi</li>
                <li>9h - 18h</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-800 mt-12 pt-8 text-center text-slate-400">
            <p>&copy; 2024 InspecteurAutomobile.fr - Tous droits réservés</p>
          </div>
        </div>
      </footer>

      {/* Auth Form Modal */}
      {showAuthForm && !isAuthenticated && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-800 rounded-2xl p-8 max-w-md w-full">
            <h3 className="text-2xl font-bold text-white mb-6 text-center">
              Inscription Formation
            </h3>
            <div className="space-y-4">
              <Link 
                to="/register"
                className="btn-primary w-full justify-center"
                onClick={() => setShowAuthForm(false)}
              >
                Créer mon compte
              </Link>
              <Link 
                to="/login"
                className="btn-secondary w-full justify-center"
                onClick={() => setShowAuthForm(false)}
              >
                J'ai déjà un compte
              </Link>
            </div>
            <button 
              onClick={() => setShowAuthForm(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white"
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default LandingPage;