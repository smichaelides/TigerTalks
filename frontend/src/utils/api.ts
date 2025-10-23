import type { User, CreateUserRequest } from '../types';
import type { Chat } from '../types';

// Generic API request helper
async function apiRequest<T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> {
  const url = `/api${endpoint}`;

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export const userAPI = {
  // Create a new user
  createUser: async (userData: CreateUserRequest): Promise<User> => {
    return apiRequest<User>('/user/create-user', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  // Get user by ID
  getUser: async (userId: string): Promise<User> => {
    return apiRequest<User>(`/user/get-user?userId=${userId}`);
  },

  // Get user by email
  getUserByEmail: async (email: string): Promise<User> => {
    return apiRequest<User>(`/user/get-user-by-email?email=${email}`);
  },

  // Update user concentration
  updateConcentration: async (userId: string, concentration: string): Promise<{ concentration: string }> => {
    return apiRequest<{ concentration: string }>('/user/update-concentration', {
      method: 'PATCH',
      body: JSON.stringify({ userId: userId, concentration }),
    });
  },

  // Update user certificates
  updateCertificates: async (userId: string, certificates: string[]): Promise<{ certificates: string[] }> => {
    return apiRequest<{ certificates: string[] }>('/user/update-certificates', {
      method: 'PATCH',
      body: JSON.stringify({ userId: userId, certificates }),
    });
  },
};

// Chat API functions
export const chatAPI = {
  createChat: async (userId: string): Promise<Chat> => {
    return apiRequest<Chat>('/chat/create-chat', {
      method: 'POST',
      body: JSON.stringify({ userId: userId }),
    });
  },

  // List user's chats
  listChats: async (userId: string): Promise<{ chats: Array<Chat> }> => {
    return apiRequest<{ chats: Array<Chat> }>(`/chat/list-chats?userId=${userId}`);
  },

  // Get chat with messages
  getChat: async (chatId: string, userId: string): Promise<Chat> => {
    return apiRequest<Chat>(`/chat/get-chat?chatId=${chatId}&userId=${userId}`);
  },

  // Send a message
  sendMessage: async (chatId: string, userId: string, message: string): Promise<{ model_message: string }> => {
    return apiRequest<{ model_message: string }>('/chat/send-message', {
      method: 'POST',
      body: JSON.stringify({
        chatId: chatId,
        userId: userId,
        message,
        timestamp: new Date().toISOString(),
      }),
    });
  },

  deleteChat: async (userId: string, chatId: string): Promise<{ chatId: string }> => {
    return apiRequest<{ model_message: string }>('/chat/delete-chat', {
      method: 'DELETE',
      body: JSON.stringify({
        chatId: chatId,
        userId: userId,
      }),
    }); 
  }
};
