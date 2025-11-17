import React, { useState, useRef } from 'react';
import { Button } from './ui/button';
import { Upload, X, Loader2 } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function ImageUploader({ onImageUploaded, currentImageUrl }) {
  const [uploading, setUploading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(currentImageUrl || '');
  const fileInputRef = useRef(null);

  // Update preview when currentImageUrl changes
  React.useEffect(() => {
    if (currentImageUrl) {
      // If it's a relative path, add BACKEND_URL for preview
      if (currentImageUrl.startsWith('/')) {
        setPreviewUrl(`${BACKEND_URL}${currentImageUrl}`);
      } else {
        setPreviewUrl(currentImageUrl);
      }
    }
  }, [currentImageUrl]);

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Vérifier le type de fichier
    if (!file.type.startsWith('image/')) {
      toast.error('Veuillez sélectionner une image valide');
      return;
    }

    // Vérifier la taille (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('L\'image est trop volumineuse (max 5MB)');
      return;
    }

    // Créer un aperçu local
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target.result);
    };
    reader.readAsDataURL(file);

    // Uploader l'image
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${BACKEND_URL}/api/admin/upload/image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });

      // L'URL retournée est relative (/uploads/images/xxx)
      // On NE préfixe PAS avec BACKEND_URL car on veut une URL relative
      // qui fonctionnera dans tous les environnements
      const imageUrl = response.data.url; // Déjà au format /uploads/images/xxx
      setPreviewUrl(`${BACKEND_URL}${imageUrl}`); // Pour l'aperçu local
      onImageUploaded(imageUrl); // Stocker l'URL relative
      toast.success('Image uploadée ! N\'oubliez pas de cliquer sur "Enregistrer les Modifications" en bas de la page.', {
        duration: 5000
      });
    } catch (error) {
      console.error('Erreur upload:', error);
      toast.error('Erreur lors de l\'upload de l\'image');
      setPreviewUrl(currentImageUrl || '');
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = () => {
    setPreviewUrl('');
    onImageUploaded('');
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={uploading}
          onClick={() => fileInputRef.current?.click()}
        >
          {uploading ? (
            <>
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              Upload en cours...
            </>
          ) : (
            <>
              <Upload className="h-4 w-4 mr-2" />
              Uploader une image
            </>
          )}
        </Button>
        
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />

        {previewUrl && (
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleRemove}
            className="text-red-600 hover:text-red-700"
          >
            <X className="h-4 w-4 mr-2" />
            Supprimer
          </Button>
        )}
      </div>

      {previewUrl && (
        <div className="relative">
          <img
            src={previewUrl}
            alt="Aperçu"
            className="w-full max-w-md h-48 object-cover rounded-lg border"
          />
        </div>
      )}

      <p className="text-xs text-gray-500">
        Formats acceptés: JPG, PNG, GIF, WebP • Max 5MB
      </p>
    </div>
  );
}

export default ImageUploader;
