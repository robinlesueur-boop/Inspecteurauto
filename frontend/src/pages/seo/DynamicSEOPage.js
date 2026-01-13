import React from 'react';
import { useParams, Link } from 'react-router-dom';
import SEOPageTemplate from '../../components/SEOPageTemplate';
import { seoPageDatabase, getPageById, allSeoPageIds } from '../../data/seoPageDatabase';

/**
 * Composant Dynamique pour toutes les pages SEO
 * Route: /seo/:pageId
 * Lit les données depuis seoPageDatabase.js
 */
function DynamicSEOPage() {
  const { pageId } = useParams();
  
  // Récupérer les données de la page
  const pageData = getPageById(pageId);

  // Si la page n'est pas trouvée
  if (!pageData) {
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
              to="/programme-detaille" 
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
            >
              Voir le Programme de Formation
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

  const relatedPages = generateRelatedPages();

  return <SEOPageTemplate pageData={pageData} relatedPages={relatedPages} />;
}

export default DynamicSEOPage;
