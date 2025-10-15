import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import toast from 'react-hot-toast';
import { CheckCircle, XCircle, Clock, ArrowRight, ArrowLeft, Trophy, AlertCircle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const QuizPage = () => {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [module, setModule] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [quizResults, setQuizResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [timeLeft, setTimeLeft] = useState(20 * 60); // 20 minutes

  useEffect(() => {
    fetchModule();
  }, [moduleId]);

  useEffect(() => {
    if (module && !showResults && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmitQuiz();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      
      return () => clearInterval(timer);
    }
  }, [module, showResults, timeLeft]);

  const fetchModule = async () => {
    try {
      const response = await axios.get(`${API}/modules/${moduleId}`);
      setModule(response.data);
    } catch (error) {
      console.error('Error fetching module:', error);
      setError('Module non trouvé');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, answer) => {
    setAnswers({
      ...answers,
      [questionId]: answer
    });
  };

  const handleSubmitQuiz = async () => {
    if (submitting) return;
    
    setSubmitting(true);
    
    try {
      const response = await axios.post(`${API}/quiz/submit`, {
        module_id: moduleId,
        answers: answers
      });
      
      setQuizResults(response.data);
      setShowResults(true);
    } catch (error) {
      console.error('Error submitting quiz:', error);
      setError('Erreur lors de la soumission du quiz');
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const getProgressPercentage = () => {
    if (!module?.quiz_questions.length) return 0;
    return ((currentQuestion + 1) / module.quiz_questions.length) * 100;
  };

  const canProceed = () => {
    if (!module?.quiz_questions[currentQuestion]) return false;
    const currentQuestionId = module.quiz_questions[currentQuestion].id;
    return answers[currentQuestionId] !== undefined;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error || !module) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">{error}</div>
          <Link to="/dashboard" className="btn-primary">
            Retour au tableau de bord
          </Link>
        </div>
      </div>
    );
  }

  if (showResults && quizResults) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700">
        
        {/* Navigation */}
        <nav className="bg-slate-900/50 backdrop-blur-lg border-b border-slate-800">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex justify-between items-center">
              <Link to="/dashboard" className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">🚗</span>
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                  InspecteurAutomobile.fr
                </span>
              </Link>
            </div>
          </div>
        </nav>

        <div className="max-w-4xl mx-auto px-6 py-12">
          <div className="text-center">
            
            {/* Results Header */}
            <div className="mb-8">
              {quizResults.passed ? (
                <div className="text-6xl mb-4">🎉</div>
              ) : (
                <div className="text-6xl mb-4">😞</div>
              )}
              
              <h1 className="text-4xl font-bold text-white mb-4">
                {quizResults.passed ? 'Quiz Réussi !' : 'Quiz Échoué'}
              </h1>
              
              <p className="text-xl text-slate-300 mb-6">
                Module: {module.title}
              </p>
            </div>

            {/* Score Display */}
            <div className="card max-w-2xl mx-auto mb-8">
              <div className="grid grid-cols-3 gap-6 text-center">
                <div>
                  <div className={`text-4xl font-bold mb-2 ${
                    quizResults.passed ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {quizResults.score}%
                  </div>
                  <div className="text-slate-300">Votre score</div>
                </div>
                
                <div>
                  <div className="text-4xl font-bold text-blue-400 mb-2">
                    {quizResults.total_questions}
                  </div>
                  <div className="text-slate-300">Questions</div>
                </div>
                
                <div>
                  <div className="text-4xl font-bold text-purple-400 mb-2">
                    70%
                  </div>
                  <div className="text-slate-300">Requis</div>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-slate-700">
                <div className="progress-bar">
                  <div 
                    className={`progress-fill ${
                      quizResults.passed 
                        ? 'bg-gradient-to-r from-green-500 to-green-600' 
                        : 'bg-gradient-to-r from-red-500 to-red-600'
                    }`}
                    style={{ width: `${quizResults.score}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-sm text-slate-400 mt-2">
                  <span>0%</span>
                  <span className="text-orange-400">70% requis</span>
                  <span>100%</span>
                </div>
              </div>
            </div>

            {/* Results Message */}
            <div className={`card max-w-2xl mx-auto mb-8 ${
              quizResults.passed 
                ? 'bg-green-500/10 border-green-500/30' 
                : 'bg-orange-500/10 border-orange-500/30'
            }`}>
              {quizResults.passed ? (
                <div className="text-center">
                  <h3 className="text-xl font-bold text-green-300 mb-4">
                    Félicitations ! Module validé
                  </h3>
                  <p className="text-slate-300 mb-4">
                    Vous avez réussi le quiz avec un score de {quizResults.score}%. 
                    Vous pouvez maintenant passer au module suivant.
                  </p>
                  <div className="flex justify-center space-x-4">
                    <Link to="/dashboard" className="btn-success">
                      Continuer ma formation
                    </Link>
                    <button 
                      onClick={() => window.location.reload()}
                      className="btn-secondary"
                    >
                      Refaire le quiz
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <h3 className="text-xl font-bold text-orange-300 mb-4">
                    Score insuffisant
                  </h3>
                  <p className="text-slate-300 mb-4">
                    Vous avez obtenu {quizResults.score}%, mais il faut 70% minimum. 
                    Révisez le contenu du module et retentez le quiz.
                  </p>
                  <div className="flex justify-center space-x-4">
                    <Link 
                      to={`/module/${moduleId}`} 
                      className="btn-primary"
                    >
                      Réviser le module
                    </Link>
                    <button 
                      onClick={() => window.location.reload()}
                      className="btn-warning"
                    >
                      Refaire le quiz
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Detailed Results */}
            <div className="card max-w-4xl mx-auto">
              <h3 className="text-xl font-bold text-white mb-6">
                Détail des réponses
              </h3>
              
              <div className="space-y-4">
                {module.quiz_questions.map((question, index) => {
                  const userAnswer = quizResults.answers[question.id];
                  const isCorrect = userAnswer === question.correct_answer;
                  
                  return (
                    <div key={question.id} className={`p-4 rounded-lg ${
                      isCorrect ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'
                    }`}>
                      <div className="flex items-start justify-between mb-3">
                        <h4 className="font-medium text-white flex-1">
                          {index + 1}. {question.question}
                        </h4>
                        <div className={`ml-4 px-3 py-1 rounded-full text-sm font-medium ${
                          isCorrect 
                            ? 'bg-green-500/20 text-green-300' 
                            : 'bg-red-500/20 text-red-300'
                        }`}>
                          {isCorrect ? '✓ Correct' : '✗ Incorrect'}
                        </div>
                      </div>
                      
                      <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <div className="text-slate-400 mb-1">Votre réponse:</div>
                          <div className={isCorrect ? 'text-green-300' : 'text-red-300'}>
                            {userAnswer || 'Aucune réponse'}
                          </div>
                        </div>
                        
                        {!isCorrect && (
                          <div>
                            <div className="text-slate-400 mb-1">Réponse correcte:</div>
                            <div className="text-green-300">
                              {question.correct_answer}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Back to Dashboard */}
            <div className="mt-8 text-center">
              <Link to="/dashboard" className="text-slate-400 hover:text-slate-300">
                ← Retour au tableau de bord
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700">
      
      {/* Navigation */}
      <nav className="bg-slate-900/50 backdrop-blur-lg border-b border-slate-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-6">
              <Link to="/dashboard" className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">🚗</span>
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                  InspecteurAutomobile.fr
                </span>
              </Link>
              
              <div className="text-slate-300">
                Quiz - {module.title}
              </div>
            </div>
            
            <div className="flex items-center space-x-6">
              {/* Timer */}
              <div className={`px-4 py-2 rounded-lg ${
                timeLeft <= 300 ? 'bg-red-500/20 text-red-300' : 'bg-blue-500/20 text-blue-300'
              }`}>
                ⏱ {formatTime(timeLeft)}
              </div>
              
              <button 
                onClick={logout} 
                className="text-slate-400 hover:text-slate-300"
              >
                Se déconnecter
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-8">
        
        {/* Quiz Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-3xl font-bold text-white">
              Quiz - {module.title}
            </h1>
            <div className="text-slate-300">
              Question {currentQuestion + 1} sur {module.quiz_questions.length}
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="progress-bar mb-4">
            <div 
              className="progress-fill"
              style={{ width: `${getProgressPercentage()}%` }}
            ></div>
          </div>
          
          <div className="flex justify-between text-sm text-slate-400">
            <span>Progression: {Math.round(getProgressPercentage())}%</span>
            <span>Score minimum requis: 70%</span>
          </div>
        </div>

        {/* Question */}
        {module.quiz_questions[currentQuestion] && (
          <div className="card mb-8">
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-white mb-4">
                {module.quiz_questions[currentQuestion].question}
              </h2>
            </div>

            {/* Answer Options */}
            <div className="space-y-4">
              {module.quiz_questions[currentQuestion].options.map((option, index) => {
                const questionId = module.quiz_questions[currentQuestion].id;
                const isSelected = answers[questionId] === option;
                
                return (
                  <label 
                    key={index}
                    className={`block p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                      isSelected 
                        ? 'border-blue-500 bg-blue-500/20' 
                        : 'border-slate-600 hover:border-slate-500 bg-slate-800/50'
                    }`}
                  >
                    <div className="flex items-center">
                      <input
                        type="radio"
                        name={questionId}
                        value={option}
                        checked={isSelected}
                        onChange={() => handleAnswerSelect(questionId, option)}
                        className="mr-4 w-4 h-4"
                        data-testid={`answer-option-${index}`}
                      />
                      <span className="text-white font-medium">
                        {option}
                      </span>
                    </div>
                  </label>
                );
              })}
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between items-center">
          <button 
            onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
            disabled={currentQuestion === 0}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← Précédent
          </button>

          <div className="flex space-x-4">
            {currentQuestion < module.quiz_questions.length - 1 ? (
              <button 
                onClick={() => setCurrentQuestion(currentQuestion + 1)}
                disabled={!canProceed()}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                data-testid="next-question-button"
              >
                Suivant →
              </button>
            ) : (
              <button 
                onClick={handleSubmitQuiz}
                disabled={!canProceed() || submitting}
                className="btn-success disabled:opacity-50 disabled:cursor-not-allowed"
                data-testid="submit-quiz-button"
              >
                {submitting ? (
                  <>
                    <span className="spinner"></span>
                    Soumission...
                  </>
                ) : (
                  'Terminer le quiz'
                )}
              </button>
            )}
          </div>
        </div>

        {/* Quiz Instructions */}
        <div className="mt-8 card bg-blue-500/10 border-blue-500/30">
          <h3 className="text-blue-300 font-medium mb-3">
            Instructions du quiz
          </h3>
          <ul className="text-sm text-slate-300 space-y-1">
            <li>• Vous avez 20 minutes pour compléter ce quiz</li>
            <li>• Score minimum requis: 70%</li>
            <li>• Vous pouvez naviguer entre les questions</li>
            <li>• Vous pouvez refaire le quiz si nécessaire</li>
            <li>• Toutes les questions sont obligatoires</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default QuizPage;