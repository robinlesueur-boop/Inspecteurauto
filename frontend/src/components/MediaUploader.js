import React, { useState, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Upload, Image, Video, Copy, Trash2, X } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function MediaUploader({ onInsert }) {
  const [isOpen, setIsOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [mediaList, setMediaList] = useState([]);
  const [activeTab, setActiveTab] = useState('image'); // 'image' or 'video'
  const imageInputRef = useRef(null);
  const videoInputRef = useRef(null);

  const loadMedia = async () => {
    try {
      const response = await axios.get(`${API}/admin/media/list`);
      setMediaList(response.data.files || []);
    } catch (error) {
      console.error('Error loading media:', error);
    }
  };

  const handleFileUpload = async (event, type) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const endpoint = type === 'image' ? '/admin/upload/image' : '/admin/upload/video';
      const response = await axios.post(`${API}${endpoint}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      toast.success(`${type === 'image' ? 'Image' : 'Vidéo'} uploadée avec succès !`);
      
      // Recharger la liste
      await loadMedia();
      
      // Reset input
      event.target.value = '';
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de l\'upload');
    } finally {
      setUploading(false);
    }
  };

  const handleCopyUrl = (url, type) => {
    const fullUrl = `${BACKEND_URL}${url}`;
    const htmlCode = type === 'image'
      ? `<img src="${fullUrl}" alt="Image du cours" style="max-width: 100%; height: auto; margin: 20px 0;" />`
      : `<video controls style="max-width: 100%; height: auto; margin: 20px 0;">
  <source src="${fullUrl}" type="video/mp4" />
</video>`;
    
    navigator.clipboard.writeText(htmlCode);
    toast.success('Code HTML copié ! Collez-le dans le contenu du module');
  };

  const handleInsert = (url, type) => {
    const fullUrl = `${BACKEND_URL}${url}`;
    const htmlCode = type === 'image'
      ? `<img src="${fullUrl}" alt="Image du cours" style="max-width: 100%; height: auto; margin: 20px 0;" />`
      : `<video controls style="max-width: 100%; height: auto; margin: 20px 0;">
  <source src="${fullUrl}" type="video/mp4" />
</video>`;
    
    if (onInsert) {
      onInsert(htmlCode);
    }
    toast.success('Code inséré !');
    setIsOpen(false);
  };

  const handleDelete = async (filename, type) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce fichier ?')) return;

    try {
      await axios.delete(`${API}/admin/media/${type}/${filename}`);
      toast.success('Fichier supprimé');
      await loadMedia();
    } catch (error) {
      console.error('Delete error:', error);
      toast.error('Erreur lors de la suppression');
    }
  };

  const filteredMedia = mediaList.filter(m => m.type === activeTab);

  return (
    <div>
      <Button
        type="button"
        onClick={() => {
          setIsOpen(true);
          loadMedia();
        }}
        variant="outline"
        className="mb-4"
      >
        <Upload className="w-4 h-4 mr-2" />
        Gérer Images & Vidéos
      </Button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <CardHeader className="border-b">
              <div className="flex items-center justify-between">
                <CardTitle>Bibliothèque de Médias</CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </CardHeader>

            <CardContent className="flex-1 overflow-auto p-6">
              {/* Tabs */}
              <div className="flex space-x-2 mb-6 border-b">
                <button
                  onClick={() => setActiveTab('image')}
                  className={`px-4 py-2 font-medium ${
                    activeTab === 'image'
                      ? 'border-b-2 border-blue-600 text-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Image className="w-4 h-4 inline mr-2" />
                  Images
                </button>
                <button
                  onClick={() => setActiveTab('video')}
                  className={`px-4 py-2 font-medium ${
                    activeTab === 'video'
                      ? 'border-b-2 border-blue-600 text-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Video className="w-4 h-4 inline mr-2" />
                  Vidéos
                </button>
              </div>

              {/* Upload Section */}
              <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-6 mb-6">
                <input
                  ref={imageInputRef}
                  type="file"
                  accept="image/*"
                  onChange={(e) => handleFileUpload(e, 'image')}
                  className="hidden"
                />
                <input
                  ref={videoInputRef}
                  type="file"
                  accept="video/*"
                  onChange={(e) => handleFileUpload(e, 'video')}
                  className="hidden"
                />

                <div className="text-center">
                  <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-700 mb-4">
                    {activeTab === 'image' 
                      ? 'Uploadez une image (JPG, PNG, GIF - Max 5MB)'
                      : 'Uploadez une vidéo (MP4, WebM - Max 50MB)'}
                  </p>
                  <Button
                    onClick={() => {
                      if (activeTab === 'image') {
                        imageInputRef.current?.click();
                      } else {
                        videoInputRef.current?.click();
                      }
                    }}
                    disabled={uploading}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {uploading ? 'Upload en cours...' : `Choisir ${activeTab === 'image' ? 'une image' : 'une vidéo'}`}
                  </Button>
                </div>
              </div>

              {/* Media Grid */}
              <div>
                <h3 className="font-semibold mb-4">
                  {activeTab === 'image' ? 'Images' : 'Vidéos'} ({filteredMedia.length})
                </h3>
                
                {filteredMedia.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">
                    Aucun {activeTab === 'image' ? 'image' : 'vidéo'} uploadé pour le moment
                  </div>
                ) : (
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {filteredMedia.map((media, index) => (
                      <div key={index} className="border rounded-lg overflow-hidden bg-white shadow-sm">
                        <div className="aspect-video bg-gray-100 flex items-center justify-center">
                          {media.type === 'image' ? (
                            <img
                              src={`${BACKEND_URL}${media.url}`}
                              alt={media.filename}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <Video className="w-12 h-12 text-gray-400" />
                          )}
                        </div>
                        <div className="p-3">
                          <p className="text-xs text-gray-600 truncate mb-2">{media.filename}</p>
                          <div className="flex space-x-2">
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleCopyUrl(media.url, media.type)}
                              className="flex-1"
                            >
                              <Copy className="w-3 h-3 mr-1" />
                              Copier
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleDelete(media.filename, media.type)}
                              className="text-red-600"
                            >
                              <Trash2 className="w-3 h-3" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Instructions */}
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">💡 Comment utiliser</h4>
                <ol className="text-sm text-blue-800 space-y-1">
                  <li>1. Uploadez votre {activeTab === 'image' ? 'image' : 'vidéo'}</li>
                  <li>2. Cliquez sur "Copier" pour copier le code HTML</li>
                  <li>3. Collez le code dans le champ "Contenu du Module"</li>
                  <li>4. Sauvegardez le module</li>
                </ol>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

export default MediaUploader;
