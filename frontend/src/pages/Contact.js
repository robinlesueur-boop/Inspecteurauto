import React, { useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Mail, Phone, MapPin, Clock, Send, GraduationCap, Users } from 'lucide-react';
import toast from 'react-hot-toast';

function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [sending, setSending] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.message) {
      toast.error('Veuillez remplir tous les champs obligatoires');
      return;
    }

    setSending(true);
    
    // Simuler l'envoi (à remplacer par vraie API email)
    setTimeout(() => {
      toast.success('Message envoyé avec succès ! Nous vous répondrons sous 24h.');
      setFormData({ name: '', email: '', subject: '', message: '' });
      setSending(false);
    }, 1500);
  };

  return (
    <>
      <Helmet>
        <title>Nous Contacter - Formation Inspecteur Automobile</title>
        <meta name="description" content="Contactez l'équipe Inspecteur Auto Formation pour toute question sur la formation, l'inscription ou le support technique." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Nous Contacter
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Une question ? Notre équipe est là pour vous aider !
            </p>
          </div>

          {/* Contact Cards */}
          <div className="grid lg:grid-cols-4 gap-6 mb-12">
            <Card>
              <CardContent className="p-6 text-center">
                <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mail className="w-7 h-7 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Email Général</h3>
                <p className="text-gray-600 text-sm mb-2">Questions générales</p>
                <a href="mailto:support@inspecteur-auto.fr" className="text-blue-600 hover:underline text-sm">
                  support@inspecteur-auto.fr
                </a>
              </CardContent>
            </Card>

            <Card className="border-2 border-green-200 bg-green-50">
              <CardContent className="p-6 text-center">
                <div className="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <GraduationCap className="w-7 h-7 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Équipe Pédagogique</h3>
                <p className="text-gray-600 text-sm mb-2">Questions sur les cours</p>
                <a href="mailto:support@inspecteur-auto.fr" className="text-green-600 hover:underline text-sm block">
                  support@inspecteur-auto.fr
                </a>
                <a href="tel:+33647891221" className="text-green-600 hover:underline text-sm block mt-1">
                  06 47 89 12 21
                </a>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6 text-center">
                <div className="w-14 h-14 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Phone className="w-7 h-7 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Téléphone</h3>
                <p className="text-gray-600 text-sm mb-2">Lun - Ven : 9h-18h</p>
                <a href="tel:+33647891221" className="text-blue-600 hover:underline text-sm">
                  06 47 89 12 21
                </a>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6 text-center">
                <div className="w-14 h-14 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MapPin className="w-7 h-7 text-orange-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Adresse</h3>
                <p className="text-gray-600 text-sm">
                  Inspecteur Auto<br />
                  Paris, France
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            <Card>
              <CardHeader>
                <CardTitle>Envoyez-nous un message</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="name">Nom complet *</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      placeholder="Jean Dupont"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email">Email *</Label>
                    <Input
                      id="email"
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      placeholder="jean.dupont@example.com"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="subject">Sujet</Label>
                    <Input
                      id="subject"
                      value={formData.subject}
                      onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                      placeholder="Question sur la formation"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="message">Message *</Label>
                    <Textarea
                      id="message"
                      value={formData.message}
                      onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                      placeholder="Votre message..."
                      rows={6}
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    disabled={sending}
                    className="w-full bg-blue-600 hover:bg-blue-700"
                  >
                    {sending ? (
                      <>
                        <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                        Envoi...
                      </>
                    ) : (
                      <>
                        <Send className="w-4 h-4 mr-2" />
                        Envoyer le message
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <GraduationCap className="w-5 h-5 text-green-600" />
                    Équipe Pédagogique
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 mb-4">
                    Pour toute question concernant le contenu des cours, les quiz, ou votre progression :
                  </p>
                  <div className="bg-green-50 p-4 rounded-lg space-y-2">
                    <div className="flex items-center gap-2">
                      <Mail className="w-4 h-4 text-green-600" />
                      <a href="mailto:support@inspecteur-auto.fr" className="text-green-700 hover:underline font-medium">
                        support@inspecteur-auto.fr
                      </a>
                    </div>
                    <div className="flex items-center gap-2">
                      <Phone className="w-4 h-4 text-green-600" />
                      <a href="tel:+33647891221" className="text-green-700 hover:underline font-medium">
                        06 47 89 12 21
                      </a>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Horaires de Support</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-start space-x-3 mb-4">
                    <Clock className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-gray-900">Support Email & Chat</p>
                      <p className="text-gray-600 text-sm">24h/24, 7j/7</p>
                      <p className="text-gray-500 text-xs">Réponse sous 24h en semaine</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <Clock className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-gray-900">Support Téléphonique</p>
                      <p className="text-gray-600 text-sm">Lundi - Vendredi : 9h00 - 18h00</p>
                      <p className="text-gray-500 text-xs">Fermé weekends et jours fériés</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Questions Fréquentes</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 mb-4">
                    Consultez notre FAQ pour des réponses immédiates aux questions les plus courantes.
                  </p>
                  <a href="/faq" className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Voir la FAQ
                  </a>
                </CardContent>
              </Card>
            </div>
          </div>

        </div>
      </div>
    </>
  );
}

export default Contact;
