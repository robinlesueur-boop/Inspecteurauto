import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Badge } from '../components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { 
  MessageCircle, 
  Plus, 
  Users, 
  Calendar, 
  Heart,
  Reply,
  Filter,
  Search
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Forum() {
  const { user } = useAuth();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreatePost, setShowCreatePost] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [newPost, setNewPost] = useState({
    title: '',
    content: '',
    category: 'general'
  });

  const categories = [
    { value: '', label: 'Toutes les catégories' },
    { value: 'general', label: 'Général' },
    { value: 'questions', label: 'Questions' },
    { value: 'discussions', label: 'Discussions' },
    { value: 'tips', label: 'Conseils' }
  ];

  useEffect(() => {
    fetchPosts();
  }, [selectedCategory]);

  const fetchPosts = async () => {
    try {
      const response = await axios.get(`${API}/forum/posts`, {
        params: { category: selectedCategory }
      });
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
      if (error.response?.status === 403) {
        toast.error('Accès au forum réservé aux membres premium');
      } else {
        toast.error('Erreur lors du chargement du forum');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    if (!newPost.title || !newPost.content) {
      toast.error('Veuillez remplir tous les champs');
      return;
    }

    try {
      await axios.post(`${API}/forum/posts`, {
        title: newPost.title,
        content: newPost.content,
        category: newPost.category
      });
      
      setNewPost({ title: '', content: '', category: 'general' });
      setShowCreatePost(false);
      fetchPosts();
      toast.success('Post créé avec succès !');
    } catch (error) {
      console.error('Error creating post:', error);
      toast.error('Erreur lors de la création du post');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getCategoryColor = (category) => {
    const colors = {
      general: 'bg-blue-100 text-blue-800',
      questions: 'bg-green-100 text-green-800',
      discussions: 'bg-purple-100 text-purple-800',
      tips: 'bg-yellow-100 text-yellow-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const filteredPosts = posts.filter(post =>
    post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-300 rounded w-48"></div>
            <div className="h-32 bg-gray-300 rounded"></div>
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-24 bg-gray-300 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Forum Communauté - Formation Inspecteur Automobile</title>
        <meta name="description" content="Échangez avec la communauté des inspecteurs automobiles certifiés. Posez vos questions et partagez vos expériences." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8" data-testid="forum">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  Forum Communauté
                </h1>
                <p className="text-gray-600">
                  Échangez avec plus de 1000 inspecteurs automobiles certifiés
                </p>
              </div>
              
              <Button 
                onClick={() => setShowCreatePost(true)}
                className="bg-blue-600 hover:bg-blue-700"
                data-testid="create-post-button"
              >
                <Plus className="h-4 w-4 mr-2" />
                Nouveau Post
              </Button>
            </div>
          </motion.div>

          {/* Filters */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-6"
          >
            <Card>
              <CardContent className="p-4">
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                      <Input
                        placeholder="Rechercher dans le forum..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                        data-testid="search-input"
                      />
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Filter className="h-4 w-4 text-gray-400" />
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="border border-gray-300 rounded-md px-3 py-2"
                      data-testid="category-filter"
                    >
                      {categories.map(cat => (
                        <option key={cat.value} value={cat.value}>
                          {cat.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Create Post Form */}
          {showCreatePost && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6"
            >
              <Card>
                <CardHeader>
                  <CardTitle>Créer un nouveau post</CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleCreatePost} className="space-y-4">
                    <div>
                      <Input
                        placeholder="Titre de votre post"
                        value={newPost.title}
                        onChange={(e) => setNewPost({...newPost, title: e.target.value})}
                        data-testid="post-title-input"
                      />
                    </div>
                    
                    <div>
                      <select
                        value={newPost.category}
                        onChange={(e) => setNewPost({...newPost, category: e.target.value})}
                        className="border border-gray-300 rounded-md px-3 py-2 w-full"
                        data-testid="post-category-select"
                      >
                        {categories.slice(1).map(cat => (
                          <option key={cat.value} value={cat.value}>
                            {cat.label}
                          </option>
                        ))}
                      </select>
                    </div>
                    
                    <div>
                      <Textarea
                        placeholder="Contenu de votre post..."
                        value={newPost.content}
                        onChange={(e) => setNewPost({...newPost, content: e.target.value})}
                        rows={4}
                        data-testid="post-content-textarea"
                      />
                    </div>
                    
                    <div className="flex space-x-2">
                      <Button type="submit" data-testid="submit-post-button">
                        Publier
                      </Button>
                      <Button 
                        type="button" 
                        variant="outline"
                        onClick={() => setShowCreatePost(false)}
                      >
                        Annuler
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Posts List */}
          <div className="space-y-4" data-testid="posts-list">
            {filteredPosts.length === 0 ? (
              <Card className="text-center py-12">
                <CardContent>
                  <MessageCircle className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-600 mb-2">
                    {searchTerm ? 'Aucun résultat' : 'Aucun post pour le moment'}
                  </h3>
                  <p className="text-gray-500 mb-6">
                    {searchTerm 
                      ? 'Essayez avec d\'autres mots-clés'
                      : 'Soyez le premier à partager avec la communauté !'
                    }
                  </p>
                  {!searchTerm && (
                    <Button 
                      onClick={() => setShowCreatePost(true)}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      Créer le premier post
                    </Button>
                  )}
                </CardContent>
              </Card>
            ) : (
              filteredPosts.map((post, index) => (
                <motion.div
                  key={post.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="hover:shadow-lg transition-shadow duration-300">
                    <CardContent className="p-6">
                      <div className="flex items-start space-x-4">
                        <Avatar className="mt-1">
                          <AvatarImage src={post.user?.avatar_url} />
                          <AvatarFallback className="bg-blue-100 text-blue-600">
                            {post.user?.full_name?.charAt(0) || 'U'}
                          </AvatarFallback>
                        </Avatar>
                        
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h3 className="text-lg font-semibold text-gray-900 mb-1">
                                {post.title}
                              </h3>
                              <div className="flex items-center space-x-2 text-sm text-gray-500">
                                <span>{post.user?.full_name || 'Utilisateur'}</span>
                                <span>•</span>
                                <Calendar className="h-3 w-3" />
                                <span>{formatDate(post.created_at)}</span>
                              </div>
                            </div>
                            
                            <Badge className={getCategoryColor(post.category)}>
                              {categories.find(c => c.value === post.category)?.label || post.category}
                            </Badge>
                          </div>
                          
                          <p className="text-gray-700 mb-4 leading-relaxed">
                            {post.content.length > 200 
                              ? `${post.content.substring(0, 200)}...` 
                              : post.content
                            }
                          </p>
                          
                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <button className="flex items-center space-x-1 hover:text-red-500 transition-colors">
                              <Heart className="h-4 w-4" />
                              <span>{post.likes}</span>
                            </button>
                            
                            <button className="flex items-center space-x-1 hover:text-blue-500 transition-colors">
                              <Reply className="h-4 w-4" />
                              <span>{post.replies_count} réponse{post.replies_count > 1 ? 's' : ''}</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))
            )}
          </div>

          {/* Stats Footer */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-12"
          >
            <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
              <CardContent className="p-6">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-blue-600">{posts.length}</div>
                    <div className="text-sm text-gray-600">Posts actifs</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-green-600">1,200+</div>
                    <div className="text-sm text-gray-600">Membres</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-purple-600">24/7</div>
                    <div className="text-sm text-gray-600">Support</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-orange-600">500+</div>
                    <div className="text-sm text-gray-600">Experts actifs</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </>
  );
}

export default Forum;