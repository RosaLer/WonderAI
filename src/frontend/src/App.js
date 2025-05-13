import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleAsk = async () => {
    try {
      const response = await axios.post("http://localhost:8001/ask", { query });
      setResults(response.data.results.documents || []);
    } catch (error) {
      console.error("Error al consultar el backend:", error);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>WonderAI</h2>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleAsk}>Preguntar</button>
      <ul>
        {results.map((doc, idx) => (
          <li key={idx}>{doc}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;