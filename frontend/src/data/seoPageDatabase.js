/**
 * BASE DE DONNÉES DES 100 PAGES SEO
 * 
 * INSTRUCTIONS POUR COMPLÉTER LE CONTENU :
 * 
 * 1. Chaque page a une structure prédéfinie
 * 2. Les champs marqués "TODO" doivent être remplis avec du contenu
 * 3. Pour chaque section, ajoutez 2-4 paragraphes de 100-200 mots
 * 4. Les listes doivent contenir 5-10 points
 * 5. Ajoutez 3-5 FAQ par page
 * 
 * COMMENT COMPLÉTER :
 * - Remplacez les "TODO: Contenu à rédiger..." par le vrai contenu
 * - Vous pouvez utiliser ChatGPT/Claude pour générer le contenu
 * - Gardez un ton professionnel et informatif
 * - Incluez des chiffres et données concrètes quand possible
 * 
 * OUTILS RECOMMANDÉS :
 * - ChatGPT : "Rédige 3 paragraphes de 150 mots sur [sujet]"
 * - Claude : Pour relire et améliorer le contenu
 * - Jasper AI : Pour la génération de contenu SEO
 */

export const seoPageDatabase = {
  
  // ============================================
  // CATÉGORIE 1 : PAGES PILIERS (10 pages)
  // ============================================
  piliers: {
    // Page 4 - À COMPLÉTER
    'tarifs-formation-inspecteur-auto': {
      title: 'Tarifs Formation Inspecteur Auto 2024',
      metaTitle: 'Tarifs Formation Inspecteur Automobile 2024 | Prix & Financement',
      metaDescription: 'Découvrez les tarifs de notre formation inspecteur automobile : 297€ paiement unique ou 4x sans frais. Financement CPF disponible. Meilleur rapport qualité-prix.',
      metaKeywords: 'tarif formation inspecteur auto, prix formation diagnostic automobile, cout formation inspecteur',
      h1: 'Tarifs Formation Inspecteur Automobile : Guide Complet 2024',
      category: 'Tarifs',
      introduction: 'TODO: Contenu à rédiger - Introduire les tarifs de la formation, expliquer la transparence des prix, mentionner les options de paiement',
      sections: [
        {
          title: 'Prix de la Formation Complète',
          content: [
            'TODO: Paragraphe 1 - Annoncer le prix (297€), expliquer ce qui est inclus',
            'TODO: Paragraphe 2 - Comparer avec la concurrence, justifier le prix'
          ],
          list: [
            'TODO: Point 1 - Ce qui est inclus (ex: 9 modules vidéo)',
            'TODO: Point 2 - Accès illimité',
            'TODO: Point 3 - Support 7j/7',
            'TODO: Point 4 - Certification incluse',
            'TODO: Point 5 - Bonus et outils'
          ]
        },
        {
          title: 'Options de Paiement',
          content: [
            'TODO: Expliquer les options de paiement (4x sans frais, CPF, etc.)'
          ]
        },
        {
          title: 'Retour sur Investissement',
          content: [
            'TODO: Calculer combien d\\'inspections pour rentabiliser',
            'TODO: Témoignages sur le ROI'
          ]
        }
      ],
      faq: [
        {
          question: 'TODO: Question FAQ 1',
          answer: 'TODO: Réponse FAQ 1'
        }
      ],
      cta: {
        title: 'Inscrivez-vous Maintenant',
        description: 'Formation complète à 297€ - Paiement 4x sans frais disponible',
        primaryLink: { text: 'S\\'inscrire', url: '/register' }
      }
    },

    // Page 5 - À COMPLÉTER
    'combien-gagne-inspecteur-automobile': {
      title: 'Combien Gagne un Inspecteur Automobile en 2024',
      metaTitle: 'Salaire Inspecteur Automobile 2024 | Revenus Réels & Témoignages',
      metaDescription: 'Découvrez les revenus réels d\\'un inspecteur automobile : 2000€ à 8000€/mois selon l\\'expérience. Analyse détaillée des tarifs, volume d\\'activité et marges.',
      metaKeywords: 'salaire inspecteur automobile, revenu inspecteur auto, combien gagne inspecteur',
      h1: 'Combien Gagne un Inspecteur Automobile : La Vérité sur les Revenus',
      category: 'Revenus',
      introduction: 'TODO: Introduire le sujet des revenus, promettre transparence et données réelles',
      sections: [
        {
          title: 'Tarifs Moyens par Inspection',
          content: [
            'TODO: Expliquer les tarifs (150-300€), variations selon régions',
            'TODO: Facteurs influençant le prix'
          ]
        },
        {
          title: 'Revenus Débutant (0-6 mois)',
          content: [
            'TODO: Calculer revenus débutant (8-12 inspections/mois)',
            'TODO: Charges à déduire'
          ]
        },
        {
          title: 'Revenus Confirmé (1-2 ans)',
          content: [
            'TODO: Revenus avec expérience (20-25 inspections/mois)'
          ]
        },
        {
          title: 'Revenus Expert (3+ ans)',
          content: [
            'TODO: Revenus expert (35-40 inspections/mois)',
            'TODO: Possibilités de diversification'
          ]
        }
      ],
      faq: [],
      cta: {
        title: 'Démarrez Votre Activité Lucrative',
        description: 'Formez-vous et générez vos premiers revenus dès le mois prochain',
        primaryLink: { text: 'Commencer la Formation', url: '/register' }
      }
    },

    // Page 6 - À COMPLÉTER
    'metier-inspecteur-automobile': {
      title: 'Métier Inspecteur Automobile : Guide Complet 2024',
      metaTitle: 'Métier Inspecteur Automobile : Missions, Formation, Débouchés',
      metaDescription: 'Tout savoir sur le métier d\\'inspecteur automobile : missions quotidiennes, compétences requises, avantages, inconvénients. Métier d\\'avenir passionnant.',
      metaKeywords: 'métier inspecteur automobile, profession inspecteur auto, travail inspecteur véhicule',
      h1: 'Le Métier d\\'Inspecteur Automobile : Tout Ce Qu\\'il Faut Savoir',
      category: 'Métier',
      introduction: 'TODO: Présenter le métier, son importance, pourquoi il attire',
      sections: [
        {
          title: 'Qu\\'est-ce qu\\'un Inspecteur Automobile ?',
          content: ['TODO: Définir le métier, différence avec mécanicien/contrôleur technique']
        },
        {
          title: 'Missions Quotidiennes',
          content: ['TODO: Décrire une journée type'],
          list: ['TODO: Liste des missions principales']
        },
        {
          title: 'Compétences Requises',
          content: ['TODO: Compétences techniques et relationnelles']
        },
        {
          title: 'Avantages du Métier',
          content: ['TODO: Liberté, revenus, passion']
        },
        {
          title: 'Inconvénients et Défis',
          content: ['TODO: Être honnête sur les difficultés']
        }
      ],
      faq: [],
      cta: {
        title: 'Découvrez Ce Métier Passionnant',
        description: 'Testez gratuitement le Module 1 de notre formation',
        primaryLink: { text: 'Essayer Gratuitement', url: '/register' }
      }
    },

    // Pages 7-10 : Structure similaire, à compléter
    'formation-en-ligne-inspecteur-automobile': {
      title: 'Formation Inspecteur Automobile en Ligne',
      metaTitle: 'Formation en Ligne Inspecteur Auto | 100% À Distance & Flexible',
      metaDescription: 'Formation inspecteur automobile 100% en ligne. Étudiez à votre rythme, accès illimité, support expert. Lancez votre carrière depuis chez vous.',
      h1: 'Formation Inspecteur Automobile en Ligne : Flexibilité et Excellence',
      sections: [
        {
          title: 'TODO: Avantages Formation en Ligne',
          content: ['TODO: Contenu sur flexibilité, accessibilité']
        }
      ],
      faq: [],
      cta: { title: 'Commencer en Ligne', primaryLink: { text: 'S\\'inscrire', url: '/register' } }
    },

    'prix-inspection-automobile-pre-achat': {
      title: 'Prix Inspection Automobile Pré-Achat 2024',
      sections: [{ title: 'TODO', content: ['TODO'] }],
      faq: [],
      cta: { primaryLink: { url: '/register' } }
    },

    'revenus-inspecteur-auto-independant': {
      title: 'Revenus Inspecteur Auto Indépendant',
      sections: [{ title: 'TODO', content: ['TODO'] }],
      faq: [],
      cta: { primaryLink: { url: '/register' } }
    },

    'rentabilite-business-inspection-auto': {
      title: 'Rentabilité Business Inspection Auto',
      sections: [{ title: 'TODO', content: ['TODO'] }],
      faq: [],
      cta: { primaryLink: { url: '/register' } }
    }
  },

  // ============================================
  // CATÉGORIE 2 : PAGES TECHNIQUES (20 pages)
  // ============================================
  techniques: {
    diagnostic: {
      'diagnostic-moteur-essence': {
        title: 'Diagnostic Moteur Essence : Guide Complet Inspecteur Auto',
        metaTitle: 'Diagnostic Moteur Essence Professionnel | Techniques & Outils',
        metaDescription: 'Guide complet du diagnostic moteur essence : points de contrôle, outils OBD2, pannes fréquentes, techniques professionnelles. Formation inspecteur automobile.',
        h1: 'Diagnostic Moteur Essence : Le Guide de l\\'Inspecteur Professionnel',
        category: 'Diagnostic Technique',
        sections: [
          {
            title: 'Points de Contrôle Essentiels',
            content: ['TODO: Expliquer les vérifications visuelles'],
            list: ['TODO: État du moteur', 'TODO: Fuites', 'TODO: Courroie', 'TODO: Bougies', 'TODO: Filtre']
          },
          {
            title: 'Utilisation de l\\'OBD2',
            content: ['TODO: Comment lire les codes défauts']
          },
          {
            title: 'Pannes Courantes Moteur Essence',
            content: ['TODO: Lister les pannes fréquentes et symptômes']
          }
        ],
        faq: [],
        cta: { primaryLink: { url: '/register' } }
      },
      // 9 autres pages diagnostic avec structure similaire
      'diagnostic-moteur-diesel': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-boite-vitesses-automatique': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-systeme-freinage-abs-esp': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-electronique-automobile-obd2': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-climatisation-automobile': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-suspension-amortisseurs': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-embrayage-signes-usure': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-turbo-pannes-courantes': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'diagnostic-systeme-antipollution-fap-scr': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } }
    },
    carrosserie: {
      'inspection-carrosserie-pre-achat': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'detection-vehicule-accidente': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'reperer-voiture-maquillee': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'inspection-chassis-points-controle': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'controle-peinture-anticorrosion': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'inspection-vitrage-automobile': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'verification-etancheite-vehicule': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'controle-geometrie-paralleli sme': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'inspection-pneumatiques-securite': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } },
      'detection-compteur-kilometrique-trafique': { title: 'TODO', sections: [{ title: 'TODO', content: ['TODO'] }], faq: [], cta: { primaryLink: { url: '/register' } } }
    }
  },

  // ============================================
  // CATÉGORIE 3 : LONG-TAIL (30 pages)
  // Structure simplifiée pour les 30 pages long-tail
  // ============================================
  longTail: {
    comment: [
      'comment-inspecter-voiture-occasion',
      'comment-verifier-etat-moteur',
      'comment-detecter-fuite-huile',
      'comment-controler-vehicule-hybride',
      'comment-inspecter-voiture-electrique',
      'comment-verifier-historique-vehicule',
      'comment-negocier-prix-apres-inspection',
      'comment-devenir-inspecteur-auto-sans-diplome',
      'comment-ouvrir-cabinet-inspection-auto',
      'comment-trouver-clients-inspecteur-auto',
      'comment-faire-inspection-pre-achat',
      'comment-rediger-rapport-inspection',
      'comment-utiliser-appareil-diagnostic-obd2',
      'comment-interpreter-codes-defauts',
      'comment-facturer-inspection-automobile'
    ],
    pourquoi: [
      'pourquoi-faire-inspecter-voiture-occasion',
      'pourquoi-devenir-inspecteur-automobile-independant',
      'pourquoi-controle-technique-ne-suffit-pas',
      'pourquoi-former-inspection-automobile',
      'pourquoi-investir-formation-certifiante',
      'pourquoi-choisir-inspection-automobile-metier',
      'pourquoi-garagistes-ne-font-pas-inspection-pre-achat',
      'pourquoi-inspection-auto-metier-avenir'
    ],
    quel: [
      'quel-equipement-inspecteur-automobile',
      'quel-statut-juridique-inspecteur-auto-independant',
      'quelle-formation-devenir-inspecteur-auto',
      'quel-budget-demarrer-inspecteur',
      'quelle-assurance-inspecteur-automobile',
      'quel-prix-facturer-inspection',
      'quelle-difference-controle-technique-inspection'
    ]
  },

  // ============================================
  // CATÉGORIE 4 : PAR MARQUE (20 pages)
  // ============================================
  marques: [
    'inspection-peugeot-occasion',
    'inspection-renault-occasion',
    'inspection-citroen-defauts',
    'inspection-volkswagen-pannes',
    'inspection-bmw-vigilance',
    'inspection-mercedes-detaillee',
    'inspection-audi-verifications',
    'inspection-toyota-fiabilite',
    'inspection-ford-guide',
    'inspection-dacia-pre-achat',
    'inspection-fiat-defauts',
    'inspection-opel-controle',
    'inspection-nissan-guide',
    'inspection-hyundai-verifications',
    'inspection-kia-complete',
    'inspection-mazda-critiques',
    'inspection-seat-pre-achat',
    'inspection-skoda-fiabilite',
    'inspection-tesla-electrique',
    'inspection-volvo-securite'
  ],

  // ============================================
  // CATÉGORIE 5 : GÉOLOCALISATION (10 pages)
  // ============================================
  geo: [
    'formation-inspecteur-automobile-paris',
    'formation-inspecteur-automobile-lyon',
    'formation-inspecteur-automobile-marseille',
    'formation-inspecteur-automobile-toulouse',
    'formation-inspecteur-automobile-bordeaux',
    'formation-inspecteur-automobile-lille',
    'formation-inspecteur-automobile-nice',
    'formation-inspecteur-automobile-nantes',
    'formation-inspecteur-automobile-strasbourg',
    'formation-inspecteur-automobile-montpellier'
  ],

  // ============================================
  // CATÉGORIE 6 : COMPARAISONS (5 pages)
  // ============================================
  comparaisons: [
    'inspecteur-auto-vs-expert-automobile',
    'inspection-pre-achat-vs-controle-technique',
    'inspecteur-independant-vs-garage',
    'formation-en-ligne-vs-presentiel',
    'auto-entrepreneur-vs-societe-inspection'
  ],

  // ============================================
  // CATÉGORIE 7 : TÉMOIGNAGES (5 pages)
  // ============================================
  temoignages: [
    'temoignages-etudiants-inspecteur-auto',
    'success-story-mecanicien-inspecteur-independant',
    'reconversion-professionnelle-inspecteur-auto',
    'avis-formation-inspecteur-automobile',
    'etudes-cas-inspections-reussies'
  ]
};

// EXPORT DES URLS POUR LE ROUTING
export const allPageIds = {
  piliers: Object.keys(seoPageDatabase.piliers),
  techniquesDiag: Object.keys(seoPageDatabase.techniques.diagnostic),
  techniquesCarr: Object.keys(seoPageDatabase.techniques.carrosserie),
  longTailComment: seoPageDatabase.longTail.comment,
  longTailPourquoi: seoPageDatabase.longTail.pourquoi,
  longTailQuel: seoPageDatabase.longTail.quel,
  marques: seoPageDatabase.marques,
  geo: seoPageDatabase.geo,
  comparaisons: seoPageDatabase.comparaisons,
  temoignages: seoPageDatabase.temoignages
};

console.log('📊 Total pages configurées :', 
  allPageIds.piliers.length +
  allPageIds.techniquesDiag.length +
  allPageIds.techniquesCarr.length +
  allPageIds.longTailComment.length +
  allPageIds.longTailPourquoi.length +
  allPageIds.longTailQuel.length +
  allPageIds.marques.length +
  allPageIds.geo.length +
  allPageIds.comparaisons.length +
  allPageIds.temoignages.length
);
