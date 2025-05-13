import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Este archivo es opcional si tienes estilos
import App from './App'; // Asegúrate de que App.js esté en la misma carpeta
import reportWebVitals from './reportWebVitals'; // Esto es opcional para medir el rendimiento

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // Este es el div donde React montará la app
);

// Si quieres medir el rendimiento de la app, puedes pasar una función a reportWebVitals
reportWebVitals();
