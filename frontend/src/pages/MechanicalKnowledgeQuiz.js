import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Label } from '../components/ui/label';
import { AlertCircle, CheckCircle, BookOpen } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function MechanicalKnowledgeQuiz() {
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);
  const [checkingStatus, setCheckingStatus] = useState(true);

  useEffect(() => {
    checkQuizStatus();
  }, []);

  const checkQuizStatus = async () => {
    try {
      // Check if user already completed this quiz
      const statusResponse = await axios.get(`${API}/preliminary-quiz/mechanical-knowledge/status`);
      
      if (statusResponse.data.completed) {
        // Already completed, redirect to dashboard
        toast.success('Quiz déjà complété !');
        navigate('/dashboard');
        return;
      }
      
      // Load the quiz
      loadQuiz();
    } catch (error) {
      console.error('Error checking quiz status:', error);
      loadQuiz();
    }
  };

  const loadQuiz = async () => {
    try {
      const response = await axios.get(`${API}/preliminary-quiz/mechanical-knowledge`);
      setQuiz(response.data);
    } catch (error) {
      console.error('Error loading quiz:', error);
      toast.error('Erreur lors du chargement du quiz');
    } finally {
      setLoading(false);
      setCheckingStatus(false);
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
    // Check if all questions are answered
    const unansweredQuestions = quiz.questions.filter(q => answers[q.id] === undefined);
    
    if (unansweredQuestions.length > 0) {
      toast.error(`Veuillez répondre à toutes les questions (${unansweredQuestions.length} restantes)`);
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(`${API}/preliminary-quiz/mechanical-knowledge/submit`, {
        answers
      });
      
      setResults(response.data);
      setSubmitted(true);
      
      // Refresh user data
      const userResponse = await axios.get(`${API}/auth/me`);
      updateUser(userResponse.data);
      
      if (response.data.needs_remedial_module) {
        toast.success('Quiz complété ! Module de remise à niveau débloqué.');
      } else {
        toast.success('Excellent ! Vous pouvez commencer la formation.');
      }
    } catch (error) {
      console.error('Error submitting quiz:', error);
      toast.error('Erreur lors de la soumission du quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = () => {
    navigate('/dashboard');
  };

  if (loading || checkingStatus) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du quiz...</p>
        </div>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6">
            <p className="text-center text-red-600">Quiz non trouvé</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (submitted && results) {
    return (
      <>
        <Helmet>
          <title>Résultats - Évaluation Connaissances Mécaniques</title>
        </Helmet>

        <div className="min-h-screen bg-gray-50 py-12">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <Card className="shadow-xl">
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  {results.needs_remedial_module ? (
                    <div className="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center">
                      <AlertCircle className="w-12 h-12 text-yellow-600" />
                    </div>
                  ) : (
                    <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-12 h-12 text-green-600" />
                    </div>
                  )}
                </div>
                <CardTitle className="text-2xl">
                  Évaluation des Connaissances Mécaniques
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-6">
                <div className="text-center">
                  <div className="text-5xl font-bold text-blue-600 mb-2">
                    {results.score.toFixed(0)}%
                  </div>
                  <p className="text-gray-600">
                    {results.correct_answers} / {results.total_questions} réponses correctes
                  </p>
                </div>

                {results.needs_remedial_module ? (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                    <h3 className="font-semibold text-yellow-800 mb-2 flex items-center">
                      <BookOpen className="w-5 h-5 mr-2" />
                      Module de Remise à Niveau Recommandé
                    </h3>
                    <p className="text-yellow-700 mb-4">
                      Votre score est inférieur à 70%. Pour optimiser votre apprentissage, 
                      nous vous recommandons de commencer par le module "Remise à Niveau Mécanique" 
                      qui vous permettra d'acquérir les bases nécessaires.
                    </p>
                    <ul className="text-yellow-700 space-y-1 text-sm">
                      <li>✓ Ce module a été débloqué pour vous</li>
                      <li>✓ Il couvre les fondamentaux de la mécanique automobile</li>
                      <li>✓ Durée: 2 heures de contenu</li>
                    </ul>
                  </div>
                ) : (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                    <h3 className="font-semibold text-green-800 mb-2 flex items-center">
                      <CheckCircle className="w-5 h-5 mr-2" />
                      Excellentes Connaissances !
                    </h3>
                    <p className="text-green-700">
                      Vos connaissances mécaniques sont solides. Vous pouvez directement 
                      commencer la formation principale sans passer par le module de remise à niveau.
                    </p>
                  </div>
                )}

                <div className="flex justify-center">
                  <Button 
                    onClick={handleContinue}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3"
                    size="lg"
                  >
                    Accéder au Tableau de Bord
                  </Button>
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
        <title>Évaluation Connaissances Mécaniques - Formation Inspecteur Automobile</title>
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
                    disabled={currentQuestion === quiz.questions.length - 1}
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

export default MechanicalKnowledgeQuiz;
