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
  Download,
  AlertCircle,
  Shield
} from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Dashboard() {
  const { user, updateUser } = useAuth();
  const [modules, setModules] = useState([]);
  const [progress, setProgress] = useState([]);
  const [moduleAccess, setModuleAccess] = useState({}); // Nouveau state pour gérer l'accès
  const [loading, setLoading] = useState(true);
  const [purchaseLoading, setPurchaseLoading] = useState(false);
  const [mechanicalAssessmentStatus, setMechanicalAssessmentStatus] = useState(null);
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
      fetchMechanicalAssessmentStatus();
    }
  }, [user]);

  const fetchModules = async () => {
    try {
      const response = await axios.get(`${API}/modules`);
      setModules(response.data);
      calculateStats(response.data, progress);
      
      // Vérifier l'accès pour chaque module
      if (user) {
        await checkModuleAccess(response.data);
      }
    } catch (error) {
      console.error("Error fetching modules:", error);
      toast.error("Erreur lors du chargement des modules");
    } finally {
      setLoading(false);
    }
  };

  const checkModuleAccess = async (moduleList) => {
    const accessMap = {};
    
    // If user is admin, grant access to all modules for preview
    if (user?.is_admin) {
      for (const module of moduleList) {
        accessMap[module.id] = { can_access: true, reason: 'admin_access' };
      }
      setModuleAccess(accessMap);
      return;
    }
    
    for (const module of moduleList) {
      try {
        const response = await axios.get(`${API}/progress/check-access/${module.id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        accessMap[module.id] = response.data;
      } catch (error) {
        // If error occurs, check if module is free
        // Free modules should always be accessible
        if (module.is_free) {
          accessMap[module.id] = { can_access: true, reason: 'free_module' };
        } else {
          accessMap[module.id] = { can_access: false, reason: 'purchase_required' };
        }
      }
    }
    
    setModuleAccess(accessMap);
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

  const fetchMechanicalAssessmentStatus = async () => {
    try {
      const response = await axios.get(`${API}/preliminary-quiz/mechanical-knowledge/status`);
      setMechanicalAssessmentStatus(response.data);
    } catch (error) {
      console.error("Error fetching mechanical assessment status:", error);
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

          {/* Admin Preview Banner */}
          {user?.is_admin && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
              className="mb-6"
            >
              <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <Shield className="h-6 w-6 text-purple-600" />
                  <div>
                    <h3 className="font-semibold text-purple-900">Mode Prévisualisation Administrateur</h3>
                    <p className="text-sm text-purple-700">
                      Tous les modules sont déverrouillés pour vous permettre de prévisualiser le parcours complet de formation.
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

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
                        Accédez à <strong>11 heures de formation</strong> avec la méthode d'inspection professionnelle exclusive, 
                        votre certification officielle et le forum privé des inspecteurs.
                      </p>
                      
                      <div className="space-y-3 mb-6">
                        <div className="flex items-center text-green-700">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          <span>7 modules premium supplémentaires</span>
                        </div>
                        <div className="flex items-center text-green-700">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          <span>Méthode d'inspection propriétaire</span>
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
                        <div className="flex items-center text-green-800 mb-3">
                          <Award className="h-5 w-5 mr-2" />
                          <span className="font-semibold">Félicitations ! Formation terminée</span>
                        </div>
                        <p className="text-green-700 mb-3">
                          Vous avez complété tous les modules. Passez maintenant l'évaluation finale 
                          pour obtenir votre certification officielle !
                        </p>
                        <Link to="/final-evaluation">
                          <Button className="bg-green-600 hover:bg-green-700 text-white">
                            <Trophy className="h-4 w-4 mr-2" />
                            Passer l'Évaluation Finale
                          </Button>
                        </Link>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* AI Chat Helper - Always visible */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="mb-8"
          >
            <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <MessageCircle className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-blue-900 mb-2">
                      🤖 Assistant IA - Aide Instantanée
                    </h3>
                    <p className="text-blue-800 mb-3">
                      Besoin d'aide sur un module ? Une question sur la mécanique ? 
                      Notre assistant IA est là pour vous aider 24h/24 !
                    </p>
                    <p className="text-sm text-blue-700 bg-white rounded px-3 py-2 border border-blue-200">
                      💡 <strong>Regardez en bas à droite de votre écran</strong> - Cliquez sur l'icône bleue 
                      de chat pour poser vos questions !
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Mechanical Knowledge Quiz Reminder */}
          {user?.has_purchased && mechanicalAssessmentStatus && !mechanicalAssessmentStatus.completed && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="mb-8"
            >
              <Card className="bg-yellow-50 border-yellow-200 shadow-lg">
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <AlertCircle className="h-8 w-8 text-yellow-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-yellow-900 mb-2">
                        📝 Évaluation des Connaissances Mécaniques
                      </h3>
                      <p className="text-yellow-800 mb-4">
                        Avant de commencer la formation, nous vous recommandons de passer l'évaluation 
                        des connaissances mécaniques pour personnaliser votre parcours d'apprentissage.
                      </p>
                      <Link to="/mechanical-knowledge-quiz">
                        <Button className="bg-yellow-600 hover:bg-yellow-700 text-white">
                          <BookOpen className="h-4 w-4 mr-2" />
                          Passer l'Évaluation
                        </Button>
                      </Link>
                    </div>
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
                  <Link to="/ressources">
                    <Button variant="outline" className="flex items-center">
                      <BookOpen className="h-4 w-4 mr-2" />
                      Ressources
                    </Button>
                  </Link>
                  <Link to="/chat">
                    <Button variant="outline" className="flex items-center">
                      <MessageCircle className="h-4 w-4 mr-2" />
                      Chat
                    </Button>
                  </Link>
                </div>
              )}
            </div>

            <div className="space-y-4" data-testid="modules-list">
              {modules
                .filter(module => {
                  // Admin can see all modules
                  if (user?.is_admin) {
                    return true;
                  }
                  
                  // Module 2 (Remise à Niveau) should only show if:
                  // 1. User has completed mechanical assessment AND
                  // 2. User needs remedial module (score < 70%)
                  if (module.order_index === 2) {
                    return mechanicalAssessmentStatus?.completed && 
                           mechanicalAssessmentStatus?.needs_remedial_module;
                  }
                  return true;
                })
                .map((module, index) => {
                const isCompleted = isModuleCompleted(module.id);
                const accessInfo = moduleAccess[module.id] || { can_access: false };
                const isAccessible = accessInfo.can_access;
                const blockReason = accessInfo.reason;
                
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
                              
                              {user?.is_admin && accessInfo.reason === 'admin_access' && (
                                <Badge className="bg-purple-100 text-purple-700">
                                  <Shield className="h-3 w-3 mr-1" />
                                  Prévisualisation Admin
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
                              <div className="text-right">
                                <Button disabled variant="outline" className="mb-2">
                                  <Lock className="h-4 w-4 mr-2" />
                                  Verrouillé
                                </Button>
                                {blockReason === 'purchase_required' && (
                                  <p className="text-xs text-gray-500">Achat requis</p>
                                )}
                                {blockReason === 'previous_module_not_completed' && (
                                  <p className="text-xs text-orange-600 font-medium">
                                    ⚠️ Terminez le module précédent
                                  </p>
                                )}
                                {blockReason === 'previous_quiz_not_passed' && (
                                  <p className="text-xs text-red-600 font-medium">
                                    🔒 Réussissez le quiz précédent (80%)
                                  </p>
                                )}
                              </div>
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