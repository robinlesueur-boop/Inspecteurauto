import React, { useState, useEffect, useRef } from 'react';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import { 
  Send, 
  MessageCircle, 
  Clock, 
  CheckCheck,
  Loader2,
  User,
  Mail,
  ArrowLeft,
  Search,
  Bell
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const WS_URL = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');

function AdminChat() {
  const { user } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [sending, setSending] = useState(false);
  const [connected, setConnected] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const messagesEndRef = useRef(null);
  const wsRef = useRef(null);

  useEffect(() => {
    fetchConversations();
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
          // Si c'est la conversation active, ajouter le message
          if (selectedConversation?.id === data.conversation_id) {
            setMessages(prev => [...prev, data.message]);
          }
          // Rafraîchir la liste des conversations
          fetchConversations();
          // Notification toast si message d'un élève
          if (data.message.sender_type === 'student') {
            toast.success(`Nouveau message de ${data.student_name || 'un élève'}`, {
              icon: '💬'
            });
          }
        }
      } catch (e) {
        console.error('Error parsing WebSocket message:', e);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      if (ws.pingInterval) clearInterval(ws.pingInterval);
      setTimeout(() => {
        if (document.visibilityState === 'visible') {
          connectWebSocket();
        }
      }, 3000);
    };

    wsRef.current = ws;
  };

  const fetchConversations = async () => {
    try {
      const response = await axios.get(`${API}/admin/chat/conversations`);
      setConversations(response.data);
    } catch (error) {
      console.error('Error fetching conversations:', error);
      toast.error('Erreur lors du chargement des conversations');
    } finally {
      setLoading(false);
    }
  };

  const selectConversation = async (conversation) => {
    setSelectedConversation(conversation);
    setLoadingMessages(true);
    
    try {
      const response = await axios.get(`${API}/admin/chat/conversations/${conversation.id}/messages`);
      setMessages(response.data);
      // Rafraîchir pour mettre à jour les compteurs
      fetchConversations();
    } catch (error) {
      console.error('Error fetching messages:', error);
      toast.error('Erreur lors du chargement des messages');
    } finally {
      setLoadingMessages(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending || !selectedConversation) return;

    setSending(true);
    const messageContent = newMessage.trim();
    setNewMessage('');

    // Optimistic update
    const optimisticMessage = {
      id: 'temp-' + Date.now(),
      content: messageContent,
      sender_type: 'admin',
      sender_id: user?.id,
      created_at: new Date().toISOString(),
      is_read: false
    };
    setMessages(prev => [...prev, optimisticMessage]);

    try {
      await axios.post(`${API}/admin/chat/conversations/${selectedConversation.id}/messages`, {
        content: messageContent
      });
      fetchConversations();
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Erreur lors de l\'envoi du message');
      setMessages(prev => prev.filter(m => m.id !== optimisticMessage.id));
      setNewMessage(messageContent);
    } finally {
      setSending(false);
    }
  };

  const formatTime = (dateString) => {
    if (!dateString) return '';
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

  const filteredConversations = conversations.filter(conv => 
    conv.student_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    conv.student_email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalUnread = conversations.reduce((sum, conv) => sum + (conv.unread_by_admin || 0), 0);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Chargement des conversations...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Chat Admin - Inspecteur Auto</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50" data-testid="admin-chat">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <MessageCircle className="h-6 w-6 text-blue-600" />
                  Chat avec les élèves
                </h1>
                <p className="text-gray-600 mt-1">
                  Répondez aux questions de vos élèves
                </p>
              </div>
              <div className="flex items-center gap-3">
                {totalUnread > 0 && (
                  <Badge className="bg-red-500 text-white">
                    <Bell className="h-3 w-3 mr-1" />
                    {totalUnread} non lu{totalUnread > 1 ? 's' : ''}
                  </Badge>
                )}
                <Badge 
                  variant={connected ? "default" : "secondary"}
                  className={connected ? "bg-green-500" : ""}
                >
                  {connected ? "En ligne" : "Hors ligne"}
                </Badge>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Conversations List */}
            <Card className="lg:col-span-1 h-[75vh] flex flex-col">
              <CardHeader className="border-b py-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Rechercher un élève..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </CardHeader>
              
              <CardContent className="flex-1 overflow-y-auto p-2">
                {filteredConversations.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <MessageCircle className="h-12 w-12 mx-auto mb-3 text-gray-300" />
                    <p>Aucune conversation</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {filteredConversations.map((conv) => (
                      <div
                        key={conv.id}
                        onClick={() => selectConversation(conv)}
                        className={`p-3 rounded-lg cursor-pointer transition-all ${
                          selectedConversation?.id === conv.id
                            ? 'bg-blue-100 border-2 border-blue-500'
                            : conv.unread_by_admin > 0
                            ? 'bg-blue-50 hover:bg-blue-100 border-2 border-blue-200'
                            : 'hover:bg-gray-100 border-2 border-transparent'
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-center gap-2">
                            <div className="bg-blue-100 text-blue-600 rounded-full p-2">
                              <User className="h-4 w-4" />
                            </div>
                            <div>
                              <h4 className="font-medium text-gray-900 text-sm">
                                {conv.student_name}
                              </h4>
                              <p className="text-xs text-gray-500">{conv.student_email}</p>
                            </div>
                          </div>
                          {conv.unread_by_admin > 0 && (
                            <Badge className="bg-red-500 text-white text-xs">
                              {conv.unread_by_admin}
                            </Badge>
                          )}
                        </div>
                        {conv.last_message && (
                          <p className="text-xs text-gray-600 mt-2 truncate">
                            {conv.last_message_by === 'admin' ? 'Vous: ' : ''}
                            {conv.last_message}
                          </p>
                        )}
                        {conv.last_message_at && (
                          <p className="text-xs text-gray-400 mt-1">
                            {formatTime(conv.last_message_at)}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Chat Area */}
            <Card className="lg:col-span-2 h-[75vh] flex flex-col">
              {selectedConversation ? (
                <>
                  <CardHeader className="border-b py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="lg:hidden"
                          onClick={() => setSelectedConversation(null)}
                        >
                          <ArrowLeft className="h-4 w-4" />
                        </Button>
                        <div className="bg-blue-100 text-blue-600 rounded-full p-2">
                          <User className="h-5 w-5" />
                        </div>
                        <div>
                          <h3 className="font-semibold text-gray-900">
                            {selectedConversation.student_name}
                          </h3>
                          <p className="text-sm text-gray-500 flex items-center gap-1">
                            <Mail className="h-3 w-3" />
                            {selectedConversation.student_email}
                          </p>
                        </div>
                      </div>
                    </div>
                  </CardHeader>

                  {/* Messages */}
                  <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
                    {loadingMessages ? (
                      <div className="flex items-center justify-center h-full">
                        <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
                      </div>
                    ) : messages.length === 0 ? (
                      <div className="h-full flex items-center justify-center text-center">
                        <div>
                          <MessageCircle className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                          <p className="text-gray-500">Aucun message dans cette conversation</p>
                        </div>
                      </div>
                    ) : (
                      <AnimatePresence initial={false}>
                        {messages.map((message) => (
                          <motion.div
                            key={message.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex ${message.sender_type === 'admin' ? 'justify-end' : 'justify-start'}`}
                          >
                            <div
                              className={`max-w-[75%] rounded-2xl px-4 py-3 ${
                                message.sender_type === 'admin'
                                  ? 'bg-blue-600 text-white rounded-br-md'
                                  : 'bg-gray-100 text-gray-900 rounded-bl-md'
                              }`}
                            >
                              {message.sender_type === 'student' && (
                                <div className="text-xs font-medium text-blue-600 mb-1">
                                  {selectedConversation.student_name}
                                </div>
                              )}
                              <p className="text-sm whitespace-pre-wrap break-words">
                                {message.content}
                              </p>
                              <div className={`flex items-center gap-1 mt-1 text-xs ${
                                message.sender_type === 'admin' ? 'text-blue-200' : 'text-gray-500'
                              }`}>
                                <Clock className="h-3 w-3" />
                                {formatTime(message.created_at)}
                                {message.sender_type === 'admin' && message.is_read && (
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

                  {/* Input */}
                  <div className="border-t p-4">
                    <form onSubmit={handleSendMessage} className="flex gap-2">
                      <Input
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Répondre à l'élève..."
                        disabled={sending}
                        className="flex-1"
                      />
                      <Button 
                        type="submit" 
                        disabled={!newMessage.trim() || sending}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        {sending ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Send className="h-4 w-4" />
                        )}
                      </Button>
                    </form>
                  </div>
                </>
              ) : (
                <div className="flex-1 flex items-center justify-center text-center p-8">
                  <div>
                    <MessageCircle className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-600 mb-2">
                      Sélectionnez une conversation
                    </h3>
                    <p className="text-gray-500">
                      Choisissez un élève dans la liste pour voir ses messages
                    </p>
                  </div>
                </div>
              )}
            </Card>
          </div>
        </div>
      </div>
    </>
  );
}

export default AdminChat;
