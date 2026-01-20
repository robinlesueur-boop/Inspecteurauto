import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { Textarea } from '../../components/ui/textarea';
import { 
  Users, 
  Clock, 
  CheckCircle, 
  AlertTriangle, 
  Search,
  Mail,
  Eye,
  FileCheck,
  XCircle,
  Loader2,
  GraduationCap,
  RefreshCw
} from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AdminStudentProgress() {
  const [students, setStudents] = useState([]);
  const [pendingValidations, setPendingValidations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [validationNotes, setValidationNotes] = useState('');
  const [weproovCode, setWeproovCode] = useState('');
  const [inspectionNotes, setInspectionNotes] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [progressRes, pendingRes] = await Promise.all([
        axios.get(`${API}/admin/students/progress`),
        axios.get(`${API}/admin/students/pending-validation`)
      ]);
      setStudents(progressRes.data);
      setPendingValidations(pendingRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const handleValidateProject = async (userId, validated) => {
    setActionLoading(true);
    try {
      await axios.post(`${API}/admin/students/${userId}/validate?validated=${validated}&notes=${encodeURIComponent(validationNotes)}`);
      toast.success(validated ? 'Projet validé !' : 'Projet refusé');
      setSelectedStudent(null);
      setValidationNotes('');
      fetchData();
    } catch (error) {
      toast.error('Erreur lors de la validation');
    } finally {
      setActionLoading(false);
    }
  };

  const handleSetWeproovCode = async (userId) => {
    if (!weproovCode.trim()) {
      toast.error('Veuillez entrer un code Weproov');
      return;
    }
    setActionLoading(true);
    try {
      await axios.post(`${API}/admin/students/${userId}/weproov-code?code=${encodeURIComponent(weproovCode)}`);
      toast.success('Code Weproov attribué !');
      setWeproovCode('');
      fetchData();
    } catch (error) {
      toast.error('Erreur lors de l\'attribution du code');
    } finally {
      setActionLoading(false);
    }
  };

  const handleValidateInspection = async (userId, validated) => {
    setActionLoading(true);
    try {
      await axios.post(`${API}/admin/students/${userId}/validate-inspection?validated=${validated}&notes=${encodeURIComponent(inspectionNotes)}`);
      toast.success(validated ? 'Inspection validée !' : 'Inspection refusée');
      setInspectionNotes('');
      fetchData();
    } catch (error) {
      toast.error('Erreur lors de la validation');
    } finally {
      setActionLoading(false);
    }
  };

  const filteredStudents = students.filter(s => 
    s.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const inactiveStudents = filteredStudents.filter(s => s.needs_reminder);
  const activeStudents = filteredStudents.filter(s => !s.needs_reminder);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Suivi des Élèves - Admin</title>
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <GraduationCap className="h-6 w-6 text-blue-600" />
                Suivi des Élèves
              </h1>
              <p className="text-gray-600 mt-1">Validation des projets, progression et inspections</p>
            </div>
            <Button onClick={fetchData} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Actualiser
            </Button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Élèves</p>
                    <p className="text-2xl font-bold">{students.length}</p>
                  </div>
                  <Users className="h-8 w-8 text-blue-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card className="border-yellow-200 bg-yellow-50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-yellow-700">En attente validation</p>
                    <p className="text-2xl font-bold text-yellow-800">{pendingValidations.length}</p>
                  </div>
                  <Clock className="h-8 w-8 text-yellow-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card className="border-red-200 bg-red-50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-red-700">Inactifs (+10j)</p>
                    <p className="text-2xl font-bold text-red-800">{inactiveStudents.length}</p>
                  </div>
                  <AlertTriangle className="h-8 w-8 text-red-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card className="border-green-200 bg-green-50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-green-700">Validés</p>
                    <p className="text-2xl font-bold text-green-800">
                      {students.filter(s => s.is_validated).length}
                    </p>
                  </div>
                  <CheckCircle className="h-8 w-8 text-green-600" />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Pending Validations */}
          {pendingValidations.length > 0 && (
            <Card className="mb-8 border-yellow-300">
              <CardHeader>
                <CardTitle className="text-yellow-800 flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Projets en attente de validation ({pendingValidations.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {pendingValidations.map(student => (
                    <div key={student.id} className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-semibold">{student.full_name}</h4>
                          <p className="text-sm text-gray-600">{student.email}</p>
                          {student.professional_project && (
                            <div className="mt-2 p-3 bg-white rounded border">
                              <p className="text-sm font-medium text-gray-700">Projet professionnel :</p>
                              <p className="text-sm text-gray-600 mt-1">{student.professional_project}</p>
                            </div>
                          )}
                          {student.has_disability && student.has_disability !== 'non' && (
                            <Badge className="mt-2 bg-purple-100 text-purple-800">
                              Situation handicap : {student.has_disability}
                            </Badge>
                          )}
                        </div>
                        <div className="flex flex-col gap-2">
                          <Button 
                            size="sm" 
                            className="bg-green-600 hover:bg-green-700"
                            onClick={() => {
                              setSelectedStudent(student);
                            }}
                          >
                            <Eye className="h-4 w-4 mr-1" />
                            Examiner
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Validation Modal */}
          {selectedStudent && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
              <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <CardHeader>
                  <CardTitle>Valider le projet de {selectedStudent.full_name}</CardTitle>
                  <CardDescription>{selectedStudent.email}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <h4 className="font-medium mb-2">Projet professionnel :</h4>
                    <p className="text-gray-700">{selectedStudent.professional_project || 'Non renseigné'}</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Handicap :</span>
                      <span className="ml-2 font-medium">{selectedStudent.has_disability || 'Non renseigné'}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Téléphone :</span>
                      <span className="ml-2 font-medium">{selectedStudent.phone || 'Non renseigné'}</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Notes (optionnel)</label>
                    <Textarea
                      value={validationNotes}
                      onChange={(e) => setValidationNotes(e.target.value)}
                      placeholder="Commentaires sur la validation..."
                      rows={3}
                    />
                  </div>

                  <div className="flex gap-3">
                    <Button
                      variant="outline"
                      onClick={() => setSelectedStudent(null)}
                      className="flex-1"
                    >
                      Annuler
                    </Button>
                    <Button
                      onClick={() => handleValidateProject(selectedStudent.id, false)}
                      disabled={actionLoading}
                      className="flex-1 bg-red-600 hover:bg-red-700"
                    >
                      <XCircle className="h-4 w-4 mr-2" />
                      Refuser
                    </Button>
                    <Button
                      onClick={() => handleValidateProject(selectedStudent.id, true)}
                      disabled={actionLoading}
                      className="flex-1 bg-green-600 hover:bg-green-700"
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Valider
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Search */}
          <div className="mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Rechercher un élève..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>

          {/* Inactive Students Alert */}
          {inactiveStudents.length > 0 && (
            <Card className="mb-6 border-red-300 bg-red-50">
              <CardHeader>
                <CardTitle className="text-red-800 flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  Élèves inactifs depuis plus de 10 jours ({inactiveStudents.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {inactiveStudents.slice(0, 5).map(student => (
                    <div key={student.id} className="flex items-center justify-between p-3 bg-white rounded-lg border">
                      <div>
                        <span className="font-medium">{student.full_name}</span>
                        <span className="text-gray-500 text-sm ml-2">({student.email})</span>
                        <span className="text-gray-500 text-sm ml-2">
                          - Progression: {student.progress?.percentage || 0}%
                        </span>
                      </div>
                      <Button size="sm" variant="outline" className="text-red-600 border-red-300">
                        <Mail className="h-4 w-4 mr-1" />
                        Relancer
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* All Students */}
          <Card>
            <CardHeader>
              <CardTitle>Tous les élèves ({filteredStudents.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Élève</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Progression</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Statut</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code Weproov</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Inspection</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {filteredStudents.map(student => (
                      <tr key={student.id} className={student.needs_reminder ? 'bg-red-50' : ''}>
                        <td className="px-4 py-4">
                          <div>
                            <p className="font-medium text-gray-900">{student.full_name}</p>
                            <p className="text-sm text-gray-500">{student.email}</p>
                          </div>
                        </td>
                        <td className="px-4 py-4">
                          <div className="w-32">
                            <div className="flex justify-between text-sm mb-1">
                              <span>{student.progress?.completed_modules || 0}/{student.progress?.total_modules || 0}</span>
                              <span>{student.progress?.percentage || 0}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full" 
                                style={{ width: `${student.progress?.percentage || 0}%` }}
                              />
                            </div>
                          </div>
                        </td>
                        <td className="px-4 py-4">
                          {student.is_validated ? (
                            <Badge className="bg-green-100 text-green-800">Validé</Badge>
                          ) : student.validation_pending ? (
                            <Badge className="bg-yellow-100 text-yellow-800">En attente</Badge>
                          ) : (
                            <Badge className="bg-gray-100 text-gray-800">Non validé</Badge>
                          )}
                        </td>
                        <td className="px-4 py-4">
                          {student.weproov_code ? (
                            <span className="text-sm font-mono bg-gray-100 px-2 py-1 rounded">
                              {student.weproov_code}
                            </span>
                          ) : (
                            <div className="flex items-center gap-2">
                              <Input
                                placeholder="Code..."
                                className="w-24 h-8 text-sm"
                                value={weproovCode}
                                onChange={(e) => setWeproovCode(e.target.value)}
                              />
                              <Button 
                                size="sm" 
                                variant="outline"
                                onClick={() => handleSetWeproovCode(student.id)}
                              >
                                OK
                              </Button>
                            </div>
                          )}
                        </td>
                        <td className="px-4 py-4">
                          {student.inspection_validated ? (
                            <Badge className="bg-green-100 text-green-800">
                              <CheckCircle className="h-3 w-3 mr-1" />
                              Validée
                            </Badge>
                          ) : student.weproov_code ? (
                            <div className="flex gap-1">
                              <Button
                                size="sm"
                                className="bg-green-600 hover:bg-green-700 h-7 px-2"
                                onClick={() => handleValidateInspection(student.id, true)}
                              >
                                ✓
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                className="h-7 px-2 text-red-600"
                                onClick={() => handleValidateInspection(student.id, false)}
                              >
                                ✗
                              </Button>
                            </div>
                          ) : (
                            <span className="text-gray-400 text-sm">-</span>
                          )}
                        </td>
                        <td className="px-4 py-4">
                          <div className="flex gap-2">
                            {student.needs_reminder && (
                              <Button size="sm" variant="outline" className="text-orange-600">
                                <Mail className="h-4 w-4" />
                              </Button>
                            )}
                            <Button size="sm" variant="outline">
                              <Eye className="h-4 w-4" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

        </div>
      </div>
    </>
  );
}

export default AdminStudentProgress;
