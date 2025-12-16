import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Target, CheckCircle, Search, FileText, Camera, Shield, TrendingUp } from 'lucide-react';

function MethodeInspection() {
  return (
    <>
      <Helmet>
        <title>Notre Méthode d'Inspection - Inspection Automobile Professionnelle</title>
        <meta name="description" content="Découvrez notre méthode d'inspection automobile : systématique, rigoureuse et reconnue par les professionnels. Formation certifiée." />
      </Helmet>

      <div className="min-h-screen bg-gray-50">
        {/* Hero */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl font-bold mb-6">
              Notre Méthode d'Inspection Professionnelle
            </h1>
            <p className="text-2xl text-blue-100 max-w-3xl mx-auto">
              La référence en inspection automobile professionnelle depuis 2018
            </p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          
          {/* Introduction */}
          <Card className="mb-12">
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">
                    Qui sommes-nous ?
                  </h2>
                  <p className="text-gray-700 mb-4">
                    <strong>Notre méthode d'inspection</strong> est la référence en inspection automobile indépendante. 
                    Développée par des experts automobiles passionnés, notre méthodologie a révolutionné 
                    le marché de l'inspection pré-achat grâce à son approche rigoureuse et systématique.
                  </p>
                  <p className="text-gray-700 mb-4">
                    Avec plus de <strong>15 000 inspections</strong> réalisées et un réseau de 
                    <strong> 200+ inspecteurs certifiés</strong> à travers la France, notre méthode est devenue 
                    la référence incontournable pour les particuliers et professionnels de l'automobile d'occasion.
                  </p>
                  <div className="flex space-x-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-600">15 000+</div>
                      <div className="text-sm text-gray-600">Inspections</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-600">200+</div>
                      <div className="text-sm text-gray-600">Inspecteurs</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-600">98%</div>
                      <div className="text-sm text-gray-600">Satisfaction</div>
                    </div>
                  </div>
                </div>
                <div>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 className="font-semibold text-blue-900 mb-4 text-xl">Notre Mission</h3>
                    <p className="text-blue-800 mb-4">
                      Protéger les acheteurs de véhicules d'occasion en détectant les vices cachés 
                      et les anomalies avant l'achat, grâce à une inspection technique complète et impartiale.
                    </p>
                    <div className="flex items-center text-blue-700">
                      <Shield className="w-5 h-5 mr-2" />
                      <span className="font-medium">Indépendance & Transparence Garanties</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Les 5 Piliers */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
              Les 5 Piliers de Notre Méthode d'Inspection
            </h2>
            
            <div className="grid md:grid-cols-5 gap-4">
              <Card>
                <CardContent className="p-6 text-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Target className="w-6 h-6 text-blue-600" />
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2">Systématisation</h3>
                  <p className="text-sm text-gray-600">
                    Chaque inspection suit le même protocole en 6 phases
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6 text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Search className="w-6 h-6 text-green-600" />
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2">Technologie</h3>
                  <p className="text-sm text-gray-600">
                    Valises OBD, caméras, outils de mesure professionnels
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6 text-center">
                  <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Camera className="w-6 h-6 text-purple-600" />
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2">Traçabilité</h3>
                  <p className="text-sm text-gray-600">
                    Plus de 100 photos par inspection + rapport détaillé
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6 text-center">
                  <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <FileText className="w-6 h-6 text-yellow-600" />
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2">Transparence</h3>
                  <p className="text-sm text-gray-600">
                    Rapport remis en main propre avec explications
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6 text-center">
                  <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <TrendingUp className="w-6 h-6 text-red-600" />
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2">Expertise</h3>
                  <p className="text-sm text-gray-600">
                    Formateurs certifiés avec 10+ ans d'expérience
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Protocole en 6 Phases */}
          <Card className="mb-12">
            <CardHeader>
              <CardTitle className="text-2xl">Le Protocole d'Inspection Professionnel en 6 Phases</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                    1
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-2">Contrôle Documentaire</h3>
                    <p className="text-gray-600">
                      Vérification identité véhicule (VIN, plaque), carte grise, historique entretien, 
                      HistoVec, détection fraude kilométrage, rappels constructeur.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                    2
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-2">Inspection Visuelle Extérieure</h3>
                    <p className="text-gray-600">
                      Carrosserie, peinture (détection repeints), vitrages, optiques, pneumatiques, 
                      soubassement. Cotation A/B/C/D de chaque élément.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                    3
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-2">Inspection Compartiment Moteur</h3>
                    <p className="text-gray-600">
                      Fuites, état courroies, niveau liquides, batterie, câblages. Plus de 30 points de contrôle.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                    4
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-2">Inspection Habitacle</h3>
                    <p className="text-gray-600">
                      Usure, odeurs, fonctionnement équipements, traces infiltration, cohérence kilométrage.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                    5
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-2">Test Routier</h3>
                    <p className="text-gray-600">
                      Démarrage, bruits moteur, boîte de vitesses, direction, freinage, vibrations, ADAS.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                    6
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-2">Diagnostic Électronique OBD</h3>
                    <p className="text-gray-600">
                      Lecture codes défauts, live data, historique, tests actifs. Analyse de tous les calculateurs.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Différences avec CT */}
          <Card className="mb-12">
            <CardHeader>
              <CardTitle className="text-2xl">Inspection Professionnelle vs Contrôle Technique</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b-2 border-gray-300">
                      <th className="text-left p-3 font-semibold">Critère</th>
                      <th className="text-left p-3 font-semibold text-blue-600">Inspection Professionnelle</th>
                      <th className="text-left p-3 font-semibold text-gray-600">Contrôle Technique</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b">
                      <td className="p-3 font-medium">Durée</td>
                      <td className="p-3 text-blue-600">2 à 3 heures</td>
                      <td className="p-3 text-gray-600">30 minutes</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">Points contrôlés</td>
                      <td className="p-3 text-blue-600">300+ points</td>
                      <td className="p-3 text-gray-600">130 points</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">Diagnostic OBD</td>
                      <td className="p-3"><CheckCircle className="w-5 h-5 text-green-600" /></td>
                      <td className="p-3 text-gray-600">Non</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">Test routier</td>
                      <td className="p-3"><CheckCircle className="w-5 h-5 text-green-600" /></td>
                      <td className="p-3 text-gray-600">Non</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">Photos détaillées</td>
                      <td className="p-3"><CheckCircle className="w-5 h-5 text-green-600" /></td>
                      <td className="p-3 text-gray-600">Non</td>
                    </tr>
                    <tr className="border-b">
                      <td className="p-3 font-medium">Estimation réparations</td>
                      <td className="p-3"><CheckCircle className="w-5 h-5 text-green-600" /></td>
                      <td className="p-3 text-gray-600">Non</td>
                    </tr>
                    <tr>
                      <td className="p-3 font-medium">Indépendance</td>
                      <td className="p-3 text-blue-600 font-semibold">Totale</td>
                      <td className="p-3 text-gray-600">Réglementaire</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          {/* CTA */}
          <Card className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
            <CardContent className="p-12 text-center">
              <h2 className="text-3xl font-bold mb-4">
                Devenez Inspecteur Automobile Certifié
              </h2>
              <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
                Rejoignez notre réseau d'inspecteurs professionnels et maîtrisez la méthode 
                d'inspection automobile la plus reconnue en France.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/register">
                  <Button className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 text-lg">
                    S'inscrire à la Formation
                  </Button>
                </Link>
                <Link to="/contact">
                  <Button variant="outline" className="border-2 border-white text-white hover:bg-blue-700 px-8 py-3 text-lg">
                    Nous Contacter
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

export default MethodeInspection;
