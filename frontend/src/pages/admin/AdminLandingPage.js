import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Save, Eye } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';
import ImageUploader from '../../components/ImageUploader';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminLandingPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [content, setContent] = useState({
    hero_title: '',
    hero_subtitle: '',
    hero_image_url: '',
    stat_graduates: '',
    stat_success_rate: '',
    stat_duration: '',
    stat_rating: '',
    price_amount: '',
    price_description: '',
    cta_primary: '',
    cta_secondary: '',
    feature_1_title: '',
    feature_1_description: '',
    feature_2_title: '',
    feature_2_description: '',
    feature_3_title: '',
    feature_3_description: '',
    feature_4_title: '',
    feature_4_description: '',
    features_image_url: '',
    training_image_url: '',
    social_proof_image_url: ''
  });

  useEffect(() => {
    fetchContent();
  }, []);

  const fetchContent = async () => {
    try {
      const response = await axios.get(`${API}/landing-page/content`);
      setContent(response.data);
    } catch (error) {
      console.error('Error fetching landing page content:', error);
      toast.error('Erreur lors du chargement du contenu');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await axios.put(`${API}/admin/landing-page/content`, content, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      toast.success('Contenu de la landing page mis à jour avec succès !');
    } catch (error) {
      console.error('Error saving content:', error);
      toast.error('Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field, value) => {
    setContent({ ...content, [field]: value });
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
        <title>Modifier Landing Page - Admin</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Modifier la Landing Page</h1>
              <p className="text-gray-600 mt-2">
                Personnalisez les textes affichés sur la page d'accueil
              </p>
            </div>
            <Button
              onClick={() => window.open('/', '_blank')}
              variant="outline"
              className="flex items-center"
            >
              <Eye className="w-4 h-4 mr-2" />
              Prévisualiser
            </Button>
          </div>

          <div className="space-y-6">
            {/* Hero Section */}
            <Card>
              <CardHeader>
                <CardTitle>Section Hero (Haut de page)</CardTitle>
                <CardDescription>
                  Titre et sous-titre principaux de la page d'accueil
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="hero_title">Titre Principal *</Label>
                  <Input
                    id="hero_title"
                    value={content.hero_title}
                    onChange={(e) => handleChange('hero_title', e.target.value)}
                    placeholder="Devenez Inspecteur Automobile Certifié"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="hero_subtitle">Sous-titre *</Label>
                  <Textarea
                    id="hero_subtitle"
                    value={content.hero_subtitle}
                    onChange={(e) => handleChange('hero_subtitle', e.target.value)}
                    rows={3}
                    placeholder="Maîtrisez l'art du diagnostic véhiculaire..."
                  />
                </div>
              </CardContent>
            </Card>

            {/* Images Section */}
            <Card>
              <CardHeader>
                <CardTitle>Images de la Landing Page</CardTitle>
                <CardDescription>
                  URLs des images Unsplash/Pexels affichées sur la page d'accueil
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="hero_image_url">Image Hero (principale)</Label>
                  <Input
                    id="hero_image_url"
                    value={content.hero_image_url}
                    onChange={(e) => handleChange('hero_image_url', e.target.value)}
                    placeholder="https://images.unsplash.com/photo-..."
                  />
                  {content.hero_image_url && (
                    <div className="mt-2">
                      <img 
                        src={content.hero_image_url} 
                        alt="Hero preview" 
                        className="w-full max-w-md h-48 object-cover rounded-lg border"
                      />
                    </div>
                  )}
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="features_image_url">Image Section Fonctionnalités</Label>
                  <Input
                    id="features_image_url"
                    value={content.features_image_url}
                    onChange={(e) => handleChange('features_image_url', e.target.value)}
                    placeholder="https://images.unsplash.com/photo-..."
                  />
                  {content.features_image_url && (
                    <div className="mt-2">
                      <img 
                        src={content.features_image_url} 
                        alt="Features preview" 
                        className="w-full max-w-md h-48 object-cover rounded-lg border"
                      />
                    </div>
                  )}
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="training_image_url">Image Section Formation</Label>
                  <Input
                    id="training_image_url"
                    value={content.training_image_url}
                    onChange={(e) => handleChange('training_image_url', e.target.value)}
                    placeholder="https://images.unsplash.com/photo-..."
                  />
                  {content.training_image_url && (
                    <div className="mt-2">
                      <img 
                        src={content.training_image_url} 
                        alt="Training preview" 
                        className="w-full max-w-md h-48 object-cover rounded-lg border"
                      />
                    </div>
                  )}
                </div>
                
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-blue-900">
                    💡 <strong>Astuce:</strong> Utilisez des images d'Unsplash ou Pexels pour des photos de haute qualité gratuites.
                    Exemple: <code className="text-xs bg-white px-2 py-1 rounded">https://images.unsplash.com/photo-xxx</code>
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Buttons */}
            <Card>
              <CardHeader>
                <CardTitle>Boutons d'Action</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="cta_primary">Bouton Principal</Label>
                    <Input
                      id="cta_primary"
                      value={content.cta_primary}
                      onChange={(e) => handleChange('cta_primary', e.target.value)}
                      placeholder="Commencer la formation"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="cta_secondary">Bouton Secondaire</Label>
                    <Input
                      id="cta_secondary"
                      value={content.cta_secondary}
                      onChange={(e) => handleChange('cta_secondary', e.target.value)}
                      placeholder="Module gratuit"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Statistics */}
            <Card>
              <CardHeader>
                <CardTitle>Statistiques</CardTitle>
                <CardDescription>
                  Les 4 statistiques affichées sous le titre
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="stat_graduates">Diplômés</Label>
                    <Input
                      id="stat_graduates"
                      value={content.stat_graduates}
                      onChange={(e) => handleChange('stat_graduates', e.target.value)}
                      placeholder="1,200+"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="stat_success_rate">Taux de Réussite</Label>
                    <Input
                      id="stat_success_rate"
                      value={content.stat_success_rate}
                      onChange={(e) => handleChange('stat_success_rate', e.target.value)}
                      placeholder="97%"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="stat_duration">Durée de Formation</Label>
                    <Input
                      id="stat_duration"
                      value={content.stat_duration}
                      onChange={(e) => handleChange('stat_duration', e.target.value)}
                      placeholder="11h"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="stat_rating">Note Moyenne</Label>
                    <Input
                      id="stat_rating"
                      value={content.stat_rating}
                      onChange={(e) => handleChange('stat_rating', e.target.value)}
                      placeholder="4.9/5"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Pricing */}
            <Card>
              <CardHeader>
                <CardTitle>Prix</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="price_amount">Montant</Label>
                    <Input
                      id="price_amount"
                      value={content.price_amount}
                      onChange={(e) => handleChange('price_amount', e.target.value)}
                      placeholder="297€"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="price_description">Description du prix</Label>
                    <Input
                      id="price_description"
                      value={content.price_description}
                      onChange={(e) => handleChange('price_description', e.target.value)}
                      placeholder="Formation complète + Certification"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Features */}
            <Card>
              <CardHeader>
                <CardTitle>Fonctionnalités (4 cartes)</CardTitle>
                <CardDescription>
                  Les 4 avantages clés affichés sur la page
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Feature 1 */}
                <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
                  <h4 className="font-semibold text-gray-900">Fonctionnalité 1</h4>
                  <div className="space-y-2">
                    <Label htmlFor="feature_1_title">Titre</Label>
                    <Input
                      id="feature_1_title"
                      value={content.feature_1_title}
                      onChange={(e) => handleChange('feature_1_title', e.target.value)}
                      placeholder="Méthode AutoJust"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="feature_1_description">Description</Label>
                    <Textarea
                      id="feature_1_description"
                      value={content.feature_1_description}
                      onChange={(e) => handleChange('feature_1_description', e.target.value)}
                      rows={2}
                    />
                  </div>
                </div>

                {/* Feature 2 */}
                <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
                  <h4 className="font-semibold text-gray-900">Fonctionnalité 2</h4>
                  <div className="space-y-2">
                    <Label htmlFor="feature_2_title">Titre</Label>
                    <Input
                      id="feature_2_title"
                      value={content.feature_2_title}
                      onChange={(e) => handleChange('feature_2_title', e.target.value)}
                      placeholder="Certification Reconnue"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="feature_2_description">Description</Label>
                    <Textarea
                      id="feature_2_description"
                      value={content.feature_2_description}
                      onChange={(e) => handleChange('feature_2_description', e.target.value)}
                      rows={2}
                    />
                  </div>
                </div>

                {/* Feature 3 */}
                <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
                  <h4 className="font-semibold text-gray-900">Fonctionnalité 3</h4>
                  <div className="space-y-2">
                    <Label htmlFor="feature_3_title">Titre</Label>
                    <Input
                      id="feature_3_title"
                      value={content.feature_3_title}
                      onChange={(e) => handleChange('feature_3_title', e.target.value)}
                      placeholder="Communauté Active"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="feature_3_description">Description</Label>
                    <Textarea
                      id="feature_3_description"
                      value={content.feature_3_description}
                      onChange={(e) => handleChange('feature_3_description', e.target.value)}
                      rows={2}
                    />
                  </div>
                </div>

                {/* Feature 4 */}
                <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
                  <h4 className="font-semibold text-gray-900">Fonctionnalité 4</h4>
                  <div className="space-y-2">
                    <Label htmlFor="feature_4_title">Titre</Label>
                    <Input
                      id="feature_4_title"
                      value={content.feature_4_title}
                      onChange={(e) => handleChange('feature_4_title', e.target.value)}
                      placeholder="Revenus Attractifs"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="feature_4_description">Description</Label>
                    <Textarea
                      id="feature_4_description"
                      value={content.feature_4_description}
                      onChange={(e) => handleChange('feature_4_description', e.target.value)}
                      rows={2}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Save Button */}
            <div className="flex justify-end space-x-4 pb-8">
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
                    Enregistrer les Modifications
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

export default AdminLandingPage;
