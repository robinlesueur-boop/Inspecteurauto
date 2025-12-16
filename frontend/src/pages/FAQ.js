import React, { useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent } from '../components/ui/card';
import { ChevronDown, ChevronUp } from 'lucide-react';

function FAQ() {
  const [openIndex, setOpenIndex] = useState(null);

  const faqs = [
    {
      category: "Formation",
      questions: [
        {
          q: "Quelle est la durée de la formation ?",
          a: "La formation compte 8 modules pour un total de 9 heures de contenu vidéo et écrit. Vous pouvez suivre la formation à votre rythme, en général entre 2 et 4 semaines selon votre disponibilité."
        },
        {
          q: "Dois-je avoir des connaissances en mécanique ?",
          a: "Des connaissances de base en mécanique sont recommandées. Si vous n'avez pas d'expérience, nous proposons un quiz d'évaluation et un module de remise à niveau gratuit pour acquérir les fondamentaux."
        },
        {
          q: "La formation est-elle certifiée ?",
          a: "Oui, notre formation respecte les critères Qualiopi (certification en cours d'obtention). Vous recevez un certificat de formation professionnelle à l'issue du parcours."
        },
        {
          q: "Puis-je suivre la formation tout en travaillant ?",
          a: "Absolument ! La formation est 100% en ligne et accessible 24h/24. Vous progressez à votre rythme selon vos disponibilités."
        }
      ]
    },
    {
      category: "Contenu",
      questions: [
        {
          q: "Que comprend la formation ?",
          a: "8 modules couvrant tous les aspects de l'inspection automobile : diagnostic moteur, carrosserie, électronique, ADAS, méthodologie méthode d'inspection, pratique professionnelle. Plus de 10 quiz d'évaluation et un examen final certifiant."
        },
        {
          q: "Ai-je accès à un support pédagogique ?",
          a: "Oui ! Vous avez accès à un assistant IA disponible 24h/24 pour répondre à vos questions, un forum communautaire, et un système de messagerie avec les formateurs."
        },
        {
          q: "Le contenu est-il mis à jour ?",
          a: "Oui, le contenu est régulièrement mis à jour pour refléter les dernières technologies automobiles et évolutions réglementaires. Vous avez accès à vie aux mises à jour."
        }
      ]
    },
    {
      category: "Financement & Tarifs",
      questions: [
        {
          q: "Quel est le prix de la formation ?",
          a: "La formation coûte 297€ TTC, paiement unique. Ce tarif inclut l'accès à vie au contenu, les mises à jour, le certificat, et l'accès au forum communauté."
        },
        {
          q: "Puis-je payer en plusieurs fois ?",
          a: "Le paiement en 4 fois sans frais sera bientôt disponible. Actuellement, seul le paiement unique par carte bancaire est accepté."
        },
        {
          q: "La formation est-elle éligible au CPF ?",
          a: "Notre certification Qualiopi est en cours d'obtention. Une fois certifiés, la formation sera éligible au CPF. Nous vous informerons dès que possible."
        },
        {
          q: "Y a-t-il une garantie satisfait ou remboursé ?",
          a: "Oui, vous disposez de 14 jours pour tester la formation. Si vous n'êtes pas satisfait, nous vous remboursons intégralement sans question."
        }
      ]
    },
    {
      category: "Après la formation",
      questions: [
        {
          q: "Puis-je exercer immédiatement après la formation ?",
          a: "Oui ! Après validation de votre examen final, vous recevez votre certificat et pouvez commencer à proposer vos services d'inspection automobile en tant qu'indépendant."
        },
        {
          q: "Quel matériel faut-il pour débuter ?",
          a: "L'investissement de départ est d'environ 5 000-15 000€ : valise de diagnostic OBD (1000-3000€), outils de mesure, caméra, équipements de protection. Un guide d'achat détaillé est fourni dans le Module 8."
        },
        {
          q: "Quel revenu peut-on espérer ?",
          a: "Les inspecteurs facturent entre 150-400€ par inspection. Avec 3-5 inspections par jour, le potentiel de revenus est de 3 000-8 000€/mois selon votre zone géographique et votre expérience."
        },
        {
          q: "Puis-je rejoindre le réseau méthode d'inspection ?",
          a: "Les meilleurs diplômés peuvent candidater pour rejoindre le réseau méthode d'inspection en tant qu'inspecteur partenaire. Des opportunités sont régulièrement publiées dans le forum."
        }
      ]
    },
    {
      category: "Technique",
      questions: [
        {
          q: "Sur quels appareils puis-je suivre la formation ?",
          a: "La plateforme est accessible depuis ordinateur, tablette et smartphone. Une connexion internet est nécessaire."
        },
        {
          q: "Puis-je télécharger les cours ?",
          a: "Les cours sont consultables en ligne. Pour des raisons de droits d'auteur et de mises à jour, le téléchargement n'est pas autorisé."
        },
        {
          q: "Que faire si j'ai un problème technique ?",
          a: "Notre support technique est disponible par email (support@inspecteur-auto.fr) et répond sous 24h maximum. L'assistant IA peut également vous aider pour les questions courantes."
        }
      ]
    }
  ];

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  let questionIndex = 0;

  return (
    <>
      <Helmet>
        <title>FAQ - Questions Fréquentes | Formation Inspecteur Automobile</title>
        <meta name="description" content="Toutes les réponses à vos questions sur la formation d'inspecteur automobile : durée, contenu, tarifs, certification, débouchés." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Questions Fréquentes
            </h1>
            <p className="text-xl text-gray-600">
              Tout ce que vous devez savoir sur la formation d'inspecteur automobile
            </p>
          </div>

          {faqs.map((category, catIndex) => (
            <div key={catIndex} className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                {category.category}
              </h2>
              
              <div className="space-y-3">
                {category.questions.map((faq, index) => {
                  const currentIndex = questionIndex++;
                  return (
                    <Card key={index} className="overflow-hidden">
                      <button
                        onClick={() => toggleFAQ(currentIndex)}
                        className="w-full text-left p-6 hover:bg-gray-50 transition-colors"
                      >
                        <div className="flex justify-between items-start">
                          <h3 className="font-semibold text-gray-900 pr-4">
                            {faq.q}
                          </h3>
                          {openIndex === currentIndex ? (
                            <ChevronUp className="w-5 h-5 text-gray-500 flex-shrink-0" />
                          ) : (
                            <ChevronDown className="w-5 h-5 text-gray-500 flex-shrink-0" />
                          )}
                        </div>
                      </button>
                      
                      {openIndex === currentIndex && (
                        <CardContent className="px-6 pb-6">
                          <p className="text-gray-700">
                            {faq.a}
                          </p>
                        </CardContent>
                      )}
                    </Card>
                  );
                })}
              </div>
            </div>
          ))}

          <Card className="bg-blue-50 border-blue-200 mt-12">
            <CardContent className="p-8 text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Vous ne trouvez pas votre réponse ?
              </h2>
              <p className="text-gray-700 mb-6">
                Notre équipe est là pour vous aider ! Contactez-nous et nous vous répondrons dans les plus brefs délais.
              </p>
              <a href="/contact" className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
                Nous Contacter
              </a>
            </CardContent>
          </Card>

        </div>
      </div>
    </>
  );
}

export default FAQ;