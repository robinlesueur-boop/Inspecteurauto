import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Textarea } from '../../components/ui/textarea';
import { Save, Bot, RefreshCw } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminChatbot() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [config, setConfig] = useState({
    system_prompt: '',
    formation_info: ''
  });

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await axios.get(`${API}/admin/chatbot/config`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setConfig(response.data);
    } catch (error) {
      console.error('Error fetching config:', error);
      toast.error('Erreur lors du chargement de la configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await axios.put(`${API}/admin/chatbot/config`, config, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      toast.success('Configuration du chatbot mise à jour ! Le prompt est maintenant actif.');
    } catch (error) {
      console.error('Error saving:', error);
      toast.error('Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Configuration Chatbot IA - Admin</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                <Bot className="h-8 w-8 mr-3 text-blue-600" />
                Configuration du Chatbot IA
              </h1>
              <p className="text-gray-600 mt-2">
                Personnalisez le comportement et les connaissances de votre assistant virtuel
              </p>
            </div>
          </div>

          {/* Instructions */}
          <Card className="mb-6 bg-blue-50 border-blue-200">
            <CardContent className="p-6">
              <h3 className="font-semibold text-blue-900 mb-3">💡 Comment ça fonctionne ?</h3>
              <ul className="space-y-2 text-sm text-blue-800">
                <li className="flex items-start">
                  <span className="mr-2">1.</span>
                  <span>Modifiez le <strong>Prompt Système</strong> ci-dessous pour définir le rôle et les instructions du chatbot</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">2.</span>
                  <span>Ajoutez toutes les <strong>informations sur votre formation</strong> (prix, durée, modules, etc.)</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">3.</span>
                  <span>Cliquez sur <strong>"Enregistrer"</strong> - le chatbot utilisera immédiatement ces informations</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">4.</span>
                  <span>Testez le chatbot sur le Dashboard pour vérifier ses réponses</span>
                </li>
              </ul>
            </CardContent>
          </Card>

          {/* Prompt Système */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Prompt Système (Instructions pour le Chatbot)</CardTitle>
              <CardDescription>
                Définissez le rôle, le ton et les instructions générales du chatbot. 
                C'est ici que vous "entraînez" son comportement.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                value={config.system_prompt}
                onChange={(e) => setConfig({ ...config, system_prompt: e.target.value })}
                rows={25}
                className="font-mono text-sm"
                placeholder="Tu es un assistant virtuel expert..."
              />
              <div className="text-xs text-gray-500">
                <strong>Astuce :</strong> Soyez précis dans les instructions. Incluez :
                <ul className="list-disc ml-5 mt-1">
                  <li>Le rôle du chatbot</li>
                  <li>Les informations clés sur la formation</li>
                  <li>Le ton à adopter (professionnel, encourageant, etc.)</li>
                  <li>Ce qu'il doit faire et ne pas faire</li>
                  <li>Comment gérer les questions hors sujet</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Exemple de Structure */}
          <Card className="mb-6 bg-gray-50">
            <CardHeader>
              <CardTitle className="text-lg">📝 Exemple de Structure</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="text-xs bg-white p-4 rounded border overflow-auto">
{`Tu es un assistant virtuel pour "Nom de Formation".

INFORMATIONS CLÉS:
- Prix: XXX€
- Durée: XX heures
- Modules: Liste des modules
- Certification: Détails
- Taux de réussite: XX%

MODULES DE FORMATION:
1. Module 1: Description
2. Module 2: Description
...

REVENUS POTENTIELS:
- Information sur les revenus

Tu dois:
1. Répondre clairement en français
2. Être encourageant et positif
3. Dire honnêtement si tu ne sais pas
4. Rediriger vers le support si nécessaire`}
              </pre>
            </CardContent>
          </Card>

          {/* Save Button */}
          <div className="sticky bottom-0 bg-white border-t-2 border-blue-200 p-4 shadow-lg">
            <div className="flex justify-between items-center max-w-5xl mx-auto">
              <div className="text-sm text-gray-600">
                💡 Les modifications seront appliquées immédiatement après sauvegarde
              </div>
              <Button
                onClick={handleSave}
                disabled={saving}
                className="bg-blue-600 hover:bg-blue-700"
                size="lg"
              >
                {saving ? (
                  <>
                    <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                    Sauvegarde...
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4 mr-2" />
                    Enregistrer la Configuration
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default AdminChatbot;
