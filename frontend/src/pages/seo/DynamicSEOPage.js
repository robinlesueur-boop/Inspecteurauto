import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import SEOPageTemplate from '../../components/SEOPageTemplate';
import { seoPageDatabase, getPageById } from '../../data/seoPageDatabase';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * Composant Dynamique pour toutes les pages SEO
 * Route: /seo/:pageId
 * 
 * Charge les données depuis:
 * 1. La base de données MongoDB (pages créées par l'admin)
 * 2. Le fichier seoPageDatabase.js (pages statiques prédéfinies)
 */
function DynamicSEOPage() {
  const { pageId } = useParams();
  const [pageData, setPageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    loadPageData();
  }, [pageId]);

  const loadPageData = async () => {
    setLoading(true);
    setNotFound(false);

    // 1. D'abord essayer de charger depuis la base de données
    try {
      const response = await axios.get(`${API}/seo-pages/${pageId}`);
      if (response.data) {
        // Convertir le format DB vers le format attendu par SEOPageTemplate
        const dbPage = response.data;
        setPageData({
          title: dbPage.title,
          metaTitle: dbPage.meta_title,
          metaDescription: dbPage.meta_description,
          metaKeywords: dbPage.meta_keywords,
          h1: dbPage.h1,
          category: dbPage.category,
          introduction: dbPage.introduction,
          sections: dbPage.sections || [],
          faq: dbPage.faq || [],
          cta: {
            title: dbPage.cta_title,
            description: dbPage.cta_description,
            primaryLink: {
              text: dbPage.cta_button_text || "S'inscrire",
              url: dbPage.cta_button_url || '/register'
            }
          }
        });
        setLoading(false);
        return;
      }
    } catch (error) {
      // Si 404, la page n'existe pas en DB, on continue vers les données statiques
      if (error.response?.status !== 404) {
        console.error('Error fetching page from DB:', error);
      }
    }

    // 2. Si pas trouvé en DB, chercher dans les données statiques
    const staticPage = getPageById(pageId);
    if (staticPage) {
      setPageData(staticPage);
      setLoading(false);
      return;
    }

    // 3. Page non trouvée
    setNotFound(true);
    setLoading(false);
  };

  // Générer des pages reliées automatiquement
  const generateRelatedPages = () => {
    const related = [];
    
    // Formation principale (si pas déjà dessus)
    if (pageId !== 'formation-inspecteur-automobile') {
      related.push({
        title: 'Formation Inspecteur Automobile Complète',
        description: 'Découvrez notre programme de formation complet en 9 modules',
        url: '/seo/formation-inspecteur-automobile'
      });
    }

    // Comment devenir (si pas déjà dessus)
    if (pageId !== 'comment-devenir-inspecteur-automobile') {
      related.push({
        title: 'Comment Devenir Inspecteur Automobile',
        description: 'Guide étape par étape pour réussir votre reconversion',
        url: '/seo/comment-devenir-inspecteur-automobile'
      });
    }

    // Certification (si pas déjà dessus)
    if (pageId !== 'certification-inspecteur-automobile') {
      related.push({
        title: 'Certification Professionnelle',
        description: 'Obtenez votre certification d\'inspecteur automobile officielle',
        url: '/seo/certification-inspecteur-automobile'
      });
    }

    // Revenus (si pas déjà dessus)
    if (pageId !== 'combien-gagne-inspecteur-automobile') {
      related.push({
        title: 'Revenus d\'un Inspecteur Automobile',
        description: 'Découvrez combien gagne un inspecteur automobile',
        url: '/seo/combien-gagne-inspecteur-automobile'
      });
    }

    // Limiter à 3 pages reliées
    return related.slice(0, 3);
  };

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  // Page non trouvée
  if (notFound || !pageData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
        <div className="max-w-2xl bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">🔍</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Page Non Trouvée
          </h1>
          <p className="text-gray-600 mb-6">
            Cette page SEO n'existe pas encore ou l'URL est incorrecte.
          </p>
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-amber-800">
              <strong>ID recherché :</strong> {pageId}
            </p>
          </div>
          <div className="space-y-4">
            <Link 
              to="/ressources" 
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
            >
              Voir toutes les Ressources
            </Link>
            <br />
            <Link 
              to="/" 
              className="inline-block text-blue-600 hover:text-blue-700 mt-2"
            >
              Retour à l'accueil
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const relatedPages = generateRelatedPages();

  return <SEOPageTemplate pageData={pageData} relatedPages={relatedPages} />;
}

export default DynamicSEOPage;
