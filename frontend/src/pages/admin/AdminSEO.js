import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Helmet } from 'react-helmet-async';
import { 
  Plus, 
  Edit, 
  Trash2, 
  Eye, 
  EyeOff, 
  Search,
  FileText,
  Globe,
  CheckCircle,
  AlertCircle,
  ArrowLeft,
  Save,
  X,
  ChevronDown,
  ChevronUp,
  Copy,
  ExternalLink
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Categories pour organiser les pages SEO
const SEO_CATEGORIES = [
  { value: 'formation', label: 'Formation & Carrière' },
  { value: 'diagnostic', label: 'Diagnostic Technique' },
  { value: 'carrosserie', label: 'Carrosserie & Inspection' },
  { value: 'revenus', label: 'Métier & Revenus' },
  { value: 'geo', label: 'Géolocalisation' },
  { value: 'marque', label: 'Par Marque' },
  { value: 'comparaison', label: 'Comparaisons' },
  { value: 'temoignage', label: 'Témoignages' },
  { value: 'general', label: 'Général' }
];

// Template de section vide
const emptySection = {
  title: '',
  content: [''],
  list: []
};

// Template de FAQ vide
const emptyFaq = {
  question: '',
  answer: ''
};

function AdminSEO() {
  const [pages, setPages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [showEditor, setShowEditor] = useState(false);
  const [editingPage, setEditingPage] = useState(null);
  const [saving, setSaving] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    slug: '',
    title: '',
    meta_title: '',
    meta_description: '',
    meta_keywords: '',
    h1: '',
    category: 'general',
    introduction: '',
    sections: [{ ...emptySection }],
    faq: [],
    cta_title: 'Lancez Votre Nouvelle Carrière',
    cta_description: 'Rejoignez les 500+ inspecteurs formés par nos experts.',
    cta_button_text: "S'inscrire",
    cta_button_url: '/register',
    is_published: false
  });

  useEffect(() => {
    fetchPages();
  }, []);

  const fetchPages = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/admin/seo-pages`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPages(response.data);
    } catch (error) {
      console.error('Error fetching SEO pages:', error);
      toast.error('Erreur lors du chargement des pages');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNew = () => {
    setEditingPage(null);
    setFormData({
      slug: '',
      title: '',
      meta_title: '',
      meta_description: '',
      meta_keywords: '',
      h1: '',
      category: 'general',
      introduction: '',
      sections: [{ title: '', content: [''], list: [] }],
      faq: [],
      cta_title: 'Lancez Votre Nouvelle Carrière',
      cta_description: 'Rejoignez les 500+ inspecteurs formés par nos experts.',
      cta_button_text: "S'inscrire",
      cta_button_url: '/register',
      is_published: false
    });
    setShowEditor(true);
  };

  const handleEdit = async (pageId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/admin/seo-pages/${pageId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEditingPage(response.data);
      setFormData({
        ...response.data,
        sections: response.data.sections?.length > 0 ? response.data.sections : [{ title: '', content: [''], list: [] }],
        faq: response.data.faq || []
      });
      setShowEditor(true);
    } catch (error) {
      console.error('Error fetching page:', error);
      toast.error('Erreur lors du chargement de la page');
    }
  };

  const handleSave = async () => {
    // Validation
    if (!formData.slug || !formData.title || !formData.meta_title || !formData.meta_description || !formData.h1) {
      toast.error('Veuillez remplir tous les champs obligatoires');
      return;
    }

    setSaving(true);
    try {
      const token = localStorage.getItem('token');
      
      // Clean up empty sections and FAQ
      const cleanedData = {
        ...formData,
        sections: formData.sections.filter(s => s.title || s.content.some(c => c)),
        faq: formData.faq.filter(f => f.question && f.answer)
      };

      if (editingPage) {
        await axios.put(`${API}/admin/seo-pages/${editingPage.id}`, cleanedData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Page mise à jour avec succès');
      } else {
        await axios.post(`${API}/admin/seo-pages`, cleanedData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Page créée avec succès');
      }
      
      setShowEditor(false);
      fetchPages();
    } catch (error) {
      console.error('Error saving page:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (pageId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette page ?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API}/admin/seo-pages/${pageId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Page supprimée');
      fetchPages();
    } catch (error) {
      console.error('Error deleting page:', error);
      toast.error('Erreur lors de la suppression');
    }
  };

  const handleTogglePublish = async (pageId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.patch(`${API}/admin/seo-pages/${pageId}/publish`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success(response.data.message);
      fetchPages();
    } catch (error) {
      console.error('Error toggling publish:', error);
      toast.error('Erreur lors de la publication');
    }
  };

  // Generate slug from title
  const generateSlug = (title) => {
    return title
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');
  };

  // Section management
  const addSection = () => {
    setFormData({
      ...formData,
      sections: [...formData.sections, { title: '', content: [''], list: [] }]
    });
  };

  const removeSection = (index) => {
    const newSections = formData.sections.filter((_, i) => i !== index);
    setFormData({ ...formData, sections: newSections.length > 0 ? newSections : [{ title: '', content: [''], list: [] }] });
  };

  const updateSection = (index, field, value) => {
    const newSections = [...formData.sections];
    newSections[index] = { ...newSections[index], [field]: value };
    setFormData({ ...formData, sections: newSections });
  };

  const addParagraph = (sectionIndex) => {
    const newSections = [...formData.sections];
    newSections[sectionIndex].content.push('');
    setFormData({ ...formData, sections: newSections });
  };

  const updateParagraph = (sectionIndex, paragraphIndex, value) => {
    const newSections = [...formData.sections];
    newSections[sectionIndex].content[paragraphIndex] = value;
    setFormData({ ...formData, sections: newSections });
  };

  const removeParagraph = (sectionIndex, paragraphIndex) => {
    const newSections = [...formData.sections];
    newSections[sectionIndex].content = newSections[sectionIndex].content.filter((_, i) => i !== paragraphIndex);
    if (newSections[sectionIndex].content.length === 0) {
      newSections[sectionIndex].content = [''];
    }
    setFormData({ ...formData, sections: newSections });
  };

  const updateSectionList = (sectionIndex, listText) => {
    const newSections = [...formData.sections];
    newSections[sectionIndex].list = listText.split('\n').filter(item => item.trim());
    setFormData({ ...formData, sections: newSections });
  };

  // FAQ management
  const addFaq = () => {
    setFormData({
      ...formData,
      faq: [...formData.faq, { question: '', answer: '' }]
    });
  };

  const removeFaq = (index) => {
    const newFaq = formData.faq.filter((_, i) => i !== index);
    setFormData({ ...formData, faq: newFaq });
  };

  const updateFaq = (index, field, value) => {
    const newFaq = [...formData.faq];
    newFaq[index] = { ...newFaq[index], [field]: value };
    setFormData({ ...formData, faq: newFaq });
  };

  // Filter pages
  const filteredPages = pages.filter(page => {
    const matchesSearch = page.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         page.slug.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === 'all' || page.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  // Character counters for SEO fields
  const getCharCountColor = (current, min, max) => {
    if (current < min) return 'text-orange-500';
    if (current > max) return 'text-red-500';
    return 'text-green-500';
  };

  if (showEditor) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <Helmet>
          <title>{editingPage ? 'Modifier' : 'Créer'} une Page SEO | Admin</title>
        </Helmet>

        <div className="max-w-5xl mx-auto px-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <Button variant="ghost" onClick={() => setShowEditor(false)}>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Retour
              </Button>
              <h1 className="text-2xl font-bold text-gray-900">
                {editingPage ? 'Modifier la Page SEO' : 'Nouvelle Page SEO'}
              </h1>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setShowEditor(false)}>
                Annuler
              </Button>
              <Button onClick={handleSave} disabled={saving}>
                <Save className="h-4 w-4 mr-2" />
                {saving ? 'Enregistrement...' : 'Enregistrer'}
              </Button>
            </div>
          </div>

          {/* SEO Score Indicator */}
          <Card className="mb-6 bg-blue-50 border-blue-200">
            <CardContent className="py-4">
              <div className="flex items-center gap-4">
                <Globe className="h-8 w-8 text-blue-600" />
                <div>
                  <h3 className="font-semibold text-blue-900">Optimisation SEO</h3>
                  <p className="text-sm text-blue-700">
                    Remplissez tous les champs pour maximiser votre référencement Google
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Form */}
          <div className="space-y-6">
            {/* Basic Info */}
            <Card>
              <CardHeader>
                <CardTitle>Informations de Base</CardTitle>
                <CardDescription>URL et titre de la page</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Titre de la Page *
                    </label>
                    <input
                      type="text"
                      value={formData.title}
                      onChange={(e) => {
                        setFormData({ 
                          ...formData, 
                          title: e.target.value,
                          slug: formData.slug || generateSlug(e.target.value)
                        });
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Formation Inspecteur Automobile Bordeaux"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Slug URL *
                    </label>
                    <div className="flex">
                      <span className="inline-flex items-center px-3 text-sm text-gray-500 bg-gray-100 border border-r-0 border-gray-300 rounded-l-lg">
                        /seo/
                      </span>
                      <input
                        type="text"
                        value={formData.slug}
                        onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-r-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="formation-inspecteur-automobile-bordeaux"
                      />
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Catégorie
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    {SEO_CATEGORIES.map(cat => (
                      <option key={cat.value} value={cat.value}>{cat.label}</option>
                    ))}
                  </select>
                </div>
              </CardContent>
            </Card>

            {/* SEO Meta Tags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" />
                  Meta Tags SEO
                </CardTitle>
                <CardDescription>Ces informations apparaissent dans les résultats Google</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Meta Title * <span className={`text-xs ${getCharCountColor(formData.meta_title.length, 50, 60)}`}>
                      ({formData.meta_title.length}/60 caractères - idéal: 50-60)
                    </span>
                  </label>
                  <input
                    type="text"
                    value={formData.meta_title}
                    onChange={(e) => setFormData({ ...formData, meta_title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Formation Inspecteur Auto Bordeaux | Certification 2024"
                    maxLength={70}
                  />
                  <p className="text-xs text-gray-500 mt-1">Titre affiché dans les résultats Google</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Meta Description * <span className={`text-xs ${getCharCountColor(formData.meta_description.length, 150, 160)}`}>
                      ({formData.meta_description.length}/160 caractères - idéal: 150-160)
                    </span>
                  </label>
                  <textarea
                    value={formData.meta_description}
                    onChange={(e) => setFormData({ ...formData, meta_description: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Devenez inspecteur automobile certifié à Bordeaux. Formation 100% en ligne, certification reconnue, support 7j/7. Inscriptions ouvertes."
                    maxLength={170}
                  />
                  <p className="text-xs text-gray-500 mt-1">Description affichée sous le titre dans Google</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Mots-clés (séparés par des virgules)
                  </label>
                  <input
                    type="text"
                    value={formData.meta_keywords}
                    onChange={(e) => setFormData({ ...formData, meta_keywords: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="formation inspecteur auto bordeaux, certification automobile, diagnostic véhicule"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Content H1 & Introduction */}
            <Card>
              <CardHeader>
                <CardTitle>Contenu Principal</CardTitle>
                <CardDescription>Titre H1 et introduction de la page</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Titre H1 * (visible sur la page)
                  </label>
                  <input
                    type="text"
                    value={formData.h1}
                    onChange={(e) => setFormData({ ...formData, h1: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Formation Inspecteur Automobile à Bordeaux : Devenez Expert Certifié"
                  />
                  <p className="text-xs text-gray-500 mt-1">Le titre principal affiché en haut de la page</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Introduction (paragraphe d'accroche)
                  </label>
                  <textarea
                    value={formData.introduction}
                    onChange={(e) => setFormData({ ...formData, introduction: e.target.value })}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Vous habitez Bordeaux ou la région Aquitaine et souhaitez devenir inspecteur automobile ? Notre formation 100% en ligne vous permet de vous former et de lancer votre activité..."
                  />
                </div>
              </CardContent>
            </Card>

            {/* Sections */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Sections de Contenu (H2)</span>
                  <Button variant="outline" size="sm" onClick={addSection}>
                    <Plus className="h-4 w-4 mr-1" />
                    Ajouter Section
                  </Button>
                </CardTitle>
                <CardDescription>Organisez votre contenu en sections avec titres H2</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {formData.sections.map((section, sectionIndex) => (
                  <div key={sectionIndex} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                    <div className="flex items-center justify-between mb-3">
                      <Badge variant="outline">Section {sectionIndex + 1}</Badge>
                      {formData.sections.length > 1 && (
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          onClick={() => removeSection(sectionIndex)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                    
                    <div className="space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Titre H2
                        </label>
                        <input
                          type="text"
                          value={section.title}
                          onChange={(e) => updateSection(sectionIndex, 'title', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          placeholder="Pourquoi Exercer à Bordeaux ?"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Paragraphes
                        </label>
                        {section.content.map((paragraph, pIndex) => (
                          <div key={pIndex} className="flex gap-2 mb-2">
                            <textarea
                              value={paragraph}
                              onChange={(e) => updateParagraph(sectionIndex, pIndex, e.target.value)}
                              rows={3}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                              placeholder="Contenu du paragraphe..."
                            />
                            <div className="flex flex-col gap-1">
                              {section.content.length > 1 && (
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => removeParagraph(sectionIndex, pIndex)}
                                  className="text-red-500"
                                >
                                  <X className="h-4 w-4" />
                                </Button>
                              )}
                            </div>
                          </div>
                        ))}
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          onClick={() => addParagraph(sectionIndex)}
                          className="text-blue-600"
                        >
                          <Plus className="h-4 w-4 mr-1" />
                          Ajouter paragraphe
                        </Button>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Liste à puces (une par ligne)
                        </label>
                        <textarea
                          value={section.list?.join('\n') || ''}
                          onChange={(e) => updateSectionList(sectionIndex, e.target.value)}
                          rows={4}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          placeholder="Point 1&#10;Point 2&#10;Point 3"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* FAQ */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>FAQ (Questions Fréquentes)</span>
                  <Button variant="outline" size="sm" onClick={addFaq}>
                    <Plus className="h-4 w-4 mr-1" />
                    Ajouter FAQ
                  </Button>
                </CardTitle>
                <CardDescription>Les FAQ améliorent le SEO avec le schema markup</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {formData.faq.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">Aucune FAQ. Cliquez sur "Ajouter FAQ" pour commencer.</p>
                ) : (
                  formData.faq.map((faq, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                      <div className="flex items-center justify-between mb-3">
                        <Badge variant="outline">FAQ {index + 1}</Badge>
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          onClick={() => removeFaq(index)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                      <div className="space-y-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Question</label>
                          <input
                            type="text"
                            value={faq.question}
                            onChange={(e) => updateFaq(index, 'question', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="Comment se déroule la formation ?"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Réponse</label>
                          <textarea
                            value={faq.answer}
                            onChange={(e) => updateFaq(index, 'answer', e.target.value)}
                            rows={3}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="La formation se déroule entièrement en ligne..."
                          />
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </CardContent>
            </Card>

            {/* CTA */}
            <Card>
              <CardHeader>
                <CardTitle>Call-to-Action (CTA)</CardTitle>
                <CardDescription>Le bloc d'appel à l'action en bas de page</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Titre CTA</label>
                    <input
                      type="text"
                      value={formData.cta_title}
                      onChange={(e) => setFormData({ ...formData, cta_title: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Lancez Votre Nouvelle Carrière"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Texte du Bouton</label>
                    <input
                      type="text"
                      value={formData.cta_button_text}
                      onChange={(e) => setFormData({ ...formData, cta_button_text: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="S'inscrire Maintenant"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description CTA</label>
                  <input
                    type="text"
                    value={formData.cta_description}
                    onChange={(e) => setFormData({ ...formData, cta_description: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Formation complète à 297€ - Paiement en 4x sans frais"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">URL du Bouton</label>
                  <input
                    type="text"
                    value={formData.cta_button_url}
                    onChange={(e) => setFormData({ ...formData, cta_button_url: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="/register"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Publish Status */}
            <Card>
              <CardContent className="py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {formData.is_published ? (
                      <CheckCircle className="h-6 w-6 text-green-500" />
                    ) : (
                      <AlertCircle className="h-6 w-6 text-orange-500" />
                    )}
                    <div>
                      <p className="font-medium">
                        {formData.is_published ? 'Page publiée' : 'Brouillon'}
                      </p>
                      <p className="text-sm text-gray-500">
                        {formData.is_published 
                          ? 'Cette page est visible publiquement' 
                          : 'Cette page n\'est pas encore visible'}
                      </p>
                    </div>
                  </div>
                  <Button
                    variant={formData.is_published ? "outline" : "default"}
                    onClick={() => setFormData({ ...formData, is_published: !formData.is_published })}
                  >
                    {formData.is_published ? (
                      <>
                        <EyeOff className="h-4 w-4 mr-2" />
                        Dépublier
                      </>
                    ) : (
                      <>
                        <Eye className="h-4 w-4 mr-2" />
                        Publier
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Save Button */}
            <div className="flex justify-end gap-2 pb-8">
              <Button variant="outline" onClick={() => setShowEditor(false)}>
                Annuler
              </Button>
              <Button onClick={handleSave} disabled={saving} size="lg">
                <Save className="h-4 w-4 mr-2" />
                {saving ? 'Enregistrement...' : 'Enregistrer la Page'}
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // List View
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <Helmet>
        <title>Gestion SEO | Admin Inspecteur Auto</title>
      </Helmet>

      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
          <div>
            <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
              <Link to="/admin" className="hover:text-blue-600">Admin</Link>
              <span>/</span>
              <span>Pages SEO</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-900">Gestion des Pages SEO</h1>
            <p className="text-gray-600 mt-1">
              Créez et gérez vos pages optimisées pour le référencement Google
            </p>
          </div>
          <Button onClick={handleCreateNew} size="lg">
            <Plus className="h-5 w-5 mr-2" />
            Nouvelle Page SEO
          </Button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Pages</p>
                  <p className="text-2xl font-bold">{pages.length}</p>
                </div>
                <FileText className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Publiées</p>
                  <p className="text-2xl font-bold text-green-600">
                    {pages.filter(p => p.is_published).length}
                  </p>
                </div>
                <Eye className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Brouillons</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {pages.filter(p => !p.is_published).length}
                  </p>
                </div>
                <EyeOff className="h-8 w-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Objectif</p>
                  <p className="text-2xl font-bold">100</p>
                </div>
                <Globe className="h-8 w-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="py-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Rechercher une page..."
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">Toutes les catégories</option>
                {SEO_CATEGORIES.map(cat => (
                  <option key={cat.value} value={cat.value}>{cat.label}</option>
                ))}
              </select>
            </div>
          </CardContent>
        </Card>

        {/* Pages List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-500">Chargement...</p>
          </div>
        ) : filteredPages.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {pages.length === 0 ? 'Aucune page SEO' : 'Aucun résultat'}
              </h3>
              <p className="text-gray-500 mb-4">
                {pages.length === 0 
                  ? 'Créez votre première page SEO pour améliorer votre référencement'
                  : 'Essayez de modifier vos filtres de recherche'}
              </p>
              {pages.length === 0 && (
                <Button onClick={handleCreateNew}>
                  <Plus className="h-4 w-4 mr-2" />
                  Créer une Page
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredPages.map(page => (
              <Card key={page.id} className="hover:shadow-md transition-shadow">
                <CardContent className="py-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-semibold text-gray-900 truncate">
                          {page.title}
                        </h3>
                        <Badge variant={page.is_published ? "default" : "secondary"}>
                          {page.is_published ? 'Publié' : 'Brouillon'}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-500 mb-2 truncate">
                        /seo/{page.slug}
                      </p>
                      <div className="flex items-center gap-4 text-xs text-gray-400">
                        <span className="bg-gray-100 px-2 py-1 rounded">
                          {SEO_CATEGORIES.find(c => c.value === page.category)?.label || page.category}
                        </span>
                        <span>
                          Créé le {new Date(page.created_at).toLocaleDateString('fr-FR')}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 ml-4">
                      {page.is_published && (
                        <a
                          href={`/seo/${page.slug}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                          title="Voir la page"
                        >
                          <ExternalLink className="h-4 w-4" />
                        </a>
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleTogglePublish(page.id)}
                        title={page.is_published ? 'Dépublier' : 'Publier'}
                      >
                        {page.is_published ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleEdit(page.id)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(page.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Info Box */}
        <Card className="mt-8 bg-blue-50 border-blue-200">
          <CardContent className="py-4">
            <div className="flex items-start gap-4">
              <Globe className="h-6 w-6 text-blue-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-blue-900 mb-1">Conseils SEO</h3>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Le meta title doit faire entre 50-60 caractères</li>
                  <li>• La meta description doit faire entre 150-160 caractères</li>
                  <li>• Utilisez votre mot-clé principal dans le H1 et le premier paragraphe</li>
                  <li>• Ajoutez des FAQ pour améliorer le référencement (rich snippets)</li>
                  <li>• Visez 1000-2000 mots de contenu par page</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default AdminSEO;
