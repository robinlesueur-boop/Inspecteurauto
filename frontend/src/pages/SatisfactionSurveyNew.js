import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Star, CheckCircle, Loader2, Award, AlertCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function SatisfactionSurveyNew() {
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [answers, setAnswers] = useState({});
  const [comments, setComments] = useState('');

  const questions = [
    {
      id: 'overall_satisfaction',
      question: 'Globalement, êtes-vous satisfait(e) de la formation ?',
      type: 'rating',
      required: true
    },
    {
      id: 'content_quality',
      question: 'Comment évaluez-vous la qualité du contenu pédagogique ?',
      type: 'rating',
      required: true
    },
    {
      id: 'platform_usability',
      question: 'La plateforme était-elle facile à utiliser ?',
      type: 'rating',
      required: true
    },
    {
      id: 'support_quality',
      question: 'Êtes-vous satisfait(e) du support pédagogique ?',
      type: 'rating',
      required: true
    },
    {
      id: 'objectives_met',
      question: 'La formation a-t-elle répondu à vos attentes ?',
      type: 'scale',
      options: [
        { value: '5', label: 'Tout à fait' },
        { value: '4', label: 'Plutôt oui' },
        { value: '3', label: 'Partiellement' },
        { value: '2', label: 'Plutôt non' },
        { value: '1', label: 'Pas du tout' }
      ],
      required: true
    },
    {
      id: 'would_recommend',
      question: 'Recommanderiez-vous cette formation à un ami ou collègue ?',
      type: 'scale',
      options: [
        { value: '5', label: 'Oui, certainement' },
        { value: '4', label: 'Oui, probablement' },
        { value: '3', label: 'Peut-être' },
        { value: '2', label: 'Probablement pas' },
        { value: '1', label: 'Non' }
      ],
      required: true
    },
    {
      id: 'ready_to_work',
      question: 'Vous sentez-vous prêt(e) à exercer le métier d\'inspecteur automobile ?',
      type: 'scale',
      options: [
        { value: '5', label: 'Oui, tout à fait prêt(e)' },
        { value: '4', label: 'Oui, avec quelques révisions' },
        { value: '3', label: 'J\'ai encore besoin de pratique' },
        { value: '2', label: 'Pas vraiment' },
        { value: '1', label: 'Non, pas du tout' }
      ],
      required: true
    }
  ];

  const handleAnswer = (questionId, value) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async () => {
    // Vérifier que toutes les questions obligatoires sont répondues
    const unanswered = questions.filter(q => q.required && !answers[q.id]);
    if (unanswered.length > 0) {
      toast.error('Veuillez répondre à toutes les questions');
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/satisfaction-survey/submit`, {
        answers,
        comments,
        user_id: user?.id
      });

      toast.success('Merci pour votre retour !');
      
      // Mettre à jour le statut de l'utilisateur
      if (updateUser) {
        updateUser({ ...user, satisfaction_completed: true });
      }
      
      navigate('/dashboard');
    } catch (error) {
      console.error('Error submitting survey:', error);
      toast.error('Erreur lors de l\'envoi du questionnaire');
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[step];
  const progressPercentage = Math.round(((step + 1) / questions.length) * 100);

  const renderStarRating = (questionId) => {
    const value = answers[questionId] || 0;
    return (
      <div className="flex items-center justify-center gap-2 my-6">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            onClick={() => handleAnswer(questionId, star.toString())}
            className="transition-transform hover:scale-110"
          >
            <Star
              className={`h-12 w-12 ${
                star <= parseInt(value) 
                  ? 'fill-yellow-400 text-yellow-400' 
                  : 'text-gray-300'
              }`}
            />
          </button>
        ))}
      </div>
    );
  };

  if (!user?.has_purchased) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 flex items-center justify-center">
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Vous devez avoir terminé la formation pour accéder à ce questionnaire.
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Questionnaire de Satisfaction - Inspecteur Auto</title>
      </Helmet>

      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12">
        <div className="max-w-2xl mx-auto px-4">
          
          <div className="text-center mb-8">
            <Award className="h-12 w-12 text-blue-600 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Questionnaire de Satisfaction
            </h1>
            <p className="text-gray-600">
              Votre avis nous aide à améliorer la formation
            </p>
          </div>

          {/* Progress bar */}
          <div className="mb-8">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Question {step + 1} sur {questions.length}</span>
              <span>{progressPercentage}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="text-xl text-center">
                {currentQuestion.question}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {currentQuestion.type === 'rating' && renderStarRating(currentQuestion.id)}

              {currentQuestion.type === 'scale' && (
                <RadioGroup
                  value={answers[currentQuestion.id] || ''}
                  onValueChange={(value) => handleAnswer(currentQuestion.id, value)}
                  className="space-y-3"
                >
                  {currentQuestion.options.map((option) => (
                    <div 
                      key={option.value} 
                      className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
                    >
                      <RadioGroupItem value={option.value} id={`${currentQuestion.id}-${option.value}`} />
                      <Label 
                        htmlFor={`${currentQuestion.id}-${option.value}`} 
                        className="cursor-pointer flex-1"
                      >
                        {option.label}
                      </Label>
                    </div>
                  ))}
                </RadioGroup>
              )}

              {/* Final step: comments */}
              {step === questions.length - 1 && (
                <div className="mt-8 pt-6 border-t">
                  <Label className="text-base font-medium">
                    Commentaires ou suggestions (optionnel)
                  </Label>
                  <Textarea
                    value={comments}
                    onChange={(e) => setComments(e.target.value)}
                    placeholder="Partagez vos remarques, suggestions d'amélioration..."
                    rows={4}
                    className="mt-2"
                  />
                </div>
              )}

              {/* Navigation */}
              <div className="flex gap-4 mt-8">
                {step > 0 && (
                  <Button 
                    variant="outline" 
                    onClick={() => setStep(step - 1)}
                    className="flex-1"
                  >
                    Précédent
                  </Button>
                )}
                
                {step < questions.length - 1 ? (
                  <Button 
                    onClick={() => setStep(step + 1)}
                    disabled={!answers[currentQuestion.id]}
                    className="flex-1"
                  >
                    Suivant
                  </Button>
                ) : (
                  <Button 
                    onClick={handleSubmit}
                    disabled={loading || !answers[currentQuestion.id]}
                    className="flex-1 bg-green-600 hover:bg-green-700"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        Envoi...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Terminer
                      </>
                    )}
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>

          <p className="text-center text-sm text-gray-500 mt-6">
            Ce questionnaire est obligatoire pour obtenir votre attestation de formation.
            Vos réponses sont confidentielles.
          </p>
        </div>
      </div>
    </>
  );
}

export default SatisfactionSurveyNew;
