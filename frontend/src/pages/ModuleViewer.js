import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { 
  BookOpen, 
  Clock, 
  ChevronLeft, 
  ChevronRight, 
  CheckCircle,
  ArrowLeft,
  Award,
  Users,
  MessageCircle,
  Trophy,
  Play,
  Video
} from 'lucide-react';
import axios from 'axios';
import VideoPlayer from '../components/VideoPlayer';
import ReadingProgressBar from '../components/ReadingProgressBar';
import KeyPointHighlight from '../components/KeyPointHighlight';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function ModuleViewer() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [module, setModule] = useState(null);
  const [allModules, setAllModules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [readingTime, setReadingTime] = useState(0);

  useEffect(() => {
    fetchModule();
    fetchAllModules();
    
    // Start reading timer
    const timer = setInterval(() => {
      setReadingTime(prev => prev + 1);
    }, 60000); // Update every minute

    return () => clearInterval(timer);
  }, [moduleId]);

  const fetchModule = async () => {
    try {
      const response = await axios.get(`${API}/modules/${moduleId}`);
      setModule(response.data);
      
      // Check if module is completed
      if (user?.has_purchased) {
        const progressResponse = await axios.get(`${API}/progress`);
        const moduleProgress = progressResponse.data.find(p => p.module_id === moduleId);
        setCompleted(moduleProgress?.completed || false);
      }
    } catch (error) {
      console.error('Error fetching module:', error);
      if (error.response?.status === 403) {
        toast.error('Accès limité - Formation complète requise');
        navigate('/dashboard');
      } else if (error.response?.status === 404) {
        toast.error('Module introuvable');
        navigate('/dashboard');
      } else {
        toast.error('Erreur lors du chargement du module');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchAllModules = async () => {
    try {
      const response = await axios.get(`${API}/modules`);
      setAllModules(response.data);
    } catch (error) {
      console.error('Error fetching all modules:', error);
    }
  };

  const handleMarkComplete = async () => {
    if (completing || completed) return;

    setCompleting(true);
    try {
      await axios.post(`${API}/progress/${moduleId}/complete`);
      setCompleted(true);
      toast.success('Module marqué comme terminé !');
      
      // Check if certificate is generated
      if (user?.has_purchased) {
        const userResponse = await axios.get(`${API}/auth/me`);
        if (userResponse.data.certificate_url && !user.certificate_url) {
          toast.success('🎉 Félicitations ! Votre certificat est prêt !');
        }
      }
    } catch (error) {
      console.error('Error marking complete:', error);
      toast.error('Erreur lors de la validation');
    } finally {
      setCompleting(false);
    }
  };

  const getCurrentModuleIndex = () => {
    return allModules.findIndex(m => m.id === moduleId);
  };

  const getNextModule = () => {
    const currentIndex = getCurrentModuleIndex();
    if (currentIndex >= 0 && currentIndex < allModules.length - 1) {
      return allModules[currentIndex + 1];
    }
    return null;
  };

  const getPreviousModule = () => {
    const currentIndex = getCurrentModuleIndex();
    if (currentIndex > 0) {
      return allModules[currentIndex - 1];
    }
    return null;
  };

  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? ` ${mins}min` : ''}`;
    }
    return `${mins}min`;
  };

  const calculateReadingProgress = () => {
    if (!module) return 0;
    const estimatedReadingTime = module.duration_minutes;
    return Math.min((readingTime / estimatedReadingTime) * 100, 100);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du module...</p>
        </div>
      </div>
    );
  }

  if (!module) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="w-96 text-center">
          <CardContent className="p-8">
            <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Module introuvable</h3>
            <Button onClick={() => navigate('/dashboard')}>
              Retour au Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const nextModule = getNextModule();
  const previousModule = getPreviousModule();
  const readingProgress = calculateReadingProgress();

  return (
    <>
      <Helmet>
        <title>{module.title} - Formation Inspecteur Automobile</title>
        <meta name="description" content={module.description} />
      </Helmet>

      <div className="min-h-screen bg-gray-50" data-testid="module-viewer">
        {/* Header */}
        <div className="bg-white shadow-sm border-b sticky top-16 z-40">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Link to="/dashboard">
                  <Button variant="outline" size="sm" data-testid="back-button" className="border-gray-600 text-gray-900 hover:bg-gray-100">
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Retour
                  </Button>
                </Link>
                
                <div>
                  <h1 className="font-semibold text-gray-900">{module.title}</h1>
                  <div className="flex items-center space-x-3 text-sm text-gray-500">
                    <span className="flex items-center">
                      <Clock className="h-4 w-4 mr-1" />
                      {formatDuration(module.duration_minutes)}
                    </span>
                    {module.is_free && (
                      <Badge variant="secondary" className="bg-green-100 text-green-700">
                        Gratuit
                      </Badge>
                    )}
                    {completed && (
                      <Badge className="bg-green-100 text-green-700">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Terminé
                      </Badge>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                {!completed && user?.has_purchased && (
                  <Button
                    onClick={handleMarkComplete}
                    disabled={completing}
                    className="bg-green-600 hover:bg-green-700"
                    data-testid="mark-complete-button"
                  >
                    {completing ? (
                      <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full"></div>
                    ) : (
                      <CheckCircle className="h-4 w-4 mr-2" />
                    )}
                    {completing ? 'Validation...' : 'Marquer terminé'}
                  </Button>
                )}
                
                {user?.has_purchased && (
                  <Link to="/forum">
                    <Button variant="outline" size="sm">
                      <MessageCircle className="h-4 w-4 mr-2" />
                      Forum
                    </Button>
                  </Link>
                )}
              </div>
            </div>

            {/* Reading Progress */}
            {readingProgress > 0 && (
              <div className="mt-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-600">Progression de lecture</span>
                  <span className="text-sm font-medium">{readingProgress.toFixed(0)}%</span>
                </div>
                <Progress value={readingProgress} className="h-2" />
              </div>
            )}
          </div>
        </div>

        {/* Content */}
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            {/* Module Content */}
            <Card className="shadow-lg">
              <CardHeader className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-t-lg">
                <CardTitle className="text-2xl">{module.title}</CardTitle>
                <p className="text-blue-100">{module.description}</p>
              </CardHeader>
              
              <CardContent className="p-0">
                <div 
                  className="prose prose-lg max-w-none p-8 leading-relaxed text-gray-900"
                  dangerouslySetInnerHTML={{ __html: module.content }}
                  style={{
                    lineHeight: '1.8',
                    fontSize: '1.1rem',
                    maxWidth: '100%',
                    width: '100%',
                    color: '#1a1a1a'
                  }}
                />
                <style jsx="true">{`
                  .prose h1 { color: #1a1a1a; font-weight: 700; font-size: 2.25rem; margin-top: 2rem; margin-bottom: 1rem; }
                  .prose h2 { color: #1f2937; font-weight: 700; font-size: 1.875rem; margin-top: 2rem; margin-bottom: 1rem; }
                  .prose h3 { color: #374151; font-weight: 600; font-size: 1.5rem; margin-top: 1.5rem; margin-bottom: 0.75rem; }
                  .prose h4 { color: #4b5563; font-weight: 600; font-size: 1.25rem; margin-top: 1.25rem; margin-bottom: 0.5rem; }
                  .prose p { color: #1f2937; font-size: 1.125rem; line-height: 1.8; margin-bottom: 1rem; }
                  .prose ul, .prose ol { color: #1f2937; font-size: 1.125rem; line-height: 1.8; margin-left: 1.5rem; margin-bottom: 1rem; }
                  .prose li { margin-bottom: 0.5rem; }
                  .prose strong { color: #111827; font-weight: 700; }
                  .prose a { color: #2563eb; text-decoration: underline; }
                  .prose code { background-color: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 0.25rem; color: #1f2937; }
                  .prose table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
                  .prose th, .prose td { border: 1px solid #e5e7eb; padding: 0.75rem; text-align: left; }
                  .prose th { background-color: #f9fafb; font-weight: 600; }
                  .prose blockquote { border-left: 4px solid #3b82f6; padding-left: 1rem; color: #4b5563; font-style: italic; margin: 1rem 0; }
                `}</style>
              </CardContent>
            </Card>

            {/* Quiz Section - Bien visible */}
            <Card className="shadow-lg bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-300">
              <CardContent className="p-8 text-center">
                <Award className="h-16 w-16 text-blue-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold mb-2">Fin du Module {module.order_index}</h3>
                <p className="text-gray-700 mb-6">
                  Pour débloquer le module suivant, vous devez réussir le quiz de validation (80% minimum requis)
                </p>
                <Button
                  onClick={() => navigate(`/quiz/${module.id}`)}
                  size="lg"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-xl"
                >
                  <Trophy className="mr-3 h-6 w-6" />
                  Passer le Quiz Maintenant
                </Button>
              </CardContent>
            </Card>

            {/* Navigation */}
            <Card className="shadow-lg">
              <CardContent className="p-6">
                <div className="flex justify-between items-center">
                  <div>
                    {previousModule ? (
                      <Link to={`/module/${previousModule.id}`}>
                        <Button variant="outline" className="mr-4">
                          <ChevronLeft className="h-4 w-4 mr-2" />
                          Module précédent
                        </Button>
                      </Link>
                    ) : (
                      <div></div>
                    )}
                  </div>

                  <div className="text-center">
                    <div className="text-sm text-gray-600 mb-2">
                      Module {getCurrentModuleIndex() + 1} sur {allModules.length}
                    </div>
                    <Progress 
                      value={((getCurrentModuleIndex() + 1) / allModules.length) * 100} 
                      className="w-32 mx-auto h-2"
                    />
                  </div>

                  <div>
                    {nextModule ? (
                      <Link to={`/module/${nextModule.id}`}>
                        <Button className="bg-blue-600 hover:bg-blue-700">
                          Module suivant
                          <ChevronRight className="h-4 w-4 ml-2" />
                        </Button>
                      </Link>
                    ) : completed ? (
                      <div className="text-center">
                        <div className="flex items-center text-green-600 mb-2">
                          <Award className="h-5 w-5 mr-2" />
                          <span className="font-semibold">Formation terminée !</span>
                        </div>
                        <Link to="/dashboard">
                          <Button className="bg-green-600 hover:bg-green-700">
                            Retour au Dashboard
                          </Button>
                        </Link>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        <Button 
                          onClick={handleMarkComplete}
                          disabled={!user?.has_purchased}
                          className="w-full bg-green-600 hover:bg-green-700"
                        >
                          <CheckCircle className="mr-2 h-5 w-5" />
                          Marquer comme terminé
                        </Button>
                        <Button
                          onClick={() => navigate(`/quiz/${module.id}`)}
                          disabled={!user?.has_purchased}
                          className="w-full"
                          variant="outline"
                        >
                          <Award className="mr-2 h-5 w-5" />
                          Passer le Quiz (obligatoire)
                        </Button>
                      </div>
                    )}
                  </div>
                </div>

                {/* Module Details */}
                <div className="mt-6 pt-6 border-t">
                  <div className="grid md:grid-cols-3 gap-6 text-center">
                    <div>
                      <div className="text-2xl font-bold text-blue-600">{formatDuration(module.duration_minutes)}</div>
                      <div className="text-sm text-gray-600">Durée estimée</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-green-600">{readingTime}min</div>
                      <div className="text-sm text-gray-600">Temps de lecture</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-purple-600">
                        {getCurrentModuleIndex() + 1}/{allModules.length}
                      </div>
                      <div className="text-sm text-gray-600">Progression</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Help Section */}
            <Card className="bg-blue-50 border-blue-200">
              <CardContent className="p-6 text-center">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                  Besoin d'aide ?
                </h3>
                <p className="text-blue-800 mb-4">
                  Rejoignez notre forum pour poser vos questions à la communauté
                </p>
                <div className="flex justify-center space-x-4">
                  {user?.has_purchased ? (
                    <Link to="/forum">
                      <Button variant="outline" className="border-blue-600 text-blue-600">
                        <Users className="h-4 w-4 mr-2" />
                        Accéder au Forum
                      </Button>
                    </Link>
                  ) : (
                    <Link to="/dashboard">
                      <Button className="bg-blue-600 hover:bg-blue-700">
                        Débloquer le Forum
                      </Button>
                    </Link>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </>
  );
}

export default ModuleViewer;