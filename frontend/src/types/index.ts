export interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export interface User {
  _id: string;
  name: string;
  email: string;
  grad_year: number;
  concentration?: string;
  certificates: string[];
}

export interface CreateUserRequest {
  name: string;
  email: string;
  grad_year: number;
  concentration?: string;
  certificates?: string[];
} 