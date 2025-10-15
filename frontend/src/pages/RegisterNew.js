import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Helmet } from 'react-helmet-async';
import { useAuth } from "../contexts/AuthContext";
import PreRegistrationForm from "../components/PreRegistrationForm";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Alert, AlertDescription } from "../components/ui/alert";
import { Checkbox } from "../components/ui/checkbox";
import { motion } from "framer-motion";
import toast from 'react-hot-toast';
import { Mail, Lock, User, Eye, EyeOff, UserPlus, CheckCircle, ArrowLeft } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function RegisterNew() {
  const [step, setStep] = useState('questionnaire'); // 'questionnaire' ou 'register'
  const [preRegData, setPreRegData] = useState(null);
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

  const handlePreRegistrationComplete = (data) => {
    setPreRegData(data);
    setFormData({
      ...formData,
      email: data.email,
      full_name: data.full_name
    });
    setStep('register');
  };

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

      toast.success("Inscription réussie ! Bienvenue !");
      
      // Auto login
      await login(formData.email, formData.password);
      navigate("/dashboard");
      
    } catch (error) {
      console.error("Registration error:", error);
      setError(
        error.response?.data?.detail || 
        "Une erreur est survenue lors de l'inscription. Veuillez réessayer."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Helmet>
        <title>Inscription - Formation Inspecteur Auto</title>
        <meta name="description" content="Inscrivez-vous à la formation d'inspecteur automobile professionnelle" />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          
          {step === 'questionnaire' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-2">
                  Avant de Commencer
                </h1>
                <p className="text-xl text-gray-600">
                  Vérifiez que votre profil correspond à nos critères de formation
                </p>
              </div>
              
              <PreRegistrationForm onComplete={handlePreRegistrationComplete} />
            </motion.div>
          )}

          {step === 'register' && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
              className="max-w-md mx-auto"
            >
              
              <div className="mb-8">
                <Button 
                  variant="ghost" 
                  onClick={() => setStep('questionnaire')}
                  className="mb-4"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Retour au questionnaire
                </Button>
              </div>

              <Card className="shadow-2xl">
                <CardHeader className="text-center space-y-2 pb-6">
                  <div className="flex justify-center mb-4">
                    <div className="bg-green-100 p-3 rounded-full">
                      <CheckCircle className="h-8 w-8 text-green-600" />
                    </div>
                  </div>
                  <CardTitle className="text-3xl font-bold">
                    Profil Validé !
                  </CardTitle>
                  <CardDescription className="text-base">
                    Créez votre compte pour accéder à la formation
                  </CardDescription>
                </CardHeader>

                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    
                    {error && (
                      <Alert variant="destructive">
                        <AlertDescription>{error}</AlertDescription>
                      </Alert>
                    )}

                    <div className="space-y-2">
                      <Label htmlFor="full_name">Nom complet</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="full_name"
                          name="full_name"
                          type="text"
                          value={formData.full_name}
                          onChange={handleChange}
                          required
                          className="pl-10"
                          placeholder="Jean Dupont"
                          disabled
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="email"
                          name="email"
                          type="email"
                          value={formData.email}
                          onChange={handleChange}
                          required
                          className="pl-10"
                          placeholder="jean.dupont@example.com"
                          disabled
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="username">Nom d'utilisateur</Label>
                      <div className="relative">
                        <UserPlus className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="username"
                          name="username"
                          type="text"
                          value={formData.username}
                          onChange={handleChange}
                          required
                          className="pl-10"
                          placeholder="jeandupont"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="password">Mot de passe</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="password"
                          name="password"
                          type={showPassword ? "text" : "password"}
                          value={formData.password}
                          onChange={handleChange}
                          required
                          className="pl-10 pr-10"
                          placeholder="••••••••"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                        >
                          {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                        </button>
                      </div>
                      <p className="text-xs text-gray-500">Minimum 6 caractères</p>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword">Confirmer le mot de passe</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="confirmPassword"
                          name="confirmPassword"
                          type={showConfirmPassword ? "text" : "password"}
                          value={formData.confirmPassword}
                          onChange={handleChange}
                          required
                          className="pl-10 pr-10"
                          placeholder="••••••••"
                        />
                        <button
                          type="button"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                        >
                          {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                        </button>
                      </div>
                    </div>

                    <div className="flex items-start space-x-2 pt-2">
                      <Checkbox
                        id="terms"
                        checked={acceptTerms}
                        onCheckedChange={setAcceptTerms}
                      />
                      <Label 
                        htmlFor="terms" 
                        className="text-sm cursor-pointer leading-relaxed"
                      >
                        J'accepte les{" "}
                        <Link to="/terms" className="text-blue-600 hover:underline">
                          conditions d'utilisation
                        </Link>{" "}
                        et la{" "}
                        <Link to="/privacy" className="text-blue-600 hover:underline">
                          politique de confidentialité
                        </Link>
                      </Label>
                    </div>

                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-6 text-lg"
                    >
                      {isLoading ? (
                        "Création du compte..."
                      ) : (
                        <>
                          <UserPlus className="mr-2 h-5 w-5" />
                          Créer mon compte
                        </>
                      )}
                    </Button>

                    <div className="text-center pt-4">
                      <p className="text-sm text-gray-600">
                        Vous avez déjà un compte ?{" "}
                        <Link 
                          to="/login" 
                          className="font-semibold text-blue-600 hover:text-blue-700 hover:underline"
                        >
                          Se connecter
                        </Link>
                      </p>
                    </div>
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          )}

        </div>
      </div>
    </>
  );
}

export default RegisterNew;
