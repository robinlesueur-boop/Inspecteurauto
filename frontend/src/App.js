import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from 'react-hot-toast';
import axios from "axios";
import "./App.css";

// Context and Auth
import { AuthProvider, useAuth } from "./contexts/AuthContext";

// Components
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

// Pages
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ModuleViewer from "./pages/ModuleViewer";
import PaymentSuccess from "./pages/PaymentSuccess";
import PaymentCancel from "./pages/PaymentCancel";
import Forum from "./pages/Forum";
import PreRegistration from "./pages/PreRegistration";

// Admin Pages
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminUsers from "./pages/admin/AdminUsers";
import AdminTransactions from "./pages/admin/AdminTransactions";
import AdminAnalytics from "./pages/admin/AdminAnalytics";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Protected Route Component
function ProtectedRoute({ children, requiresPurchase = false, requiresAdmin = false }) {
  const { isAuthenticated, user } = useAuth();
  
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
  const { setUser } = useAuth();

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Verify token and get user info
      axios.get(`${API}/auth/me`)
        .then(response => {
          setUser(response.data);
        })
        .catch(error => {
          console.error('Token verification failed:', error);
          localStorage.removeItem('token');
          delete axios.defaults.headers.common['Authorization'];
        });
    }
  }, [setUser]);

  return (
    <div className="App min-h-screen bg-gray-50 flex flex-col">
      <BrowserRouter>
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
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
              path="/forum" 
              element={
                <ProtectedRoute requiresPurchase={true}>
                  <Forum />
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
          </Routes>
        </main>
        <Footer />
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