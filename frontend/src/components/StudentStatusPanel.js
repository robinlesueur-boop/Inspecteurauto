import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Upload, 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  FileCheck,
  Download,
  Loader2,
  Car,
  ClipboardCheck
} from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function StudentStatusPanel({ user }) {
  const [accessStatus, setAccessStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchAccessStatus();
  }, []);

  const fetchAccessStatus = async () => {
    try {
      const response = await axios.get(`${API}/user/access-status`);
      setAccessStatus(response.data);
    } catch (error) {
      console.error('Error fetching access status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    if (!validTypes.includes(file.type)) {
      toast.error('Format non supporté. Utilisez JPG, PNG ou PDF.');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('Fichier trop volumineux (max 5 Mo)');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${API}/user/upload-license`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      toast.success('Permis uploadé avec succès !');
      fetchAccessStatus();
    } catch (error) {
      toast.error('Erreur lors de l\'upload');
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="p-8 flex items-center justify-center">
          <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
        </CardContent>
      </Card>
    );
  }

  if (!accessStatus?.has_purchased) {
    return null;
  }

  // En attente de validation
  if (accessStatus.validation_pending && !accessStatus.is_validated) {
    return (
      <Card className="border-yellow-300 bg-yellow-50 mb-6">
        <CardHeader>
          <CardTitle className="text-yellow-800 flex items-center gap-2">
            <Clock className="h-5 w-5" />
            En attente de validation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-yellow-700 mb-4">
            Votre projet professionnel est en cours d'examen par notre équipe pédagogique. 
            Vous recevrez une notification dès que votre accès sera validé.
          </p>
          <p className="text-sm text-yellow-600">
            Délai moyen : 24-48h ouvrées
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4 mb-6">
      {/* Statut général */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ClipboardCheck className="h-5 w-5 text-blue-600" />
            Mon Dossier de Formation
          </CardTitle>
          <CardDescription>
            Complétez votre dossier pour valider votre formation
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          
          {/* Validation du projet */}
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-full ${accessStatus.is_validated ? 'bg-green-100' : 'bg-yellow-100'}`}>
                {accessStatus.is_validated ? (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                ) : (
                  <Clock className="h-5 w-5 text-yellow-600" />
                )}
              </div>
              <div>
                <p className="font-medium">Projet professionnel</p>
                <p className="text-sm text-gray-500">Validation par l'équipe pédagogique</p>
              </div>
            </div>
            <Badge className={accessStatus.is_validated ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
              {accessStatus.is_validated ? 'Validé' : 'En attente'}
            </Badge>
          </div>

          {/* Permis de conduire */}
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-full ${accessStatus.driving_license_uploaded ? 'bg-green-100' : 'bg-gray-100'}`}>
                {accessStatus.driving_license_uploaded ? (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                ) : (
                  <Upload className="h-5 w-5 text-gray-600" />
                )}
              </div>
              <div>
                <p className="font-medium">Permis de conduire</p>
                <p className="text-sm text-gray-500">Scan ou photo de votre permis B</p>
              </div>
            </div>
            {accessStatus.driving_license_uploaded ? (
              <Badge className="bg-green-100 text-green-800">Uploadé</Badge>
            ) : (
              <div>
                <input
                  type="file"
                  accept="image/*,.pdf"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="license-upload"
                />
                <label htmlFor="license-upload">
                  <Button 
                    asChild 
                    size="sm" 
                    variant="outline"
                    disabled={uploading}
                  >
                    <span className="cursor-pointer">
                      {uploading ? (
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      ) : (
                        <Upload className="h-4 w-4 mr-2" />
                      )}
                      Uploader
                    </span>
                  </Button>
                </label>
              </div>
            )}
          </div>

          {/* Code Weproov - Inspection test */}
          {accessStatus.weproov_code && (
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-full bg-blue-100">
                  <Car className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="font-medium">Inspection Test</p>
                  <p className="text-sm text-gray-500">Code Weproov : <span className="font-mono font-bold">{accessStatus.weproov_code}</span></p>
                </div>
              </div>
              {accessStatus.inspection_validated ? (
                <Badge className="bg-green-100 text-green-800">Validée</Badge>
              ) : (
                <Badge className="bg-blue-100 text-blue-800">En attente</Badge>
              )}
            </div>
          )}

          {/* Questionnaire satisfaction */}
          {accessStatus.inspection_validated && !accessStatus.satisfaction_completed && (
            <Alert className="border-orange-300 bg-orange-50">
              <AlertCircle className="h-4 w-4 text-orange-600" />
              <AlertDescription className="text-orange-800">
                Pour obtenir votre attestation, veuillez compléter le questionnaire de satisfaction.
              </AlertDescription>
            </Alert>
          )}

          {/* Certificat */}
          {accessStatus.certificate_url && (
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-full bg-green-100">
                  <FileCheck className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-green-900">Attestation de formation</p>
                  <p className="text-sm text-green-700">Votre attestation est disponible !</p>
                </div>
              </div>
              <Button 
                size="sm" 
                className="bg-green-600 hover:bg-green-700"
                onClick={() => window.open(accessStatus.certificate_url, '_blank')}
              >
                <Download className="h-4 w-4 mr-2" />
                Télécharger
              </Button>
            </div>
          )}

        </CardContent>
      </Card>
    </div>
  );
}
