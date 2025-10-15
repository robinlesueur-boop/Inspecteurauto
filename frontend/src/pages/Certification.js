import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Award, CheckCircle, FileText, Shield } from 'lucide-react';

function Certification() {
  return (
    <>
      <Helmet>
        <title>Certification Qualiopi - Formation Inspecteur Automobile</title>
        <meta name="description" content="Notre formation d'inspecteur automobile est certifiée Qualiopi, garantissant la qualité de nos programmes. Éligible au financement CPF." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Hero Section */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center">
                <Award className="w-12 h-12 text-blue-600" />
              </div>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Certification Qualiopi
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Notre formation d'inspecteur automobile répond aux critères de qualité Qualiopi, 
              gage d'excellence reconnu par l'État français.
            </p>
          </div>

          {/* Qualiopi Info */}
          <Card className="mb-8 border-blue-200">
            <CardHeader className="bg-blue-50">
              <CardTitle className="flex items-center text-2xl">
                <Shield className="w-6 h-6 mr-3 text-blue-600" />
                Qu'est-ce que Qualiopi ?
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <p className="text-gray-700 mb-4">
                <strong>Qualiopi</strong> est la certification nationale des organismes de formation en France. 
                Mise en place en 2021, elle garantit la qualité des processus mis en œuvre par les prestataires 
                d'actions de formation.
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                <p className="text-blue-900 font-semibold mb-2">Notre Numéro de Certification :</p>
                <p className="text-blue-700 text-lg font-mono">En cours d'obtention - Processus 2025</p>
              </div>
              <p className="text-gray-700">
                La certification Qualiopi est <strong>obligatoire</strong> pour bénéficier de financements publics 
                ou mutualisés (CPF, Pôle Emploi, OPCO, etc.).
              </p>
            </CardContent>
          </Card>

          {/* Les 7 critères Qualiopi */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="text-2xl">Les 7 Critères de Qualité Qualiopi</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        1. Conditions d'information du public
                      </h3>
                      <p className="text-sm text-gray-600">
                        Information claire et accessible sur nos offres de formation, modalités et objectifs pédagogiques.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        2. Identification précise des objectifs
                      </h3>
                      <p className="text-sm text-gray-600">
                        Objectifs professionnels clairement définis et adaptés au marché de l'emploi.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        3. Adaptation des prestations
                      </h3>
                      <p className="text-sm text-gray-600">
                        Questionnaire de pré-inscription et évaluation des connaissances mécaniques pour personnaliser le parcours.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        4. Adéquation des moyens pédagogiques
                      </h3>
                      <p className="text-sm text-gray-600">
                        8 modules structurés, quiz d'évaluation, plateforme e-learning moderne, assistant IA.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        5. Qualifications des formateurs
                      </h3>
                      <p className="text-sm text-gray-600">
                        Équipe d'experts automobiles certifiés avec expérience terrain dans l'inspection.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        6. Insertion professionnelle
                      </h3>
                      <p className="text-sm text-gray-600">
                        Accompagnement à l'installation professionnelle, guide business et tarification.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        7. Recueil des appréciations
                      </h3>
                      <p className="text-sm text-gray-600">
                        Enquête de satisfaction obligatoire en fin de formation pour amélioration continue.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Financement */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="text-2xl">Financement de la Formation</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center p-4 border border-gray-200 rounded-lg">
                  <div className="text-3xl mb-2">💳</div>
                  <h3 className="font-semibold mb-2">CPF</h3>
                  <p className="text-sm text-gray-600">
                    Compte Personnel de Formation (En cours d'enregistrement)
                  </p>
                </div>

                <div className="text-center p-4 border border-gray-200 rounded-lg">
                  <div className="text-3xl mb-2">🏢</div>
                  <h3 className="font-semibold mb-2">OPCO</h3>
                  <p className="text-sm text-gray-600">
                    Opérateurs de Compétences pour financement entreprises
                  </p>
                </div>

                <div className="text-center p-4 border border-gray-200 rounded-lg">
                  <div className="text-3xl mb-2">💼</div>
                  <h3 className="font-semibold mb-2">Pôle Emploi</h3>
                  <p className="text-sm text-gray-600">
                    Aide Individuelle à la Formation (AIF)
                  </p>
                </div>
              </div>

              <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-800 text-sm">
                  <strong>Note :</strong> Notre certification Qualiopi est en cours d'obtention (processus 2025). 
                  En attendant, le paiement direct reste la seule option disponible. Nous vous informerons 
                  dès que les financements publics seront accessibles.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Certification Délivrée */}
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl flex items-center">
                <FileText className="w-6 h-6 mr-3 text-blue-600" />
                Votre Certification d'Inspecteur Automobile
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <p className="text-gray-700 mb-4">
                À l'issue de la formation, après validation de l'évaluation finale (score minimum 80%), 
                vous recevez :
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                  <span><strong>Certificat de Formation Professionnelle</strong> - Attestation officielle de compétences</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                  <span><strong>Badge numérique</strong> - Partageable sur LinkedIn et CV</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                  <span><strong>Accès à vie</strong> - Au contenu de formation et mises à jour</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                  <span><strong>Communauté professionnelle</strong> - Réseau d'inspecteurs certifiés</span>
                </li>
              </ul>

              <div className="text-center">
                <Link to="/register">
                  <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3">
                    S'inscrire à la Formation
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

        </div>
      </div>
    </>
  );
}

export default Certification;
