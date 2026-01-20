import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Checkbox } from './ui/checkbox';
import { Textarea } from './ui/textarea';
import { Alert, AlertDescription } from './ui/alert';
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function PreRegistrationForm({ onComplete }) {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    phone: '',
    answers: {},
    has_driving_license: false,
    professional_project: '',
    has_disability: '',
    has_smartphone: ''
  });

  const questions = [
    {
      id: 'q1',
      question: "Avez-vous une expérience professionnelle dans l'automobile ?",
      options: [
        { value: 'oui_pro', label: 'Oui, je travaille/ai travaillé dans l\'automobile' },
        { value: 'oui_hobby', label: 'Non professionnellement, mais je suis passionné' },
        { value: 'non', label: 'Non, mais je souhaite me reconvertir' }
      ]
    },
    {
      id: 'q2',
      question: "Avez-vous des connaissances en mécanique automobile ?",
      options: [
        { value: 'expert', label: 'Oui, niveau expert (mécanicien, technicien)' },
        { value: 'intermediaire', label: 'Oui, niveau intermédiaire (entretien courant)' },
        { value: 'debutant', label: 'Niveau débutant' },
        { value: 'aucune', label: 'Aucune connaissance' }
      ]
    },
    {
      id: 'q3',
      question: "Quel est votre projet professionnel après cette formation ?",
      options: [
        { value: 'independant', label: 'Devenir inspecteur indépendant' },
        { value: 'salarie', label: 'Travailler en concession/garage' },
        { value: 'complement', label: 'Activité complémentaire à temps partiel' },
        { value: 'reconversion', label: 'Reconversion professionnelle complète' }
      ]
    },
    {
      id: 'q4',
      question: "Dans quel délai souhaitez-vous démarrer votre activité ?",
      options: [
        { value: 'immediat', label: 'Immédiatement après la formation' },
        { value: '3mois', label: 'Dans les 3 mois' },
        { value: '6mois', label: 'Dans les 6 mois' },
        { value: 'plus', label: 'Plus de 6 mois / En réflexion' }
      ]
    },
    {
      id: 'q5',
      question: "Avez-vous déjà acheté ou vendu des véhicules d'occasion ?",
      options: [
        { value: 'souvent', label: 'Oui, régulièrement (5+ véhicules)' },
        { value: 'parfois', label: 'Oui, quelques fois (2-4 véhicules)' },
        { value: 'une_fois', label: 'Une seule fois' },
        { value: 'jamais', label: 'Jamais' }
      ]
    },
    {
      id: 'q6',
      question: "Êtes-vous à l'aise avec les outils informatiques et numériques ?",
      options: [
        { value: 'tres', label: 'Très à l\'aise' },
        { value: 'moyennement', label: 'Moyennement à l\'aise' },
        { value: 'peu', label: 'Peu à l\'aise' },
        { value: 'pas', label: 'Pas du tout à l\'aise' }
      ]
    },
    {
      id: 'q7',
      question: "Quelle est votre situation professionnelle actuelle ?",
      options: [
        { value: 'salarie', label: 'Salarié(e)' },
        { value: 'independant', label: 'Indépendant / Auto-entrepreneur' },
        { value: 'recherche', label: 'En recherche d\'emploi' },
        { value: 'autre', label: 'Autre (étudiant, retraité...)' }
      ]
    },
    {
      id: 'q8',
      question: "Combien de temps pouvez-vous consacrer à la formation par semaine ?",
      options: [
        { value: '10plus', label: 'Plus de 10 heures' },
        { value: '5-10', label: '5 à 10 heures' },
        { value: '2-5', label: '2 à 5 heures' },
        { value: 'moins2', label: 'Moins de 2 heures' }
      ]
    },
    {
      id: 'q9',
      question: "Avez-vous un budget pour démarrer votre activité d'inspecteur ?",
      options: [
        { value: 'oui_complet', label: 'Oui, budget de 3000€ et plus' },
        { value: 'oui_partiel', label: 'Oui, budget de 1500-3000€' },
        { value: 'limite', label: 'Budget limité (moins de 1500€)' },
        { value: 'non', label: 'Pas encore de budget défini' }
      ]
    },
    {
      id: 'q10',
      question: "Qu'est-ce qui vous motive le plus dans ce projet ?",
      options: [
        { value: 'independance', label: 'L\'indépendance et la liberté' },
        { value: 'passion', label: 'La passion de l\'automobile' },
        { value: 'revenus', label: 'Les revenus attractifs' },
        { value: 'reconversion', label: 'Une nouvelle carrière' }
      ]
    }
  ];

  const handleAnswerChange = (questionId, value) => {
    setFormData(prev => ({
      ...prev,
      answers: {
        ...prev.answers,
        [questionId]: value
      }
    }));
  };

  const handleSubmit = async () => {
    const allAnswered = questions.every(q => formData.answers[q.id]);
    
    if (!allAnswered) {
      toast.error('Veuillez répondre à toutes les questions');
      return;
    }

    if (!formData.has_driving_license) {
      toast.error('Le permis B est obligatoire pour cette formation');
      return;
    }

    if (!formData.professional_project || formData.professional_project.length < 50) {
      toast.error('Veuillez décrire votre projet professionnel (minimum 50 caractères)');
      return;
    }

    if (!formData.has_smartphone) {
      toast.error('Veuillez indiquer si vous possédez un smartphone');
      return;
    }

    if (!formData.has_disability) {
      toast.error('Veuillez répondre à la question sur le handicap');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${API}/pre-registration/submit`, formData);
      
      if (response.data.validated) {
        toast.success('Profil validé avec succès !');
        
        if (onComplete) {
          onComplete(formData);
        } else {
          navigate('/register', { state: { preRegistration: response.data } });
        }
      }
    } catch (error) {
      console.error('Erreur lors de la soumission:', error);
      toast.error(error.response?.data?.detail || 'Une erreur est survenue');
    } finally {
      setLoading(false);
    }
  };

  const totalSteps = 13; // 0: info, 1-10: questions, 11: projet pro, 12: handicap/smartphone, 13: permis
  const displayStep = Math.min(step, totalSteps);
  const progressPercentage = Math.round((displayStep / totalSteps) * 100);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Questionnaire de Pré-inscription</CardTitle>
          <CardDescription>
            Pour garantir la qualité de notre formation et valider votre projet professionnel, 
            nous analysons chaque candidature. Ce questionnaire nous aide à vous accompagner au mieux.
          </CardDescription>
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Étape {displayStep} sur {totalSteps}</span>
              <span>{progressPercentage}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          
          {/* Step 0: Contact Info */}
          {step === 0 && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="full_name">Nom complet *</Label>
                <Input
                  id="full_name"
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  placeholder="Jean Dupont"
                  required
                  data-testid="full-name-input"
                />
              </div>
              <div>
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="jean.dupont@example.com"
                  required
                  data-testid="email-input"
                />
              </div>
              <div>
                <Label htmlFor="phone">Numéro de téléphone *</Label>
                <Input
                  id="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="06 12 34 56 78"
                  required
                  data-testid="phone-input"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Pour que notre équipe puisse vous contacter et répondre à vos questions
                </p>
              </div>
              <Button 
                onClick={() => setStep(1)} 
                disabled={!formData.email || !formData.full_name || !formData.phone || formData.phone.length < 10}
                className="w-full"
                data-testid="start-quiz-btn"
              >
                Commencer le questionnaire
              </Button>
            </div>
          )}

          {/* Steps 1-10: Questions */}
          {step >= 1 && step <= 10 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-4">
                  {questions[step - 1].question}
                </h3>
                <RadioGroup
                  value={formData.answers[questions[step - 1].id] || ''}
                  onValueChange={(value) => handleAnswerChange(questions[step - 1].id, value)}
                >
                  <div className="space-y-3">
                    {questions[step - 1].options.map((option) => (
                      <div key={option.value} className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                        <RadioGroupItem value={option.value} id={option.value} />
                        <Label htmlFor={option.value} className="cursor-pointer flex-1">
                          {option.label}
                        </Label>
                      </div>
                    ))}
                  </div>
                </RadioGroup>
              </div>

              <div className="flex gap-4">
                <Button 
                  variant="outline" 
                  onClick={() => setStep(step - 1)}
                  disabled={step === 1}
                  className="flex-1"
                >
                  Précédent
                </Button>
                <Button 
                  onClick={() => setStep(step + 1)}
                  disabled={!formData.answers[questions[step - 1].id]}
                  className="flex-1"
                >
                  Suivant
                </Button>
              </div>
            </div>
          )}

          {/* Step 11: Professional Project Description */}
          {step === 11 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-2">
                  Décrivez votre projet professionnel
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  Expliquez-nous en quelques lignes pourquoi vous souhaitez devenir inspecteur automobile 
                  et quels sont vos objectifs professionnels. Cette information nous aide à valider votre projet.
                </p>
                <Textarea
                  value={formData.professional_project}
                  onChange={(e) => setFormData({ ...formData, professional_project: e.target.value })}
                  placeholder="Ex: Je souhaite me reconvertir dans l'inspection automobile car j'ai toujours été passionné par les voitures. Mon objectif est de devenir inspecteur indépendant dans ma région et de proposer mes services aux particuliers..."
                  rows={6}
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-2">
                  Minimum 50 caractères ({formData.professional_project.length}/50)
                </p>
              </div>

              <div className="flex gap-4">
                <Button 
                  variant="outline" 
                  onClick={() => setStep(10)}
                  className="flex-1"
                >
                  Précédent
                </Button>
                <Button 
                  onClick={() => setStep(12)}
                  disabled={formData.professional_project.length < 50}
                  className="flex-1"
                >
                  Suivant
                </Button>
              </div>
            </div>
          )}

          {/* Step 12: Disability & Smartphone */}
          {step === 12 && (
            <div className="space-y-6">
              {/* Disability Question */}
              <div className="p-4 border rounded-lg">
                <h3 className="text-lg font-semibold mb-4">
                  Êtes-vous en situation de handicap ?
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  Cette information nous permet d'adapter la formation à vos besoins spécifiques si nécessaire.
                </p>
                <RadioGroup
                  value={formData.has_disability}
                  onValueChange={(value) => setFormData({ ...formData, has_disability: value })}
                >
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                      <RadioGroupItem value="non" id="disability_non" />
                      <Label htmlFor="disability_non" className="cursor-pointer flex-1">
                        Non
                      </Label>
                    </div>
                    <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                      <RadioGroupItem value="oui" id="disability_oui" />
                      <Label htmlFor="disability_oui" className="cursor-pointer flex-1">
                        Oui (nous vous contacterons pour adapter la formation)
                      </Label>
                    </div>
                    <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                      <RadioGroupItem value="ne_souhaite_pas_repondre" id="disability_no_answer" />
                      <Label htmlFor="disability_no_answer" className="cursor-pointer flex-1">
                        Je ne souhaite pas répondre
                      </Label>
                    </div>
                  </div>
                </RadioGroup>
              </div>

              {/* Smartphone Question */}
              <div className="p-4 border rounded-lg">
                <h3 className="text-lg font-semibold mb-4">
                  Possédez-vous un smartphone récent (2015 ou plus récent) ?
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  Un smartphone est nécessaire pour réaliser les inspections et utiliser l'application.
                </p>
                <RadioGroup
                  value={formData.has_smartphone}
                  onValueChange={(value) => setFormData({ ...formData, has_smartphone: value })}
                >
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                      <RadioGroupItem value="oui" id="smartphone_oui" />
                      <Label htmlFor="smartphone_oui" className="cursor-pointer flex-1">
                        Oui, j'ai un smartphone récent
                      </Label>
                    </div>
                    <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                      <RadioGroupItem value="oui_ancien" id="smartphone_ancien" />
                      <Label htmlFor="smartphone_ancien" className="cursor-pointer flex-1">
                        J'ai un smartphone mais il est ancien (avant 2015)
                      </Label>
                    </div>
                    <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                      <RadioGroupItem value="non" id="smartphone_non" />
                      <Label htmlFor="smartphone_non" className="cursor-pointer flex-1">
                        Non, je n'ai pas de smartphone
                      </Label>
                    </div>
                  </div>
                </RadioGroup>
              </div>

              <div className="flex gap-4">
                <Button 
                  variant="outline" 
                  onClick={() => setStep(11)}
                  className="flex-1"
                >
                  Précédent
                </Button>
                <Button 
                  onClick={() => setStep(13)}
                  disabled={!formData.has_disability || !formData.has_smartphone}
                  className="flex-1"
                >
                  Suivant
                </Button>
              </div>
            </div>
          )}

          {/* Step 13: Driving License Confirmation */}
          {step === 13 && (
            <div className="space-y-6">
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  <strong>Prérequis obligatoire</strong> - Un permis de conduire B en cours de validité est nécessaire pour exercer le métier d'inspecteur automobile.
                </AlertDescription>
              </Alert>

              <div className="flex items-start space-x-3 p-4 border-2 border-blue-200 rounded-lg bg-blue-50">
                <Checkbox
                  id="driving_license"
                  checked={formData.has_driving_license}
                  onCheckedChange={(checked) => setFormData({ ...formData, has_driving_license: checked })}
                />
                <Label htmlFor="driving_license" className="cursor-pointer text-sm leading-relaxed">
                  Je certifie être titulaire d'un permis de conduire B en cours de validité.
                  Je comprends que ce prérequis est obligatoire pour accéder à la formation d'inspecteur automobile.
                </Label>
              </div>

              <div className="flex gap-4">
                <Button 
                  variant="outline" 
                  onClick={() => setStep(12)}
                  className="flex-1"
                >
                  Précédent
                </Button>
                <Button 
                  onClick={handleSubmit}
                  disabled={!formData.has_driving_license || loading}
                  className="flex-1"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyse en cours...
                    </>
                  ) : (
                    <>
                      <CheckCircle className="mr-2 h-4 w-4" />
                      Valider mon profil
                    </>
                  )}
                </Button>
              </div>
            </div>
          )}

        </CardContent>
      </Card>
    </div>
  );
}
