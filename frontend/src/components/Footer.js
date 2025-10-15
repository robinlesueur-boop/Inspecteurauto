import React from "react";
import { Link } from "react-router-dom";
import { Car, Mail, Phone, MapPin, Facebook, Twitter, Linkedin, Instagram } from "lucide-react";

function Footer() {
  return (
    <footer className="bg-gray-900 text-white mt-auto" data-testid="footer">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center space-x-3 text-xl font-bold mb-6">
              <div className="bg-blue-600 text-white p-2 rounded-lg">
                <Car className="h-6 w-6" />
              </div>
              <span>Inspecteur Auto</span>
            </Link>
            <p className="text-gray-300 mb-6 max-w-md leading-relaxed">
              Formation professionnelle d'inspecteur automobile. Devenez expert en diagnostic véhiculaire 
              avec notre méthode AutoJust reconnue par les professionnels.
            </p>
            
            {/* Contact Info */}
            <div className="space-y-3">
              <div className="flex items-center text-gray-300">
                <Mail className="h-4 w-4 mr-3 text-blue-400" />
                <span>contact@inspecteur-auto.fr</span>
              </div>
              <div className="flex items-center text-gray-300">
                <Phone className="h-4 w-4 mr-3 text-blue-400" />
                <span>01 23 45 67 89</span>
              </div>
              <div className="flex items-center text-gray-300">
                <MapPin className="h-4 w-4 mr-3 text-blue-400" />
                <span>Paris, France</span>
              </div>
            </div>
          </div>

          {/* Formation Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white">Formation</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/register" className="text-gray-300 hover:text-blue-400 transition-colors">
                  S'inscrire
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Mes cours
                </Link>
              </li>
              <li>
                <Link to="/methode-autojust" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Méthode AutoJust
                </Link>
              </li>
              <li>
                <Link to="/certification" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Certification
                </Link>
              </li>
              <li>
                <Link to="/forum" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Forum communauté
                </Link>
              </li>
              <li>
                <Link to="/blog" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Blog & Conseils
                </Link>
              </li>
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-white">Support</h3>
            <ul className="space-y-3">
              <li>
                <a href="#faq" className="text-gray-300 hover:text-blue-400 transition-colors">
                  FAQ
                </a>
              </li>
              <li>
                <a href="#help" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Centre d'aide
                </a>
              </li>
              <li>
                <a href="#contact" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Nous contacter
                </a>
              </li>
              <li>
                <a href="#legal" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Mentions légales
                </a>
              </li>
              <li>
                <a href="#privacy" className="text-gray-300 hover:text-blue-400 transition-colors">
                  Confidentialité
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Social Media & Bottom */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-6 mb-4 md:mb-0">
              <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors" aria-label="Facebook">
                <Facebook className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors" aria-label="Twitter">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors" aria-label="LinkedIn">
                <Linkedin className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors" aria-label="Instagram">
                <Instagram className="h-5 w-5" />
              </a>
            </div>
            
            <div className="text-center md:text-right">
              <p className="text-gray-400 text-sm mb-1">
                © {new Date().getFullYear()} Inspecteur Auto. Tous droits réservés.
              </p>
              <p className="text-gray-500 text-xs">
                Organisme de formation professionnelle certifié Qualiopi
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;