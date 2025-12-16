import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../App';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const RegisterPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    phone: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return false;
    }
    if (formData.password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    setError('');

    try {
      const registerData = {
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name,
        phone: formData.phone
      };

      const response = await axios.post(`${API}/auth/register`, registerData);
      login(response.data);
      navigate('/dashboard');
    } catch (error) {
      console.error('Register error:', error);
      setError(error.response?.data?.detail || 'Erreur lors de l\'inscription');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        
        {/* Header */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center space-x-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">🚗</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              InspecteurAutomobile.fr
            </span>
          </Link>
          
          <h1 className="text-3xl font-bold text-white mb-2">
            Créer un compte
          </h1>
          <p className="text-slate-300">
            Commencez votre formation d'inspecteur automobile
          </p>
        </div>

        {/* Registration Form */}
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {error && (
              <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 text-red-200 text-center">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Nom complet *
              </label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                className="form-input"
                placeholder="Prénom Nom"
                required
                data-testid="register-name-input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Adresse email *
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="form-input"
                placeholder="votre@email.com"
                required
                data-testid="register-email-input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Téléphone
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="form-input"
                placeholder="+33 6 XX XX XX XX"
                data-testid="register-phone-input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Mot de passe *
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="form-input"
                placeholder="Minimum 6 caractères"
                required
                data-testid="register-password-input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Confirmer le mot de passe *
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="form-input"
                placeholder="Répétez votre mot de passe"
                required
                data-testid="register-confirm-password-input"
              />
            </div>

            <div className="bg-blue-500/20 border border-blue-500/50 rounded-lg p-4">
              <h4 className="text-blue-300 font-medium mb-2">Votre formation inclut :</h4>
              <ul className="text-sm text-blue-200 space-y-1">
                <li>• 9h de formation certifiante</li>
                <li>• Méthodologie méthode d'inspection (200+ points)</li>
                <li>• Certification officielle</li>
                <li>• Ressources téléchargeables</li>
                <li>• Support personnalisé</li>
              </ul>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full justify-center text-lg py-4"
              data-testid="register-submit-button"
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  Création du compte...
                </>
              ) : (
                <>
                  Créer mon compte - 299€
                  <span>🚀</span>
                </>
              )}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-700">
            <div className="text-xs text-slate-400 mb-4">
              En créant un compte, vous acceptez nos{' '}
              <a href="#" className="text-blue-400 hover:text-blue-300">
                Conditions générales
              </a>{' '}
              et notre{' '}
              <a href="#" className="text-blue-400 hover:text-blue-300">
                Politique de confidentialité
              </a>
            </div>
            
            <div className="text-center">
              <p className="text-slate-400">
                Déjà un compte ?{' '}
                <Link 
                  to="/login" 
                  className="text-blue-400 hover:text-blue-300 font-medium"
                >
                  Se connecter
                </Link>
              </p>
            </div>
          </div>
        </div>

        {/* Benefits */}
        <div className="mt-8 text-center">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-400">9h</div>
              <div className="text-xs text-slate-400">Formation</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-400">98%</div>
              <div className="text-xs text-slate-400">Réussite</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-400">300+</div>
              <div className="text-xs text-slate-400">Certifiés</div>
            </div>
          </div>
        </div>

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <Link 
            to="/" 
            className="text-slate-400 hover:text-slate-300 text-sm"
          >
            ← Retour à l'accueil
          </Link>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;