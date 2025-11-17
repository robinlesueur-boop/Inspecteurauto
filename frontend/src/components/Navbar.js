import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Button } from "./ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { 
  Menu, 
  X, 
  Car, 
  User, 
  LogOut, 
  BookOpen, 
  MessageCircle,
  Settings,
  Award,
  Shield,
  BarChart3
} from "lucide-react";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const isActive = (path) => location.pathname === path;
  const isAdmin = user?.is_admin;

  return (
    <nav className="bg-white shadow-lg border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link 
            to="/" 
            className="flex items-center space-x-3 text-xl font-bold text-blue-600 hover:text-blue-700 transition-colors"
            data-testid="navbar-logo"
          >
            <div className="bg-blue-600 text-white p-2 rounded-lg">
              <Car className="h-6 w-6" />
            </div>
            <span className="hidden sm:block">Inspecteur Auto</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {user ? (
              <>
                <Link 
                  to="/dashboard" 
                  className={`text-gray-700 hover:text-blue-600 transition-colors font-medium ${
                    isActive('/dashboard') ? 'text-blue-600 border-b-2 border-blue-600 pb-1' : ''
                  }`}
                  data-testid="navbar-dashboard-link"
                >
                  <div className="flex items-center space-x-1">
                    <BookOpen className="h-4 w-4" />
                    <span>Formation</span>
                  </div>
                </Link>
                
                {user.has_purchased && (
                  <Link 
                    to="/forum" 
                    className={`text-gray-700 hover:text-blue-600 transition-colors font-medium ${
                      isActive('/forum') ? 'text-blue-600 border-b-2 border-blue-600 pb-1' : ''
                    }`}
                    data-testid="navbar-forum-link"
                  >
                    <div className="flex items-center space-x-1">
                      <MessageCircle className="h-4 w-4" />
                      <span>Forum</span>
                    </div>
                  </Link>
                )}

                {/* Admin Link */}
                {isAdmin && (
                  <Link 
                    to="/admin" 
                    className={`text-gray-700 hover:text-blue-600 transition-colors font-medium ${
                      location.pathname.startsWith('/admin') ? 'text-blue-600 border-b-2 border-blue-600 pb-1' : ''
                    }`}
                    data-testid="navbar-admin-link"
                  >
                    <div className="flex items-center space-x-1">
                      <Shield className="h-4 w-4" />
                      <span>Admin</span>
                    </div>
                  </Link>
                )}
                
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="relative h-10 w-10 rounded-full" data-testid="user-menu-trigger">
                      <Avatar className="h-10 w-10">
                        <AvatarImage src={user.avatar_url} alt={user.full_name} />
                        <AvatarFallback className="bg-blue-100 text-blue-600 font-semibold">
                          {user.full_name?.charAt(0) || 'U'}
                        </AvatarFallback>
                      </Avatar>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="w-56" align="end" forceMount>
                    <div className="flex items-center justify-start gap-2 p-2">
                      <div className="flex flex-col space-y-1 leading-none">
                        <p className="font-medium text-sm">{user.full_name}</p>
                        <p className="text-xs text-muted-foreground">{user.email}</p>
                        {isAdmin && (
                          <div className="flex items-center text-xs text-blue-600">
                            <Shield className="h-3 w-3 mr-1" />
                            Administrateur
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <DropdownMenuSeparator />
                    
                    <DropdownMenuItem asChild>
                      <Link to="/dashboard" className="flex items-center">
                        <BookOpen className="mr-2 h-4 w-4" />
                        <span>Ma Formation</span>
                      </Link>
                    </DropdownMenuItem>
                    
                    {user.has_purchased && (
                      <>
                        <DropdownMenuItem asChild>
                          <Link to="/forum" className="flex items-center">
                            <MessageCircle className="mr-2 h-4 w-4" />
                            <span>Forum</span>
                          </Link>
                        </DropdownMenuItem>
                        
                        {user.certificate_url && (
                          <DropdownMenuItem 
                            onClick={() => window.open(user.certificate_url, '_blank')}
                            className="flex items-center cursor-pointer"
                          >
                            <Award className="mr-2 h-4 w-4" />
                            <span>Mon Certificat</span>
                          </DropdownMenuItem>
                        )}
                      </>
                    )}

                    {/* Admin Menu Items */}
                    {isAdmin && (
                      <>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem asChild>
                          <Link to="/admin" className="flex items-center">
                            <BarChart3 className="mr-2 h-4 w-4" />
                            <span>Dashboard Admin</span>
                          </Link>
                        </DropdownMenuItem>
                        <DropdownMenuItem asChild>
                          <Link to="/admin/users" className="flex items-center">
                            <User className="mr-2 h-4 w-4" />
                            <span>Utilisateurs</span>
                          </Link>
                        </DropdownMenuItem>
                      </>
                    )}
                    
                    <DropdownMenuSeparator />
                    
                    <DropdownMenuItem onClick={handleLogout} data-testid="logout-button">
                      <LogOut className="mr-2 h-4 w-4" />
                      <span>Se déconnecter</span>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login" data-testid="navbar-login-link">
                  <Button variant="outline" className="font-medium border-gray-600 text-gray-900 hover:border-blue-600 hover:text-blue-600 hover:bg-blue-50">
                    Connexion
                  </Button>
                </Link>
                <Link to="/register" data-testid="navbar-register-link">
                  <Button className="bg-blue-600 hover:bg-blue-700 font-medium">
                    S'inscrire
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              data-testid="mobile-menu-button"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t bg-white" data-testid="mobile-menu">
            <div className="flex flex-col space-y-4">
              {user ? (
                <>
                  <Link 
                    to="/dashboard" 
                    className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors px-4 py-2 font-medium"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <BookOpen className="h-4 w-4" />
                    <span>Formation</span>
                  </Link>
                  
                  {user.has_purchased && (
                    <Link 
                      to="/forum" 
                      className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors px-4 py-2 font-medium"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      <MessageCircle className="h-4 w-4" />
                      <span>Forum</span>
                    </Link>
                  )}

                  {isAdmin && (
                    <Link 
                      to="/admin" 
                      className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors px-4 py-2 font-medium"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      <Shield className="h-4 w-4" />
                      <span>Admin</span>
                    </Link>
                  )}
                  
                  <div className="flex items-center px-4 py-2 text-sm text-gray-600">
                    <User className="mr-2 h-4 w-4" />
                    {user.full_name}
                    {isAdmin && <Shield className="ml-2 h-3 w-3 text-blue-600" />}
                  </div>
                  
                  <button
                    onClick={() => {
                      handleLogout();
                      setMobileMenuOpen(false);
                    }}
                    className="flex items-center px-4 py-2 text-gray-700 hover:text-blue-600 transition-colors font-medium"
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    Se déconnecter
                  </button>
                </>
              ) : (
                <div className="flex flex-col space-y-2 px-4">
                  <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
                    <Button variant="ghost" className="w-full justify-start font-medium">
                      Connexion
                    </Button>
                  </Link>
                  <Link to="/register" onClick={() => setMobileMenuOpen(false)}>
                    <Button className="w-full justify-start bg-blue-600 hover:bg-blue-700 font-medium">
                      S'inscrire
                    </Button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;