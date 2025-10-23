import React, { useState, useRef, useEffect } from "react";
import Header from "../components/Header";
import WelcomeScreen from "../components/WelcomeScreen";
import ChatInterface from "../components/ChatInterface";
import ChatSidebar from "../components/ChatSidebar";
import type { Message, Chat } from "../types";
import { chatAPI } from "../utils/api";
import { userAPI } from "../utils/api";
import { useNavigate } from "react-router-dom";

// Import avatar images
import tigerAvatar from "../assets/tiggy.png";
import { useAuth0 } from "@auth0/auth0-react";

interface MainPageProps {
  onLogout: () => void;
}

function MainPage({ onLogout }: MainPageProps) {
  const [chats, setChats] = useState<Chat[]>([]);
  const navigate = useNavigate();
  const [currentChat, setCurrentChat] = useState<Chat | null>(null);
  const [currentChatId, setCurrentChatId] = useState("default");
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const messages = currentChat?.messages || [];

  const { user } = useAuth0();

  // Auto-scroll to bottom whenever messages or loading state changes
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const getAvatar = () => tigerAvatar;

  const getUser = async () => {
    const userId = user?.email;
    console.log("User email:", userId);


    try {
      const response = await userAPI.getUser(userId || "");
      if (!response.ok) {
        const createUserResponse = await userAPI.createUser({
          email: userId || "",
          name: user?.name || "",
          grad_year: user?.grad_year || 0,
          concentration: user?.concentration || "",
          certificates: user?.certificates || [],
        });
        console.log("Created user:", createUserResponse);
      }
      console.log("User:", response);
    } catch (error) {
      console.error("Unable to get user:", error);
      navigate("/login");
      return "";
    }


    if (userId === "undefined" || userId === null) {
      navigate("/login");
      return "";
    }

    return userId;
  };

  const getChatTitle = (title: string, messages: Message[]) => {
    return title === "New Chat" && messages.length > 0
      ? messages[0].message.substring(0, 30) +
          (messages[0].message.length > 30 ? "..." : "")
      : title;
  };

  const listChats = async () => {
    const userId = getUser();

    try {
      const response = await chatAPI.listChats(userId);
      const chats = response.chats.map((chat): Chat => {
        console.log();
        const userMessages = chat.userMessages.map((m: Message) => ({
          message: m.message,
          isUser: true,
          timestamp: new Date(m.timestamp),
        }));

        const modelMessages = chat.modelMessages.map((m: Message) => ({
          message: m.message,
          isUser: false,
          timestamp: new Date(m.timestamp),
        }));

        const messages = [...userMessages, ...modelMessages].sort(
          (a, b) => a.timestamp.getTime() - b.timestamp.getTime()
        );
        return {
          _id: chat._id,
          title: getChatTitle("New Chat", messages),
          userMessages: chat.userMessages,
          modelMessages: chat.modelMessages,
          messages: messages,
          messageCount: messages.length,
          createdAt: new Date(chat.createdAt),
          updatedAt: new Date(chat.updatedAt),
        };
      });

      chats.reverse()
      setCurrentChatId(chats[0]._id);
      setCurrentChat(chats[0]);
      console.log("Chats[0]", chats[0])
      setChats(chats);
      setInputValue("");
    } catch (error) {
      console.error("Unable to list new chats:", error);
    }
  };

  // load all chats and create new chat if none exists.
  useEffect(() => {
    listChats();
  }, []);

  const createNewChat = async () => {
    const userId = getUser();

    try {
      const chat = await chatAPI.createChat(userId);

      const newChat: Chat = {
        _id: chat._id,
        title: "New Chat",
        userMessages: [],
        modelMessages: [],
        messages: [],
        messageCount: 0,
        createdAt: new Date(chat.createdAt),
        updatedAt: new Date(chat.updatedAt),
      };

      setChats((prev) => [...prev, newChat]);
      setCurrentChatId(newChat._id);
      setCurrentChat(newChat);
      setInputValue("");
    } catch (error) {
      console.error("Unable to create new chat:", error);
    }
  };

  const selectChat = async (chatId: string) => {
    setCurrentChatId(chatId);
    setInputValue("");
    const userId = getUser();
    if (!userId) return;

    const fetchedChat = chats.find((chat) => chat._id === chatId);

    if (!fetchedChat) return;

    const userMessages: Message[] = (fetchedChat.userMessages || []).map(
      (message: Message) => {
        const userMessage: Message = {
          message: message.message,
          isUser: true,
          timestamp: new Date(message.timestamp),
        };
        return userMessage;
      }
    );

    const modelMessages: Message[] = (fetchedChat.modelMessages || []).map(
      (message: Message) => {
        const modelMessage: Message = {
          message: message.message,
          isUser: false,
          timestamp: new Date(message.timestamp),
        };
        return modelMessage;
      }
    );

    const messages = [...userMessages, ...modelMessages].sort(
      (a, b) => a.timestamp.getTime() - b.timestamp.getTime()
    );

    const tempChatForTitle = {
      ...(fetchedChat || {}),
      title: fetchedChat.title ?? "New Chat",
      messages,
    } as Chat;

    const currentChat: Chat = {
      _id: fetchedChat._id,
      title: getChatTitle(tempChatForTitle.title, tempChatForTitle.messages),
      userMessages,
      modelMessages,
      messages,
      messageCount: messages.length,
      createdAt: new Date(fetchedChat.createdAt),
      updatedAt: new Date(fetchedChat.updatedAt),
    };

    setCurrentChat(currentChat);

    setChats((prev) =>
      prev.map((c) => {
        if (c._id === chatId) {
          return currentChat;
        }
        return c;
      })
    );
  };

  const deleteChat = async (chatId: string) => {
    if (chats.length <= 1) return;

    const userId = getUser();

    try {
      await chatAPI.deleteChat(userId, chatId);
    } catch (error) {
      console.error("Unable to delete chat. Ex:", chatId, error);
    }

    setChats((prev) => prev.filter((chat) => chat._id !== chatId));

    // If we're deleting the current chat, switch to new chat
    if (chatId === currentChatId) {
      const remainingChats = chats.filter((chat) => chat._id !== chatId);
      if (remainingChats.length > 0) {
        setCurrentChatId(remainingChats[0]._id);
      }
    }
  };

  const updateChatMessages = (chatId: string, newMessages: Message[]) => {
    setCurrentChat((prev) => {
      if (!prev) return prev;
      const newTitle =
        prev.title === "New Chat" && newMessages.length > 0
          ? newMessages[0].message.substring(0, 30) +
            (newMessages[0].message.length > 30 ? "..." : "")
          : prev.title;
      return {
        ...prev,
        messages: newMessages,
        messageCount: newMessages.length,
        updatedAt: new Date(),
        title: newTitle,
      };
    });

    setChats((prev) =>
      prev.map((chat) =>
        chat._id === chatId
          ? {
              ...chat,
              messages: newMessages,
              messageCount: newMessages.length,
              updatedAt: new Date(),
              title:
                chat.title === "New Chat" && newMessages.length > 0
                  ? newMessages[0].message.substring(0, 30) +
                    (newMessages[0].message.length > 30 ? "..." : "")
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
      message: textToSend,
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

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        message: chatResponse.model_message,
        isUser: false,
        timestamp: new Date(),
      };
      const finalMessages = [...newMessages, aiMessage];
      updateChatMessages(currentChatId, finalMessages);
      setIsLoading(false);
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
            !(currentChat && currentChat.messages.length > 0) ? "chat-container-with-messages" : ""
          }`}
        >
          {(currentChat && currentChat.messages.length === 0) ? (
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
