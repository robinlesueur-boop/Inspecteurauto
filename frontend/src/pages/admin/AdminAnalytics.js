import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Loader2, Users, BookOpen, TrendingUp, DollarSign, Award, Eye } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function AdminAnalytics() {
  const [analytics, setAnalytics] = useState(null);
  const [courseProgress, setCourseProgress] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
    fetchCourseProgress();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API}/admin/analytics`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCourseProgress = async () => {
    try {
      const response = await axios.get(`${API}/admin/course-progress`);
      setCourseProgress(response.data);
    } catch (error) {
      console.error('Error fetching course progress:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-gray-600 mt-2">Vue d'ensemble des performances de la plateforme</p>
      </div>

      {/* User Analytics */}
      {analytics?.user_analytics && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Utilisateurs</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Utilisateurs</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.user_analytics.total_users}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Nouveaux aujourd'hui</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">
                  +{analytics.user_analytics.new_users_today}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Cette semaine</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">
                  +{analytics.user_analytics.new_users_this_week}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Utilisateurs payants</CardTitle>
                <Award className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-600">
                  {analytics.user_analytics.paid_users}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  {analytics.course_analytics.conversion_rate.toFixed(1)}% conversion
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Course Analytics */}
      {analytics?.course_analytics && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Formation</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Modules</CardTitle>
                <BookOpen className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.course_analytics.total_modules}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Complétions totales</CardTitle>
                <Award className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.course_analytics.total_completions}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Taux de complétion</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {analytics.user_analytics.completion_rate.toFixed(1)}%
                </div>
              </CardContent>
            </Card>
          </div>

          {analytics.course_analytics.most_popular_module !== "N/A" && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle className="text-sm font-medium">Module le plus populaire</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <Eye className="h-5 w-5 text-blue-600" />
                  <span className="text-lg font-semibold">{analytics.course_analytics.most_popular_module}</span>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Revenue Analytics */}
      {analytics?.revenue_analytics && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Revenus</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Revenu total</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">
                  {analytics.revenue_analytics.total_revenue}€
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Revenu mensuel</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">
                  {analytics.revenue_analytics.monthly_revenue}€
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Panier moyen</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {analytics.revenue_analytics.average_order_value}€
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Course Progress Details */}
      {courseProgress.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Progression par module</h2>
          <Card>
            <CardHeader>
              <CardTitle>Statistiques détaillées</CardTitle>
              <CardDescription>Performance de chaque module de formation</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-4">Module</th>
                      <th className="text-left p-4">Tentatives</th>
                      <th className="text-left p-4">Complétés</th>
                      <th className="text-left p-4">Taux de complétion</th>
                      <th className="text-left p-4">Temps moyen</th>
                    </tr>
                  </thead>
                  <tbody>
                    {courseProgress.map((stat, index) => (
                      <tr key={index} className="border-b hover:bg-gray-50">
                        <td className="p-4 font-medium">{stat.module_title || 'Module inconnu'}</td>
                        <td className="p-4">{stat.total_attempts}</td>
                        <td className="p-4 text-green-600 font-semibold">{stat.completed}</td>
                        <td className="p-4">
                          <div className="flex items-center gap-2">
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-blue-600 h-2 rounded-full"
                                style={{ width: `${stat.completion_rate}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium">{stat.completion_rate.toFixed(0)}%</span>
                          </div>
                        </td>
                        <td className="p-4">{stat.avg_reading_time.toFixed(0)} min</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
