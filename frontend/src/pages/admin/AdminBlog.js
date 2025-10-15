import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Badge } from '../../components/ui/badge';
import { Plus, Edit, Trash2, Eye, EyeOff, Save, X } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminBlog() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingPost, setEditingPost] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    excerpt: '',
    content: '',
    author: 'Équipe Inspecteur Auto',
    category: 'Technique',
    image_url: '',
    published: false
  });

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await axios.get(`${API}/admin/blog/posts`);
      setPosts(response.data || []);
    } catch (error) {
      console.error('Error fetching posts:', error);
      toast.error('Erreur lors du chargement des articles');
    } finally {
      setLoading(false);
    }
  };

  const generateSlug = (title) => {
    return title
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');
  };

  const handleTitleChange = (title) => {
    setFormData({
      ...formData,
      title,
      slug: generateSlug(title)
    });
  };

  const handleCreate = () => {
    setIsCreating(true);
    setEditingPost(null);
    setFormData({
      title: '',
      slug: '',
      excerpt: '',
      content: '',
      author: 'Équipe Inspecteur Auto',
      category: 'Technique',
      image_url: 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&q=80',
      published: false
    });
  };

  const handleEdit = (post) => {
    setEditingPost(post);
    setIsCreating(false);
    setFormData({
      title: post.title,
      slug: post.slug,
      excerpt: post.excerpt,
      content: post.content,
      author: post.author,
      category: post.category,
      image_url: post.image_url,
      published: post.published
    });
  };

  const handleCancel = () => {
    setEditingPost(null);
    setIsCreating(false);
    setFormData({
      title: '',
      slug: '',
      excerpt: '',
      content: '',
      author: 'Équipe Inspecteur Auto',
      category: 'Technique',
      image_url: '',
      published: false
    });
  };

  const handleSave = async () => {
    if (!formData.title.trim() || !formData.excerpt.trim() || !formData.content.trim()) {
      toast.error('Titre, extrait et contenu sont obligatoires');
      return;
    }

    try {
      setSaving(true);

      if (isCreating) {
        // Create new post
        await axios.post(`${API}/admin/blog/posts`, formData);
        toast.success('Article créé avec succès !');
      } else {
        // Update existing post
        await axios.put(`${API}/admin/blog/posts/${editingPost.id}`, formData);
        toast.success('Article mis à jour avec succès !');
      }

      await fetchPosts();
      handleCancel();
    } catch (error) {
      console.error('Error saving post:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (postId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cet article ?')) return;

    try {
      await axios.delete(`${API}/admin/blog/posts/${postId}`);
      toast.success('Article supprimé');
      await fetchPosts();
    } catch (error) {
      console.error('Error deleting post:', error);
      toast.error('Erreur lors de la suppression');
    }
  };

  const handleTogglePublish = async (postId, currentStatus) => {
    try {
      await axios.patch(`${API}/admin/blog/posts/${postId}/publish`, null, {
        params: { published: !currentStatus }
      });
      toast.success(!currentStatus ? 'Article publié' : 'Article dépublié');
      await fetchPosts();
    } catch (error) {
      console.error('Error toggling publish:', error);
      toast.error('Erreur');
    }
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

  if (isCreating || editingPost) {
    return (
      <>
        <Helmet>
          <title>{isCreating ? 'Nouvel Article' : 'Éditer Article'} - Admin</title>
        </Helmet>

        <div className="min-h-screen bg-gray-50 py-8">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  {isCreating ? 'Nouvel Article de Blog' : 'Éditer l\'Article'}
                </h1>
              </div>
              <Button onClick={handleCancel} variant="outline">
                <X className="w-4 h-4 mr-2" />
                Annuler
              </Button>
            </div>

            <Card>
              <CardContent className="p-6 space-y-6">
                {/* Title */}
                <div className="space-y-2">
                  <Label htmlFor="title">Titre de l'Article *</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => handleTitleChange(e.target.value)}
                    placeholder="Ex: Les 10 points essentiels d'une inspection automobile"
                  />
                </div>

                {/* Slug */}
                <div className="space-y-2">
                  <Label htmlFor="slug">Slug (URL) *</Label>
                  <Input
                    id="slug"
                    value={formData.slug}
                    onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                    placeholder="les-10-points-essentiels"
                  />
                  <p className="text-sm text-gray-500">URL de l'article : /blog/{formData.slug}</p>
                </div>

                {/* Excerpt */}
                <div className="space-y-2">
                  <Label htmlFor="excerpt">Extrait (résumé) *</Label>
                  <Textarea
                    id="excerpt"
                    value={formData.excerpt}
                    onChange={(e) => setFormData({ ...formData, excerpt: e.target.value })}
                    placeholder="Court résumé de l'article (150-200 caractères)"
                    rows={3}
                  />
                  <p className="text-sm text-gray-500">{formData.excerpt.length} caractères</p>
                </div>

                {/* Content */}
                <div className="space-y-2">
                  <Label htmlFor="content">Contenu Complet *</Label>
                  <Textarea
                    id="content"
                    value={formData.content}
                    onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                    placeholder="Contenu de l'article en HTML ou texte"
                    rows={20}
                    className="font-mono text-sm"
                  />
                  <p className="text-sm text-gray-500">
                    Vous pouvez utiliser du HTML : &lt;h2&gt;, &lt;p&gt;, &lt;ul&gt;, &lt;strong&gt;, etc.
                  </p>
                </div>

                {/* Author & Category */}
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="author">Auteur</Label>
                    <Input
                      id="author"
                      value={formData.author}
                      onChange={(e) => setFormData({ ...formData, author: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="category">Catégorie</Label>
                    <select
                      id="category"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                    >
                      <option value="Technique">Technique</option>
                      <option value="Carrière">Carrière</option>
                      <option value="Marché">Marché</option>
                      <option value="Technologie">Technologie</option>
                      <option value="Business">Business</option>
                      <option value="Actualité">Actualité</option>
                    </select>
                  </div>
                </div>

                {/* Image URL */}
                <div className="space-y-2">
                  <Label htmlFor="image_url">URL de l'Image</Label>
                  <Input
                    id="image_url"
                    value={formData.image_url}
                    onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                    placeholder="https://images.unsplash.com/..."
                  />
                  {formData.image_url && (
                    <img
                      src={formData.image_url}
                      alt="Aperçu"
                      className="mt-2 w-full max-w-md rounded-lg"
                      onError={(e) => e.target.style.display = 'none'}
                    />
                  )}
                </div>

                {/* Published Toggle */}
                <div className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg">
                  <input
                    type="checkbox"
                    id="published"
                    checked={formData.published}
                    onChange={(e) => setFormData({ ...formData, published: e.target.checked })}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <Label htmlFor="published" className="cursor-pointer">
                    Publier l'article immédiatement
                  </Label>
                </div>

                {/* Actions */}
                <div className="flex justify-end space-x-4 pt-4 border-t">
                  <Button onClick={handleCancel} variant="outline" disabled={saving}>
                    Annuler
                  </Button>
                  <Button onClick={handleSave} disabled={saving} className="bg-blue-600 hover:bg-blue-700">
                    {saving ? (
                      <>
                        <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                        Sauvegarde...
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4 mr-2" />
                        {isCreating ? 'Créer l\'Article' : 'Sauvegarder'}
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

  return (
    <>
      <Helmet>
        <title>Gestion du Blog - Admin</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Gestion du Blog</h1>
              <p className="text-gray-600 mt-2">{posts.length} article{posts.length > 1 ? 's' : ''}</p>
            </div>
            <Button onClick={handleCreate} className="bg-blue-600 hover:bg-blue-700">
              <Plus className="w-4 h-4 mr-2" />
              Nouvel Article
            </Button>
          </div>

          {posts.length === 0 ? (
            <Card>
              <CardContent className="text-center py-12">
                <p className="text-gray-500">Aucun article pour le moment</p>
                <Button onClick={handleCreate} className="mt-4">
                  Créer le premier article
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-6">
              {posts.map((post) => (
                <Card key={post.id} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-xl font-semibold text-gray-900">{post.title}</h3>
                          {post.published ? (
                            <Badge className="bg-green-100 text-green-800">Publié</Badge>
                          ) : (
                            <Badge className="bg-gray-100 text-gray-800">Brouillon</Badge>
                          )}
                          <Badge variant="outline">{post.category}</Badge>
                        </div>
                        <p className="text-gray-600 text-sm mb-3">{post.excerpt}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span>Par {post.author}</span>
                          <span>•</span>
                          <span>{new Date(post.created_at).toLocaleDateString('fr-FR')}</span>
                          <span>•</span>
                          <span className="text-blue-600">/blog/{post.slug}</span>
                        </div>
                      </div>

                      <div className="flex space-x-2 ml-4">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleTogglePublish(post.id, post.published)}
                        >
                          {post.published ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleEdit(post)}
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDelete(post.id)}
                          className="text-red-600 hover:bg-red-50"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default AdminBlog;
