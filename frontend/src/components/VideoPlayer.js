import React, { useState } from "react";
import { Play, Volume2, VolumeX, Maximize } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function VideoPlayer({ videoUrl, title = "Vidéo du module", className = "" }) {
  const [isPlaying, setIsPlaying] = useState(false);

  if (!videoUrl) return null;

  // Détecter le type de vidéo
  const getVideoType = (url) => {
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
      return 'youtube';
    } else if (url.includes('vimeo.com')) {
      return 'vimeo';
    } else {
      return 'uploaded';
    }
  };

  // Extraire l'ID YouTube
  const getYouTubeId = (url) => {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  };

  // Extraire l'ID Vimeo
  const getVimeoId = (url) => {
    const regExp = /vimeo.*\/(\d+)/i;
    const match = url.match(regExp);
    return match ? match[1] : null;
  };

  // Construire l'URL d'embed
  const getEmbedUrl = () => {
    const videoType = getVideoType(videoUrl);
    
    if (videoType === 'youtube') {
      const videoId = getYouTubeId(videoUrl);
      return `https://www.youtube.com/embed/${videoId}?rel=0&modestbranding=1`;
    } else if (videoType === 'vimeo') {
      const videoId = getVimeoId(videoUrl);
      return `https://player.vimeo.com/video/${videoId}`;
    } else {
      // Vidéo uploadée
      if (videoUrl.startsWith('http://') || videoUrl.startsWith('https://')) {
        return videoUrl;
      }
      return `${BACKEND_URL}${videoUrl}`;
    }
  };

  const videoType = getVideoType(videoUrl);
  const embedUrl = getEmbedUrl();

  // Pour YouTube et Vimeo, utiliser iframe
  if (videoType === 'youtube' || videoType === 'vimeo') {
    return (
      <div className={`relative w-full rounded-xl overflow-hidden shadow-2xl bg-gray-900 ${className}`}>
        <div className="relative" style={{ paddingBottom: '56.25%' }}>
          <iframe
            className="absolute top-0 left-0 w-full h-full"
            src={embedUrl}
            title={title}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
          <p className="text-white text-sm font-medium">{title}</p>
        </div>
      </div>
    );
  }

  // Pour les vidéos uploadées, utiliser la balise video HTML5
  return (
    <div className={`relative w-full rounded-xl overflow-hidden shadow-2xl bg-gray-900 ${className}`}>
      <video
        className="w-full h-auto"
        controls
        controlsList="nodownload"
        preload="metadata"
        poster={`${embedUrl}#t=0.5`}
      >
        <source src={embedUrl} type="video/mp4" />
        Votre navigateur ne supporte pas la lecture de vidéos.
      </video>
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4 pointer-events-none">
        <p className="text-white text-sm font-medium">{title}</p>
      </div>
    </div>
  );
}

export default VideoPlayer;
