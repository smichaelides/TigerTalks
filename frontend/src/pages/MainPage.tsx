import React, { useState, useRef } from 'react';
import Header from '../components/Header';
import WelcomeScreen from '../components/WelcomeScreen';
import ChatInterface from '../components/ChatInterface';
import type { Message } from '../types';

// Import avatar images
import tigerAvatar from '../assets/tiggy.png';

interface MainPageProps {
  onLogout: () => void;
}

function MainPage({ onLogout }: MainPageProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const hasMessages = messages.length > 0;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

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

  const getAvatar = () => tigerAvatar;

  const handleSendMessage = (customText?: string) => {
    const textToSend = customText || inputValue;
    if (!textToSend.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: textToSend,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    scrollToBottom();

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'This is a simulated response. The backend integration will be added later!',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsLoading(false);
      scrollToBottom();
    }, 1000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="app">
      <Header 
        onLogout={onLogout} 
        onDownloadChat={handleDownloadChat}
        hasMessages={hasMessages}
      />
      
      <main className={`chat-container ${hasMessages ? 'chat-container-with-messages' : ''}`}>
        {!hasMessages ? (
          <WelcomeScreen 
            inputValue={inputValue}
            setInputValue={setInputValue}
            handleSendMessage={handleSendMessage}
            handleKeyDown={handleKeyDown}
            isLoading={isLoading}
          />
        ) : (
          <ChatInterface 
            messages={messages}
            inputValue={inputValue}
            setInputValue={setInputValue}
            handleSendMessage={handleSendMessage}
            handleKeyDown={handleKeyDown}
            isLoading={isLoading}
            getAvatar={getAvatar}
            messagesEndRef={messagesEndRef}
          />
        )}
      </main>
    </div>
  );
}

export default MainPage; 