import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Shield, Lock, Eye, Database, UserCheck, FileText } from 'lucide-react';

function Confidentialite() {
  return (
    <>
      <Helmet>
        <title>Politique de Confidentialité - Formation Inspecteur Automobile</title>
        <meta name="robots" content="noindex, nofollow" />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center">
                <Shield className="w-12 h-12 text-blue-600" />
              </div>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Politique de Confidentialité</h1>
            <p className="text-lg text-gray-600">Votre vie privée est notre priorité</p>
          </div>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center">
                <FileText className="w-5 h-5 mr-2 text-blue-600" />
                Introduction
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                La présente Politique de Confidentialité décrit comment Inspecteur Auto Formation collecte, utilise, partage et protège vos données personnelles conformément au Règlement Général sur la Protection des Données (RGPD) et à la loi Informatique et Libertés.
              </p>
              <p className="text-gray-700">
                <strong>Responsable du traitement :</strong> Inspecteur Auto Formation, SAS<br />
                <strong>Contact DPO :</strong> <a href="mailto:rgpd@inspecteur-auto.fr" className="text-blue-600 hover:underline">rgpd@inspecteur-auto.fr</a>
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Database className="w-5 h-5 mr-2 text-blue-600" />
                1. Données Collectées
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">1.1 Données d'inscription</h4>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Nom et prénom</li>
                    <li>Adresse email</li>
                    <li>Numéro de téléphone (optionnel)</li>
                    <li>Mot de passe (chiffré)</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">1.2 Données de pré-inscription (questionnaire Qualiopi)</h4>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Expérience professionnelle dans l'automobile</li>
                    <li>Projet professionnel</li>
                    <li>Disponibilité pour la formation</li>
                    <li>Possession du permis de conduire (permis B)</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">1.3 Données de paiement</h4>
                  <p className="text-gray-700">Traitées de manière sécurisée par notre partenaire Stripe (certifié PCI-DSS). Nous ne stockons jamais vos informations bancaires complètes.</p>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">1.4 Données de suivi pédagogique</h4>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Modules consultés et progression</li>
                    <li>Résultats aux quiz et évaluations</li>
                    <li>Temps passé sur la plateforme</li>
                    <li>Échanges avec l'assistant IA et le forum</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">1.5 Données techniques</h4>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Adresse IP</li>
                    <li>Type de navigateur et appareil</li>
                    <li>Cookies (voir section dédiée)</li>
                    <li>Logs de connexion</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Eye className="w-5 h-5 mr-2 text-blue-600" />
                2. Finalités du Traitement
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">Vos données sont collectées pour :</p>
              <ul className="list-disc list-inside text-gray-700 space-y-2">
                <li><strong>Gestion de votre compte</strong> - Création, authentification, accès à la plateforme</li>
                <li><strong>Suivi pédagogique</strong> - Personnalisation du parcours, évaluation des compétences, délivrance du certificat</li>
                <li><strong>Facturation</strong> - Émission de factures, gestion des paiements et remboursements</li>
                <li><strong>Communication</strong> - Envoi d'emails de confirmation, notifications de progression, support client</li>
                <li><strong>Amélioration du service</strong> - Statistiques d'usage (anonymisées), optimisation de la plateforme</li>
                <li><strong>Conformité Qualiopi</strong> - Conservation des preuves de formation pour audits</li>
                <li><strong>Obligations légales</strong> - Respect des obligations fiscales et comptables</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Lock className="w-5 h-5 mr-2 text-blue-600" />
                3. Base Légale et Durée de Conservation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="border-b-2">
                    <tr>
                      <th className="text-left p-2">Type de données</th>
                      <th className="text-left p-2">Base légale</th>
                      <th className="text-left p-2">Durée</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    <tr>
                      <td className="p-2">Données d'inscription</td>
                      <td className="p-2">Contrat</td>
                      <td className="p-2">3 ans après dernière connexion</td>
                    </tr>
                    <tr>
                      <td className="p-2">Données pédagogiques</td>
                      <td className="p-2">Obligation légale (Qualiopi)</td>
                      <td className="p-2">10 ans (archives)</td>
                    </tr>
                    <tr>
                      <td className="p-2">Données de facturation</td>
                      <td className="p-2">Obligation légale (fiscale)</td>
                      <td className="p-2">10 ans</td>
                    </tr>
                    <tr>
                      <td className="p-2">Cookies analytiques</td>
                      <td className="p-2">Consentement</td>
                      <td className="p-2">13 mois</td>
                    </tr>
                    <tr>
                      <td className="p-2">Logs techniques</td>
                      <td className="p-2">Intérêt légitime (sécurité)</td>
                      <td className="p-2">1 an</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>4. Partage des Données</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">Vos données ne sont jamais vendues. Elles peuvent être partagées uniquement avec :</p>
              <ul className="list-disc list-inside text-gray-700 space-y-2">
                <li><strong>Stripe</strong> - Traitement des paiements (certifié PCI-DSS)</li>
                <li><strong>SendGrid</strong> - Envoi d'emails transactionnels (sous-traitant RGPD)</li>
                <li><strong>OpenAI</strong> - Fonctionnement de l'assistant IA (données anonymisées)</li>
                <li><strong>Hébergeur cloud</strong> - Stockage sécurisé des données (UE)</li>
                <li><strong>Autorités compétentes</strong> - Sur réquisition judiciaire uniquement</li>
              </ul>
              <p className="text-gray-700 mt-4">
                Tous nos sous-traitants sont conformes au RGPD et ont signé des accords de confidentialité.
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center">
                <UserCheck className="w-5 h-5 mr-2 text-blue-600" />
                5. Vos Droits
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">Conformément au RGPD, vous disposez des droits suivants :</p>
              <ul className="space-y-3">
                <li className="flex items-start">
                  <span className="font-semibold text-gray-900 mr-2">•</span>
                  <div>
                    <strong>Droit d'accès</strong> - Obtenir une copie de vos données personnelles
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="font-semibold text-gray-900 mr-2">•</span>
                  <div>
                    <strong>Droit de rectification</strong> - Corriger des données inexactes
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="font-semibold text-gray-900 mr-2">•</span>
                  <div>
                    <strong>Droit à l'effacement</strong> - Supprimer vos données (sauf obligations légales)
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="font-semibold text-gray-900 mr-2">•</span>
                  <div>
                    <strong>Droit d'opposition</strong> - Vous opposer à certains traitements
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="font-semibold text-gray-900 mr-2">•</span>
                  <div>
                    <strong>Droit à la portabilité</strong> - Récupérer vos données dans un format structuré
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="font-semibold text-gray-900 mr-2">•</span>
                  <div>
                    <strong>Droit de limitation</strong> - Limiter le traitement de vos données
                  </div>
                </li>
              </ul>
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-900 font-semibold mb-2">Pour exercer vos droits :</p>
                <p className="text-blue-800">Envoyez un email à <a href="mailto:rgpd@inspecteur-auto.fr" className="underline">rgpd@inspecteur-auto.fr</a> avec une copie de votre pièce d'identité.<br />Délai de réponse : 1 mois maximum.</p>
              </div>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>6. Sécurité des Données</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">Nous mettons en œuvre des mesures de sécurité appropriées :</p>
              <ul className="list-disc list-inside text-gray-700 space-y-2">
                <li>Chiffrement des données sensibles (SSL/TLS)</li>
                <li>Mots de passe hashés avec bcrypt</li>
                <li>Authentification sécurisée (JWT tokens)</li>
                <li>Sauvegardes régulières et redondantes</li>
                <li>Accès restreint aux données (principe du moindre privilège)</li>
                <li>Surveillance et logs de sécurité</li>
                <li>Tests de sécurité réguliers</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>7. Cookies</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">Nous utilisons les types de cookies suivants :</p>
              <ul className="space-y-3">
                <li>
                  <strong className="text-gray-900">Cookies essentiels</strong> (pas de consentement requis)<br />
                  <span className="text-gray-600 text-sm">Authentification, sécurité, panier</span>
                </li>
                <li>
                  <strong className="text-gray-900">Cookies fonctionnels</strong> (consentement requis)<br />
                  <span className="text-gray-600 text-sm">Préférences utilisateur, langue</span>
                </li>
                <li>
                  <strong className="text-gray-900">Cookies analytiques</strong> (consentement requis)<br />
                  <span className="text-gray-600 text-sm">Statistiques d'usage anonymisées</span>
                </li>
              </ul>
              <p className="text-gray-700 mt-4">
                Vous pouvez gérer vos préférences cookies depuis les paramètres de votre navigateur.
              </p>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>8. Transferts Internationaux</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700">
                Vos données sont stockées au sein de l'Union Européenne. Certains sous-traitants (OpenAI, Stripe) peuvent transférer des données hors UE dans le respect des garanties appropriées (clauses contractuelles types de la Commission Européenne).
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>9. Modifications</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                Nous nous réservons le droit de modifier cette politique de confidentialité à tout moment. Les modifications entreront en vigueur dès leur publication sur cette page.
              </p>
              <p className="text-gray-700">
                Date de dernière mise à jour : <strong>Janvier 2025</strong>
              </p>
            </CardContent>
          </Card>

          <div className="mt-8 p-6 bg-green-50 border border-green-200 rounded-lg">
            <h3 className="font-semibold text-green-900 mb-2">Réclamation CNIL</h3>
            <p className="text-green-800 text-sm">
              Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une réclamation auprès de la CNIL :<br />
              <a href="https://www.cnil.fr/" target="_blank" rel="noopener noreferrer" className="underline">www.cnil.fr</a>
            </p>
          </div>

        </div>
      </div>
    </>
  );
}

export default Confidentialite;