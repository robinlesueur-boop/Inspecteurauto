import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Clock, 
  Euro, 
  FileCheck, 
  Target, 
  Calendar,
  Phone,
  BookOpen,
  CheckCircle,
  Users,
  Accessibility
} from 'lucide-react';

export default function QualiopiInfo() {
  const pedagogicalObjectives = [
    "Comprendre le rôle et les missions de l'inspecteur automobile",
    "Acquérir les méthodes d'inspection complètes (techniques, visuelles, administratives)",
    "Maîtriser les outils et diagnostics pour évaluer un véhicule",
    "Savoir établir un rapport clair et objectif à destination du client",
    "Appliquer les règles légales et éthiques de la profession"
  ];

  const programDetails = [
    { module: "Module 1", title: "Introduction à l'Inspection Automobile", duration: "60 min", type: "Gratuit" },
    { module: "Module 2", title: "Fondamentaux Techniques Automobiles", duration: "70 min", type: "Payant" },
    { module: "Module 3", title: "Diagnostic Moteur et Transmission", duration: "75 min", type: "Payant" },
    { module: "Module 4", title: "Inspection Carrosserie et Châssis", duration: "65 min", type: "Payant" },
    { module: "Module 5", title: "Systèmes Électroniques et ADAS", duration: "70 min", type: "Payant" },
    { module: "Module 6", title: "Sécurité et Équipements", duration: "60 min", type: "Payant" },
    { module: "Module 7", title: "Méthodologie AutoJust", duration: "70 min", type: "Payant" },
    { module: "Module 8", title: "Pratique Professionnelle et Certification", duration: "70 min", type: "Payant" }
  ];

  return (
    <div className="py-16 bg-gradient-to-b from-white to-gray-50">
      <div className="container mx-auto px-4">
        
        {/* En-tête avec Badge Qualiopi */}
        <div className="text-center mb-12">
          <Badge className="mb-4 px-4 py-2 text-lg" variant="secondary">
            <CheckCircle className="h-5 w-5 mr-2 inline" />
            Formation Conforme Qualiopi
          </Badge>
          <h2 className="text-4xl font-bold mb-4">Programme Complet de Formation</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Formation professionnelle d'inspecteur automobile certifiante
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          
          {/* Informations Générales */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileCheck className="h-6 w-6 text-blue-600" />
                Informations Générales
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start gap-3">
                <Clock className="h-5 w-5 text-blue-600 mt-1" />
                <div>
                  <p className="font-semibold">Durée</p>
                  <p className="text-gray-600">9 heures de formation (540 minutes)</p>
                  <p className="text-sm text-gray-500">Réparties en 8 modules progressifs</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Euro className="h-5 w-5 text-green-600 mt-1" />
                <div>
                  <p className="font-semibold">Tarif</p>
                  <p className="text-gray-600">297€ TTC</p>
                  <p className="text-sm text-green-600 font-medium">Payable en 4 fois sans frais</p>
                  <p className="text-xs text-gray-500">Soit 4 x 74,25€</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Calendar className="h-5 w-5 text-purple-600 mt-1" />
                <div>
                  <p className="font-semibold">Délai et Modalités d'Accès</p>
                  <p className="text-gray-600">Accès immédiat après paiement</p>
                  <p className="text-sm text-gray-500">Formation 100% en ligne, accessible 24/7 pendant 12 mois</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <BookOpen className="h-5 w-5 text-orange-600 mt-1" />
                <div>
                  <p className="font-semibold">Méthodes Mobilisées</p>
                  <p className="text-gray-600">• Cours théoriques interactifs</p>
                  <p className="text-gray-600">• Études de cas pratiques</p>
                  <p className="text-gray-600">• Quiz d'évaluation (12 questions/module)</p>
                  <p className="text-gray-600">• Forum communautaire</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Prérequis et Évaluation */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-6 w-6 text-blue-600" />
                Prérequis et Évaluation
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-blue-600 mt-1" />
                <div>
                  <p className="font-semibold">Prérequis</p>
                  <p className="text-gray-600">• Permis B en cours de validité <span className="text-red-600 font-semibold">(obligatoire)</span></p>
                  <p className="text-gray-600">• Passion pour l'automobile</p>
                  <p className="text-gray-600">• Motivation professionnelle</p>
                  <p className="text-sm text-gray-500 mt-2">Un questionnaire pré-inscription validera votre profil</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <FileCheck className="h-5 w-5 text-green-600 mt-1" />
                <div>
                  <p className="font-semibold">Modalités d'Évaluation</p>
                  <p className="text-gray-600">• Quiz de validation par module (80% requis)</p>
                  <p className="text-gray-600">• Évaluation des compétences mécaniques</p>
                  <p className="text-gray-600">• Examen final de certification</p>
                  <p className="text-gray-600">• Questionnaire de satisfaction</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Accessibility className="h-5 w-5 text-purple-600 mt-1" />
                <div>
                  <p className="font-semibold">Accessibilité Handicap</p>
                  <p className="text-gray-600">Formation accessible aux personnes en situation de handicap.</p>
                  <p className="text-sm text-gray-500">Contactez-nous pour adapter la formation à vos besoins spécifiques.</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Phone className="h-5 w-5 text-blue-600 mt-1" />
                <div>
                  <p className="font-semibold">Contact</p>
                  <p className="text-gray-600">Email : contact@inspecteur-auto.fr</p>
                  <p className="text-gray-600">Support technique disponible 7j/7</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Objectifs Pédagogiques */}
        <Card className="mb-12">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-2xl">
              <Target className="h-7 w-7 text-blue-600" />
              Objectifs Pédagogiques
            </CardTitle>
            <CardDescription>
              À l'issue de cette formation, vous serez capable de :
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              {pedagogicalObjectives.map((objective, index) => (
                <div key={index} className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                  <p className="text-gray-800">{objective}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Détail du Programme */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-2xl">
              <BookOpen className="h-7 w-7 text-blue-600" />
              Détail du Programme - 9 heures
            </CardTitle>
            <CardDescription>
              8 modules progressifs avec quiz de validation
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {programDetails.map((item, index) => (
                <div 
                  key={index} 
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">{item.title}</p>
                      <p className="text-sm text-gray-600">{item.module}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Clock className="h-4 w-4" />
                      <span className="font-medium">{item.duration}</span>
                    </div>
                    <Badge variant={item.type === "Gratuit" ? "success" : "default"}>
                      {item.type}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 bg-green-50 border-l-4 border-green-600 rounded">
              <p className="font-semibold text-green-900 mb-2">
                Durée Totale : 9 heures (540 minutes)
              </p>
              <p className="text-sm text-green-800">
                Formation progressive avec validation à chaque étape. Module 1 gratuit pour découvrir la méthode.
              </p>
            </div>
          </CardContent>
        </Card>

      </div>
    </div>
  );
}
