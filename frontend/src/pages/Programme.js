import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { CheckCircle, Clock, BookOpen, Award } from 'lucide-react';

function Programme() {
  const modules = [
    {
      number: 1,
      title: "Introduction à l'Inspection Automobile",
      duration: "1h30",
      description: "Découvrez les fondamentaux de l'inspection automobile professionnelle",
      topics: [
        "Historique et évolution du métier d'inspecteur",
        "Cadre légal et réglementaire",
        "Méthodologie méthode d'inspection",
        "Outils et équipements essentiels",
        "Éthique professionnelle"
      ]
    },
    {
      number: 2,
      title: "Remise à Niveau Mécanique",
      duration: "1h",
      description: "Renforcez vos connaissances en mécanique automobile (selon évaluation)",
      topics: [
        "Principes de base de la mécanique",
        "Composants clés d'un véhicule",
        "Lecture de schémas techniques",
        "Vocabulaire technique professionnel",
        "Notions de sécurité"
      ]
    },
    {
      number: 3,
      title: "Moteur et Transmission",
      duration: "1h30",
      description: "Maîtrisez l'inspection du groupe motopropulseur",
      topics: [
        "Analyse du moteur (essence et diesel)",
        "Système d'injection et turbocompresseur",
        "Boîte de vitesses manuelle et automatique",
        "Embrayage et différentiel",
        "Diagnostic OBD et codes défauts"
      ]
    },
    {
      number: 4,
      title: "Systèmes Électriques et Électroniques",
      duration: "1h30",
      description: "Inspectez les systèmes électroniques modernes",
      topics: [
        "Circuit électrique et batterie",
        "Alternateur et démarreur",
        "Systèmes de gestion moteur (ECU)",
        "Réseaux multiplexés (CAN bus)",
        "Diagnostic électronique avancé"
      ]
    },
    {
      number: 5,
      title: "Freinage et Suspension",
      duration: "1h",
      description: "Évaluez la sécurité active du véhicule",
      topics: [
        "Système de freinage hydraulique",
        "ABS, ESP et aide au freinage",
        "Suspensions et amortisseurs",
        "Direction assistée",
        "Contrôle de l'usure et tests pratiques"
      ]
    },
    {
      number: 6,
      title: "ADAS (Systèmes d'Aide à la Conduite)",
      duration: "1h30",
      description: "Expertise des technologies d'assistance moderne",
      topics: [
        "Caméras et capteurs (radar, lidar)",
        "Régulateur adaptatif (ACC)",
        "Aide au stationnement",
        "Détection d'angle mort",
        "Calibration et maintenance"
      ]
    },
    {
      number: 7,
      title: "Aspects Réglementaires et Légaux",
      duration: "1h",
      description: "Connaissez le cadre juridique et administratif",
      topics: [
        "Législation française et européenne",
        "Contrôle technique et contre-visite",
        "Responsabilité professionnelle",
        "Rédaction de rapports d'inspection",
        "Expertise contradictoire"
      ]
    },
    {
      number: 8,
      title: "Carrosserie et Châssis",
      duration: "2h",
      description: "Inspection complète de la structure et de la carrosserie",
      topics: [
        "Détection des chocs et réparations",
        "Mesure de l'épaisseur de peinture",
        "Corrosion et points sensibles",
        "Contrôle du châssis et soubassement",
        "Vitrage et étanchéité"
      ]
    }
  ];

  return (
    <>
      <Helmet>
        <title>Programme Détaillé Formation Inspecteur Auto – 8 Modules | InspecteurAuto</title>
        <meta name="description" content="Programme complet de la formation inspecteur automobile : 8 modules, 11h de cours. Moteur, ADAS, carrosserie, diagnostic OBD. Certification professionnelle." />
        <meta name="keywords" content="programme formation inspecteur auto, modules formation automobile, diagnostic OBD, ADAS, expertise carrosserie" />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Programme Détaillé de la Formation
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              8 modules professionnels pour maîtriser l'inspection automobile de A à Z
            </p>
            <div className="flex justify-center items-center space-x-8 mt-8">
              <div className="flex items-center">
                <Clock className="h-6 w-6 text-blue-600 mr-2" />
                <span className="text-lg font-semibold">11 heures</span>
              </div>
              <div className="flex items-center">
                <BookOpen className="h-6 w-6 text-blue-600 mr-2" />
                <span className="text-lg font-semibold">8 modules</span>
              </div>
              <div className="flex items-center">
                <Award className="h-6 w-6 text-blue-600 mr-2" />
                <span className="text-lg font-semibold">Certification</span>
              </div>
            </div>
          </div>

          {/* Modules */}
          <div className="space-y-6 mb-12">
            {modules.map((module) => (
              <Card key={module.number} className="hover:shadow-lg transition-shadow">
                <CardHeader className="bg-gradient-to-r from-blue-50 to-white">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4">
                      <div className="flex items-center justify-center w-12 h-12 rounded-full bg-blue-600 text-white text-xl font-bold flex-shrink-0">
                        {module.number}
                      </div>
                      <div>
                        <CardTitle className="text-2xl mb-2">{module.title}</CardTitle>
                        <p className="text-gray-600">{module.description}</p>
                      </div>
                    </div>
                    <div className="flex items-center text-blue-600 font-semibold ml-4">
                      <Clock className="h-4 w-4 mr-1" />
                      {module.duration}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Ce que vous apprendrez :</h4>
                  <ul className="grid md:grid-cols-2 gap-3">
                    {module.topics.map((topic, idx) => (
                      <li key={idx} className="flex items-start">
                        <CheckCircle className="h-5 w-5 text-green-600 mr-2 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700">{topic}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* CTA */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-center text-white">
            <h2 className="text-3xl font-bold mb-4">Prêt à Démarrer Votre Formation ?</h2>
            <p className="text-xl mb-6 opacity-90">
              Accédez immédiatement aux 8 modules et commencez votre parcours vers la certification
            </p>
            <Link to="/register">
              <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-4">
                S'inscrire Maintenant - 297€
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}

export default Programme;