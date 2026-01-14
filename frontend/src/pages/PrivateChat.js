import React, { useState, useEffect, useRef } from 'react';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import { 
  Send, 
  MessageCircle, 
  Clock, 
  CheckCheck,
  Loader2,
  HelpCircle,
  BookOpen
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const WS_URL = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');

function PrivateChat() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [connected, setConnected] = useState(false);
  const messagesEndRef = useRef(null);
  const wsRef = useRef(null);

  useEffect(() => {
    fetchMessages();
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectWebSocket = () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    const ws = new WebSocket(`${WS_URL}/ws/chat/${token}`);

    ws.onopen = () => {
      setConnected(true);
      // Ping régulier pour garder la connexion
      const pingInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send('ping');
        }
      }, 30000);
      ws.pingInterval = pingInterval;
    };

    ws.onmessage = (event) => {
      if (event.data === 'pong') return;
      
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'new_message') {
          setMessages(prev => [...prev, data.message]);
        }
      } catch (e) {
        console.error('Error parsing WebSocket message:', e);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      if (ws.pingInterval) clearInterval(ws.pingInterval);
      // Reconnexion automatique après 3 secondes
      setTimeout(() => {
        if (document.visibilityState === 'visible') {
          connectWebSocket();
        }
      }, 3000);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    wsRef.current = ws;
  };

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${API}/chat/messages`);
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
      if (error.response?.status === 403) {
        toast.error('Chat réservé aux membres premium');
      }
    } finally {
      setLoading(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;

    setSending(true);
    const messageContent = newMessage.trim();
    setNewMessage('');

    // Optimistic update
    const optimisticMessage = {
      id: 'temp-' + Date.now(),
      content: messageContent,
      sender_type: 'student',
      sender_id: user?.id,
      created_at: new Date().toISOString(),
      is_read: false
    };
    setMessages(prev => [...prev, optimisticMessage]);

    try {
      await axios.post(`${API}/chat/messages`, { content: messageContent });
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Erreur lors de l\'envoi du message');
      // Retirer le message optimiste en cas d'erreur
      setMessages(prev => prev.filter(m => m.id !== optimisticMessage.id));
      setNewMessage(messageContent);
    } finally {
      setSending(false);
    }
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const isToday = date.toDateString() === now.toDateString();
    
    if (isToday) {
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    }
    
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Chargement du chat...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Chat avec l'équipe - Formation Inspecteur Automobile</title>
        <meta name="description" content="Posez vos questions directement à l'équipe pédagogique" />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8" data-testid="private-chat">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <MessageCircle className="h-6 w-6 text-blue-600" />
                  Chat avec l'équipe pédagogique
                </h1>
                <p className="text-gray-600 mt-1">
                  Posez vos questions sur les cours, nous vous répondons rapidement
                </p>
              </div>
              <Badge 
                variant={connected ? "default" : "secondary"}
                className={connected ? "bg-green-500" : ""}
              >
                {connected ? "En ligne" : "Hors ligne"}
              </Badge>
            </div>
          </motion.div>

          {/* Info Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-6"
          >
            <Card className="bg-blue-50 border-blue-200">
              <CardContent className="p-4">
                <div className="flex items-start gap-3">
                  <HelpCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div>
                    <p className="text-sm text-blue-800 font-medium">
                      Ce chat est privé et confidentiel
                    </p>
                    <p className="text-sm text-blue-700 mt-1">
                      Seuls les formateurs peuvent voir vos messages. N'hésitez pas à poser toutes vos questions !
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Chat Container */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="h-[60vh] flex flex-col">
              <CardHeader className="border-b py-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-blue-600" />
                  Vos questions sur la formation
                </CardTitle>
              </CardHeader>

              {/* Messages Area */}
              <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-center">
                    <div>
                      <MessageCircle className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-600 mb-2">
                        Aucun message pour le moment
                      </h3>
                      <p className="text-gray-500 text-sm">
                        Posez votre première question à l'équipe pédagogique !
                      </p>
                    </div>
                  </div>
                ) : (
                  <AnimatePresence initial={false}>
                    {messages.map((message, index) => (
                      <motion.div
                        key={message.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`flex ${message.sender_type === 'student' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-[75%] rounded-2xl px-4 py-3 ${
                            message.sender_type === 'student'
                              ? 'bg-blue-600 text-white rounded-br-md'
                              : 'bg-gray-100 text-gray-900 rounded-bl-md'
                          }`}
                        >
                          {message.sender_type === 'admin' && (
                            <div className="text-xs font-medium text-blue-600 mb-1">
                              Équipe pédagogique
                            </div>
                          )}
                          <p className="text-sm whitespace-pre-wrap break-words">
                            {message.content}
                          </p>
                          <div className={`flex items-center gap-1 mt-1 text-xs ${
                            message.sender_type === 'student' ? 'text-blue-200' : 'text-gray-500'
                          }`}>
                            <Clock className="h-3 w-3" />
                            {formatTime(message.created_at)}
                            {message.sender_type === 'student' && message.is_read && (
                              <CheckCheck className="h-3 w-3 ml-1" />
                            )}
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                )}
                <div ref={messagesEndRef} />
              </CardContent>

              {/* Input Area */}
              <div className="border-t p-4">
                <form onSubmit={handleSendMessage} className="flex gap-2">
                  <Input
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Écrivez votre message..."
                    disabled={sending}
                    className="flex-1"
                    data-testid="chat-input"
                  />
                  <Button 
                    type="submit" 
                    disabled={!newMessage.trim() || sending}
                    className="bg-blue-600 hover:bg-blue-700"
                    data-testid="send-message-btn"
                  >
                    {sending ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="h-4 w-4" />
                    )}
                  </Button>
                </form>
              </div>
            </Card>
          </motion.div>

          {/* Quick Tips */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-6"
          >
            <Card className="bg-gradient-to-r from-gray-50 to-blue-50">
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">
                  <strong>💡 Astuce :</strong> Mentionnez le numéro du module concerné dans votre question pour une réponse plus rapide !
                </p>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </>
  );
}

export default PrivateChat;
