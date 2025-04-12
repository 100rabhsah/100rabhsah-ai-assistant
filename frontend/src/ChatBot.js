import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ChatBot.css";
import ThemeToggle from "./ThemeToggle";

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [introText, setIntroText] = useState("");
  const [introDone, setIntroDone] = useState(false);

  const welcomeMessage =
    "Hey there! 👋 I'm Sourabh's personal AI assistant. I’ve been trained on his thoughts, experiences, and journey. Feel free to ask anything about his professional work, personal growth, or the insights he’s shared along the way!";

  useEffect(() => {
    let index = 0;
    const typingInterval = setInterval(() => {
      setIntroText((prev) => prev + welcomeMessage[index]);
      index++;
      if (index === welcomeMessage.length) {
        clearInterval(typingInterval);
        setIntroDone(true);
        setMessages([
          {
            role: "assistant",
            content: welcomeMessage,
          },
        ]);
      }
    }, 25);

    return () => clearInterval(typingInterval);
  }, []);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setLoading(true);
    setInput("");

    try {
      const response = await axios.post("https://one00rabhsah-ai-assistant.onrender.com/chat", {
        query: input,
      });

      setMessages([
        ...newMessages,
        { role: "assistant", content: response.data.response },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages([
        ...newMessages,
        { role: "assistant", content: "Sorry, something went wrong." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    if (isDarkMode) {
      document.body.classList.add("light-mode");
      document.body.classList.remove("dark-mode");
    } else {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
    }
  };

  return (
    <div className={`chatbot-container ${isDarkMode ? "dark-mode" : "light-mode"}`}>
      <ThemeToggle toggleTheme={toggleTheme} isDarkMode={isDarkMode} />
      <div className="chatbot-header">
        <h1>Sourabh's AI Assistant</h1>
      </div>

      <div className="chat-box">
        {!introDone ? (
          <div className="message assistant">{introText}</div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`message ${msg.role === "user" ? "user" : "assistant"}`}
              >
                {msg.content}
              </div>
            ))}
            {loading && <div className="message assistant">Typing...</div>}
          </>
        )}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything about Sourabh..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBot;
