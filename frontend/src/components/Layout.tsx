import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  DocumentTextIcon, 
  DocumentDuplicateIcon, 
  UserIcon, 
  ArrowRightOnRectangleIcon,
  HomeIcon
} from '@heroicons/react/24/outline';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const navigation = [
    { name: 'Tableau de bord', href: '/', icon: HomeIcon },
    { name: 'Documents', href: '/documents', icon: DocumentTextIcon },
    { name: 'Templates', href: '/templates', icon: DocumentDuplicateIcon },
    { name: 'Profil', href: '/profile', icon: UserIcon },
  ];

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link to="/" className="flex items-center">
                <DocumentTextIcon className="h-8 w-8 text-primary-600" />
                <span className="ml-2 text-xl font-bold text-gray-900">Draftly</span>
              </Link>
            </div>

            {user && (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  Bonjour, {user.full_name}
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center text-sm text-gray-500 hover:text-gray-700"
                >
                  <ArrowRightOnRectangleIcon className="h-5 w-5 mr-1" />
                  Déconnexion
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        {user && (
          <nav className="w-64 bg-white shadow-sm min-h-screen">
            <div className="p-4">
              <nav className="space-y-2">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                        isActive
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <item.icon className="h-5 w-5 mr-3" />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
          </nav>
        )}

        {/* Main content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout; 