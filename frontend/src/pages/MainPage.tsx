import React, { useState, useRef, useEffect } from 'react';
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

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

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
      <Header onLogout={onLogout} />
      
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