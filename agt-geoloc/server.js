const express = require('express');
const http = require('http');
const cors = require('cors');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const PORT = process.env.PORT || 7009;

app.use(cors());
app.use(express.json());

// Base de données en mémoire (RAM)
const positionsDB = new Map();

const router = express.Router();

// 1. Health Check
router.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'geoloc-simulator', version: '1.0.0' });
});

// 2. Mettre à jour une position (REST)
router.post('/positions', (req, res) => {
  const { entity_id, latitude, longitude } = req.body;
  if (!entity_id) return res.status(400).json({ detail: 'entity_id requis' });
  
  const pos = { 
    entity_id, 
    latitude, 
    longitude, 
    recorded_at: new Date().toISOString() 
  };
  positionsDB.set(entity_id, pos);
  
  // Diffuser via WebSocket
  io.emit('position:updated', pos);
  
  res.status(200).json({ entity_id, status: 'updated' });
});

// 3. Recherche de proximité (Mock)
router.get('/proximity', (req, res) => {
  const lat = parseFloat(req.query.latitude) || 3.8480;
  const lng = parseFloat(req.query.longitude) || 11.5021;
  
  // Génère de fausses données autour du point demandé
  const results =[
    { entity_id: 'mock-driver-1', latitude: lat + 0.001, longitude: lng + 0.001, distance_meters: 150 },
    { entity_id: 'mock-driver-2', latitude: lat - 0.002, longitude: lng - 0.001, distance_meters: 320 }
  ];
  
  res.json({ results, total: 2 });
});

// 4. Purge RGPD (Contrat S2S avec Users)
router.delete('/by-user/:userId', (req, res) => {
  positionsDB.delete(req.params.userId);
  res.json({ message: 'Données purgées', user_id: req.params.userId });
});

// Nginx route vers /api/v1/geoloc/
app.use('/api/v1/geoloc', router);
// Alias au cas où certains services utilisent /api/v1/geo/ (selon le CDC)
app.use('/api/v1/geo', router);

// --- WEBSOCKET (Socket.io) ---
const io = new Server(server, {
  cors: { origin: '*' },
  path: '/geoloc/socket.io/' // Correspond à la config Nginx
});

io.on('connection', (socket) => {
  console.log(`[WS] Client Geo connecté: ${socket.id}`);
  
  socket.on('position:update', (data) => {
    if(data.entity_id) {
      positionsDB.set(data.entity_id, data);
      socket.broadcast.emit('position:updated', data);
    }
  });

  socket.on('disconnect', () => {
    console.log(`[WS] Client Geo déconnecté: ${socket.id}`);
  });
});

server.listen(PORT, () => {
  console.log(`[Geoloc Simulator] Démarré sur le port ${PORT} (REST + WS)`);
});