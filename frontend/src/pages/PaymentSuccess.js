import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { CheckCircle, BookOpen, MessageCircle } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function PaymentSuccess() {
  const [searchParams] = useSearchParams();
  const { user, updateUser } = useAuth();
  const sessionId = searchParams.get('session_id');
  const [loading, setLoading] = useState(true);
  const [paymentStatus, setPaymentStatus] = useState(null);

  useEffect(() => {
    if (sessionId && user) {
      checkPaymentStatus();
    }
  }, [sessionId, user]);

  const checkPaymentStatus = async () => {
    try {
      const response = await axios.get(`${API}/payments/status/${sessionId}`);
      setPaymentStatus(response.data);
      
      // Update user status if payment is successful
      if (response.data.payment_status === 'paid') {
        // Refresh user data
        const userResponse = await axios.get(`${API}/auth/me`);
        updateUser(userResponse.data);
      }
    } catch (error) {
      console.error('Error checking payment status:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Vérification du paiement...</p>
        </div>
      </div>
    );
  }

  const isPaymentSuccessful = paymentStatus?.payment_status === 'paid';

  return (
    <>
      <Helmet>
        <title>Paiement {isPaymentSuccessful ? 'Réussi' : 'En cours'} - Formation Inspecteur Automobile</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="text-center shadow-xl">
            <CardHeader className="pb-4">
              <div className="flex justify-center mb-4">
                {isPaymentSuccessful ? (
                  <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="w-12 h-12 text-green-600" />
                  </div>
                ) : (
                  <div className="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center">
                    <div className="animate-spin h-8 w-8 border-2 border-yellow-600 border-t-transparent rounded-full"></div>
                  </div>
                )}
              </div>
              <CardTitle className="text-2xl">
                {isPaymentSuccessful ? 'Paiement Réussi !' : 'Traitement en cours...'}
              </CardTitle>
            </CardHeader>
            
            <CardContent className="space-y-6">
              {isPaymentSuccessful ? (
                <>
                  <p className="text-gray-600 text-lg">
                    Félicitations ! Votre paiement a été traité avec succès. 
                    Vous avez maintenant accès à la formation complète.
                  </p>
                  
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <h3 className="font-semibold text-green-800 mb-2">
                      Vous avez accès à :
                    </h3>
                    <ul className="text-green-700 space-y-1 text-left">
                      <li>✅ 8 modules de formation (11h de contenu)</li>
                      <li>✅ Méthode AutoJust exclusive</li>
                      <li>✅ Certification officielle</li>
                      <li>✅ Forum communauté à vie</li>
                    </ul>
                  </div>
                  
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Link to="/dashboard">
                      <Button className="bg-blue-600 hover:bg-blue-700">
                        <BookOpen className="w-4 h-4 mr-2" />
                        Commencer la Formation
                      </Button>
                    </Link>
                    <Link to="/forum">
                      <Button variant="outline">
                        <MessageCircle className="w-4 h-4 mr-2" />
                        Rejoindre le Forum
                      </Button>
                    </Link>
                  </div>
                </>
              ) : (
                <>
                  <p className="text-gray-600">
                    Votre paiement est en cours de traitement. 
                    Veuillez patienter quelques instants...
                  </p>
                  
                  <Button onClick={checkPaymentStatus} variant="outline">
                    Vérifier à nouveau
                  </Button>
                </>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}

export default PaymentSuccess;