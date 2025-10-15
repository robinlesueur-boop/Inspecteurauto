import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Mail, MailOpen, Clock } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Messages() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedMessage, setSelectedMessage] = useState(null);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${API}/messages`);
      setMessages(response.data || []);
    } catch (error) {
      console.error('Error fetching messages:', error);
      toast.error('Erreur lors du chargement des messages');
    } finally {
      setLoading(false);
    }
  };

  const handleMessageClick = async (message) => {
    setSelectedMessage(message);
    
    // Mark as read if not already
    if (!message.is_read) {
      try {
        await axios.patch(`${API}/messages/${message.id}/read`);
        // Update local state
        setMessages(messages.map(m =>
          m.id === message.id ? { ...m, is_read: true } : m
        ));
      } catch (error) {
        console.error('Error marking message as read:', error);
      }
    }
  };

  const unreadCount = messages.filter(m => !m.is_read).length;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des messages...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Messages - Formation Inspecteur Automobile</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Mes Messages</h1>
            <p className="text-gray-600 mt-2">
              {unreadCount > 0 ? `${unreadCount} message${unreadCount > 1 ? 's' : ''} non lu${unreadCount > 1 ? 's' : ''}` : 'Aucun nouveau message'}
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Messages List */}
            <div className="lg:col-span-1">
              <Card>
                <CardHeader>
                  <CardTitle>Boîte de Réception</CardTitle>
                </CardHeader>
                
                <CardContent>
                  {messages.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      <Mail className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                      <p>Aucun message</p>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {messages.map((message) => (
                        <div
                          key={message.id}
                          onClick={() => handleMessageClick(message)}
                          className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                            selectedMessage?.id === message.id
                              ? 'border-blue-600 bg-blue-50'
                              : message.is_read
                              ? 'border-gray-200 hover:border-gray-300'
                              : 'border-blue-200 bg-blue-50 hover:border-blue-300'
                          }`}
                        >
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              {message.is_read ? (
                                <MailOpen className="w-4 h-4 text-gray-400" />
                              ) : (
                                <Mail className="w-4 h-4 text-blue-600" />
                              )}
                              <h4 className={`text-sm font-medium ${!message.is_read ? 'font-bold' : ''}`}>
                                {message.subject}
                              </h4>
                            </div>
                            {!message.is_read && (
                              <Badge className="bg-blue-600 text-white text-xs">
                                Nouveau
                              </Badge>
                            )}
                          </div>
                          <div className="flex items-center text-xs text-gray-500">
                            <Clock className="w-3 h-3 mr-1" />
                            {new Date(message.created_at).toLocaleDateString('fr-FR', {
                              day: 'numeric',
                              month: 'short',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Message Content */}
            <div className="lg:col-span-2">
              <Card className="min-h-[500px]">
                {selectedMessage ? (
                  <>
                    <CardHeader className="border-b">
                      <div className="flex items-start justify-between">
                        <div>
                          <CardTitle>{selectedMessage.subject}</CardTitle>
                          <div className="flex items-center text-sm text-gray-500 mt-2">
                            <Clock className="w-4 h-4 mr-1" />
                            {new Date(selectedMessage.created_at).toLocaleDateString('fr-FR', {
                              weekday: 'long',
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </div>
                        </div>
                        <Badge variant="outline">
                          Administration
                        </Badge>
                      </div>
                    </CardHeader>
                    
                    <CardContent className="pt-6">
                      <div className="prose max-w-none">
                        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
                          {selectedMessage.message}
                        </p>
                      </div>
                    </CardContent>
                  </>
                ) : (
                  <CardContent className="flex items-center justify-center h-full">
                    <div className="text-center text-gray-500">
                      <Mail className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                      <p>Sélectionnez un message pour le lire</p>
                    </div>
                  </CardContent>
                )}
              </Card>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Messages;
