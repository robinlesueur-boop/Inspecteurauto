import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { BookOpen, Save, Edit, X, CheckCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';
import MediaUploader from '../../components/MediaUploader';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminModules() {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingModule, setEditingModule] = useState(null);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    content: '',
    duration_minutes: 60,
    is_free: false
  });

  useEffect(() => {
    fetchModules();
  }, []);

  const fetchModules = async () => {
    try {
      const response = await axios.get(`${API}/modules`);
      setModules(response.data);
    } catch (error) {
      console.error('Error fetching modules:', error);
      toast.error('Erreur lors du chargement des modules');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (module) => {
    setEditingModule(module);
    setFormData({
      title: module.title,
      description: module.description,
      content: module.content,
      duration_minutes: module.duration_minutes,
      is_free: module.is_free
    });
  };

  const handleCancel = () => {
    setEditingModule(null);
    setFormData({
      title: '',
      description: '',
      content: '',
      duration_minutes: 60,
      is_free: false
    });
  };

  const handleSave = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      toast.error('Le titre et le contenu sont obligatoires');
      return;
    }

    try {
      setSaving(true);
      
      // Send as JSON body
      const response = await axios.put(`${API}/admin/modules/${editingModule.id}`, {
        title: formData.title,
        description: formData.description,
        content: formData.content,
        duration_minutes: formData.duration_minutes,
        is_free: formData.is_free
      });
      
      console.log('Module update response:', response.data);
      toast.success('Module mis à jour avec succès !');
      
      // Refresh modules list
      await fetchModules();
      handleCancel();
    } catch (error) {
      console.error('Error updating module:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de la mise à jour du module');
    } finally {
      setSaving(false);
    }
  };

  const getWordCount = (text) => {
    return text.trim().split(/\s+/).length;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des modules...</p>
        </div>
      </div>
    );
  }

  if (editingModule) {
    return (
      <>
        <Helmet>
          <title>Éditer Module - Admin</title>
        </Helmet>

        <div className="min-h-screen bg-gray-50 py-8">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Éditer le Module
                </h1>
                <p className="text-gray-600 mt-1">Module {editingModule.order_index}</p>
              </div>
              <Button
                onClick={handleCancel}
                variant="outline"
                className="flex items-center"
              >
                <X className="w-4 h-4 mr-2" />
                Annuler
              </Button>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Informations du Module</CardTitle>
                <CardDescription>
                  Copiez-collez le contenu généré par ChatGPT dans le champ "Contenu"
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-6">
                {/* Title */}
                <div className="space-y-2">
                  <Label htmlFor="title">Titre du Module *</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="Ex: Introduction à l'Inspection Automobile"
                  />
                </div>

                {/* Description */}
                <div className="space-y-2">
                  <Label htmlFor="description">Description courte *</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Description courte du module (1-2 phrases)"
                    rows={3}
                  />
                </div>

                {/* Duration */}
                <div className="space-y-2">
                  <Label htmlFor="duration">Durée (minutes)</Label>
                  <Input
                    id="duration"
                    type="number"
                    value={formData.duration_minutes}
                    onChange={(e) => setFormData({ ...formData, duration_minutes: parseInt(e.target.value) })}
                    min="1"
                  />
                  <p className="text-sm text-gray-500">
                    Durée actuelle: {Math.floor(formData.duration_minutes / 60)}h{formData.duration_minutes % 60}min
                  </p>
                </div>

                {/* Media Uploader */}
                <MediaUploader 
                  onInsert={(htmlCode) => {
                    // Insérer le code HTML à la fin du contenu
                    setFormData({ 
                      ...formData, 
                      content: formData.content + '\n\n' + htmlCode 
                    });
                  }}
                />

                {/* Content */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="content">Contenu du Module *</Label>
                    <span className="text-sm text-gray-500">
                      {getWordCount(formData.content)} mots
                    </span>
                  </div>
                  <Textarea
                    id="content"
                    value={formData.content}
                    onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                    placeholder="Collez ici le contenu généré par ChatGPT...

Vous pouvez utiliser du texte simple ou du HTML.

Exemple:
# Titre
## Sous-titre
- Point 1
- Point 2"
                    rows={25}
                    className="font-mono text-sm"
                  />
                  <p className="text-sm text-gray-500">
                    💡 Astuce: Vous pouvez utiliser du HTML pour la mise en forme (balises &lt;h2&gt;, &lt;p&gt;, &lt;ul&gt;, &lt;strong&gt;, etc.)
                  </p>
                </div>

                {/* Free Module Toggle */}
                <div className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg">
                  <input
                    type="checkbox"
                    id="is_free"
                    checked={formData.is_free}
                    onChange={(e) => setFormData({ ...formData, is_free: e.target.checked })}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <Label htmlFor="is_free" className="cursor-pointer">
                    Module gratuit (accessible sans achat)
                  </Label>
                </div>

                {/* Action Buttons */}
                <div className="flex justify-end space-x-4 pt-4 border-t">
                  <Button
                    onClick={handleCancel}
                    variant="outline"
                    disabled={saving}
                  >
                    Annuler
                  </Button>
                  <Button
                    onClick={handleSave}
                    disabled={saving}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {saving ? (
                      <>
                        <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                        Sauvegarde...
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4 mr-2" />
                        Enregistrer les modifications
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Helmet>
        <title>Gestion des Modules - Admin</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Gestion des Modules</h1>
            <p className="text-gray-600 mt-2">
              Éditez le contenu des modules de formation
            </p>
          </div>

          <div className="grid gap-6">
            {modules.map((module) => {
              const wordCount = getWordCount(module.content);
              
              return (
                <Card key={module.id} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <div className="flex items-center justify-center w-10 h-10 rounded-full bg-blue-100 text-blue-600 font-semibold">
                            {module.order_index}
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
                        
                        <div className="flex items-center space-x-6 mt-4 text-sm text-gray-500">
                          <div className="flex items-center">
                            <BookOpen className="w-4 h-4 mr-1" />
                            {wordCount} mots
                          </div>
                          <div>
                            Durée: {Math.floor(module.duration_minutes / 60)}h{module.duration_minutes % 60}min
                          </div>
                          {module.is_free && (
                            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-medium">
                              Gratuit
                            </span>
                          )}
                        </div>
                      </div>

                      <Button
                        onClick={() => handleEdit(module)}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        <Edit className="w-4 h-4 mr-2" />
                        Éditer
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </div>
    </>
  );
}

export default AdminModules;
