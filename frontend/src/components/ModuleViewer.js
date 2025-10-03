import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../App';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ModuleViewer = () => {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchModule();
  }, [moduleId]);

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

  const getModuleImage = (moduleOrder) => {
    const images = [
      "https://images.unsplash.com/photo-1487754180451-c456f719a1fc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85",
      "https://images.unsplash.com/photo-1498887960847-2a5e46312788?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85",
      "https://images.unsplash.com/photo-1606577924006-27d39b132ae2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85",
      "https://images.unsplash.com/photo-1746079074522-2b14240d932c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxjYXIlMjBpbnNwZWN0aW9ufGVufDB8fHx8MTc1ODcxNjI5NXww&ixlib=rb-4.1.0&q=85",
      "https://images.pexels.com/photos/4489749/pexels-photo-4489749.jpeg"
    ];
    return images[(moduleOrder - 1) % images.length];
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
              
              <div className="hidden md:block text-slate-400">
                <span>Module {module.order}</span>
                <span className="mx-2">•</span>
                <span>{module.duration_minutes} min</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link to="/dashboard" className="btn-secondary">
                ← Tableau de bord
              </Link>
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

      <div className="max-w-5xl mx-auto px-6 py-8">
        
        {/* Module Header */}
        <div className="mb-12">
          <div className="flex items-center space-x-4 mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-2xl">{module.order}</span>
            </div>
            <div>
              <h1 className="text-4xl font-bold text-white mb-2" data-testid="module-title">
                {module.title}
              </h1>
              <p className="text-xl text-slate-300">
                {module.description}
              </p>
            </div>
          </div>

          {/* Module Image */}
          <div className="relative mb-8">
            <img 
              src={getModuleImage(module.order)}
              alt={module.title}
              className="w-full h-64 object-cover rounded-2xl shadow-2xl"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/70 via-transparent to-transparent rounded-2xl"></div>
            <div className="absolute bottom-6 left-6 text-white">
              <div className="text-sm opacity-75">Durée estimée</div>
              <div className="text-2xl font-bold">{module.duration_minutes} minutes</div>
            </div>
          </div>
        </div>

        {/* Module Content */}
        <div className="grid lg:grid-cols-3 gap-8">
          
          {/* Main Content */}
          <div className="lg:col-span-2">
            <div className="card">
              <div 
                className="module-content"
                dangerouslySetInnerHTML={{ __html: module.content }}
                data-testid="module-content"
              />
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            {/* Module Info */}
            <div className="card">
              <h3 className="text-lg font-semibold text-white mb-4">
                Informations du module
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-slate-400">Durée</span>
                  <span className="text-white">{module.duration_minutes} min</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Questions quiz</span>
                  <span className="text-white">{module.quiz_questions.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Note de passage</span>
                  <span className="text-white">70%</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <Link
                to={`/quiz/${module.id}`}
                className="btn-primary w-full justify-center"
                data-testid="start-quiz-button"
              >
                Passer le quiz
                <span>→</span>
              </Link>
              
              <button 
                onClick={() => window.print()}
                className="btn-secondary w-full justify-center"
              >
                📄 Imprimer le module
              </button>
            </div>

            {/* Progress Indicator */}
            <div className="card bg-blue-500/10 border-blue-500/30">
              <h4 className="text-blue-300 font-medium mb-3">
                Progression du module
              </h4>
              <div className="space-y-2">
                <div className="flex items-center text-sm">
                  <span className="w-4 h-4 bg-green-500 rounded-full mr-3"></span>
                  <span className="text-slate-300">Contenu consulté</span>
                </div>
                <div className="flex items-center text-sm">
                  <span className="w-4 h-4 bg-slate-600 rounded-full mr-3"></span>
                  <span className="text-slate-400">Quiz à passer</span>
                </div>
              </div>
            </div>

            {/* Tips */}
            <div className="card bg-orange-500/10 border-orange-500/30">
              <h4 className="text-orange-300 font-medium mb-3">
                💡 Conseils de réussite
              </h4>
              <ul className="text-sm text-slate-300 space-y-2">
                <li>• Lisez attentivement tout le contenu</li>
                <li>• Prenez des notes importantes</li>
                <li>• Le quiz nécessite 70% minimum</li>
                <li>• Vous pouvez repasser le quiz si nécessaire</li>
              </ul>
            </div>

            {/* Support */}
            <div className="card">
              <h4 className="text-white font-medium mb-3">
                Besoin d'aide ?
              </h4>
              <p className="text-sm text-slate-400 mb-4">
                Notre équipe est disponible pour vous accompagner.
              </p>
              <a 
                href="mailto:support@inspecteurautomobile.fr"
                className="btn-secondary w-full justify-center text-sm"
              >
                📧 Contacter le support
              </a>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex justify-between items-center">
            <Link 
              to="/dashboard"
              className="btn-secondary"
            >
              ← Retour au tableau de bord
            </Link>
            
            <Link
              to={`/quiz/${module.id}`}
              className="btn-primary"
              data-testid="bottom-quiz-button"
            >
              Continuer vers le quiz
              <span>→</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModuleViewer;