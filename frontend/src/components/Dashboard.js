import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../App';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [modules, setModules] = useState([]);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [modulesResponse, progressResponse] = await Promise.all([
        axios.get(`${API}/modules`),
        axios.get(`${API}/user/progress`)
      ]);
      
      setModules(modulesResponse.data);
      setProgress(progressResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getModuleStatus = (moduleId) => {
    const completed = progress.completed_modules?.includes(moduleId);
    const quizScore = progress.quiz_scores?.[moduleId];
    
    if (completed && quizScore >= 70) {
      return 'completed';
    } else if (quizScore !== undefined && quizScore < 70) {
      return 'failed';
    } else {
      return 'available';
    }
  };

  const getProgressPercentage = () => {
    const totalModules = modules.length;
    const completedCount = progress.completed_modules?.length || 0;
    return totalModules > 0 ? (completedCount / totalModules) * 100 : 0;
  };

  const canAccessModule = (moduleId, moduleOrder) => {
    if (moduleOrder === 1) return true;
    
    const previousModule = modules.find(m => m.order === moduleOrder - 1);
    if (!previousModule) return true;
    
    return getModuleStatus(previousModule.id) === 'completed';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700">
      
      {/* Navigation */}
      <nav className="bg-slate-900/50 backdrop-blur-lg border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">🚗</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                InspecteurAutomobile.fr
              </span>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-slate-300">
                Bonjour, <span className="text-white font-medium">{user?.full_name}</span>
              </div>
              <button 
                onClick={logout} 
                className="btn-secondary"
                data-testid="logout-button"
              >
                Se déconnecter
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        
        {/* Header & Progress */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-6" data-testid="dashboard-title">
            Formation Inspecteur Automobile
          </h1>
          
          {/* Global Progress */}
          <div className="card mb-8">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white">Progression globale</h3>
              <span className="text-2xl font-bold text-blue-400">
                {Math.round(getProgressPercentage())}%
              </span>
            </div>
            
            <div className="progress-bar mb-4">
              <div 
                className="progress-fill" 
                style={{ width: `${getProgressPercentage()}%` }}
              ></div>
            </div>
            
            <div className="flex justify-between text-sm text-slate-400">
              <span>{progress.completed_modules?.length || 0} modules terminés</span>
              <span>{modules.length} modules au total</span>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            <div className="card text-center">
              <div className="text-3xl font-bold text-blue-400 mb-2">
                {progress.completed_modules?.length || 0}
              </div>
              <div className="text-slate-300">Modules terminés</div>
            </div>
            
            <div className="card text-center">
              <div className="text-3xl font-bold text-green-400 mb-2">
                {Object.values(progress.quiz_scores || {}).filter(score => score >= 70).length}
              </div>
              <div className="text-slate-300">Quiz réussis</div>
            </div>
            
            <div className="card text-center">
              <div className="text-3xl font-bold text-orange-400 mb-2">
                {modules.reduce((total, module) => total + module.duration_minutes, 0)} min
              </div>
              <div className="text-slate-300">Durée totale</div>
            </div>
            
            <div className="card text-center">
              <div className="text-3xl font-bold text-purple-400 mb-2">
                {getProgressPercentage() >= 100 ? '🏆' : '📚'}
              </div>
              <div className="text-slate-300">
                {getProgressPercentage() >= 100 ? 'Certifié' : 'En cours'}
              </div>
            </div>
          </div>
        </div>

        {/* Modules List */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-white mb-6">
            Modules de Formation
          </h2>
          
          {modules
            .sort((a, b) => a.order - b.order)
            .map((module) => {
              const status = getModuleStatus(module.id);
              const quizScore = progress.quiz_scores?.[module.id];
              const canAccess = canAccessModule(module.id, module.order);
              
              return (
                <div key={module.id} className="card hover:scale-105 transition-all duration-300">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-4 mb-3">
                        <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                          <span className="text-white font-bold">{module.order}</span>
                        </div>
                        
                        <div className="flex-1">
                          <h3 className="text-xl font-semibold text-white mb-1">
                            {module.title}
                          </h3>
                          <p className="text-slate-300 text-sm">
                            {module.description}
                          </p>
                        </div>

                        <div className="flex items-center space-x-4">
                          <div className="text-sm text-slate-400">
                            {module.duration_minutes} min
                          </div>
                          
                          {status === 'completed' && (
                            <div className="badge badge-success" data-testid={`module-${module.id}-completed-badge`}>
                              ✓ Terminé ({quizScore}%)
                            </div>
                          )}
                          
                          {status === 'failed' && (
                            <div className="badge badge-warning" data-testid={`module-${module.id}-failed-badge`}>
                              ⚠ Échec ({quizScore}%)
                            </div>
                          )}
                          
                          {status === 'available' && canAccess && (
                            <div className="badge badge-info" data-testid={`module-${module.id}-available-badge`}>
                              📚 Disponible
                            </div>
                          )}
                          
                          {!canAccess && (
                            <div className="badge" style={{ background: 'rgba(100, 116, 139, 0.2)', color: '#64748b' }}>
                              🔒 Verrouillé
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Progress for current module */}
                      {status !== 'available' && (
                        <div className="ml-16">
                          <div className="w-full bg-slate-700 rounded-full h-2 mb-2">
                            <div 
                              className={`h-2 rounded-full ${
                                status === 'completed' 
                                  ? 'bg-gradient-to-r from-green-500 to-green-600' 
                                  : 'bg-gradient-to-r from-yellow-500 to-orange-500'
                              }`}
                              style={{ 
                                width: status === 'completed' ? '100%' : '50%' 
                              }}
                            ></div>
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="ml-6 flex space-x-3">
                      {canAccess && (
                        <>
                          <Link
                            to={`/module/${module.id}`}
                            className="btn-primary"
                            data-testid={`module-${module.id}-view-button`}
                          >
                            {status === 'completed' ? 'Revoir' : 'Commencer'}
                          </Link>
                          
                          {status !== 'available' && (
                            <Link
                              to={`/quiz/${module.id}`}
                              className={status === 'completed' ? 'btn-secondary' : 'btn-warning'}
                              data-testid={`module-${module.id}-quiz-button`}
                            >
                              {status === 'completed' ? 'Refaire le quiz' : 'Passer le quiz'}
                            </Link>
                          )}
                        </>
                      )}
                      
                      {!canAccess && (
                        <div className="text-slate-500 text-sm italic py-2 px-4">
                          Terminez le module précédent
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
        </div>

        {/* Final Certification */}
        {getProgressPercentage() >= 100 && (
          <div className="mt-12">
            <div className="card bg-gradient-to-r from-green-500/20 to-blue-500/20 border-green-500/30">
              <div className="text-center">
                <div className="text-6xl mb-4">🏆</div>
                <h3 className="text-2xl font-bold text-white mb-4">
                  Félicitations ! Formation Terminée
                </h3>
                <p className="text-slate-300 mb-6">
                  Vous avez terminé tous les modules avec succès. Votre certification d'Inspecteur Automobile est maintenant disponible.
                </p>
                <button className="btn-success" data-testid="download-certificate-button">
                  Télécharger mon certificat
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Support Section */}
        <div className="mt-12">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  Besoin d'aide ?
                </h3>
                <p className="text-slate-300">
                  Notre équipe est là pour vous accompagner dans votre formation.
                </p>
              </div>
              <div className="flex space-x-4">
                <a 
                  href="mailto:support@inspecteurautomobile.fr"
                  className="btn-secondary"
                >
                  📧 Contact Support
                </a>
                <a 
                  href="#"
                  className="btn-secondary"
                >
                  📚 Documentation
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;