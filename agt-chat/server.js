const express = require('express');
const http = require('http');
const cors = require('cors');
const { Server } = require('socket.io');
const crypto = require('crypto');

const app = express();
const server = http.createServer(app);
const PORT = process.env.PORT || 7008;

app.use(cors());
app.use(express.json());

// Base de données en mémoire (RAM)
const conversationsDB = new Map();
const messagesDB = new Map();

// --- API REST ---
const router = express.Router();

// 1. Health Check
router.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'chat-simulator', version: '1.0.0' });
});

// 2. Transfert Bot -> Humain (Contrat S2S avec Chatbot)
router.post('/conversations/transfer', (req, res) => {
  const { user_id, platform_id, bot_history } = req.body;
  const transferId = crypto.randomUUID();
  const convId = crypto.randomUUID();

  conversationsDB.set(convId, {
    id: convId,
    type: 'transfert',
    status: 'en_attente',
    user_id,
    platform_id,
    created_at: new Date().toISOString()
  });

  // On sauvegarde l'historique du bot comme premiers messages
  messagesDB.set(convId, bot_history ||[]);

  res.status(201).json({
    transfer_id: transferId,
    conversation_id: convId,
    status: 'en_attente',
    message: 'Transfert pris en charge par le simulateur'
  });
});

// 3. Lister les conversations
router.get('/conversations', (req, res) => {
  res.json({ data: Array.from(conversationsDB.values()) });
});

// 4. Ajouter un message (Fallback REST)
router.post('/conversations/:id/messages', (req, res) => {
  const convId = req.params.id;
  if (!conversationsDB.has(convId)) return res.status(404).json({ detail: 'Conversation introuvable' });

  const msg = {
    id: crypto.randomUUID(),
    sender_id: req.body.sender_id || 'anonymous',
    content: req.body.content,
    created_at: new Date().toISOString()
  };

  if (!messagesDB.has(convId)) messagesDB.set(convId,[]);
  messagesDB.get(convId).push(msg);

  // Diffuser via WebSocket si possible
  io.to(convId).emit('message:new', msg);

  res.status(201).json(msg);
});

// 5. Lire l'historique
router.get('/conversations/:id/messages', (req, res) => {
  const msgs = messagesDB.get(req.params.id) ||[];
  res.json({ data: msgs });
});

app.use('/api/v1/chat', router);

// --- WEBSOCKET (Socket.io) ---
const io = new Server(server, {
  cors: { origin: '*' },
  path: '/socket.io/'
});

io.on('connection', (socket) => {
  console.log(`[WS] Client connecté: ${socket.id}`);

  // Rejoindre une conversation (room)
  socket.on('join_conversation', (convId) => {
    socket.join(convId);
    console.log(`[WS] Client ${socket.id} a rejoint la conv ${convId}`);
  });

  // Echo: quand on reçoit un message, on le renvoie à la room
  socket.on('message:send', (data) => {
    const { conversation_id, content, sender_id } = data;
    const msg = {
      id: crypto.randomUUID(),
      conversation_id,
      sender_id,
      content,
      created_at: new Date().toISOString()
    };
    
    // Sauvegarde en RAM
    if (!messagesDB.has(conversation_id)) messagesDB.set(conversation_id,[]);
    messagesDB.get(conversation_id).push(msg);

    // Diffusion
    io.to(conversation_id).emit('message:new', msg);
  });

  socket.on('disconnect', () => {
    console.log(`[WS] Client déconnecté: ${socket.id}`);
  });
});

server.listen(PORT, () => {
  console.log(`[Chat Simulator] Démarré sur le port ${PORT} (REST + WS)`);
});