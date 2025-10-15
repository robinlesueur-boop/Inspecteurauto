import os
import uuid
from pathlib import Path
from typing import List
import shutil

class MediaUploadService:
    def __init__(self):
        # Dossier pour stocker les médias uploadés
        self.upload_dir = Path("/app/frontend/public/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer les sous-dossiers
        (self.upload_dir / "images").mkdir(exist_ok=True)
        (self.upload_dir / "videos").mkdir(exist_ok=True)
    
    def save_file(self, file_content: bytes, filename: str, file_type: str) -> dict:
        """
        Sauvegarde un fichier et retourne l'URL
        
        Args:
            file_content: Contenu du fichier en bytes
            filename: Nom original du fichier
            file_type: 'image' ou 'video'
        
        Returns:
            dict avec url et filename
        """
        # Générer un nom unique
        file_extension = Path(filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Déterminer le dossier de destination
        if file_type == "image":
            dest_folder = self.upload_dir / "images"
        else:
            dest_folder = self.upload_dir / "videos"
        
        # Chemin complet du fichier
        file_path = dest_folder / unique_filename
        
        # Sauvegarder le fichier
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Retourner l'URL publique
        public_url = f"/uploads/{file_type}s/{unique_filename}"
        
        return {
            "url": public_url,
            "filename": unique_filename,
            "original_filename": filename,
            "type": file_type
        }
    
    def list_files(self, file_type: str = None) -> List[dict]:
        """Liste tous les fichiers uploadés"""
        files = []
        
        if file_type == "image" or file_type is None:
            images_dir = self.upload_dir / "images"
            if images_dir.exists():
                for file in images_dir.iterdir():
                    if file.is_file():
                        files.append({
                            "url": f"/uploads/images/{file.name}",
                            "filename": file.name,
                            "type": "image",
                            "size": file.stat().st_size
                        })
        
        if file_type == "video" or file_type is None:
            videos_dir = self.upload_dir / "videos"
            if videos_dir.exists():
                for file in videos_dir.iterdir():
                    if file.is_file():
                        files.append({
                            "url": f"/uploads/videos/{file.name}",
                            "filename": file.name,
                            "type": "video",
                            "size": file.stat().st_size
                        })
        
        return files
    
    def delete_file(self, filename: str, file_type: str) -> bool:
        """Supprime un fichier"""
        if file_type == "image":
            file_path = self.upload_dir / "images" / filename
        else:
            file_path = self.upload_dir / "videos" / filename
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False

# Instance globale
media_service = MediaUploadService()
