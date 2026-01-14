import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from 'react-hot-toast';
import "./App.css";

// Context and Auth
import { AuthProvider, useAuth } from "./contexts/AuthContext";

// Components
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import AIChatWidget from "./components/AIChatWidget";
import ScrollToTop from "./components/ScrollToTop";

// Pages
import Home from "./pages/Home";
import Login from "./pages/Login";
import RegisterNew from "./pages/RegisterNew";
import Dashboard from "./pages/Dashboard";
import ModuleViewer from "./pages/ModuleViewer";
import PaymentSuccess from "./pages/PaymentSuccess";
import PaymentCancel from "./pages/PaymentCancel";
import PrivateChat from "./pages/PrivateChat";
import PreRegistration from "./pages/PreRegistration";
import QuizPageNew from "./components/QuizPageNew";
import MechanicalKnowledgeQuiz from "./pages/MechanicalKnowledgeQuiz";
import FinalEvaluation from "./pages/FinalEvaluation";
import SatisfactionSurvey from "./pages/SatisfactionSurvey";
import Blog from "./pages/Blog";
import Messages from "./pages/Messages";
import Certification from "./pages/Certification";
import MethodeInspection from "./pages/MethodeAutoJust";
import ProgrammeDetaille from "./pages/ProgrammeDetaille";
import FAQ from "./pages/FAQ";
import Contact from "./pages/Contact";
import MentionsLegales from "./pages/MentionsLegales";
import Confidentialite from "./pages/Confidentialite";

// Admin Pages
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminUsers from "./pages/admin/AdminUsers";
import AdminTransactions from "./pages/admin/AdminTransactions";
import AdminAnalytics from "./pages/admin/AdminAnalytics";
import AdminPreRegistrations from "./pages/admin/AdminPreRegistrations";
import AdminMessaging from "./pages/admin/AdminMessaging";
import AdminChat from "./pages/admin/AdminChat";
import AdminModules from "./pages/admin/AdminModules";
import AdminModulesNew from "./pages/admin/AdminModulesNew";
import AdminBlog from "./pages/admin/AdminBlog";
import AdminLandingPage from "./pages/admin/AdminLandingPage";
import AdminMechanicalQuiz from "./pages/admin/AdminMechanicalQuiz";
import AdminSEO from "./pages/admin/AdminSEO";

// SEO Pages
import DynamicSEOPage from "./pages/seo/DynamicSEOPage";
import SEOIndex from "./pages/seo/SEOIndex";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Protected Route Component with proper loading state
function ProtectedRoute({ children, requiresPurchase = false, requiresAdmin = false }) {
  const { isAuthenticated, user, loading } = useAuth();
  
  // Show loading spinner while checking auth
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (requiresAdmin && !user?.is_admin) {
    return <Navigate to="/dashboard" />;
  }
  
  if (requiresPurchase && !user?.has_purchased) {
    return <Navigate to="/dashboard" />;
  }
  
  return children;
}

function AppContent() {
  const { user } = useAuth();

  return (
    <div className="App min-h-screen bg-gray-50 flex flex-col">
      <BrowserRouter>
        <ScrollToTop />
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/certification" element={<Certification />} />
            <Route path="/methode-autojust" element={<MethodeInspection />} />
            <Route path="/programme-detaille" element={<ProgrammeDetaille />} />
            <Route path="/faq" element={<FAQ />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/mentions-legales" element={<MentionsLegales />} />
            <Route path="/confidentialite" element={<Confidentialite />} />
            <Route path="/pre-registration" element={<PreRegistration />} />
            
            {/* Dynamic SEO Pages - Route pour les 100 pages SEO */}
            <Route path="/seo/:pageId" element={<DynamicSEOPage />} />
            <Route path="/ressources" element={<SEOIndex />} />
            <Route path="/seo" element={<SEOIndex />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<RegisterNew />} />
            <Route path="/payment-success" element={<PaymentSuccess />} />
            <Route path="/payment-cancel" element={<PaymentCancel />} />
            
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/module/:moduleId" 
              element={
                <ProtectedRoute>
                  <ModuleViewer />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/quiz/:moduleId" 
              element={
                <ProtectedRoute>
                  <QuizPageNew />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/mechanical-knowledge-quiz" 
              element={
                <ProtectedRoute>
                  <MechanicalKnowledgeQuiz />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/final-evaluation" 
              element={
                <ProtectedRoute requiresPurchase={true}>
                  <FinalEvaluation />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/satisfaction-survey" 
              element={
                <ProtectedRoute requiresPurchase={true}>
                  <SatisfactionSurvey />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/messages" 
              element={
                <ProtectedRoute>
                  <Messages />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/chat" 
              element={
                <ProtectedRoute requiresPurchase={true}>
                  <PrivateChat />
                </ProtectedRoute>
              } 
            />

            {/* Admin Routes */}
            <Route 
              path="/admin" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminDashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/users" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminUsers />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/transactions" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminTransactions />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/analytics" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminAnalytics />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/pre-registrations" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminPreRegistrations />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/messaging" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminMessaging />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/modules" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminModulesNew />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/mechanical-quiz" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminMechanicalQuiz />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/blog" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminBlog />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/landing-page" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminLandingPage />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin/seo" 
              element={
                <ProtectedRoute requiresAdmin={true}>
                  <AdminSEO />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </main>
        <Footer />
        <AIChatWidget user={user} />
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </BrowserRouter>
    </div>
  );
}

function App() {
  return (
    <HelmetProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </HelmetProvider>
  );
}

export default App;