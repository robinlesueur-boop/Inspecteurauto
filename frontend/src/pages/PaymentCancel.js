import React from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { XCircle, ArrowLeft, CreditCard } from 'lucide-react';

function PaymentCancel() {
  return (
    <>
      <Helmet>
        <title>Paiement Annulé - Formation Inspecteur Automobile</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="text-center shadow-xl">
            <CardHeader className="pb-4">
              <div className="flex justify-center mb-4">
                <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center">
                  <XCircle className="w-12 h-12 text-red-600" />
                </div>
              </div>
              <CardTitle className="text-2xl text-gray-900">
                Paiement Annulé
              </CardTitle>
            </CardHeader>
            
            <CardContent className="space-y-6">
              <p className="text-gray-600 text-lg">
                Votre paiement a été annulé. Aucun montant n'a été débité de votre compte.
              </p>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-blue-800 mb-2">
                  Besoin d'aide ?
                </h3>
                <p className="text-blue-700 text-sm">
                  Si vous rencontrez des difficultés avec le paiement, 
                  n'hésitez pas à nous contacter à contact@inspecteur-auto.fr
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/dashboard">
                  <Button variant="outline">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Retour au Dashboard
                  </Button>
                </Link>
                <Link to="/dashboard">
                  <Button className="bg-blue-600 hover:bg-blue-700">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Réessayer le Paiement
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}

export default PaymentCancel;