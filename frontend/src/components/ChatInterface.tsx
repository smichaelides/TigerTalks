import React from 'react';
import { FiArrowUp, FiDownload } from 'react-icons/fi';
import type { Message } from '../types';

interface ChatInterfaceProps {
  messages: Message[];
  inputValue: string;
  setInputValue: (value: string) => void;
  handleSendMessage: (customText?: string) => void;
  handleKeyDown: (e: React.KeyboardEvent) => void;
  isLoading: boolean;
  getAvatar: () => string;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
}

function ChatInterface({
  messages,
  inputValue,
  setInputValue,
  handleSendMessage,
  handleKeyDown,
  isLoading,
  getAvatar,
  messagesEndRef
}: ChatInterfaceProps) {

  const handleDownloadChat = () => {
    if (messages.length === 0) return;

    const chatContent = messages.map(message => {
      const sender = message.isUser ? 'You' : 'Tiggy';
      const time = message.timestamp.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
      return `[${time}] ${sender}: ${message.text}`;
    }).join('\n\n');

    const blob = new Blob([chatContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tiggy-chat-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="chat-layout">
      {messages.length > 0 && (
        <button 
          className="download-chat-button"
          onClick={handleDownloadChat}
          title="Download Chat"
          data-tooltip="Download Chat"
        >
          <FiDownload />
        </button>
      )}
      {/* Messages */}
      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.isUser ? 'message-user' : 'message-ai'}`}
          >
            <div className="message-content">
              {!message.isUser && (
                <div className="avatar ai-avatar">
                  <img src={getAvatar()} alt="Tiger AI" />
                </div>
              )}
              <div className={`message-bubble ${message.isUser ? 'user-bubble' : 'ai-bubble'}`}>
                <p className="message-text">{message.text}</p>
              </div>
            </div>
            <div className={`message-time ${message.isUser ? 'time-right' : 'time-left'}`}>
              {message.timestamp.toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message message-ai">
            <div className="message-content">
              <div className="avatar ai-avatar">
                <img src={getAvatar()} alt="Tiger AI" />
              </div>
              <div className="message-bubble ai-bubble">
                <p className="message-text">Tiggy is thinking...</p>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          <input
            type="text"
            placeholder="Ask me anything..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="chat-input"
            disabled={isLoading}
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            <FiArrowUp />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInterface; 