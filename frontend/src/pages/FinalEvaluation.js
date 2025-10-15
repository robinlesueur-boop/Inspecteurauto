import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Label } from '../components/ui/label';
import { Trophy, CheckCircle, XCircle, Award } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function FinalEvaluation() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);

  useEffect(() => {
    loadQuiz();
  }, []);

  const loadQuiz = async () => {
    try {
      const response = await axios.get(`${API}/quizzes/module/final_evaluation`);
      setQuiz(response.data);
    } catch (error) {
      console.error('Error loading final evaluation:', error);
      toast.error('Erreur lors du chargement de l\'évaluation');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, optionIndex) => {
    setAnswers({
      ...answers,
      [questionId]: optionIndex
    });
  };

  const handleNext = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    const unansweredQuestions = quiz.questions.filter(q => answers[q.id] === undefined);
    
    if (unansweredQuestions.length > 0) {
      toast.error(`Veuillez répondre à toutes les questions (${unansweredQuestions.length} restantes)`);
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(`${API}/quizzes/${quiz.id}/submit`, {
        answers
      });
      
      setResults(response.data);
      setSubmitted(true);
      
      if (response.data.passed) {
        toast.success('🎉 Félicitations ! Vous avez réussi l\'évaluation finale !');
      } else {
        toast.error('Score insuffisant. Vous pouvez repasser l\'évaluation.');
      }
    } catch (error) {
      console.error('Error submitting evaluation:', error);
      toast.error('Erreur lors de la soumission');
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    setAnswers({});
    setCurrentQuestion(0);
    setSubmitted(false);
    setResults(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de l'évaluation...</p>
        </div>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6">
            <p className="text-center text-red-600">Évaluation non trouvée</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (submitted && results) {
    return (
      <>
        <Helmet>
          <title>Résultats - Évaluation Finale</title>
        </Helmet>

        <div className="min-h-screen bg-gray-50 py-12">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <Card className="shadow-xl">
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  {results.passed ? (
                    <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center">
                      <Trophy className="w-16 h-16 text-green-600" />
                    </div>
                  ) : (
                    <div className="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center">
                      <XCircle className="w-16 h-16 text-red-600" />
                    </div>
                  )}
                </div>
                <CardTitle className="text-3xl">
                  {results.passed ? '🎉 Félicitations !' : 'Évaluation Non Réussie'}
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-6">
                <div className="text-center">
                  <div className="text-6xl font-bold text-blue-600 mb-2">
                    {results.score.toFixed(0)}%
                  </div>
                  <p className="text-gray-600 text-lg">
                    {results.correct_answers} / {results.total_questions} réponses correctes
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    Score requis: {results.passing_score}%
                  </p>
                </div>

                {results.passed ? (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                    <h3 className="font-semibold text-green-800 mb-3 flex items-center text-lg">
                      <Award className="w-6 h-6 mr-2" />
                      Certification Obtenue
                    </h3>
                    <p className="text-green-700 mb-4">
                      Vous avez brillamment réussi l'évaluation finale ! Vous maîtrisez maintenant 
                      toutes les compétences nécessaires pour devenir inspecteur automobile professionnel.
                    </p>
                    <ul className="text-green-700 space-y-2 text-sm">
                      <li>✓ Votre certificat est maintenant disponible</li>
                      <li>✓ Vous êtes qualifié pour exercer en tant qu'inspecteur automobile</li>
                      <li>✓ Rejoignez notre communauté de professionnels certifiés</li>
                    </ul>
                  </div>
                ) : (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                    <h3 className="font-semibold text-red-800 mb-3">
                      Continuez vos efforts !
                    </h3>
                    <p className="text-red-700 mb-4">
                      Votre score est légèrement en dessous du seuil requis. Nous vous recommandons 
                      de revoir les modules de formation et de repasser l'évaluation.
                    </p>
                    <Button
                      onClick={handleRetry}
                      className="bg-blue-600 hover:bg-blue-700 mt-2"
                    >
                      Repasser l'Évaluation
                    </Button>
                  </div>
                )}

                {/* Detailed Results */}
                <div className="border-t pt-6">
                  <h3 className="font-semibold text-gray-900 mb-4">Détails des Réponses</h3>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {results.detailed_results.map((result, index) => (
                      <div
                        key={index}
                        className={`p-4 rounded-lg border-2 ${
                          result.is_correct
                            ? 'bg-green-50 border-green-200'
                            : 'bg-red-50 border-red-200'
                        }`}
                      >
                        <div className="flex items-start">
                          <div className="flex-shrink-0 mr-3">
                            {result.is_correct ? (
                              <CheckCircle className="w-5 h-5 text-green-600" />
                            ) : (
                              <XCircle className="w-5 h-5 text-red-600" />
                            )}
                          </div>
                          <div className="flex-1">
                            <p className="font-medium text-gray-900 mb-2">
                              Question {index + 1}: {result.question}
                            </p>
                            {!result.is_correct && result.explanation && (
                              <p className="text-sm text-gray-700 mt-2 italic">
                                💡 {result.explanation}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-center space-x-4 pt-4">
                  <Button
                    onClick={() => navigate('/dashboard')}
                    variant="outline"
                  >
                    Retour au Dashboard
                  </Button>
                  {results.passed && (
                    <Button
                      onClick={() => navigate('/satisfaction-survey')}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      Enquête de Satisfaction
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </>
    );
  }

  const question = quiz.questions[currentQuestion];
  const progress = ((currentQuestion + 1) / quiz.questions.length) * 100;

  return (
    <>
      <Helmet>
        <title>Évaluation Finale - Formation Inspecteur Automobile</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="shadow-xl">
            <CardHeader>
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-600">
                    Question {currentQuestion + 1} sur {quiz.questions.length}
                  </span>
                  <span className="text-sm font-semibold text-blue-600">
                    {Math.round(progress)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                <p className="text-sm text-yellow-800">
                  <Trophy className="inline w-4 h-4 mr-1" />
                  <strong>Évaluation Finale Certifiante</strong> - Score minimum requis: 80%
                </p>
              </div>
              
              <CardTitle className="text-xl">
                {question.question}
              </CardTitle>
            </CardHeader>
            
            <CardContent className="space-y-6">
              <RadioGroup
                value={answers[question.id]?.toString()}
                onValueChange={(value) => handleAnswerChange(question.id, parseInt(value))}
              >
                <div className="space-y-3">
                  {question.options.map((option, index) => (
                    <div
                      key={index}
                      className={`flex items-center space-x-3 p-4 rounded-lg border-2 cursor-pointer transition-all ${
                        answers[question.id] === index
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => handleAnswerChange(question.id, index)}
                    >
                      <RadioGroupItem value={index.toString()} id={`option-${index}`} />
                      <Label 
                        htmlFor={`option-${index}`} 
                        className="flex-1 cursor-pointer"
                      >
                        {option}
                      </Label>
                    </div>
                  ))}
                </div>
              </RadioGroup>

              <div className="flex justify-between items-center pt-4">
                <Button
                  onClick={handlePrevious}
                  disabled={currentQuestion === 0}
                  variant="outline"
                >
                  Précédent
                </Button>

                <div className="text-sm text-gray-500">
                  {Object.keys(answers).length} / {quiz.questions.length} répondues
                </div>

                {currentQuestion === quiz.questions.length - 1 ? (
                  <Button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    {loading ? 'Envoi...' : 'Soumettre'}
                  </Button>
                ) : (
                  <Button
                    onClick={handleNext}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    Suivant
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}

export default FinalEvaluation;
