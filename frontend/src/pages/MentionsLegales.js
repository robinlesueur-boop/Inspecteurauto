import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

function MentionsLegales() {
  return (
    <>
      <Helmet>
        <title>Mentions Légales - Formation Inspecteur Automobile</title>
        <meta name="robots" content="noindex, nofollow" />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <h1 className="text-4xl font-bold text-gray-900 mb-8">Mentions Légales</h1>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>1. Éditeur du Site</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-2"><strong>Raison sociale :</strong> Inspecteur Auto Formation</p>
              <p className="text-gray-700 mb-2"><strong>Forme juridique :</strong> SAS (Société par Actions Simplifiée)</p>
              <p className="text-gray-700 mb-2"><strong>Capital social :</strong> 10 000 €</p>
              <p className="text-gray-700 mb-2"><strong>SIRET :</strong> [En cours d'attribution]</p>
              <p className="text-gray-700 mb-2"><strong>Numéro de déclaration d'activité :</strong> [En cours d'attribution]</p>
              <p className="text-gray-700 mb-2"><strong>Siège social :</strong> Paris, France</p>
              <p className="text-gray-700 mb-2"><strong>Email :</strong> contact@inspecteur-auto.fr</p>
              <p className="text-gray-700 mb-2"><strong>Directeur de publication :</strong> [Nom du Responsable]</p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>2. Hébergement</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-2"><strong>Hébergeur :</strong> Emergent Cloud Services</p>
              <p className="text-gray-700 mb-2"><strong>Adresse :</strong> [Adresse hébergeur]</p>
              <p className="text-gray-700">Les données sont hébergées sur des serveurs sécurisés situés en France/Union Européenne.</p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>3. Propriété Intellectuelle</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                L'ensemble de ce site relève de la législation française et internationale sur le droit d'auteur et la propriété intellectuelle. Tous les droits de reproduction sont réservés.
              </p>
              <p className="text-gray-700 mb-4">
                Les contenus de formation, textes, images, vidéos, logos et marques présents sur ce site sont protégés par le droit d'auteur. Toute reproduction, représentation, modification, publication, adaptation de tout ou partie des éléments du site, quel que soit le moyen ou le procédé utilisé, est interdite, sauf autorisation écrite préalable.
              </p>
              <p className="text-gray-700">
                <strong>Marques déposées :</strong> "AutoJust", "Méthode AutoJust" et le logo Inspecteur Auto sont des marques déposées.
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>4. Responsabilité</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                <strong>4.1 Contenu de la formation</strong><br />
                L'éditeur s'efforce d'assurer l'exactitude et la mise à jour des informations diffusées sur ce site. Toutefois, il ne peut garantir l'exactitude, la précision ou l'exhaustivité des informations mises à disposition.
              </p>
              <p className="text-gray-700 mb-4">
                <strong>4.2 Limitation de responsabilité</strong><br />
                L'éditeur ne saurait être tenu responsable des dommages directs ou indirects résultant de l'accès au site ou de l'utilisation des informations qui y figurent.
              </p>
              <p className="text-gray-700 mb-4">
                <strong>4.3 Exercice professionnel</strong><br />
                La formation dispensée ne constitue pas une garantie de résultats professionnels. L'exercice du métier d'inspecteur automobile requiert des compétences, une expérience pratique et le respect de la réglementation en vigueur.
              </p>
              <p className="text-gray-700">
                <strong>4.4 Liens hypertextes</strong><br />
                Le site peut contenir des liens vers d'autres sites. L'éditeur n'exerce aucun contrôle sur ces sites et décline toute responsabilité quant à leur contenu.
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>5. Protection des Données Personnelles</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                Conformément au Règlement Général sur la Protection des Données (RGPD) et à la loi Informatique et Libertés, vous disposez d'un droit d'accès, de rectification, de suppression et d'opposition aux données personnelles vous concernant.
              </p>
              <p className="text-gray-700 mb-4">
                <strong>Responsable du traitement :</strong> Inspecteur Auto Formation<br />
                <strong>Finalité :</strong> Gestion des inscriptions, suivi pédagogique, facturation, communication<br />
                <strong>Durée de conservation :</strong> Durée légale (10 ans pour documents comptables, 3 ans pour données marketing)
              </p>
              <p className="text-gray-700">
                Pour exercer vos droits, contactez : <a href="mailto:rgpd@inspecteur-auto.fr" className="text-blue-600 hover:underline">rgpd@inspecteur-auto.fr</a>
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>6. Cookies</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                Ce site utilise des cookies pour améliorer l'expérience utilisateur, réaliser des statistiques de visite et permettre le bon fonctionnement de la plateforme d'apprentissage.
              </p>
              <p className="text-gray-700">
                Vous pouvez paramétrer votre navigateur pour refuser les cookies. Toutefois, certaines fonctionnalités du site pourraient être impactées.
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>7. Conditions Générales de Vente</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                <strong>7.1 Prix</strong><br />
                Le prix de la formation est de 297€ TTC. Ce tarif est susceptible de modification sans préavis pour les nouvelles inscriptions.
              </p>
              <p className="text-gray-700 mb-4">
                <strong>7.2 Paiement</strong><br />
                Le paiement s'effectue par carte bancaire via notre partenaire sécurisé Stripe. L'accès à la formation est immédiat après validation du paiement.
              </p>
              <p className="text-gray-700 mb-4">
                <strong>7.3 Droit de rétractation</strong><br />
                Conformément à l'article L221-18 du Code de la consommation, vous disposez d'un délai de 14 jours pour exercer votre droit de rétractation sans avoir à justifier de motif. Le remboursement sera effectué sous 14 jours.
              </p>
              <p className="text-gray-700">
                <strong>7.4 Garantie</strong><br />
                Nous garantissons la qualité de notre formation. En cas d'insatisfaction, contactez notre service client : <a href="mailto:support@inspecteur-auto.fr" className="text-blue-600 hover:underline">support@inspecteur-auto.fr</a>
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>8. Règlement des Litiges</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                Les présentes mentions légales sont régies par le droit français. En cas de litige, une solution amiable sera recherchée avant toute action judiciaire.
              </p>
              <p className="text-gray-700 mb-4">
                <strong>Médiation de la consommation :</strong><br />
                Conformément à l'article L612-1 du Code de la consommation, nous proposons un dispositif de médiation de la consommation. Le médiateur peut être saisi sur : <a href="https://www.economie.gouv.fr/mediation-conso" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">https://www.economie.gouv.fr/mediation-conso</a>
              </p>
              <p className="text-gray-700">
                <strong>Juridiction compétente :</strong> En cas d'échec de la médiation, les tribunaux français seront seuls compétents.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>9. Contact</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-2">Pour toute question relative aux mentions légales :</p>
              <p className="text-gray-700"><strong>Email :</strong> <a href="mailto:legal@inspecteur-auto.fr" className="text-blue-600 hover:underline">legal@inspecteur-auto.fr</a></p>
            </CardContent>
          </Card>

          <div className="mt-8 text-sm text-gray-500 text-center">
            <p>Dernière mise à jour : Janvier 2025</p>
          </div>

        </div>
      </div>
    </>
  );
}

export default MentionsLegales;