import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Badge } from '../../components/ui/badge';
import { Send, Users, User, Mail, Clock } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminMessaging() {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [formData, setFormData] = useState({
    recipient_id: '',
    subject: '',
    message: ''
  });

  useEffect(() => {
    fetchUsers();
    fetchMessages();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API}/admin/users`);
      setUsers(response.data.users || []);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${API}/admin/messages`);
      setMessages(response.data || []);
    } catch (error) {
      console.error('Error fetching messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!formData.subject.trim() || !formData.message.trim()) {
      toast.error('Veuillez remplir tous les champs');
      return;
    }

    try {
      setSending(true);
      await axios.post(`${API}/admin/messages/send`, formData);
      
      toast.success('Message envoyé avec succès');
      
      // Reset form
      setFormData({
        recipient_id: '',
        subject: '',
        message: ''
      });
      
      // Refresh messages
      fetchMessages();
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Erreur lors de l\'envoi du message');
    } finally {
      setSending(false);
    }
  };

  const handleBroadcast = () => {
    setFormData({
      ...formData,
      recipient_id: 'all'
    });
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
        <title>Messagerie Admin - Formation Inspecteur Automobile</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Messagerie Étudiants</h1>
            <p className="text-gray-600 mt-2">
              Envoyez des messages individuels ou des annonces à tous les étudiants
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Message Form */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Nouveau Message</CardTitle>
                  <CardDescription>
                    Envoyez un message à un étudiant ou à tous les étudiants
                  </CardDescription>
                </CardHeader>
                
                <CardContent>
                  <form onSubmit={handleSendMessage} className="space-y-6">
                    {/* Recipient Selection */}
                    <div className="space-y-2">
                      <Label htmlFor="recipient">Destinataire</Label>
                      <div className="flex space-x-2">
                        <select
                          id="recipient"
                          value={formData.recipient_id}
                          onChange={(e) => setFormData({ ...formData, recipient_id: e.target.value })}
                          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">Sélectionner un étudiant</option>
                          {users.map((u) => (
                            <option key={u.id} value={u.id}>
                              {u.full_name} ({u.email})
                            </option>
                          ))}
                        </select>
                        <Button
                          type="button"
                          onClick={handleBroadcast}
                          variant="outline"
                          className="flex items-center"
                        >
                          <Users className="w-4 h-4 mr-2" />
                          Tous
                        </Button>
                      </div>
                      {formData.recipient_id === 'all' && (
                        <Badge className="bg-orange-100 text-orange-800">
                          Message envoyé à tous les étudiants
                        </Badge>
                      )}
                    </div>

                    {/* Subject */}
                    <div className="space-y-2">
                      <Label htmlFor="subject">Objet</Label>
                      <Input
                        id="subject"
                        value={formData.subject}
                        onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                        placeholder="Objet du message"
                        required
                      />
                    </div>

                    {/* Message */}
                    <div className="space-y-2">
                      <Label htmlFor="message">Message</Label>
                      <Textarea
                        id="message"
                        value={formData.message}
                        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                        placeholder="Votre message..."
                        rows={8}
                        required
                        className="resize-none"
                      />
                    </div>

                    {/* Submit Button */}
                    <div className="flex justify-end">
                      <Button
                        type="submit"
                        disabled={sending || !formData.recipient_id}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        {sending ? (
                          <>
                            <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                            Envoi...
                          </>
                        ) : (
                          <>
                            <Send className="w-4 h-4 mr-2" />
                            Envoyer
                          </>
                        )}
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Statistics */}
            <div className="space-y-6">
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-gray-600">Total Étudiants</div>
                    <Users className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="text-3xl font-bold text-gray-900">{users.length}</div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-gray-600">Messages Envoyés</div>
                    <Mail className="w-5 h-5 text-green-600" />
                  </div>
                  <div className="text-3xl font-bold text-gray-900">{messages.length}</div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Messages History */}
          <div className="mt-8">
            <Card>
              <CardHeader>
                <CardTitle>Historique des Messages</CardTitle>
                <CardDescription>
                  Liste des messages envoyés récemment
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                {messages.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    Aucun message envoyé pour le moment
                  </div>
                ) : (
                  <div className="space-y-4">
                    {messages.slice(0, 10).map((msg) => (
                      <div
                        key={msg.id}
                        className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <h4 className="font-semibold text-gray-900">
                                {msg.subject}
                              </h4>
                              {msg.recipient_id === 'all' ? (
                                <Badge className="bg-orange-100 text-orange-800">
                                  <Users className="w-3 h-3 mr-1" />
                                  Tous
                                </Badge>
                              ) : (
                                <Badge variant="outline">
                                  <User className="w-3 h-3 mr-1" />
                                  {msg.recipient_info?.full_name}
                                </Badge>
                              )}
                            </div>
                            <p className="text-sm text-gray-600 line-clamp-2">
                              {msg.message}
                            </p>
                          </div>
                          <div className="flex items-center text-xs text-gray-500 ml-4">
                            <Clock className="w-3 h-3 mr-1" />
                            {new Date(msg.created_at).toLocaleDateString('fr-FR')}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </>
  );
}

export default AdminMessaging;
