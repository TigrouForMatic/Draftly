import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { User, Document, Template, AuthResponse, LoginCredentials, RegisterData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Intercepteur pour ajouter le token d'authentification
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Intercepteur pour gérer les erreurs
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentification
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/login', formData);
    return response.data;
  }

  async register(userData: RegisterData): Promise<User> {
    const response: AxiosResponse<User> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/auth/me');
    return response.data;
  }

  // Documents
  async getDocuments(params?: { skip?: number; limit?: number; document_type?: string }): Promise<Document[]> {
    const response: AxiosResponse<Document[]> = await this.api.get('/documents', { params });
    return response.data;
  }

  async getDocument(id: number): Promise<Document> {
    const response: AxiosResponse<Document> = await this.api.get(`/documents/${id}`);
    return response.data;
  }

  async createDocument(document: Partial<Document>): Promise<Document> {
    const response: AxiosResponse<Document> = await this.api.post('/documents', document);
    return response.data;
  }

  async updateDocument(id: number, document: Partial<Document>): Promise<Document> {
    const response: AxiosResponse<Document> = await this.api.put(`/documents/${id}`, document);
    return response.data;
  }

  async deleteDocument(id: number): Promise<void> {
    await this.api.delete(`/documents/${id}`);
  }

  async generateDocumentContent(id: number): Promise<{ content: string }> {
    const response: AxiosResponse<{ content: string }> = await this.api.post(`/documents/${id}/generate`);
    return response.data;
  }

  async exportDocument(id: number, format: 'docx' | 'pdf' = 'docx'): Promise<{ file_path: string; message: string }> {
    const response: AxiosResponse<{ file_path: string; message: string }> = await this.api.post(`/documents/${id}/export`, null, {
      params: { format }
    });
    return response.data;
  }

  // Templates
  async getTemplates(params?: { skip?: number; limit?: number; category?: string; public_only?: boolean }): Promise<Template[]> {
    const response: AxiosResponse<Template[]> = await this.api.get('/templates', { params });
    return response.data;
  }

  async getTemplate(id: number): Promise<Template> {
    const response: AxiosResponse<Template> = await this.api.get(`/templates/${id}`);
    return response.data;
  }

  async createTemplate(template: Partial<Template>): Promise<Template> {
    const response: AxiosResponse<Template> = await this.api.post('/templates', template);
    return response.data;
  }

  async updateTemplate(id: number, template: Partial<Template>): Promise<Template> {
    const response: AxiosResponse<Template> = await this.api.put(`/templates/${id}`, template);
    return response.data;
  }

  async deleteTemplate(id: number): Promise<void> {
    await this.api.delete(`/templates/${id}`);
  }

  async duplicateTemplate(id: number): Promise<Template> {
    const response: AxiosResponse<Template> = await this.api.post(`/templates/${id}/duplicate`);
    return response.data;
  }

  async getTemplateCategories(): Promise<string[]> {
    const response: AxiosResponse<string[]> = await this.api.get('/templates/categories/list');
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService; 