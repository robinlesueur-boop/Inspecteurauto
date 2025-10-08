import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Helmet } from 'react-helmet-async';
import { useAuth } from "../contexts/AuthContext";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Progress } from "../components/ui/progress";
import { motion } from "framer-motion";
import toast from 'react-hot-toast';
import { 
  BookOpen, 
  Clock, 
  Trophy, 
  Target, 
  Play, 
  CheckCircle,
  Lock,
  CreditCard,
  Award,
  TrendingUp,
  Users,
  MessageCircle,
  Download
} from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Dashboard() {
  const { user, updateUser } = useAuth();
  const [modules, setModules] = useState([]);
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [purchaseLoading, setPurchaseLoading] = useState(false);
  const [stats, setStats] = useState({
    totalModules: 0,
    completedModules: 0,
    totalHours: 0,
    progressPercentage: 0
  });

  useEffect(() => {
    fetchModules();
    if (user?.has_purchased) {
      fetchProgress();
    }
  }, [user]);

  const fetchModules = async () => {
    try {
      const response = await axios.get(`${API}/modules`);
      setModules(response.data);
      calculateStats(response.data, progress);
    } catch (error) {
      console.error("Error fetching modules:", error);
      toast.error("Erreur lors du chargement des modules");
    } finally {
      setLoading(false);
    }
  };

  const fetchProgress = async () => {
    try {
      const response = await axios.get(`${API}/progress`);
      setProgress(response.data);
      calculateStats(modules, response.data);
    } catch (error) {
      console.error("Error fetching progress:", error);
    }
  };

  const calculateStats = (moduleList, progressList) => {
    if (moduleList.length === 0) return;

    const totalModules = moduleList.length;
    const completedModules = progressList.filter(p => p.completed).length;
    const totalHours = moduleList.reduce((sum, m) => sum + (m.duration_minutes || 0), 0) / 60;
    const progressPercentage = totalModules > 0 ? (completedModules / totalModules) * 100 : 0;

    setStats({
      totalModules,
      completedModules,
      totalHours,
      progressPercentage
    });
  };

  const handlePurchase = async () => {
    if (purchaseLoading) return;
    
    setPurchaseLoading(true);
    try {
      const response = await axios.post(`${API}/payments/checkout-session`);
      window.location.href = response.data.url;
    } catch (error) {
      console.error("Payment error:", error);
      toast.error("Erreur lors du paiement: " + (error.response?.data?.detail || "Veuillez réessayer"));
    } finally {
      setPurchaseLoading(false);
    }
  };

  const isModuleCompleted = (moduleId) => {
    return progress.some(p => p.module_id === moduleId && p.completed);
  };

  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? ` ${mins}min` : ''}`;
    }
    return `${mins}min`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="space-y-6">
            <div className="animate-pulse h-8 bg-gray-300 rounded w-64"></div>
            <div className="grid md:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="animate-pulse h-24 bg-gray-300 rounded-lg"></div>
              ))}
            </div>
            <div className="animate-pulse h-64 bg-gray-300 rounded-lg"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Mon Dashboard - Formation Inspecteur Automobile</title>
        <meta name="description" content="Suivez votre progression dans la formation inspecteur automobile et accédez à vos modules de cours." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8" data-testid="dashboard">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Welcome Header */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl p-8 text-white">
              <h1 className="text-3xl font-bold mb-2" data-testid="welcome-message">
                Bonjour {user?.full_name} ! 👋
              </h1>
              <p className="text-blue-100 text-lg">
                {user?.has_purchased 
                  ? "Continuez votre parcours pour devenir inspecteur automobile expert" 
                  : "Accédez au module gratuit ou débloquez la formation complète"
                }
              </p>
              
              {user?.has_purchased && user?.certificate_url && (
                <div className="mt-4 flex items-center space-x-4">
                  <Badge className="bg-yellow-500 text-yellow-900">
                    <Award className="h-4 w-4 mr-1" />
                    Certifié
                  </Badge>
                  <Button
                    onClick={() => window.open(user.certificate_url, '_blank')}
                    variant="outline"
                    className="border-white text-white hover:bg-white hover:text-blue-600"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Télécharger Certificat
                  </Button>
                </div>
              )}
            </div>
          </motion.div>

          {/* Stats Cards */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8"
          >
            <Card className="text-center hover:shadow-lg transition-shadow" data-testid="total-modules-stat">
              <CardContent className="pt-6">
                <div className="flex items-center justify-center mb-2">
                  <BookOpen className="h-8 w-8 text-blue-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">
                  {user?.has_purchased ? stats.totalModules : "1"}
                </div>
                <div className="text-sm text-gray-600">
                  Module{user?.has_purchased && stats.totalModules > 1 ? 's' : ''} disponible{user?.has_purchased && stats.totalModules > 1 ? 's' : ''}
                </div>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow" data-testid="completed-modules-stat">
              <CardContent className="pt-6">
                <div className="flex items-center justify-center mb-2">
                  <Trophy className="h-8 w-8 text-yellow-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">{stats.completedModules}</div>
                <div className="text-sm text-gray-600">Module{stats.completedModules > 1 ? 's' : ''} terminé{stats.completedModules > 1 ? 's' : ''}</div>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow" data-testid="total-hours-stat">
              <CardContent className="pt-6">
                <div className="flex items-center justify-center mb-2">
                  <Clock className="h-8 w-8 text-green-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">{stats.totalHours.toFixed(1)}h</div>
                <div className="text-sm text-gray-600">de formation</div>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow" data-testid="progress-stat">
              <CardContent className="pt-6">
                <div className="flex items-center justify-center mb-2">
                  <Target className="h-8 w-8 text-purple-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">{stats.progressPercentage.toFixed(0)}%</div>
                <div className="text-sm text-gray-600">progression</div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Purchase Section for Non-Purchased Users */}
          {!user?.has_purchased && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mb-8"
            >
              <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200 shadow-lg">
                <CardContent className="p-8">
                  <div className="grid lg:grid-cols-2 gap-8 items-center">
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900 mb-4">
                        🚀 Débloquez la Formation Complète
                      </h3>
                      <p className="text-gray-700 mb-6 text-lg">
                        Accédez à <strong>11 heures de formation</strong> avec la méthode AutoJust exclusive, 
                        votre certification officielle et le forum privé des inspecteurs.
                      </p>
                      
                      <div className="space-y-3 mb-6">
                        <div className="flex items-center text-green-700">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          <span>7 modules premium supplémentaires</span>
                        </div>
                        <div className="flex items-center text-green-700">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          <span>Méthode AutoJust propriétaire</span>
                        </div>
                        <div className="flex items-center text-green-700">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          <span>Certification reconnue</span>
                        </div>
                        <div className="flex items-center text-green-700">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          <span>Accès au forum à vie</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-center">
                      <div className="bg-white rounded-xl p-6 shadow-lg">
                        <div className="text-3xl font-bold text-blue-600 mb-2">297€</div>
                        <p className="text-gray-600 mb-6">Formation complète + Certification</p>
                        
                        <Button
                          onClick={handlePurchase}
                          disabled={purchaseLoading}
                          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg"
                          data-testid="purchase-button"
                        >
                          {purchaseLoading ? (
                            <div className="animate-spin h-5 w-5 mr-2 border-2 border-white border-t-transparent rounded-full"></div>
                          ) : (
                            <CreditCard className="h-5 w-5 mr-2" />
                          )}
                          {purchaseLoading ? "Redirection..." : "Acheter Maintenant"}
                        </Button>
                        
                        <p className="text-sm text-gray-500 mt-3">
                          🔒 Paiement sécurisé • Garantie 30 jours
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Progress Overview for Purchased Users */}
          {user?.has_purchased && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="mb-8"
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
                    Votre Progression
                  </CardTitle>
                  <CardDescription>
                    {stats.completedModules} sur {stats.totalModules} modules terminés
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <Progress value={stats.progressPercentage} className="h-3" />
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-600">Progression globale</span>
                      <span className="font-medium">{stats.progressPercentage.toFixed(0)}%</span>
                    </div>
                    
                    {stats.progressPercentage === 100 && (
                      <div className="bg-green-50 border border-green-200 rounded-lg p-4 mt-4">
                        <div className="flex items-center text-green-800">
                          <Award className="h-5 w-5 mr-2" />
                          <span className="font-semibold">Félicitations ! Formation terminée</span>
                        </div>
                        <p className="text-green-700 mt-2">
                          Vous avez complété tous les modules. Votre certificat est maintenant disponible.
                        </p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Modules List */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Modules de Formation</h2>
              {user?.has_purchased && (
                <div className="flex items-center space-x-4">
                  <Link to="/forum">
                    <Button variant="outline" className="flex items-center">
                      <MessageCircle className="h-4 w-4 mr-2" />
                      Forum
                    </Button>
                  </Link>
                </div>
              )}
            </div>

            <div className="space-y-4" data-testid="modules-list">
              {modules.map((module, index) => {
                const isCompleted = isModuleCompleted(module.id);
                const isAccessible = module.is_free || user?.has_purchased;
                
                return (
                  <motion.div
                    key={module.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card className={`transition-all duration-300 ${
                      isAccessible ? 'hover:shadow-lg cursor-pointer' : 'opacity-75'
                    }`}>
                      <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                          <div className="flex-1 mr-6">
                            <div className="flex items-center space-x-3 mb-2">
                              <div className={`flex items-center justify-center w-10 h-10 rounded-full ${
                                isCompleted 
                                  ? 'bg-green-100 text-green-600' 
                                  : isAccessible 
                                    ? 'bg-blue-100 text-blue-600'
                                    : 'bg-gray-100 text-gray-400'
                              }`}>
                                {isCompleted ? (
                                  <CheckCircle className="h-5 w-5" />
                                ) : isAccessible ? (
                                  <BookOpen className="h-5 w-5" />
                                ) : (
                                  <Lock className="h-5 w-5" />
                                )}
                              </div>
                              
                              <div>
                                <h3 className="text-lg font-semibold text-gray-900">
                                  {module.title}
                                </h3>
                                <p className="text-sm text-gray-600">
                                  {module.description}
                                </p>
                              </div>
                            </div>
                            
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <div className="flex items-center">
                                <Clock className="h-4 w-4 mr-1" />
                                {formatDuration(module.duration_minutes)}
                              </div>
                              
                              {module.is_free && (
                                <Badge variant="secondary" className="bg-green-100 text-green-700">
                                  Gratuit
                                </Badge>
                              )}
                              
                              {isCompleted && (
                                <Badge className="bg-green-100 text-green-700">
                                  <CheckCircle className="h-3 w-3 mr-1" />
                                  Terminé
                                </Badge>
                              )}
                            </div>
                          </div>

                          <div className="flex flex-col items-end space-y-2">
                            {isAccessible ? (
                              <Link 
                                to={`/module/${module.id}`}
                                data-testid={`module-link-${module.id}`}
                              >
                                <Button 
                                  className={`${
                                    isCompleted 
                                      ? 'bg-green-600 hover:bg-green-700' 
                                      : 'bg-blue-600 hover:bg-blue-700'
                                  }`}
                                >
                                  <Play className="h-4 w-4 mr-2" />
                                  {isCompleted ? 'Revoir' : 'Commencer'}
                                </Button>
                              </Link>
                            ) : (
                              <Button disabled variant="outline">
                                <Lock className="h-4 w-4 mr-2" />
                                Verrouillé
                              </Button>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;