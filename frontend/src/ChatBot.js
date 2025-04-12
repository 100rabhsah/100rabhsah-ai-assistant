import React, { useState } from "react";
import axios from "axios";
import "./ChatBot.css"; // For basic styling

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!input.trim()) return;
  
    setMessages([...messages, { role: "user", content: input }]);
    setLoading(true);
    setInput("");
  
    try {
      const response = await axios.post("http://localhost:8000/chat", {
        query: input,
      });
  
      setMessages([
        ...messages,
        { role: "user", content: input },
        { role: "assistant", content: response.data.response },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages([
        ...messages,
        { role: "user", content: input },
        { role: "assistant", content: "Sorry, something went wrong." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`message ${msg.role === "user" ? "user" : "assistant"}`}
          >
            {msg.content}
          </div>
        ))}
        {loading && <div className="message assistant">Typing...</div>}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me something..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBot;
