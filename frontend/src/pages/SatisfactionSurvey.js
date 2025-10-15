import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Star, CheckCircle, Send } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function SatisfactionSurvey() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [checkingStatus, setCheckingStatus] = useState(true);
  const [submitted, setSubmitted] = useState(false);
  const [ratings, setRatings] = useState({
    content_quality: 0,
    teaching_method: 0,
    platform_usability: 0,
    support_quality: 0,
    overall_satisfaction: 0,
    would_recommend: 0
  });
  const [openFeedback, setOpenFeedback] = useState('');

  useEffect(() => {
    checkSurveyStatus();
  }, []);

  const checkSurveyStatus = async () => {
    try {
      const response = await axios.get(`${API}/satisfaction-survey/check`);
      if (response.data.submitted) {
        setSubmitted(true);
      }
    } catch (error) {
      console.error('Error checking survey status:', error);
    } finally {
      setCheckingStatus(false);
    }
  };

  const handleRatingChange = (category, value) => {
    setRatings({
      ...ratings,
      [category]: parseInt(value)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if all ratings are provided
    const allRated = Object.values(ratings).every(rating => rating > 0);
    if (!allRated) {
      toast.error('Veuillez répondre à toutes les questions');
      return;
    }

    if (!openFeedback.trim()) {
      toast.error('Veuillez fournir un commentaire');
      return;
    }

    try {
      setLoading(true);
      await axios.post(`${API}/satisfaction-survey/submit`, {
        ratings,
        open_feedback: openFeedback
      });

      toast.success('Merci pour votre retour !');
      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting survey:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de la soumission');
    } finally {
      setLoading(false);
    }
  };

  const RatingQuestion = ({ question, category, value }) => {
    return (
      <div className="space-y-3">
        <Label className="text-base font-medium">{question}</Label>
        <RadioGroup
          value={value.toString()}
          onValueChange={(val) => handleRatingChange(category, val)}
        >
          <div className="flex justify-between items-center">
            {[1, 2, 3, 4, 5].map((rating) => (
              <div
                key={rating}
                className="flex flex-col items-center cursor-pointer"
                onClick={() => handleRatingChange(category, rating)}
              >
                <RadioGroupItem value={rating.toString()} id={`${category}-${rating}`} />
                <div className="mt-2 flex">
                  {[...Array(rating)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-4 h-4 ${
                        value >= rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-xs text-gray-500 mt-1">
                  {rating === 1 && 'Très insatisfait'}
                  {rating === 3 && 'Neutre'}
                  {rating === 5 && 'Très satisfait'}
                </span>
              </div>
            ))}
          </div>
        </RadioGroup>
      </div>
    );
  };

  if (checkingStatus) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (submitted) {
    return (
      <>
        <Helmet>
          <title>Enquête Soumise - Formation Inspecteur Automobile</title>
        </Helmet>

        <div className="min-h-screen bg-gray-50 py-12">
          <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
            <Card className="shadow-xl">
              <CardContent className="pt-12 pb-12 text-center">
                <div className="flex justify-center mb-6">
                  <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="w-12 h-12 text-green-600" />
                  </div>
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  Merci pour votre retour !
                </h2>
                <p className="text-gray-600 mb-6">
                  Votre avis a été enregistré avec succès. Vos commentaires nous aident 
                  à améliorer continuellement notre formation.
                </p>
                <Button onClick={() => navigate('/dashboard')} className="bg-blue-600 hover:bg-blue-700">
                  Retour au Dashboard
                </Button>
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
        <title>Enquête de Satisfaction - Formation Inspecteur Automobile</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="shadow-xl">
            <CardHeader>
              <CardTitle className="text-2xl">Enquête de Satisfaction</CardTitle>
              <CardDescription>
                Votre avis nous est précieux ! Prenez quelques minutes pour nous faire part 
                de votre expérience avec la formation Inspecteur Auto.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-8">
                {/* Rating Questions */}
                <div className="space-y-6">
                  <RatingQuestion
                    question="1. Comment évaluez-vous la qualité du contenu de la formation ?"
                    category="content_quality"
                    value={ratings.content_quality}
                  />

                  <div className="border-t pt-6">
                    <RatingQuestion
                      question="2. La méthode pédagogique était-elle adaptée ?"
                      category="teaching_method"
                      value={ratings.teaching_method}
                    />
                  </div>

                  <div className="border-t pt-6">
                    <RatingQuestion
                      question="3. La plateforme était-elle facile à utiliser ?"
                      category="platform_usability"
                      value={ratings.platform_usability}
                    />
                  </div>

                  <div className="border-t pt-6">
                    <RatingQuestion
                      question="4. Comment évaluez-vous la qualité du support et de l'accompagnement ?"
                      category="support_quality"
                      value={ratings.support_quality}
                    />
                  </div>

                  <div className="border-t pt-6">
                    <RatingQuestion
                      question="5. Satisfaction globale par rapport à la formation ?"
                      category="overall_satisfaction"
                      value={ratings.overall_satisfaction}
                    />
                  </div>

                  <div className="border-t pt-6">
                    <RatingQuestion
                      question="6. Recommanderiez-vous cette formation à un proche ?"
                      category="would_recommend"
                      value={ratings.would_recommend}
                    />
                  </div>
                </div>

                {/* Open Feedback */}
                <div className="border-t pt-6 space-y-3">
                  <Label htmlFor="feedback" className="text-base font-medium">
                    7. Commentaires et suggestions d'amélioration
                  </Label>
                  <Textarea
                    id="feedback"
                    value={openFeedback}
                    onChange={(e) => setOpenFeedback(e.target.value)}
                    placeholder="Partagez vos commentaires, suggestions ou remarques..."
                    rows={6}
                    className="resize-none"
                  />
                  <p className="text-sm text-gray-500">
                    Vos commentaires nous aident à améliorer la formation pour les futurs étudiants.
                  </p>
                </div>

                {/* Submit Button */}
                <div className="flex justify-end pt-4">
                  <Button
                    type="submit"
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-700 px-8"
                    size="lg"
                  >
                    {loading ? (
                      <>
                        <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                        Envoi...
                      </>
                    ) : (
                      <>
                        <Send className="w-4 h-4 mr-2" />
                        Envoyer mon avis
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}

export default SatisfactionSurvey;
