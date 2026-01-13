import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Save, Plus, Trash2, AlertCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminMechanicalQuiz() {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchQuiz();
  }, []);

  const fetchQuiz = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/admin/quizzes/mechanical-knowledge`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setQuiz(response.data);
    } catch (error) {
      console.error('Error fetching quiz:', error);
      toast.error('Erreur lors du chargement du quiz');
    } finally {
      setLoading(false);
    }
  };

  const updateQuestion = (qIndex, field, value) => {
    const newQuestions = [...quiz.questions];
    newQuestions[qIndex] = {
      ...newQuestions[qIndex],
      [field]: value
    };
    setQuiz({ ...quiz, questions: newQuestions });
  };

  const updateOption = (qIndex, optionIndex, value) => {
    const newQuestions = [...quiz.questions];
    newQuestions[qIndex].options[optionIndex] = value;
    setQuiz({ ...quiz, questions: newQuestions });
  };

  const addQuestion = () => {
    const newQuestion = {
      id: `mech_q_${Date.now()}`,
      question: '',
      options: ['', '', '', ''],
      correct_answer: 0,
      explanation: ''
    };
    setQuiz({
      ...quiz,
      questions: [...quiz.questions, newQuestion]
    });
  };

  const removeQuestion = (qIndex) => {
    if (quiz.questions.length <= 1) {
      toast.error('Le quiz doit contenir au moins une question');
      return;
    }
    const newQuestions = quiz.questions.filter((_, idx) => idx !== qIndex);
    setQuiz({ ...quiz, questions: newQuestions });
  };

  const handleSave = async () => {
    // Validation
    if (!quiz.title.trim()) {
      toast.error('Le titre est obligatoire');
      return;
    }

    if (quiz.questions.length === 0) {
      toast.error('Ajoutez au moins une question');
      return;
    }

    for (const q of quiz.questions) {
      if (!q.question.trim()) {
        toast.error('Toutes les questions doivent avoir un texte');
        return;
      }
      if (q.options.some(opt => !opt.trim())) {
        toast.error('Toutes les options doivent être remplies');
        return;
      }
    }

    setSaving(true);
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API}/admin/quizzes/mechanical-knowledge`, quiz, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Quiz sauvegardé avec succès !');
    } catch (error) {
      console.error('Error saving quiz:', error);
      toast.error('Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="p-6 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <p className="text-gray-600">Quiz non trouvé</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Éditer Quiz Mécanique - Admin</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">
              📝 Évaluation des Connaissances Mécaniques
            </h1>
            <p className="text-gray-600 mt-1">
              Quiz de pré-évaluation après paiement (détermine si le module de remise à niveau est nécessaire)
            </p>
          </div>

          {/* Informations générales */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Informations du Quiz</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="title">Titre du Quiz *</Label>
                <Input
                  id="title"
                  value={quiz.title}
                  onChange={(e) => setQuiz({ ...quiz, title: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={quiz.description || ''}
                  onChange={(e) => setQuiz({ ...quiz, description: e.target.value })}
                  rows={3}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="passing_score">Score de réussite (%)</Label>
                  <Input
                    id="passing_score"
                    type="number"
                    value={quiz.passing_score || 70}
                    onChange={(e) => setQuiz({ ...quiz, passing_score: parseInt(e.target.value) })}
                    min="0"
                    max="100"
                  />
                  <p className="text-xs text-gray-500">
                    Si score {'<'} 70%, l'étudiant devra suivre le Module 2 "Remise à Niveau"
                  </p>
                </div>
                <div className="space-y-2">
                  <Label>Nombre de questions</Label>
                  <div className="text-2xl font-bold text-blue-600">{quiz.questions.length}</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Questions */}
          <div className="space-y-4 mb-6">
            {quiz.questions.map((q, qIndex) => (
              <Card key={q.id} className="border-l-4 border-l-purple-500">
                <CardHeader className="pb-3 bg-purple-50">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg text-purple-900">
                      Question {qIndex + 1}
                    </CardTitle>
                    {quiz.questions.length > 1 && (
                      <Button
                        onClick={() => removeQuestion(qIndex)}
                        variant="outline"
                        size="sm"
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4 mr-1" />
                        Supprimer
                      </Button>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4 pt-4">
                  {/* Question text */}
                  <div className="space-y-2">
                    <Label>Texte de la question *</Label>
                    <Textarea
                      value={q.question}
                      onChange={(e) => updateQuestion(qIndex, 'question', e.target.value)}
                      placeholder="Entrez la question..."
                      rows={2}
                      className="font-medium"
                    />
                  </div>

                  {/* Options */}
                  <div className="space-y-3">
                    <Label>Réponses (4 options) *</Label>
                    {q.options.map((option, optIndex) => (
                      <div key={optIndex} className="flex items-center space-x-3">
                        <div className="flex items-center space-x-2">
                          <input
                            type="radio"
                            name={`correct_${qIndex}`}
                            checked={q.correct_answer === optIndex}
                            onChange={() => updateQuestion(qIndex, 'correct_answer', optIndex)}
                            className="w-4 h-4 text-green-600"
                          />
                          <span className="text-sm font-medium text-gray-700">
                            {optIndex === 0 ? 'A' : optIndex === 1 ? 'B' : optIndex === 2 ? 'C' : 'D'}
                          </span>
                        </div>
                        <Input
                          value={option}
                          onChange={(e) => updateOption(qIndex, optIndex, e.target.value)}
                          placeholder={`Option ${optIndex + 1}`}
                          className={q.correct_answer === optIndex ? 'border-green-500 bg-green-50' : ''}
                        />
                      </div>
                    ))}
                    <p className="text-xs text-gray-500">
                      💡 Cochez la case radio pour marquer la bonne réponse
                    </p>
                  </div>

                  {/* Explanation */}
                  <div className="space-y-2">
                    <Label>Explication (optionnel)</Label>
                    <Textarea
                      value={q.explanation || ''}
                      onChange={(e) => updateQuestion(qIndex, 'explanation', e.target.value)}
                      placeholder="Expliquez pourquoi cette réponse est correcte..."
                      rows={2}
                      className="text-sm"
                    />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Ajouter une question */}
          <div className="mb-6">
            <Button
              onClick={addQuestion}
              variant="outline"
              className="w-full border-dashed border-2 border-purple-300 text-purple-600 hover:bg-purple-50"
            >
              <Plus className="w-4 h-4 mr-2" />
              Ajouter une Question
            </Button>
          </div>

          {/* Bouton Sauvegarder */}
          <div className="flex justify-end space-x-4">
            <Button
              onClick={handleSave}
              disabled={saving}
              className="bg-green-600 hover:bg-green-700"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Sauvegarde...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4 mr-2" />
                  Sauvegarder le Quiz
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}

export default AdminMechanicalQuiz;
