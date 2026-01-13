import React from 'react';
import { useParams } from 'react-router-dom';
import SEOPageTemplate from '../../components/SEOPageTemplate';
import { seoPageDatabase } from '../../data/seoPageDatabase';

/**
 * Composant Dynamique pour toutes les pages SEO
 * Lit les données depuis seoPageDatabase.js
 */
function DynamicSEOPage() {
  const { pageId } = useParams();
  
  // Chercher la page dans toutes les catégories
  let pageData = null;
  let relatedPages = [];

  // Recherche dans les piliers
  if (seoPageDatabase.piliers[pageId]) {
    pageData = seoPageDatabase.piliers[pageId];
  }
  // Recherche dans les techniques - diagnostic
  else if (seoPageDatabase.techniques?.diagnostic[pageId]) {
    pageData = seoPageDatabase.techniques.diagnostic[pageId];
  }
  // Recherche dans les techniques - carrosserie
  else if (seoPageDatabase.techniques?.carrosserie[pageId]) {
    pageData = seoPageDatabase.techniques.carrosserie[pageId];
  }

  // Si la page n'est pas trouvée (contenu TODO)
  if (!pageData || !pageData.sections || pageData.sections[0]?.content[0]?.includes('TODO')) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
        <div className="max-w-2xl bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Page en Construction
          </h1>
          <p className="text-gray-600 mb-6">
            Le contenu de cette page est en cours de rédaction. Cette page fait partie de notre stratégie SEO de 100 pages.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-800">
              <strong>ID de la page :</strong> {pageId}
            </p>
            <p className="text-sm text-blue-800 mt-2">
              Pour compléter cette page, éditez le fichier :<br />
              <code className="bg-blue-100 px-2 py-1 rounded">/app/frontend/src/data/seoPageDatabase.js</code>
            </p>
          </div>
          <div className="space-y-2">
            <a 
              href="/formation-inspecteur-automobile" 
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
            >
              Voir notre Formation Complète
            </a>
            <br />
            <a 
              href="/" 
              className="inline-block text-blue-600 hover:text-blue-700 mt-2"
            >
              Retour à l'accueil
            </a>
          </div>
        </div>
      </div>
    );
  }

  // Générer des pages reliées automatiquement
  const generateRelatedPages = () => {
    const related = [];
    
    // Toujours suggérer la formation principale
    related.push({
      title: 'Formation Inspecteur Automobile Complète',
      description: 'Découvrez notre programme de formation complet en 9 modules',
      url: '/seo/formation-inspecteur-automobile'
    });

    // Ajouter la certification si pas déjà sur cette page
    if (pageId !== 'certification-inspecteur-automobile') {
      related.push({
        title: 'Certification Reconnue',
        description: 'Obtenez votre certification d\'inspecteur automobile officielle',
        url: '/seo/certification-inspecteur-automobile'
      });
    }

    // Ajouter "Comment devenir" si pas déjà sur cette page
    if (pageId !== 'comment-devenir-inspecteur') {
      related.push({
        title: 'Comment Devenir Inspecteur Automobile',
        description: 'Guide étape par étape pour réussir votre reconversion',
        url: '/seo/comment-devenir-inspecteur'
      });
    }

    return related;
  };

  relatedPages = generateRelatedPages();

  return <SEOPageTemplate pageData={pageData} relatedPages={relatedPages} />;
}

export default DynamicSEOPage;
