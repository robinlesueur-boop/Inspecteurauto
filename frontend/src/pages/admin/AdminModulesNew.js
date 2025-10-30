import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { BookOpen, Save, Edit, X, CheckCircle, Plus, Trash2, HelpCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';
import MediaUploader from '../../components/MediaUploader';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminModulesNew() {
  const [modules, setModules] = useState([]);
  const [quizzes, setQuizzes] = useState({});
  const [loading, setLoading] = useState(true);
  const [editingModule, setEditingModule] = useState(null);
  const [editingQuiz, setEditingQuiz] = useState(null);
  const [isCreatingNew, setIsCreatingNew] = useState(false);
  const [saving, setSaving] = useState(false);
  const [viewMode, setViewMode] = useState('modules'); // 'modules' or 'quiz'
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    content: '',
    duration_minutes: 60,
    is_free: false
  });

  const [quizFormData, setQuizFormData] = useState({
    title: '',
    description: '',
    passing_score: 80,
    questions: []
  });

  useEffect(() => {
    fetchModules();
  }, []);

  const fetchModules = async () => {
    try {
      const response = await axios.get(`${API}/modules`);
      setModules(response.data);
      
      // Fetch quizzes for each module
      for (const module of response.data) {
        await fetchQuizForModule(module.id);
      }
    } catch (error) {
      console.error('Error fetching modules:', error);
      toast.error('Erreur lors du chargement des modules');
    } finally {
      setLoading(false);
    }
  };

  const fetchQuizForModule = async (moduleId) => {
    try {
      const response = await axios.get(`${API}/quizzes/module/${moduleId}`);
      setQuizzes(prev => ({ ...prev, [moduleId]: response.data }));
    } catch (error) {
      // Quiz doesn't exist yet
      setQuizzes(prev => ({ ...prev, [moduleId]: null }));
    }
  };

  const handleCreateNew = () => {
    setIsCreatingNew(true);
    setEditingModule(null);
    setFormData({
      title: '',
      description: '',
      content: '',
      duration_minutes: 60,
      is_free: false
    });
    setViewMode('modules');
  };

  const handleEdit = (module) => {
    setIsCreatingNew(false);
    setEditingModule(module);
    setFormData({
      title: module.title,
      description: module.description,
      content: module.content,
      duration_minutes: module.duration_minutes,
      is_free: module.is_free
    });
    setViewMode('modules');
  };

  const handleEditQuiz = (moduleId) => {
    const module = modules.find(m => m.id === moduleId);
    const quiz = quizzes[moduleId];
    
    setEditingQuiz(moduleId);
    setEditingModule(module);
    
    if (quiz) {
      setQuizFormData({
        title: quiz.title,
        description: quiz.description || '',
        passing_score: quiz.passing_score,
        questions: quiz.questions || []
      });
    } else {
      // Creating new quiz
      setQuizFormData({
        title: `Quiz - ${module.title}`,
        description: '',
        passing_score: 80,
        questions: [
          {
            id: `q${Date.now()}`,
            question: '',
            options: ['', '', '', ''],
            correct_answer: 0,
            explanation: ''
          }
        ]
      });
    }
    setViewMode('quiz');
  };

  const handleCancel = () => {
    setIsCreatingNew(false);
    setEditingModule(null);
    setEditingQuiz(null);
    setFormData({
      title: '',
      description: '',
      content: '',
      duration_minutes: 60,
      is_free: false
    });
    setQuizFormData({
      title: '',
      description: '',
      passing_score: 80,
      questions: []
    });
  };

  const handleSaveModule = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      toast.error('Le titre et le contenu sont obligatoires');
      return;
    }

    try {
      setSaving(true);
      
      if (isCreatingNew) {
        // Create new module
        const response = await axios.post(`${API}/admin/modules`, {
          title: formData.title,
          description: formData.description,
          content: formData.content,
          duration_minutes: formData.duration_minutes,
          is_free: formData.is_free
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        
        toast.success('Module créé avec succès !');
      } else {
        // Update existing module
        await axios.put(`${API}/admin/modules/${editingModule.id}`, {
          title: formData.title,
          description: formData.description,
          content: formData.content,
          duration_minutes: formData.duration_minutes,
          is_free: formData.is_free
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        
        toast.success('Module mis à jour avec succès !');
      }
      
      // Refresh modules list
      await fetchModules();
      handleCancel();
    } catch (error) {
      console.error('Error saving module:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de la sauvegarde du module');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveQuiz = async () => {
    if (!quizFormData.title.trim()) {
      toast.error('Le titre du quiz est obligatoire');
      return;
    }

    if (quizFormData.questions.length === 0) {
      toast.error('Ajoutez au moins une question');
      return;
    }

    // Validate all questions
    for (const q of quizFormData.questions) {
      if (!q.question.trim()) {
        toast.error('Toutes les questions doivent avoir un texte');
        return;
      }
      if (q.options.some(opt => !opt.trim())) {
        toast.error('Toutes les options doivent être remplies');
        return;
      }
    }

    try {
      setSaving(true);
      
      const quiz = quizzes[editingQuiz];
      const payload = {
        ...quizFormData,
        module_id: editingQuiz
      };

      if (quiz) {
        // Update existing quiz
        await axios.put(`${API}/admin/quizzes/${quiz.id}`, payload, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        toast.success('Quiz mis à jour avec succès !');
      } else {
        // Create new quiz
        await axios.post(`${API}/admin/quizzes`, payload, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        toast.success('Quiz créé avec succès !');
      }
      
      // Refresh
      await fetchModules();
      handleCancel();
    } catch (error) {
      console.error('Error saving quiz:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de la sauvegarde du quiz');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteModule = async (moduleId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce module ? Cette action est irréversible.')) {
      return;
    }

    try {
      await axios.delete(`${API}/admin/modules/${moduleId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      toast.success('Module supprimé avec succès');
      await fetchModules();
    } catch (error) {
      console.error('Error deleting module:', error);
      toast.error('Erreur lors de la suppression du module');
    }
  };

  const addQuestion = () => {
    setQuizFormData({
      ...quizFormData,
      questions: [
        ...quizFormData.questions,
        {
          id: `q${Date.now()}`,
          question: '',
          options: ['', '', '', ''],
          correct_answer: 0,
          explanation: ''
        }
      ]
    });
  };

  const removeQuestion = (index) => {
    const newQuestions = quizFormData.questions.filter((_, i) => i !== index);
    setQuizFormData({ ...quizFormData, questions: newQuestions });
  };

  const updateQuestion = (index, field, value) => {
    const newQuestions = [...quizFormData.questions];
    newQuestions[index][field] = value;
    setQuizFormData({ ...quizFormData, questions: newQuestions });
  };

  const updateOption = (qIndex, oIndex, value) => {
    const newQuestions = [...quizFormData.questions];
    newQuestions[qIndex].options[oIndex] = value;
    setQuizFormData({ ...quizFormData, questions: newQuestions });
  };

  const getWordCount = (text) => {
    return text.trim().split(/\s+/).length;
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

  // EDITING MODULE VIEW
  if ((editingModule || isCreatingNew) && viewMode === 'modules') {
    return (
      <>
        <Helmet>
          <title>{isCreatingNew ? 'Nouveau Module' : 'Éditer Module'} - Admin</title>
        </Helmet>

        <div className="min-h-screen bg-gray-50 py-8">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  {isCreatingNew ? 'Créer un Nouveau Module' : 'Éditer le Module'}
                </h1>
                {editingModule && (
                  <p className="text-gray-600 mt-1">Module {editingModule.order_index}</p>
                )}
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
                  Remplissez les informations du module de formation
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="title">Titre du Module *</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="Ex: Introduction à l'Inspection Automobile"
                  />
                </div>

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
                    Durée: {Math.floor(formData.duration_minutes / 60)}h{formData.duration_minutes % 60}min
                  </p>
                </div>

                {/* Media Uploader */}
                <div className="space-y-2">
                  <Label>Images et Vidéos</Label>
                  <MediaUploader 
                    onInsert={(htmlCode) => {
                      // Insérer le code HTML à la fin du contenu
                      setFormData({ 
                        ...formData, 
                        content: formData.content + '\n\n' + htmlCode 
                      });
                      toast.success('Média inséré dans le contenu !');
                    }}
                  />
                  <p className="text-sm text-gray-500">
                    💡 Uploadez des images ou vidéos et insérez-les dans le contenu
                  </p>
                </div>

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
                    placeholder="Collez ici le contenu..."
                    rows={25}
                    className="font-mono text-sm"
                  />
                </div>

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

                <div className="flex justify-end space-x-4 pt-4 border-t">
                  <Button
                    onClick={handleCancel}
                    variant="outline"
                    disabled={saving}
                  >
                    Annuler
                  </Button>
                  <Button
                    onClick={handleSaveModule}
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
                        {isCreatingNew ? 'Créer le Module' : 'Enregistrer'}
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

  // EDITING QUIZ VIEW
  if (editingQuiz && viewMode === 'quiz') {
    return (
      <>
        <Helmet>
          <title>Gérer Quiz - Admin</title>
        </Helmet>

        <div className="min-h-screen bg-gray-50 py-8">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  {quizzes[editingQuiz] ? 'Éditer le Quiz' : 'Créer un Quiz'}
                </h1>
                <p className="text-gray-600 mt-1">{editingModule?.title}</p>
              </div>
              <Button
                onClick={handleCancel}
                variant="outline"
              >
                <X className="w-4 h-4 mr-2" />
                Annuler
              </Button>
            </div>

            <Card className="mb-6">
              <CardHeader>
                <CardTitle>Informations du Quiz</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="quiz_title">Titre du Quiz *</Label>
                  <Input
                    id="quiz_title"
                    value={quizFormData.title}
                    onChange={(e) => setQuizFormData({ ...quizFormData, title: e.target.value })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="quiz_description">Description</Label>
                  <Textarea
                    id="quiz_description"
                    value={quizFormData.description}
                    onChange={(e) => setQuizFormData({ ...quizFormData, description: e.target.value })}
                    rows={2}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="passing_score">Score de réussite (%)</Label>
                  <Input
                    id="passing_score"
                    type="number"
                    value={quizFormData.passing_score}
                    onChange={(e) => setQuizFormData({ ...quizFormData, passing_score: parseInt(e.target.value) })}
                    min="0"
                    max="100"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Questions */}
            <div className="space-y-4 mb-6">
              {quizFormData.questions.map((q, qIndex) => (
                <Card key={q.id}>
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">Question {qIndex + 1}</CardTitle>
                      {quizFormData.questions.length > 1 && (
                        <Button
                          onClick={() => removeQuestion(qIndex)}
                          variant="outline"
                          size="sm"
                          className="text-red-600 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label>Question *</Label>
                      <Textarea
                        value={q.question}
                        onChange={(e) => updateQuestion(qIndex, 'question', e.target.value)}
                        placeholder="Entrez la question..."
                        rows={2}
                      />
                    </div>

                    <div className="space-y-3">
                      <Label>Options (4 réponses) *</Label>
                      {q.options.map((opt, oIndex) => (
                        <div key={oIndex} className="flex items-center space-x-3">
                          <input
                            type="radio"
                            name={`correct_${qIndex}`}
                            checked={q.correct_answer === oIndex}
                            onChange={() => updateQuestion(qIndex, 'correct_answer', oIndex)}
                            className="w-4 h-4 text-blue-600"
                          />
                          <Input
                            value={opt}
                            onChange={(e) => updateOption(qIndex, oIndex, e.target.value)}
                            placeholder={`Option ${String.fromCharCode(65 + oIndex)}`}
                          />
                        </div>
                      ))}
                      <p className="text-sm text-gray-500">
                        ⭕ Cochez le bouton radio pour la bonne réponse
                      </p>
                    </div>

                    <div className="space-y-2">
                      <Label>Explication (optionnelle)</Label>
                      <Textarea
                        value={q.explanation}
                        onChange={(e) => updateQuestion(qIndex, 'explanation', e.target.value)}
                        placeholder="Explication de la réponse correcte..."
                        rows={2}
                      />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            <div className="flex justify-between items-center pb-6">
              <Button
                onClick={addQuestion}
                variant="outline"
                className="flex items-center"
              >
                <Plus className="w-4 h-4 mr-2" />
                Ajouter une Question
              </Button>

              <div className="flex space-x-4">
                <Button
                  onClick={handleCancel}
                  variant="outline"
                  disabled={saving}
                >
                  Annuler
                </Button>
                <Button
                  onClick={handleSaveQuiz}
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
                      Enregistrer le Quiz
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

  // MODULES LIST VIEW
  return (
    <>
      <Helmet>
        <title>Gestion des Modules - Admin</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Gestion des Modules</h1>
              <p className="text-gray-600 mt-2">
                Créez et éditez les modules de formation et leurs quiz
              </p>
            </div>
            <Button
              onClick={handleCreateNew}
              className="bg-blue-600 hover:bg-blue-700 flex items-center"
            >
              <Plus className="w-4 h-4 mr-2" />
              Nouveau Module
            </Button>
          </div>

          <div className="grid gap-6">
            {modules.map((module) => {
              const wordCount = getWordCount(module.content);
              const hasQuiz = quizzes[module.id];
              
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
                          {hasQuiz && (
                            <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs font-medium flex items-center">
                              <HelpCircle className="w-3 h-3 mr-1" />
                              Quiz: {hasQuiz.questions?.length || 0} questions
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="flex flex-col space-y-2">
                        <Button
                          onClick={() => handleEdit(module)}
                          className="bg-blue-600 hover:bg-blue-700"
                        >
                          <Edit className="w-4 h-4 mr-2" />
                          Éditer Module
                        </Button>
                        <Button
                          onClick={() => handleEditQuiz(module.id)}
                          variant="outline"
                          className="border-purple-600 text-purple-600 hover:bg-purple-50"
                        >
                          <HelpCircle className="w-4 h-4 mr-2" />
                          {hasQuiz ? 'Éditer Quiz' : 'Créer Quiz'}
                        </Button>
                        <Button
                          onClick={() => handleDeleteModule(module.id)}
                          variant="outline"
                          className="border-red-300 text-red-600 hover:bg-red-50"
                        >
                          <Trash2 className="w-4 h-4 mr-2" />
                          Supprimer
                        </Button>
                      </div>
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

export default AdminModulesNew;
