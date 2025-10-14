import React from 'react';
import { Helmet } from 'react-helmet-async';
import PreRegistrationForm from '../components/PreRegistrationForm';

export default function PreRegistration() {
  return (
    <>
      <Helmet>
        <title>Pré-inscription - Formation Inspecteur Auto</title>
        <meta name="description" content="Validez votre profil pour accéder à la formation d'inspecteur automobile" />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-12">
        <PreRegistrationForm />
      </div>
    </>
  );
}
