import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { 
  Users, 
  DollarSign, 
  BookOpen, 
  TrendingUp,
  Activity,
  CreditCard,
  UserCheck,
  BarChart3,
  ArrowUpRight,
  ArrowDownRight,
  Eye,
  Settings
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [recentUsers, setRecentUsers] = useState([]);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [analyticsRes, usersRes, transactionsRes] = await Promise.all([
        axios.get(`${API}/admin/analytics`),
        axios.get(`${API}/admin/users?limit=5`),
        axios.get(`${API}/admin/transactions`)
      ]);

      setAnalytics(analyticsRes.data);
      setRecentUsers(usersRes.data.users);
      setRecentTransactions(transactionsRes.data.slice(0, 5));
    } catch (error) {
      console.error('Error fetching admin data:', error);
      toast.error('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-gray-300 rounded w-64"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-32 bg-gray-300 rounded-lg"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="h-96 bg-gray-300 rounded-lg"></div>
              <div className="h-96 bg-gray-300 rounded-lg"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!analytics) return null;

  const stats = [
    {
      title: "Utilisateurs Totaux",
      value: analytics.user_analytics.total_users,
      change: `+${analytics.user_analytics.new_users_this_week} cette semaine`,
      changeType: "positive",
      icon: <Users className="h-6 w-6" />,
      color: "text-blue-600",
      bgColor: "bg-blue-100"
    },
    {
      title: "Revenus Totaux",
      value: formatCurrency(analytics.revenue_analytics.total_revenue),
      change: `${formatCurrency(analytics.revenue_analytics.monthly_revenue)} ce mois`,
      changeType: "positive",
      icon: <DollarSign className="h-6 w-6" />,
      color: "text-green-600",
      bgColor: "bg-green-100"
    },
    {
      title: "Utilisateurs Premium",
      value: analytics.user_analytics.paid_users,
      change: `${analytics.course_analytics.conversion_rate.toFixed(1)}% conversion`,
      changeType: analytics.course_analytics.conversion_rate > 10 ? "positive" : "neutral",
      icon: <UserCheck className="h-6 w-6" />,
      color: "text-purple-600",
      bgColor: "bg-purple-100"
    },
    {
      title: "Taux de Completion",
      value: `${analytics.user_analytics.completion_rate.toFixed(1)}%`,
      change: `${analytics.course_analytics.total_completions} modules terminés`,
      changeType: analytics.user_analytics.completion_rate > 50 ? "positive" : "neutral",
      icon: <BookOpen className="h-6 w-6" />,
      color: "text-orange-600",
      bgColor: "bg-orange-100"
    }
  ];

  return (
    <>
      <Helmet>
        <title>Dashboard Admin - Inspecteur Auto</title>
        <meta name="description" content="Tableau de bord administrateur pour la plateforme Inspecteur Auto" />
      </Helmet>

      <div className="min-h-screen bg-gray-50" data-testid="admin-dashboard">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Dashboard Administrateur</h1>
                <p className="text-gray-600 mt-1">
                  Vue d'ensemble de la plateforme Inspecteur Auto
                </p>
              </div>
              
              <div className="flex space-x-3">
                <Button variant="outline" onClick={fetchData}>
                  <Activity className="h-4 w-4 mr-2" />
                  Actualiser
                </Button>
                <Link to="/admin/analytics">
                  <Button className="bg-blue-600 hover:bg-blue-700">
                    <BarChart3 className="h-4 w-4 mr-2" />
                    Analytics Détaillées
                  </Button>
                </Link>
              </div>
            </div>
          </motion.div>

          {/* Stats Cards */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          >
            {stats.map((stat, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                      <p className="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
                      <div className={`flex items-center mt-2 text-sm ${
                        stat.changeType === 'positive' ? 'text-green-600' : 
                        stat.changeType === 'negative' ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {stat.changeType === 'positive' && <ArrowUpRight className="h-3 w-3 mr-1" />}
                        {stat.changeType === 'negative' && <ArrowDownRight className="h-3 w-3 mr-1" />}
                        {stat.change}
                      </div>
                    </div>
                    <div className={`p-3 rounded-full ${stat.bgColor}`}>
                      <div className={stat.color}>
                        {stat.icon}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Users */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>Nouveaux Utilisateurs</CardTitle>
                    <CardDescription>
                      Dernières inscriptions sur la plateforme
                    </CardDescription>
                  </div>
                  <Link to="/admin/users">
                    <Button variant="outline" size="sm">
                      <Eye className="h-4 w-4 mr-2" />
                      Voir tout
                    </Button>
                  </Link>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentUsers.map((user) => (
                      <div key={user.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className="bg-blue-100 text-blue-600 rounded-full p-2">
                            <Users className="h-4 w-4" />
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{user.full_name}</p>
                            <p className="text-sm text-gray-500">{user.email}</p>
                          </div>
                        </div>
                        <div className="flex flex-col items-end">
                          <Badge variant={user.has_purchased ? "default" : "secondary"}>
                            {user.has_purchased ? "Premium" : "Gratuit"}
                          </Badge>
                          <span className="text-xs text-gray-500 mt-1">
                            {formatDate(user.created_at)}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Recent Transactions */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>Transactions Récentes</CardTitle>
                    <CardDescription>
                      Derniers paiements et achats
                    </CardDescription>
                  </div>
                  <Link to="/admin/transactions">
                    <Button variant="outline" size="sm">
                      <CreditCard className="h-4 w-4 mr-2" />
                      Voir tout
                    </Button>
                  </Link>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentTransactions.map((transaction) => (
                      <div key={transaction.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`rounded-full p-2 ${
                            transaction.payment_status === 'completed' 
                              ? 'bg-green-100 text-green-600' 
                              : 'bg-yellow-100 text-yellow-600'
                          }`}>
                            <CreditCard className="h-4 w-4" />
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">
                              {transaction.user?.full_name || 'Utilisateur inconnu'}
                            </p>
                            <p className="text-sm text-gray-500">
                              {transaction.user?.email || 'Email non disponible'}
                            </p>
                          </div>
                        </div>
                        <div className="flex flex-col items-end">
                          <span className="font-semibold text-gray-900">
                            {formatCurrency(transaction.amount)}
                          </span>
                          <Badge variant={
                            transaction.payment_status === 'completed' ? 'default' : 
                            transaction.payment_status === 'pending' ? 'secondary' : 'destructive'
                          }>
                            {transaction.payment_status === 'completed' ? 'Payé' : 
                             transaction.payment_status === 'pending' ? 'En attente' : 'Échoué'}
                          </Badge>
                          <span className="text-xs text-gray-500 mt-1">
                            {formatDate(transaction.created_at)}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mt-8"
          >
            <Card>
              <CardHeader>
                <CardTitle>Actions Rapides</CardTitle>
                <CardDescription>
                  Accédez rapidement aux fonctions d'administration
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Link to="/admin/users">
                    <Button variant="outline" className="w-full h-20 flex flex-col">
                      <Users className="h-6 w-6 mb-2" />
                      Gérer les Utilisateurs
                    </Button>
                  </Link>
                  
                  <Link to="/admin/transactions">
                    <Button variant="outline" className="w-full h-20 flex flex-col">
                      <CreditCard className="h-6 w-6 mb-2" />
                      Voir les Transactions
                    </Button>
                  </Link>
                  
                  <Link to="/admin/analytics">
                    <Button variant="outline" className="w-full h-20 flex flex-col">
                      <BarChart3 className="h-6 w-6 mb-2" />
                      Analytics Détaillées
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </>
  );
}

export default AdminDashboard;