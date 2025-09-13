import React, { useState, useRef, useEffect } from "react";
import Header from "../components/Header";
import WelcomeScreen from "../components/WelcomeScreen";
import ChatInterface from "../components/ChatInterface";
import ChatSidebar from "../components/ChatSidebar";
import type { Message, Chat } from "../types";
import { chatAPI } from "../utils/api";
import { useNavigate } from "react-router-dom";

// Import avatar images
import tigerAvatar from "../assets/tiggy.png";

interface MainPageProps {
  onLogout: () => void;
}

function MainPage({ onLogout }: MainPageProps) {
  const [chats, setChats] = useState<Chat[]>([
    {
      id: "default",
      title: "New Chat",
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    },
  ]);
  const navigate = useNavigate();
  const [currentChatId, setCurrentChatId] = useState("default");
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentChat = chats.find((chat) => chat.id === currentChatId);
  const messages = currentChat?.messages || [];
  const hasMessages = messages.length > 0;

  // Auto-scroll to bottom whenever messages or loading state changes
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const getAvatar = () => tigerAvatar;

  const createNewChat = async () => {
    const userId = localStorage.getItem("userId");

    try {
      if (!userId) {
        console.error("User ID is null. Redirecting to login.");
        navigate("/login");
        return;
      }

      const chat = await chatAPI.createChat(userId);

      const newChat: Chat = {
        id: chat.id,
        title: "New Chat",
        messages: [],
        createdAt: new Date(chat.created_at),
        updatedAt: new Date(chat.updated_at),
      };

      setChats((prev) => [...prev, newChat]);
      setCurrentChatId(chat.id);
      setInputValue("");
    } catch (error) {
      console.error("Unable to create new chat:", error);
    }
  };

  const selectChat = (chatId: string) => {
    setCurrentChatId(chatId);
    setInputValue("");
  };

  const deleteChat = (chatId: string) => {
    if (chats.length <= 1) return;

    setChats((prev) => prev.filter((chat) => chat.id !== chatId));

    // If we're deleting the current chat, switch to new chat
    if (chatId === currentChatId) {
      const remainingChats = chats.filter((chat) => chat.id !== chatId);
      if (remainingChats.length > 0) {
        setCurrentChatId(remainingChats[0].id);
      }
    }
  };

  const updateChatMessages = (chatId: string, newMessages: Message[]) => {
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? {
              ...chat,
              messages: newMessages,
              updatedAt: new Date(),
              title:
                chat.title === "New Chat" && newMessages.length > 0
                  ? newMessages[0].text.substring(0, 30) +
                    (newMessages[0].text.length > 30 ? "..." : "")
                  : chat.title,
            }
          : chat
      )
    );
  };

  const handleSendMessage = async (customText?: string) => {
    const userId = localStorage.getItem("userId");
    if (!userId) {
      console.error("User ID is null. Redirecting to login.");
      navigate("/login");
      return;
    }

    const textToSend = customText || inputValue;
    if (!textToSend.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: textToSend,
      isUser: true,
      timestamp: new Date(),
    };

    const chatResponse = await chatAPI.sendMessage(
      currentChatId,
      userId,
      textToSend
    );

    const newMessages = [...messages, userMessage];
    updateChatMessages(currentChatId, newMessages);
    setInputValue("");
    setIsLoading(true);
    console.log("Loading state set to true");

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: chatResponse.model_message,
        isUser: false,
        timestamp: new Date(),
      };
      const finalMessages = [...newMessages, aiMessage];
      updateChatMessages(currentChatId, finalMessages);
      setIsLoading(false);
      console.log("Loading state set to false");
    }, 2000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="app">
      <Header onLogout={onLogout} messages={messages} />

      <div className="main-content">
        <ChatSidebar
          chats={chats}
          currentChatId={currentChatId}
          onChatSelect={selectChat}
          onNewChat={createNewChat}
          onDeleteChat={deleteChat}
        />

        <main
          className={`chat-container ${
            hasMessages ? "chat-container-with-messages" : ""
          }`}
        >
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
    </div>
  );
}

export default MainPage;
