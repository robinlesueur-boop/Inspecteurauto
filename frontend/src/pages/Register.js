import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Helmet } from 'react-helmet-async';
import { useAuth } from "../contexts/AuthContext";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Alert, AlertDescription } from "../components/ui/alert";
import { Checkbox } from "../components/ui/checkbox";
import { motion } from "framer-motion";
import toast from 'react-hot-toast';
import { Mail, Lock, User, Eye, EyeOff, UserPlus, Car, CheckCircle } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Register() {
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    full_name: "",
    password: "",
    confirmPassword: ""
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    // Validations
    if (!acceptTerms) {
      setError("Veuillez accepter les conditions d'utilisation.");
      setIsLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Les mots de passe ne correspondent pas.");
      setIsLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setError("Le mot de passe doit contenir au moins 6 caractères.");
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.post(`${API}/auth/register`, {
        email: formData.email,
        username: formData.username,
        full_name: formData.full_name,
        password: formData.password
      });

      const { access_token, user } = response.data;
      
      // Set authorization header for future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Update auth context
      login(user, access_token);
      
      toast.success(`Bienvenue ${user.full_name} ! Votre compte a été créé avec succès.`);
      
      // Redirect to dashboard
      navigate("/dashboard");
    } catch (error) {
      console.error("Registration error:", error);
      const errorMessage = error.response?.data?.detail || 
        "Erreur lors de l'inscription. Veuillez réessayer.";
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const benefits = [
    "Accès immédiat au module gratuit",
    "Contenu créé par des experts",
    "Communauté de 1200+ membres", 
    "Support prioritaire inclus"
  ];

  return (
    <>
      <Helmet>
        <title>Inscription - Formation Inspecteur Automobile</title>
        <meta name="description" content="Créez votre compte gratuit et commencez votre formation d'inspecteur automobile dès aujourd'hui." />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 py-12 px-4 sm:px-6 lg:px-8">
        {/* Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-600 opacity-20 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-600 opacity-20 rounded-full blur-3xl"></div>
        </div>

        <div className="max-w-6xl mx-auto relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Benefits */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="text-white lg:pr-8"
            >
              <div className="mb-8">
                <div className="flex items-center mb-4">
                  <div className="bg-white p-2 rounded-lg mr-3">
                    <Car className="h-6 w-6 text-blue-600" />
                  </div>
                  <h1 className="text-3xl lg:text-4xl font-bold">Inspecteur Auto</h1>
                </div>
                <h2 className="text-2xl lg:text-3xl font-bold mb-4">
                  Rejoignez la Formation #1 en France
                </h2>
                <p className="text-xl text-blue-100 leading-relaxed">
                  Transformez votre passion automobile en expertise professionnelle 
                  avec notre méthode AutoJust reconnue.
                </p>
              </div>

              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                    className="flex items-center"
                  >
                    <CheckCircle className="h-5 w-5 text-green-400 mr-3 flex-shrink-0" />
                    <span className="text-blue-100">{benefit}</span>
                  </motion.div>
                ))}
              </div>

              <div className="mt-8 p-6 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold">1200+</div>
                    <div className="text-sm text-blue-200">Diplômés</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">97%</div>
                    <div className="text-sm text-blue-200">Succès</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">4.9/5</div>
                    <div className="text-sm text-blue-200">Note</div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Right Column - Form */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Card className="shadow-2xl border-0 bg-white/95 backdrop-blur-sm" data-testid="register-form">
                <CardHeader className="text-center pb-4">
                  <CardTitle className="text-2xl font-bold text-gray-900">
                    Créer mon compte
                  </CardTitle>
                  <CardDescription className="text-gray-600">
                    Commencez votre formation gratuitement
                  </CardDescription>
                </CardHeader>
                
                <CardContent>
                  {error && (
                    <Alert className="mb-6 border-red-200 bg-red-50" data-testid="error-alert">
                      <AlertDescription className="text-red-700">
                        {error}
                      </AlertDescription>
                    </Alert>
                  )}

                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="full_name" className="text-gray-700 font-medium">Nom complet</Label>
                        <div className="relative">
                          <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                          <Input
                            id="full_name"
                            name="full_name"
                            type="text"
                            placeholder="Jean Dupont"
                            value={formData.full_name}
                            onChange={handleChange}
                            className="pl-10 h-11"
                            required
                            data-testid="fullname-input"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="username" className="text-gray-700 font-medium">Nom d'utilisateur</Label>
                        <div className="relative">
                          <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                          <Input
                            id="username"
                            name="username"
                            type="text"
                            placeholder="jean_dupont"
                            value={formData.username}
                            onChange={handleChange}
                            className="pl-10 h-11"
                            required
                            data-testid="username-input"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="email" className="text-gray-700 font-medium">Adresse email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <Input
                          id="email"
                          name="email"
                          type="email"
                          placeholder="jean@example.com"
                          value={formData.email}
                          onChange={handleChange}
                          className="pl-10 h-11"
                          required
                          data-testid="email-input"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="password" className="text-gray-700 font-medium">Mot de passe</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <Input
                          id="password"
                          name="password"
                          type={showPassword ? "text" : "password"}
                          placeholder="Minimum 6 caractères"
                          value={formData.password}
                          onChange={handleChange}
                          className="pl-10 pr-12 h-11"
                          required
                          data-testid="password-input"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                          data-testid="toggle-password"
                        >
                          {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword" className="text-gray-700 font-medium">Confirmer le mot de passe</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <Input
                          id="confirmPassword"
                          name="confirmPassword"
                          type={showConfirmPassword ? "text" : "password"}
                          placeholder="Confirmez votre mot de passe"
                          value={formData.confirmPassword}
                          onChange={handleChange}
                          className="pl-10 pr-12 h-11"
                          required
                          data-testid="confirm-password-input"
                        />
                        <button
                          type="button"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                          data-testid="toggle-confirm-password"
                        >
                          {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </button>
                      </div>
                    </div>

                    <div className="flex items-start space-x-3 py-3">
                      <Checkbox
                        id="terms"
                        checked={acceptTerms}
                        onCheckedChange={setAcceptTerms}
                        data-testid="terms-checkbox"
                      />
                      <div className="text-sm">
                        <label htmlFor="terms" className="text-gray-700 leading-relaxed">
                          J'accepte les{" "}
                          <a href="#" className="text-blue-600 hover:underline">
                            conditions d'utilisation
                          </a>{" "}
                          et la{" "}
                          <a href="#" className="text-blue-600 hover:underline">
                            politique de confidentialité
                          </a>
                        </label>
                      </div>
                    </div>

                    <Button 
                      type="submit" 
                      className="w-full bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white h-12 text-lg font-semibold shadow-lg"
                      disabled={isLoading}
                      data-testid="register-submit-button"
                    >
                      {isLoading ? (
                        <div className="animate-spin h-5 w-5 mr-2 border-2 border-white border-t-transparent rounded-full"></div>
                      ) : (
                        <UserPlus className="mr-2 h-5 w-5" />
                      )}
                      {isLoading ? "Création..." : "Créer mon compte gratuit"}
                    </Button>
                  </form>

                  <div className="mt-6 text-center">
                    <p className="text-sm text-gray-600">
                      Déjà inscrit ?{" "}
                      <Link 
                        to="/login" 
                        className="font-semibold text-blue-600 hover:text-blue-500"
                        data-testid="login-link"
                      >
                        Connectez-vous ici
                      </Link>
                    </p>
                  </div>

                  <div className="mt-6 pt-6 border-t text-center">
                    <p className="text-xs text-gray-500">
                      🔒 Vos données sont sécurisées et ne seront jamais partagées
                    </p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Register;