import React from 'react';
import { FiArrowUp } from 'react-icons/fi';
import tigerAvatar from '../assets/tiggy.png';

interface WelcomeScreenProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  handleSendMessage: (customText?: string) => void;
  handleKeyDown: (e: React.KeyboardEvent) => void;
  isLoading: boolean;
}

function WelcomeScreen({ 
  inputValue, 
  setInputValue, 
  handleSendMessage, 
  handleKeyDown, 
  isLoading 
}: WelcomeScreenProps) {
  const suggestedQuestions = [
    "What events are happening tomorrow?",
    "Should I take COS217 or COS226?",
    "How do I register for classes?",
    "What's the weather like today?"
  ];

  const handleQuestionClick = (question: string) => handleSendMessage(question);

  return (
    <div className="welcome-container">
      <div className="welcome-content">
        <div className="welcome-title-container">
          <img src={tigerAvatar} alt="Tiggy" className="welcome-avatar" />
          <h2 className="welcome-title">What can I help you with today?</h2>
        </div>
        <div className="input-container-centered">
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
        {/* Suggested Questions */}
        <div className="suggested-questions">
          {suggestedQuestions.map((question, index) => (
            <button
              key={index}
              className="suggested-question-btn"
              onClick={() => handleQuestionClick(question)}
              disabled={isLoading}
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default WelcomeScreen; 