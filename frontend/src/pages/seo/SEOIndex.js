import React from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { BookOpen, Car, MapPin, Search, TrendingUp, Award } from 'lucide-react';

/**
 * Page Index SEO - Liste toutes les pages SEO disponibles
 * Route: /seo ou /ressources
 */
function SEOIndex() {
  const categories = [
    {
      title: 'Formation & Carrière',
      icon: <BookOpen className="h-6 w-6" />,
      description: 'Guides complets pour devenir inspecteur automobile',
      color: 'bg-blue-500',
      pages: [
        { id: 'formation-inspecteur-automobile', title: 'Formation Inspecteur Automobile Complète' },
        { id: 'comment-devenir-inspecteur-automobile', title: 'Comment Devenir Inspecteur Automobile' },
        { id: 'tarifs-formation-inspecteur-auto', title: 'Tarifs de la Formation' },
        { id: 'formation-en-ligne-inspecteur-automobile', title: 'Formation 100% en Ligne' },
        { id: 'certification-inspecteur-automobile', title: 'Certification Professionnelle' },
      ]
    },
    {
      title: 'Métier & Revenus',
      icon: <TrendingUp className="h-6 w-6" />,
      description: 'Tout savoir sur le métier et les perspectives',
      color: 'bg-green-500',
      pages: [
        { id: 'metier-inspecteur-automobile', title: 'Le Métier d\'Inspecteur Automobile' },
        { id: 'combien-gagne-inspecteur-automobile', title: 'Combien Gagne un Inspecteur Auto' },
      ]
    },
    {
      title: 'Diagnostic Technique',
      icon: <Search className="h-6 w-6" />,
      description: 'Techniques de diagnostic automobile',
      color: 'bg-purple-500',
      pages: [
        { id: 'diagnostic-moteur-essence', title: 'Diagnostic Moteur Essence' },
        { id: 'diagnostic-moteur-diesel', title: 'Diagnostic Moteur Diesel' },
        { id: 'diagnostic-boite-vitesses-automatique', title: 'Diagnostic Boîte Automatique' },
        { id: 'diagnostic-systeme-freinage-abs-esp', title: 'Diagnostic Freinage ABS/ESP' },
        { id: 'diagnostic-electronique-automobile-obd2', title: 'Diagnostic OBD2' },
        { id: 'diagnostic-climatisation-automobile', title: 'Diagnostic Climatisation' },
        { id: 'diagnostic-suspension-amortisseurs', title: 'Diagnostic Suspension' },
        { id: 'diagnostic-embrayage-signes-usure', title: 'Diagnostic Embrayage' },
        { id: 'diagnostic-turbo-pannes-courantes', title: 'Diagnostic Turbo' },
        { id: 'diagnostic-systeme-antipollution-fap-scr', title: 'Diagnostic FAP/SCR/EGR' },
      ]
    },
    {
      title: 'Inspection Carrosserie',
      icon: <Car className="h-6 w-6" />,
      description: 'Contrôle extérieur et détection de fraudes',
      color: 'bg-orange-500',
      pages: [
        { id: 'inspection-carrosserie-pre-achat', title: 'Inspection Carrosserie Pré-Achat' },
        { id: 'detection-vehicule-accidente', title: 'Détecter un Véhicule Accidenté' },
        { id: 'detection-compteur-kilometrique-trafique', title: 'Compteur Kilométrique Trafiqué' },
        { id: 'reperer-voiture-maquillee', title: 'Repérer une Voiture Maquillée' },
        { id: 'inspection-chassis-points-controle', title: 'Inspection du Châssis' },
        { id: 'controle-peinture-anticorrosion', title: 'Contrôle Peinture' },
        { id: 'inspection-vitrage-automobile', title: 'Inspection Vitrage' },
        { id: 'verification-etancheite-vehicule', title: 'Vérification Étanchéité' },
        { id: 'controle-geometrie-parallelisme', title: 'Contrôle Géométrie' },
        { id: 'inspection-pneumatiques-securite', title: 'Inspection Pneumatiques' },
      ]
    },
    {
      title: 'Par Région',
      icon: <MapPin className="h-6 w-6" />,
      description: 'Formation accessible partout en France',
      color: 'bg-red-500',
      pages: [
        { id: 'formation-inspecteur-automobile-paris', title: 'Formation à Paris & IDF' },
        { id: 'formation-inspecteur-automobile-lyon', title: 'Formation à Lyon' },
        { id: 'formation-inspecteur-automobile-marseille', title: 'Formation à Marseille' },
      ]
    },
  ];

  return (
    <>
      <Helmet>
        <title>Ressources & Guides | Formation Inspecteur Automobile</title>
        <meta name="description" content="Découvrez tous nos guides et ressources pour devenir inspecteur automobile : formation, diagnostic technique, détection fraudes, revenus du métier." />
        <meta name="keywords" content="guide inspecteur automobile, ressources formation auto, diagnostic véhicule, inspection pré-achat" />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
          <div className="max-w-6xl mx-auto px-4 text-center">
            <Badge className="mb-4 bg-white/20 text-white border-white/30">
              Ressources
            </Badge>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Centre de Ressources
            </h1>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto">
              Guides complets, techniques d'inspection, et tout ce que vous devez savoir 
              pour devenir un inspecteur automobile professionnel.
            </p>
          </div>
        </section>

        {/* Categories */}
        <section className="py-16">
          <div className="max-w-6xl mx-auto px-4">
            <div className="space-y-12">
              {categories.map((category, idx) => (
                <div key={idx} className="space-y-4">
                  <div className="flex items-center gap-3 mb-6">
                    <div className={`${category.color} p-3 rounded-lg text-white`}>
                      {category.icon}
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900">
                        {category.title}
                      </h2>
                      <p className="text-gray-600">{category.description}</p>
                    </div>
                  </div>
                  
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {category.pages.map((page, pageIdx) => (
                      <Link 
                        key={pageIdx} 
                        to={`/seo/${page.id}`}
                        className="group"
                        data-testid={`seo-link-${page.id}`}
                      >
                        <Card className="h-full hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-transparent hover:border-l-blue-500">
                          <CardContent className="p-4">
                            <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                              {page.title}
                            </h3>
                            <span className="text-sm text-blue-600 mt-2 inline-block">
                              Lire l'article →
                            </span>
                          </CardContent>
                        </Card>
                      </Link>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gray-100">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <Award className="h-16 w-16 text-blue-600 mx-auto mb-6" />
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Prêt à Devenir Inspecteur Automobile ?
            </h2>
            <p className="text-gray-600 mb-8 text-lg">
              Notre formation complète vous guide de A à Z. Rejoignez les 500+ inspecteurs 
              formés par nos experts.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
                data-testid="cta-register"
              >
                S'inscrire à la Formation
              </Link>
              <Link
                to="/programme-detaille"
                className="inline-flex items-center justify-center px-6 py-3 bg-white text-blue-600 font-medium rounded-lg border border-blue-200 hover:bg-blue-50 transition"
                data-testid="cta-programme"
              >
                Voir le Programme
              </Link>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}

export default SEOIndex;
