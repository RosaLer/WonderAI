import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([
    {
      text: "¡Hola! Soy tu asistente de viajes WonderAI. ¿Sobre qué ciudad quieres información?",
      sender: "bot"
    }
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setMessages(prev => [...prev, { text: query, sender: "user" }]);
    setQuery("");

    try {
      const response = await axios.post("http://localhost:8001/ask", { query });
      setMessages(prev => [...prev, { 
        text: response.data.response || "No tengo información sobre ese tema.", 
        sender: "bot" 
      }]);
    } catch (err) {
      console.error("Error al consultar el backend:", err);
      setMessages(prev => [...prev, { 
        text: "Lo siento, hubo un error al procesar tu pregunta.", 
        sender: "bot" 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>WonderAI</h2>
        <p>Asistente de viajes inteligente</p>
      </div>

      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleAsk} className="chat-input">
        <input
          type="text"
          placeholder="Escribe tu pregunta sobre viajes..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" disabled={!query.trim() || loading}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </form>
    </div>
  );
}

export default App;