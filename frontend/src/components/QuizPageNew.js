import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import toast from 'react-hot-toast';
import { CheckCircle, XCircle, Clock, ArrowRight, ArrowLeft, Trophy, AlertCircle, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function QuizPageNew() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [quiz, setQuiz] = useState(null);
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);
  const [timeLeft, setTimeLeft] = useState(1800); // 30 minutes

  useEffect(() => {
    fetchQuiz();
  }, [moduleId]);

  useEffect(() => {
    if (quiz && !submitted && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [quiz, submitted, timeLeft]);

  const fetchQuiz = async () => {
    try {
      setLoading(true);
      
      // Fetch module info
      const moduleRes = await axios.get(`${API}/modules/${moduleId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setModule(moduleRes.data);
      
      // Fetch quiz
      const quizRes = await axios.get(`${API}/quizzes/module/${moduleId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setQuiz(quizRes.data);
      
    } catch (error) {
      console.error('Error fetching quiz:', error);
      if (error.response?.status === 403) {
        toast.error('Vous devez acheter la formation pour accéder à ce quiz');
        navigate('/dashboard');
      } else {
        toast.error('Quiz non trouvé');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, answerIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }));
  };

  const handleSubmit = async () => {
    // Check if all questions answered
    const allAnswered = quiz.questions.every(q => answers[q.id] !== undefined);
    
    if (!allAnswered) {
      toast.error('Veuillez répondre à toutes les questions');
      return;
    }

    try {
      setSubmitted(true);
      const response = await axios.post(
        `${API}/quizzes/${quiz.id}/submit`,
        { answers },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      
      setResults(response.data);
      
      if (response.data.passed) {
        toast.success(`Félicitations ! Score : ${response.data.score.toFixed(1)}% - Module validé !`);
        // Redirection automatique après 3 secondes
        setTimeout(() => {
          navigate('/dashboard');
        }, 3000);
      } else {
        toast.error(`Score insuffisant : ${response.data.score.toFixed(1)}% (80% requis)`);
      }
      
    } catch (error) {
      console.error('Error submitting quiz:', error);
      toast.error('Erreur lors de la soumission');
      setSubmitted(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="container mx-auto p-6">
        <Card>
          <CardContent className="p-12 text-center">
            <AlertCircle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">Quiz non disponible</h2>
            <p className="text-gray-600 mb-4">Ce module ne dispose pas encore de quiz</p>
            <Button onClick={() => navigate('/dashboard')}>
              Retour au tableau de bord
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Results View
  if (submitted && results) {
    return (
      <div className="container mx-auto p-6 max-w-4xl">
        <Card>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              {results.passed ? (
                <Trophy className="h-16 w-16 text-green-600" />
              ) : (
                <XCircle className="h-16 w-16 text-red-600" />
              )}
            </div>
            <CardTitle className="text-3xl">
              {results.passed ? 'Quiz Réussi !' : 'Quiz Non Réussi'}
            </CardTitle>
            <CardDescription>
              {module?.title}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            
            {/* Score Summary */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-sm text-gray-600">Score</p>
                  <p className="text-3xl font-bold text-blue-600">{results.score.toFixed(1)}%</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Bonnes Réponses</p>
                  <p className="text-3xl font-bold text-green-600">
                    {results.correct_answers}/{results.total_questions}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Requis</p>
                  <p className="text-3xl font-bold text-gray-600">{results.passing_score}%</p>
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span>Progression</span>
                <span>{results.score.toFixed(1)}%</span>
              </div>
              <Progress value={results.score} className="h-3" />
            </div>

            {/* Detailed Results */}
            <div className="space-y-4">
              <h3 className="text-xl font-semibold">Détail des Réponses</h3>
              {results.detailed_results.map((result, index) => (
                <Card key={result.question_id} className={result.is_correct ? 'border-green-200' : 'border-red-200'}>
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      {result.is_correct ? (
                        <CheckCircle className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                      ) : (
                        <XCircle className="h-6 w-6 text-red-600 flex-shrink-0 mt-1" />
                      )}
                      <div className="flex-1">
                        <p className="font-semibold mb-2">Question {index + 1}: {result.question}</p>
                        <p className="text-sm text-gray-600 mb-2">
                          <strong>Votre réponse :</strong> {quiz.questions[index].options[result.user_answer]}
                        </p>
                        {!result.is_correct && (
                          <p className="text-sm text-green-600 mb-2">
                            <strong>Bonne réponse :</strong> {quiz.questions[index].options[result.correct_answer]}
                          </p>
                        )}
                        {result.explanation && (
                          <p className="text-sm text-gray-700 bg-blue-50 p-3 rounded mt-2">
                            💡 {result.explanation}
                          </p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Actions */}
            <div className="flex gap-4 justify-center pt-6">
              {!results.passed && (
                <Button onClick={() => window.location.reload()} variant="default">
                  Refaire le Quiz
                </Button>
              )}
              <Button onClick={() => navigate('/dashboard')} variant="outline">
                Retour au Tableau de Bord
              </Button>
            </div>

          </CardContent>
        </Card>
      </div>
    );
  }

  // Quiz View
  const question = quiz.questions[currentQuestion];
  const progress = ((currentQuestion + 1) / quiz.questions.length) * 100;

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      
      {/* Header */}
      <Card className="mb-6">
        <CardContent className="p-4">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-xl font-bold">{quiz.title}</h2>
              <p className="text-sm text-gray-600">{module?.title}</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-gray-600" />
                <span className={`font-mono text-lg ${timeLeft < 300 ? 'text-red-600 font-bold' : ''}`}>
                  {formatTime(timeLeft)}
                </span>
              </div>
              <Badge variant={timeLeft < 300 ? 'destructive' : 'default'}>
                Question {currentQuestion + 1}/{quiz.questions.length}
              </Badge>
            </div>
          </div>
          <Progress value={progress} className="mt-4" />
        </CardContent>
      </Card>

      {/* Question Card */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">
            Question {currentQuestion + 1}
          </CardTitle>
          <CardDescription className="text-lg mt-4">
            {question.question}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          
          {/* Options */}
          {question.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswerSelect(question.id, index)}
              className={`w-full p-4 text-left border-2 rounded-lg transition-all ${
                answers[question.id] === index
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                  answers[question.id] === index
                    ? 'border-blue-600 bg-blue-600'
                    : 'border-gray-300'
                }`}>
                  {answers[question.id] === index && (
                    <div className="w-3 h-3 bg-white rounded-full"></div>
                  )}
                </div>
                <span className="font-medium">{String.fromCharCode(65 + index)}.</span>
                <span>{option}</span>
              </div>
            </button>
          ))}

          {/* Navigation */}
          <div className="flex justify-between pt-6">
            <Button
              onClick={() => setCurrentQuestion(prev => Math.max(0, prev - 1))}
              disabled={currentQuestion === 0}
              variant="outline"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Précédent
            </Button>

            {currentQuestion < quiz.questions.length - 1 ? (
              <Button
                onClick={() => setCurrentQuestion(prev => prev + 1)}
                disabled={answers[question.id] === undefined}
              >
                Suivant
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            ) : (
              <Button
                onClick={handleSubmit}
                disabled={!quiz.questions.every(q => answers[q.id] !== undefined)}
                className="bg-green-600 hover:bg-green-700"
              >
                <Trophy className="h-4 w-4 mr-2" />
                Soumettre le Quiz
              </Button>
            )}
          </div>

          {/* Progress Indicators */}
          <div className="flex flex-wrap gap-2 pt-4 border-t">
            {quiz.questions.map((q, idx) => (
              <button
                key={q.id}
                onClick={() => setCurrentQuestion(idx)}
                className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold ${
                  answers[q.id] !== undefined
                    ? 'bg-blue-600 text-white'
                    : idx === currentQuestion
                    ? 'bg-blue-100 text-blue-600 border-2 border-blue-600'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                {idx + 1}
              </button>
            ))}
          </div>

        </CardContent>
      </Card>

    </div>
  );
}
