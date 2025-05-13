const express = require('express');
const cors = require('cors');
const ragService = require('./services/ragService');

const app = express();
const PORT = 8001;

app.use(cors());
app.use(express.json());

app.post('/api/ask', async (req, res) => {
  const question = req.body.question;
  if (!question) return res.status(400).json({ error: 'Pregunta vacía' });

  const answer = await ragService.answerQuestion(question);
  res.json({ answer });
});

app.listen(PORT, () => {
  console.log(`Backend escuchando en http://localhost:${PORT}`);
});
