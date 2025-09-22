import type { User, CreateUserRequest } from '../types';

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
    return apiRequest<User>(`/user/get-user?user_id=${userId}`);
  },

  // Update user concentration
  updateConcentration: async (userId: string, concentration: string): Promise<{ concentration: string }> => {
    return apiRequest<{ concentration: string }>('/user/update-concentration', {
      method: 'PATCH',
      body: JSON.stringify({ user_id: userId, concentration }),
    });
  },

  // Update user certificates
  updateCertificates: async (userId: string, certificates: string[]): Promise<{ certificates: string[] }> => {
    return apiRequest<{ certificates: string[] }>('/user/update-certificates', {
      method: 'PATCH',
      body: JSON.stringify({ user_id: userId, certificates }),
    });
  },
};

// Chat API functions
export const chatAPI = {
  createChat: async (userId: string): Promise<any> => {
    return apiRequest<any>('/chat/create-chat', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    });
  },

  // List user's chats
  listChats: async (userId: string): Promise<{ chats: Array<{ _id: string, created_at: string, updated_at: string }> }> => {
    return apiRequest<{ chats: Array<{ _id: string, created_at: string, updated_at: string  }> }>(`/chat/list-chats?user_id=${userId}`);
  },

  // Get chat with messages
  getChat: async (chatId: string, userId: string): Promise<any> => {
    return apiRequest<any>(`/chat/get-chat?chat_id=${chatId}&user_id=${userId}`);
  },

  // Send a message
  sendMessage: async (chatId: string, userId: string, message: string): Promise<{ model_message: string }> => {
    return apiRequest<{ model_message: string }>('/chat/send-message', {
      method: 'POST',
      body: JSON.stringify({
        chat_id: chatId,
        user_id: userId,
        message,
        timestamp: new Date().toISOString(),
      }),
    });
  },

  deleteChat: async (userId: string, chatId: string): Promise<{ chat_id: string }> => {
    return apiRequest<{ model_message: string }>('/chat/delete-chat', {
      method: 'DELETE',
      body: JSON.stringify({
        chat_id: chatId,
        user_id: userId,
      }),
    }); 
  }
};
