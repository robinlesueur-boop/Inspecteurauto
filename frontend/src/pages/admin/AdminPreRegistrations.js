import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { Loader2, CheckCircle, XCircle, Eye } from 'lucide-react';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function AdminPreRegistrations() {
  const [questionnaires, setQuestionnaires] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedQuestionnaire, setSelectedQuestionnaire] = useState(null);

  useEffect(() => {
    fetchQuestionnaires();
  }, []);

  const fetchQuestionnaires = async () => {
    try {
      // For now, we'll create a route to get all questionnaires
      const response = await axios.get(`${API}/admin/pre-registrations`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setQuestionnaires(response.data);
    } catch (error) {
      console.error('Error fetching questionnaires:', error);
      toast.error('Erreur lors du chargement');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Questionnaires Pré-inscription</h1>
        <p className="text-gray-600 mt-2">Candidatures en attente de validation (Qualiopi)</p>
      </div>

      {questionnaires.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <p className="text-gray-500">Aucun questionnaire soumis pour le moment</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {questionnaires.map((q) => (
            <Card key={q.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-semibold">{q.full_name}</h3>
                      {q.profile_validated ? (
                        <Badge variant="success" className="bg-green-100 text-green-800">
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Validé
                        </Badge>
                      ) : (
                        <Badge variant="secondary">En attente</Badge>
                      )}
                      {q.has_driving_license && (
                        <Badge variant="outline" className="bg-blue-50 text-blue-700">
                          Permis B ✓
                        </Badge>
                      )}
                    </div>
                    
                    <p className="text-gray-600 mb-2">📧 {q.email}</p>
                    <p className="text-sm text-gray-500">
                      📅 Soumis le {formatDate(q.created_at)}
                    </p>
                    
                    {q.profile_validated && (
                      <div className="mt-3 p-3 bg-green-50 rounded-lg">
                        <p className="text-sm font-semibold text-green-800">
                          Score d'adéquation : {q.validation_score.toFixed(0)}%
                        </p>
                        <p className="text-xs text-green-700 mt-1">
                          ✓ Profil analysé et validé pour la formation
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col gap-2">
                    <Button
                      onClick={() => setSelectedQuestionnaire(selectedQuestionnaire?.id === q.id ? null : q)}
                      variant="outline"
                      size="sm"
                    >
                      <Eye className="h-4 w-4 mr-2" />
                      {selectedQuestionnaire?.id === q.id ? 'Masquer' : 'Détails'}
                    </Button>
                  </div>
                </div>

                {/* Details */}
                {selectedQuestionnaire?.id === q.id && (
                  <div className="mt-6 pt-6 border-t">
                    <h4 className="font-semibold mb-4">Réponses au Questionnaire :</h4>
                    <div className="space-y-3">
                      {Object.entries(q.answers).map(([key, value]) => (
                        <div key={key} className="bg-gray-50 p-3 rounded">
                          <p className="text-sm font-medium text-gray-700">{key} :</p>
                          <p className="text-gray-900">{value}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
