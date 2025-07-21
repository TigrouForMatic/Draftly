import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  DocumentTextIcon, 
  DocumentDuplicateIcon, 
  PlusIcon,
  ArrowUpIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { Document, Template } from '../types';
import apiService from '../services/api';

const Dashboard: React.FC = () => {
  const [recentDocuments, setRecentDocuments] = useState<Document[]>([]);
  const [recentTemplates, setRecentTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [documents, templates] = await Promise.all([
          apiService.getDocuments({ limit: 5 }),
          apiService.getTemplates({ limit: 5 })
        ]);
        setRecentDocuments(documents);
        setRecentTemplates(templates);
      } catch (error) {
        console.error('Erreur lors du chargement du tableau de bord:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const getDocumentTypeColor = (type: string) => {
    const colors = {
      devis: 'bg-blue-100 text-blue-800',
      facture: 'bg-green-100 text-green-800',
      contrat: 'bg-purple-100 text-purple-800',
      lettre: 'bg-yellow-100 text-yellow-800',
      cgv: 'bg-gray-100 text-gray-800',
      autre: 'bg-gray-100 text-gray-800',
    };
    return colors[type as keyof typeof colors] || colors.autre;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'finalized':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'sent':
        return <ArrowUpIcon className="h-5 w-5 text-blue-500" />;
      case 'draft':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tableau de bord</h1>
          <p className="text-gray-600">Bienvenue sur Draftly, votre générateur de documents IA</p>
        </div>
        <Link
          to="/documents/new"
          className="btn-primary flex items-center"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Nouveau document
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <DocumentTextIcon className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Documents créés</p>
              <p className="text-2xl font-semibold text-gray-900">{recentDocuments.length}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <DocumentDuplicateIcon className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Templates disponibles</p>
              <p className="text-2xl font-semibold text-gray-900">{recentTemplates.length}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircleIcon className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Documents finalisés</p>
              <p className="text-2xl font-semibold text-gray-900">
                {recentDocuments.filter(doc => doc.status === 'finalized').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Documents */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Documents récents</h2>
          <Link to="/documents" className="text-primary-600 hover:text-primary-500 text-sm">
            Voir tout
          </Link>
        </div>
        
        {recentDocuments.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Aucun document créé pour le moment</p>
        ) : (
          <div className="space-y-3">
            {recentDocuments.map((document) => (
              <div key={document.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(document.status)}
                  <div>
                    <p className="font-medium text-gray-900">{document.title}</p>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDocumentTypeColor(document.document_type)}`}>
                        {document.document_type}
                      </span>
                      <span className="text-sm text-gray-500">
                        {new Date(document.created_at).toLocaleDateString('fr-FR')}
                      </span>
                    </div>
                  </div>
                </div>
                <Link
                  to={`/documents/${document.id}`}
                  className="text-primary-600 hover:text-primary-500 text-sm"
                >
                  Voir
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent Templates */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Templates récents</h2>
          <Link to="/templates" className="text-primary-600 hover:text-primary-500 text-sm">
            Voir tout
          </Link>
        </div>
        
        {recentTemplates.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Aucun template disponible</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recentTemplates.map((template) => (
              <div key={template.id} className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <h3 className="font-medium text-gray-900 mb-2">{template.name}</h3>
                <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                <div className="flex items-center justify-between">
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDocumentTypeColor(template.category)}`}>
                    {template.category}
                  </span>
                  <Link
                    to={`/templates/${template.id}`}
                    className="text-primary-600 hover:text-primary-500 text-sm"
                  >
                    Utiliser
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 