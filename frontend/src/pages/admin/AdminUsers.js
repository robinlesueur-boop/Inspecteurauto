import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogHeader, 
  DialogTitle 
} from '../../components/ui/dialog';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { 
  Users, 
  Search, 
  Filter,
  Eye,
  Edit,
  UserCheck,
  UserX,
  Shield,
  ShieldCheck,
  Calendar,
  Mail,
  TrendingUp,
  ArrowLeft
} from 'lucide-react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [pagination, setPagination] = useState({});
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showUserModal, setShowUserModal] = useState(false);
  const [updatingUser, setUpdatingUser] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, [currentPage, searchTerm]);

  const fetchUsers = async () => {
    try {
      const params = {
        page: currentPage,
        limit: 20
      };
      if (searchTerm) {
        params.search = searchTerm;
      }

      const response = await axios.get(`${API}/admin/users`, { params });
      setUsers(response.data.users);
      setPagination(response.data.pagination);
    } catch (error) {
      console.error('Error fetching users:', error);
      toast.error('Erreur lors du chargement des utilisateurs');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const handleUserClick = (user) => {
    setSelectedUser(user);
    setShowUserModal(true);
  };

  const toggleUserAccess = async (userId, currentStatus) => {
    setUpdatingUser(true);
    try {
      await axios.put(`${API}/admin/users/${userId}`, {
        has_purchased: !currentStatus
      });
      
      toast.success(`Accès ${!currentStatus ? 'accordé' : 'révoqué'} avec succès`);
      fetchUsers();
      setShowUserModal(false);
    } catch (error) {
      console.error('Error updating user:', error);
      toast.error('Erreur lors de la modification');
    } finally {
      setUpdatingUser(false);
    }
  };

  const toggleAdminRole = async (userId, currentStatus) => {
    setUpdatingUser(true);
    try {
      await axios.put(`${API}/admin/users/${userId}`, {
        is_admin: !currentStatus
      });
      
      toast.success(`Rôle admin ${!currentStatus ? 'accordé' : 'révoqué'} avec succès`);
      fetchUsers();
      setShowUserModal(false);
    } catch (error) {
      console.error('Error updating user role:', error);
      toast.error('Erreur lors de la modification du rôle');
    } finally {
      setUpdatingUser(false);
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

  const getProgressColor = (percentage) => {
    if (percentage >= 100) return 'text-green-600 bg-green-100';
    if (percentage >= 50) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-gray-300 rounded w-64"></div>
            <div className="h-12 bg-gray-300 rounded"></div>
            <div className="space-y-4">
              {[...Array(10)].map((_, i) => (
                <div key={i} className="h-16 bg-gray-300 rounded"></div>
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
        <title>Gestion Utilisateurs - Admin Inspecteur Auto</title>
        <meta name="description" content="Gérez tous les utilisateurs de la plateforme Inspecteur Auto" />
      </Helmet>

      <div className="min-h-screen bg-gray-50" data-testid="admin-users">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <div className="flex items-center mb-2">
                  <Link to="/admin" className="text-gray-500 hover:text-gray-700 mr-2">
                    <ArrowLeft className="h-4 w-4" />
                  </Link>
                  <h1 className="text-3xl font-bold text-gray-900">Gestion des Utilisateurs</h1>
                </div>
                <p className="text-gray-600">
                  Gérez tous les utilisateurs inscrits sur la plateforme
                </p>
              </div>
              
              <div className="flex items-center space-x-4">
                <Badge variant="outline" className="text-lg py-2 px-4">
                  <Users className="h-4 w-4 mr-2" />
                  {pagination.total_users || 0} utilisateurs
                </Badge>
              </div>
            </div>
          </motion.div>

          {/* Search and Filters */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-6"
          >
            <Card>
              <CardContent className="p-4">
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <Input
                      placeholder="Rechercher par nom, email ou nom d'utilisateur..."
                      value={searchTerm}
                      onChange={handleSearch}
                      className="pl-10"
                      data-testid="search-users"
                    />
                  </div>
                  
                  <Button variant="outline" onClick={fetchUsers}>
                    <Filter className="h-4 w-4 mr-2" />
                    Actualiser
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Users List */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Utilisateurs Inscrits</CardTitle>
                <CardDescription>
                  Page {pagination.current_page} sur {pagination.total_pages} 
                  ({pagination.total_users} utilisateurs au total)
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                {users.length === 0 ? (
                  <div className="text-center py-12">
                    <Users className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-gray-600 mb-2">
                      Aucun utilisateur trouvé
                    </h3>
                    <p className="text-gray-500">
                      Essayez de modifier vos critères de recherche
                    </p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-200">
                    {users.map((user, index) => (
                      <motion.div
                        key={user.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className="p-6 hover:bg-gray-50 transition-colors cursor-pointer"
                        onClick={() => handleUserClick(user)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4">
                            <Avatar className="h-12 w-12">
                              <AvatarImage src={user.avatar_url} />
                              <AvatarFallback className="bg-blue-100 text-blue-600">
                                {user.full_name?.charAt(0) || 'U'}
                              </AvatarFallback>
                            </Avatar>
                            
                            <div>
                              <div className="flex items-center space-x-2">
                                <h3 className="font-semibold text-gray-900">{user.full_name}</h3>
                                {user.is_admin && (
                                  <Badge className="bg-red-100 text-red-700">
                                    <Shield className="h-3 w-3 mr-1" />
                                    Admin
                                  </Badge>
                                )}
                                {user.has_purchased && (
                                  <Badge className="bg-green-100 text-green-700">
                                    <UserCheck className="h-3 w-3 mr-1" />
                                    Premium
                                  </Badge>
                                )}
                              </div>
                              <p className="text-gray-600">{user.email}</p>
                              <p className="text-sm text-gray-500">@{user.username}</p>
                            </div>
                          </div>

                          <div className="flex items-center space-x-6">
                            {/* Progress */}
                            <div className="text-center">
                              <div className={`text-sm font-semibold px-2 py-1 rounded ${getProgressColor(user.progress?.completion_percentage || 0)}`}>
                                {user.progress?.completion_percentage?.toFixed(0) || 0}%
                              </div>
                              <p className="text-xs text-gray-500 mt-1">
                                {user.progress?.completed_modules || 0}/{user.progress?.total_modules || 0} modules
                              </p>
                            </div>

                            {/* Registration Date */}
                            <div className="text-right">
                              <div className="flex items-center text-sm text-gray-600">
                                <Calendar className="h-4 w-4 mr-1" />
                                {formatDate(user.created_at)}
                              </div>
                              {user.last_login && (
                                <p className="text-xs text-gray-500 mt-1">
                                  Dernière connexion: {formatDate(user.last_login)}
                                </p>
                              )}
                            </div>

                            {/* Actions */}
                            <div className="flex space-x-2">
                              <Button variant="outline" size="sm">
                                <Eye className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Pagination */}
          {pagination.total_pages > 1 && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="mt-6 flex justify-center space-x-2"
            >
              <Button
                variant="outline"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(currentPage - 1)}
              >
                Précédent
              </Button>
              
              <div className="flex items-center space-x-2">
                {Array.from({ length: Math.min(5, pagination.total_pages) }, (_, i) => {
                  const page = i + 1;
                  return (
                    <Button
                      key={page}
                      variant={page === currentPage ? "default" : "outline"}
                      size="sm"
                      onClick={() => setCurrentPage(page)}
                    >
                      {page}
                    </Button>
                  );
                })}
              </div>

              <Button
                variant="outline"
                disabled={currentPage === pagination.total_pages}
                onClick={() => setCurrentPage(currentPage + 1)}
              >
                Suivant
              </Button>
            </motion.div>
          )}
        </div>

        {/* User Detail Modal */}
        <Dialog open={showUserModal} onOpenChange={setShowUserModal}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Détails de l'utilisateur</DialogTitle>
              <DialogDescription>
                Gérez les permissions et informations de l'utilisateur
              </DialogDescription>
            </DialogHeader>

            {selectedUser && (
              <div className="space-y-6">
                {/* User Info */}
                <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                  <Avatar className="h-16 w-16">
                    <AvatarImage src={selectedUser.avatar_url} />
                    <AvatarFallback className="bg-blue-100 text-blue-600 text-xl">
                      {selectedUser.full_name?.charAt(0) || 'U'}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <h3 className="text-xl font-semibold">{selectedUser.full_name}</h3>
                    <p className="text-gray-600">{selectedUser.email}</p>
                    <p className="text-sm text-gray-500">@{selectedUser.username}</p>
                    <div className="flex items-center space-x-2 mt-2">
                      {selectedUser.is_admin && (
                        <Badge className="bg-red-100 text-red-700">
                          <Shield className="h-3 w-3 mr-1" />
                          Administrateur
                        </Badge>
                      )}
                      {selectedUser.has_purchased && (
                        <Badge className="bg-green-100 text-green-700">
                          <UserCheck className="h-3 w-3 mr-1" />
                          Premium
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>

                {/* Progress Info */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-blue-900 mb-2">Progression</h4>
                    <div className="text-2xl font-bold text-blue-600">
                      {selectedUser.progress?.completion_percentage?.toFixed(0) || 0}%
                    </div>
                    <p className="text-sm text-blue-700">
                      {selectedUser.progress?.completed_modules || 0}/{selectedUser.progress?.total_modules || 0} modules terminés
                    </p>
                  </div>

                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-green-900 mb-2">Statut</h4>
                    <div className="text-sm text-green-700">
                      <p>Inscrit le : {formatDate(selectedUser.created_at)}</p>
                      {selectedUser.last_login && (
                        <p>Dernière connexion : {formatDate(selectedUser.last_login)}</p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col space-y-3 pt-4 border-t">
                  <h4 className="font-semibold text-gray-900">Actions administrateur</h4>
                  
                  <div className="flex space-x-3">
                    <Button
                      onClick={() => toggleUserAccess(selectedUser.id, selectedUser.has_purchased)}
                      disabled={updatingUser}
                      variant={selectedUser.has_purchased ? "destructive" : "default"}
                      className="flex-1"
                    >
                      {updatingUser ? (
                        <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full" />
                      ) : selectedUser.has_purchased ? (
                        <UserX className="h-4 w-4 mr-2" />
                      ) : (
                        <UserCheck className="h-4 w-4 mr-2" />
                      )}
                      {selectedUser.has_purchased ? 'Révoquer Accès Premium' : 'Accorder Accès Premium'}
                    </Button>

                    <Button
                      onClick={() => toggleAdminRole(selectedUser.id, selectedUser.is_admin)}
                      disabled={updatingUser}
                      variant={selectedUser.is_admin ? "destructive" : "outline"}
                      className="flex-1"
                    >
                      {updatingUser ? (
                        <div className="animate-spin h-4 w-4 mr-2 border-2 border-gray-600 border-t-transparent rounded-full" />
                      ) : selectedUser.is_admin ? (
                        <Shield className="h-4 w-4 mr-2" />
                      ) : (
                        <ShieldCheck className="h-4 w-4 mr-2" />
                      )}
                      {selectedUser.is_admin ? 'Retirer Admin' : 'Promouvoir Admin'}
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </>
  );
}

export default AdminUsers;