export interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatMessage {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export interface User {
  id: string;
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