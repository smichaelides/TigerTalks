import { FiPlus, FiMessageSquare, FiTrash2 } from 'react-icons/fi';
import type { Chat } from '../types';

interface ChatSidebarProps {
  chats: Chat[];
  currentChatId: string;
  onChatSelect: (chatId: string) => void;
  onNewChat: () => void;
  onDeleteChat: (chatId: string) => void;
}

function ChatSidebar({ 
  chats, 
  currentChatId, 
  onChatSelect, 
  onNewChat, 
  onDeleteChat 
}: ChatSidebarProps) {
  const formatDate = (date: Date) => {
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffInHours < 48) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  };

  const getChatTitle = (chat: Chat) => {
    if (chat.title) return chat.title;
    
    // Generate title from first user message
    const firstUserMessage = chat.messages.find(msg => msg.isUser);
    if (firstUserMessage) {
      return firstUserMessage.text.length > 30 
        ? firstUserMessage.text.substring(0, 30) + '...'
        : firstUserMessage.text;
    }
    
    return 'New Chat';
  };

  return (
    <div className="chat-sidebar">
      <div className="sidebar-header">
        <button className="new-chat-button" onClick={onNewChat}>
          <FiPlus />
          <span>New Chat</span>
        </button>
      </div>
      
      <div className="chat-list">
        {chats.map((chat) => (
          <div
            key={chat.id}
            className={`chat-item ${chat.id === currentChatId ? 'active' : ''}`}
            onClick={() => onChatSelect(chat.id)}
          >
            <div className="chat-item-content">
              <FiMessageSquare className="chat-icon" />
              <div className="chat-info">
                <div className="chat-title">{getChatTitle(chat)}</div>
                <div className="chat-meta">
                  {chat.messages.length} messages • {formatDate(chat.updatedAt)}
                </div>
              </div>
            </div>
            {chats.length > 1 && (
              <button
                className="delete-chat-button"
                onClick={(e) => {
                  e.stopPropagation();
                  onDeleteChat(chat.id);
                }}
                title="Delete chat"
              >
                <FiTrash2 />
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatSidebar;
