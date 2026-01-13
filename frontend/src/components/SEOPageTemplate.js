import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { CheckCircle, ArrowRight, BookOpen, Award, Users } from 'lucide-react';

/**
 * Template réutilisable pour les pages SEO
 * Optimisé pour le référencement avec schema markup, meta tags, etc.
 */
function SEOPageTemplate({ 
  pageData,
  relatedPages = []
}) {
  const {
    title,
    metaTitle,
    metaDescription,
    metaKeywords,
    h1,
    introduction,
    sections,
    faq,
    cta,
    breadcrumbs,
    category
  } = pageData;

  // Schema markup
  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": metaTitle || title,
    "description": metaDescription,
    "author": {
      "@type": "Organization",
      "name": "Inspecteur Auto"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Inspecteur Auto",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.inspecteur-auto.fr/logo.png"
      }
    },
    "datePublished": new Date().toISOString(),
    "dateModified": new Date().toISOString()
  };

  // FAQ Schema
  const faqSchema = faq ? {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faq.map(item => ({
      "@type": "Question",
      "name": item.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": item.answer
      }
    }))
  } : null;

  return (
    <>
      <Helmet>
        <title>{metaTitle || title}</title>
        <meta name="description" content={metaDescription} />
        {metaKeywords && <meta name="keywords" content={metaKeywords} />}
        
        {/* Open Graph */}
        <meta property="og:title" content={metaTitle || title} />
        <meta property="og:description" content={metaDescription} />
        <meta property="og:type" content="article" />
        
        {/* Structured Data */}
        <script type="application/ld+json">
          {JSON.stringify(articleSchema)}
        </script>
        {faqSchema && (
          <script type="application/ld+json">
            {JSON.stringify(faqSchema)}
          </script>
        )}
      </Helmet>

      <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
        {/* Breadcrumbs */}
        {breadcrumbs && (
          <div className="bg-white border-b">
            <div className="max-w-4xl mx-auto px-4 py-3">
              <nav className="flex items-center space-x-2 text-sm text-gray-600">
                <Link to="/" className="hover:text-blue-600">Accueil</Link>
                {breadcrumbs.map((crumb, idx) => (
                  <React.Fragment key={idx}>
                    <span>›</span>
                    {crumb.url ? (
                      <Link to={crumb.url} className="hover:text-blue-600">{crumb.label}</Link>
                    ) : (
                      <span className="text-gray-900 font-medium">{crumb.label}</span>
                    )}
                  </React.Fragment>
                ))}
              </nav>
            </div>
          </div>
        )}

        {/* Hero Section */}
        <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
          <div className="max-w-4xl mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              {category && (
                <Badge className="mb-4 bg-white/20 text-white border-white/30">
                  {category}
                </Badge>
              )}
              <h1 className="text-4xl md:text-5xl font-bold mb-4">
                {h1 || title}
              </h1>
              {introduction && (
                <p className="text-xl text-blue-100 leading-relaxed">
                  {introduction}
                </p>
              )}
            </motion.div>
          </div>
        </section>

        {/* Main Content */}
        <section className="py-12">
          <div className="max-w-4xl mx-auto px-4">
            <article className="prose prose-lg max-w-none">
              {sections && sections.map((section, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: idx * 0.1 }}
                  viewport={{ once: true }}
                  className="mb-12"
                >
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">
                    {section.title}
                  </h2>
                  <div className="text-gray-700 leading-relaxed space-y-4">
                    {section.content.map((paragraph, pIdx) => (
                      <p key={pIdx}>{paragraph}</p>
                    ))}
                  </div>
                  
                  {section.list && (
                    <ul className="list-none space-y-3 my-6">
                      {section.list.map((item, lIdx) => (
                        <li key={lIdx} className="flex items-start">
                          <CheckCircle className="h-6 w-6 text-green-600 mr-3 flex-shrink-0 mt-1" />
                          <span className="text-gray-700">{item}</span>
                        </li>
                      ))}
                    </ul>
                  )}

                  {section.subsections && section.subsections.map((sub, sIdx) => (
                    <div key={sIdx} className="ml-6 mt-6">
                      <h3 className="text-2xl font-semibold text-gray-900 mb-3">
                        {sub.title}
                      </h3>
                      <div className="text-gray-700 space-y-2">
                        {sub.content.map((p, pIdx) => (
                          <p key={pIdx}>{p}</p>
                        ))}
                      </div>
                    </div>
                  ))}
                </motion.div>
              ))}
            </article>

            {/* FAQ Section */}
            {faq && faq.length > 0 && (
              <div className="mt-16">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
                  Questions Fréquentes
                </h2>
                <div className="space-y-4">
                  {faq.map((item, idx) => (
                    <Card key={idx}>
                      <CardHeader>
                        <CardTitle className="text-lg">{item.question}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-gray-700">{item.answer}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Related Pages */}
            {relatedPages.length > 0 && (
              <div className="mt-16">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">
                  Articles Connexes
                </h3>
                <div className="grid md:grid-cols-2 gap-6">
                  {relatedPages.map((page, idx) => (
                    <Link key={idx} to={page.url}>
                      <Card className="hover:shadow-lg transition-shadow h-full">
                        <CardContent className="p-6">
                          <h4 className="font-semibold text-lg mb-2 text-gray-900">
                            {page.title}
                          </h4>
                          <p className="text-gray-600 text-sm mb-4">
                            {page.description}
                          </p>
                          <span className="text-blue-600 text-sm font-medium inline-flex items-center">
                            Lire la suite <ArrowRight className="ml-2 h-4 w-4" />
                          </span>
                        </CardContent>
                      </Card>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* CTA Section */}
            {cta && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
                className="mt-16 bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-2xl p-8 md:p-12 text-center"
              >
                <h3 className="text-3xl font-bold mb-4">{cta.title}</h3>
                <p className="text-xl text-blue-100 mb-8">{cta.description}</p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link to={cta.primaryLink.url}>
                    <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                      {cta.primaryLink.text}
                    </Button>
                  </Link>
                  {cta.secondaryLink && (
                    <Link to={cta.secondaryLink.url}>
                      <Button 
                        size="lg" 
                        variant="outline" 
                        className="w-full sm:w-auto border-white text-white hover:bg-white/10"
                      >
                        {cta.secondaryLink.text}
                      </Button>
                    </Link>
                  )}
                </div>
              </motion.div>
            )}
          </div>
        </section>
      </div>
    </>
  );
}

export default SEOPageTemplate;
