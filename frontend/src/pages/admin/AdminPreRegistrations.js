import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { 
  Loader2, 
  CheckCircle, 
  XCircle, 
  Eye, 
  Phone, 
  Mail, 
  Calendar,
  User,
  MessageSquare,
  Clock,
  Filter,
  Search,
  Trash2,
  PhoneCall,
  PhoneOff,
  ThumbsUp,
  ThumbsDown,
  UserCheck
} from 'lucide-react';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Statuts de rappel avec couleurs et icônes
const CALLBACK_STATUSES = {
  pending: { label: 'À rappeler', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
  called: { label: 'Appelé', color: 'bg-blue-100 text-blue-800', icon: PhoneCall },
  interested: { label: 'Intéressé', color: 'bg-green-100 text-green-800', icon: ThumbsUp },
  not_interested: { label: 'Pas intéressé', color: 'bg-red-100 text-red-800', icon: ThumbsDown },
  no_answer: { label: 'Ne répond pas', color: 'bg-gray-100 text-gray-800', icon: PhoneOff },
  converted: { label: 'Converti', color: 'bg-purple-100 text-purple-800', icon: UserCheck }
};

export default function AdminPreRegistrations() {
  const [prospects, setProspects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProspect, setSelectedProspect] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [callbackNotes, setCallbackNotes] = useState('');
  const [callbackStatus, setCallbackStatus] = useState('');

  useEffect(() => {
    fetchProspects();
  }, []);

  const fetchProspects = async () => {
    try {
      const response = await axios.get(`${API}/admin/pre-registrations`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setProspects(response.data);
    } catch (error) {
      console.error('Error fetching prospects:', error);
      toast.error('Erreur lors du chargement des prospects');
    } finally {
      setLoading(false);
    }
  };

  const updateCallbackStatus = async () => {
    if (!selectedProspect || !callbackStatus) return;
    
    try {
      await axios.patch(
        `${API}/admin/pre-registrations/${selectedProspect.id}/callback`,
        { callback_status: callbackStatus, callback_notes: callbackNotes },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}
      );
      
      toast.success('Statut mis à jour');
      setShowModal(false);
      setSelectedProspect(null);
      setCallbackNotes('');
      setCallbackStatus('');
      fetchProspects();
    } catch (error) {
      console.error('Error updating status:', error);
      toast.error('Erreur lors de la mise à jour');
    }
  };

  const deleteProspect = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce prospect ?')) return;
    
    try {
      await axios.delete(`${API}/admin/pre-registrations/${id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      toast.success('Prospect supprimé');
      fetchProspects();
    } catch (error) {
      console.error('Error deleting prospect:', error);
      toast.error('Erreur lors de la suppression');
    }
  };

  const openCallbackModal = (prospect) => {
    setSelectedProspect(prospect);
    setCallbackStatus(prospect.callback_status || 'pending');
    setCallbackNotes(prospect.callback_notes || '');
    setShowModal(true);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatPhone = (phone) => {
    if (!phone) return 'Non renseigné';
    // Format French phone number
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) {
      return cleaned.replace(/(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/, '$1 $2 $3 $4 $5');
    }
    return phone;
  };

  // Filtrage des prospects
  const filteredProspects = prospects.filter(p => {
    const matchesStatus = filterStatus === 'all' || (p.callback_status || 'pending') === filterStatus;
    const matchesSearch = 
      p.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.phone?.includes(searchTerm);
    return matchesStatus && matchesSearch;
  });

  // Statistiques
  const stats = {
    total: prospects.length,
    pending: prospects.filter(p => !p.callback_status || p.callback_status === 'pending').length,
    interested: prospects.filter(p => p.callback_status === 'interested').length,
    converted: prospects.filter(p => p.callback_status === 'converted').length
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Gestion des Prospects</h1>
          <p className="text-gray-600 mt-2">
            Suivez et rappelez les personnes ayant rempli le questionnaire de pré-inscription
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Prospects</p>
                  <p className="text-3xl font-bold">{stats.total}</p>
                </div>
                <User className="h-10 w-10 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-l-4 border-l-yellow-500">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">À Rappeler</p>
                  <p className="text-3xl font-bold text-yellow-600">{stats.pending}</p>
                </div>
                <Phone className="h-10 w-10 text-yellow-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-l-4 border-l-green-500">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Intéressés</p>
                  <p className="text-3xl font-bold text-green-600">{stats.interested}</p>
                </div>
                <ThumbsUp className="h-10 w-10 text-green-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-l-4 border-l-purple-500">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Convertis</p>
                  <p className="text-3xl font-bold text-purple-600">{stats.converted}</p>
                </div>
                <UserCheck className="h-10 w-10 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="py-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Rechercher par nom, email ou téléphone..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-gray-500" />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Tous les statuts</option>
                  {Object.entries(CALLBACK_STATUSES).map(([key, value]) => (
                    <option key={key} value={key}>{value.label}</option>
                  ))}
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Prospects List */}
        {filteredProspects.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <User className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">
                {prospects.length === 0 
                  ? "Aucun prospect pour le moment" 
                  : "Aucun prospect ne correspond à vos critères"}
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredProspects.map((prospect) => {
              const status = CALLBACK_STATUSES[prospect.callback_status || 'pending'];
              const StatusIcon = status.icon;
              
              return (
                <Card key={prospect.id} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      {/* Info principale */}
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-xl font-semibold text-gray-900">
                            {prospect.full_name}
                          </h3>
                          <Badge className={status.color}>
                            <StatusIcon className="h-3 w-3 mr-1" />
                            {status.label}
                          </Badge>
                          {prospect.profile_validated && (
                            <Badge className="bg-green-100 text-green-800">
                              <CheckCircle className="h-3 w-3 mr-1" />
                              Validé
                            </Badge>
                          )}
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm">
                          <div className="flex items-center gap-2 text-gray-600">
                            <Phone className="h-4 w-4" />
                            <a 
                              href={`tel:${prospect.phone}`} 
                              className="hover:text-blue-600 font-medium"
                            >
                              {formatPhone(prospect.phone)}
                            </a>
                          </div>
                          <div className="flex items-center gap-2 text-gray-600">
                            <Mail className="h-4 w-4" />
                            <a 
                              href={`mailto:${prospect.email}`}
                              className="hover:text-blue-600"
                            >
                              {prospect.email}
                            </a>
                          </div>
                          <div className="flex items-center gap-2 text-gray-500">
                            <Calendar className="h-4 w-4" />
                            {formatDate(prospect.created_at)}
                          </div>
                        </div>
                        
                        {prospect.callback_notes && (
                          <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                            <div className="flex items-start gap-2">
                              <MessageSquare className="h-4 w-4 text-gray-400 mt-0.5" />
                              <p className="text-sm text-gray-600">{prospect.callback_notes}</p>
                            </div>
                          </div>
                        )}
                      </div>
                      
                      {/* Actions */}
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => openCallbackModal(prospect)}
                          className="flex items-center gap-1"
                        >
                          <Phone className="h-4 w-4" />
                          Mettre à jour
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => deleteProspect(prospect.id)}
                          className="text-red-500 hover:text-red-700 hover:bg-red-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {/* Modal de mise à jour du statut */}
        {showModal && selectedProspect && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Phone className="h-5 w-5" />
                  Suivi de {selectedProspect.full_name}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Téléphone</p>
                  <a 
                    href={`tel:${selectedProspect.phone}`}
                    className="text-lg font-semibold text-blue-600 hover:underline"
                  >
                    {formatPhone(selectedProspect.phone)}
                  </a>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Statut du rappel
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(CALLBACK_STATUSES).map(([key, value]) => {
                      const Icon = value.icon;
                      return (
                        <button
                          key={key}
                          onClick={() => setCallbackStatus(key)}
                          className={`flex items-center gap-2 p-3 rounded-lg border-2 transition-all ${
                            callbackStatus === key 
                              ? 'border-blue-500 bg-blue-50' 
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <Icon className="h-4 w-4" />
                          <span className="text-sm font-medium">{value.label}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Notes (résumé de l'appel)
                  </label>
                  <textarea
                    value={callbackNotes}
                    onChange={(e) => setCallbackNotes(e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Ex: Intéressé, souhaite rappeler la semaine prochaine..."
                  />
                </div>
                
                <div className="flex gap-2 pt-4">
                  <Button 
                    variant="outline" 
                    onClick={() => {
                      setShowModal(false);
                      setSelectedProspect(null);
                    }}
                    className="flex-1"
                  >
                    Annuler
                  </Button>
                  <Button 
                    onClick={updateCallbackStatus}
                    className="flex-1"
                    disabled={!callbackStatus}
                  >
                    Enregistrer
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
