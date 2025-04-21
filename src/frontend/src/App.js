import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleSearch = async () => {
    const res = await axios.get(`http://localhost:8001/ask?query=${query}`);
    setResponse(res.data.context.join("\n\n"));
  };

  return (
    <div>
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
      />
      <button onClick={handleSearch}>Buscar</button>
      <div>{response}</div>
    </div>
  );
}

export default App;