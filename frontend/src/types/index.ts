export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Document {
  id: number;
  title: string;
  document_type: 'devis' | 'facture' | 'contrat' | 'lettre' | 'cgv' | 'autre';
  status: 'draft' | 'finalized' | 'sent' | 'archived';
  content?: string;
  template_data?: Record<string, any>;
  file_path?: string;
  user_id: number;
  template_id?: number;
  created_at: string;
  updated_at?: string;
}

export interface Template {
  id: number;
  name: string;
  description?: string;
  category: 'freelance' | 'agence' | 'juridique' | 'comptabilite' | 'rh' | 'autre';
  template_content: string;
  variables_schema?: Record<string, any>;
  is_public: boolean;
  is_active: boolean;
  user_id?: number;
  created_at: string;
  updated_at?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  full_name: string;
  password: string;
}

export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
} 