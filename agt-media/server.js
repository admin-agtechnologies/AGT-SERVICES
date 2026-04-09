const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 7003;

app.use(cors());
app.use(express.json());

// Configuration Multer pour stocker les fichiers localement
const uploadDir = path.join(__dirname, 'uploads');
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const uniqueId = crypto.randomUUID();
    cb(null, uniqueId + path.extname(file.originalname));
  }
});
const upload = multer({ storage });

// Base de données en mémoire (RAM)
const mediaDB = new Map();

const router = express.Router();

// 1. Health Check
router.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'media-simulator', version: '1.0.0' });
});

// 2. Upload d'un fichier
router.post('/', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ detail: 'Fichier requis (champ "file")' });
  
  const mediaId = req.file.filename.split('.')[0]; // L'UUID généré
  const mediaInfo = {
    id: mediaId,
    original_name: req.file.originalname,
    mime_type: req.file.mimetype,
    size_bytes: req.file.size,
    url: `/api/v1/media/${req.file.filename}`,
    created_at: new Date().toISOString()
  };
  
  mediaDB.set(mediaId, mediaInfo);
  res.status(201).json(mediaInfo);
});

// 3. Récupérer les métadonnées d'un fichier
router.get('/:id/info', (req, res) => {
  const mediaInfo = mediaDB.get(req.params.id);
  if (!mediaInfo) return res.status(404).json({ detail: 'Média introuvable' });
  res.json(mediaInfo);
});

// 4. Télécharger/Voir le fichier brut
router.get('/:filename', (req, res) => {
  const filePath = path.join(uploadDir, req.params.filename);
  if (!fs.existsSync(filePath)) return res.status(404).json({ detail: 'Fichier introuvable sur le disque' });
  res.sendFile(filePath);
});

// 5. Purge RGPD (Appelé par le Service Users en S2S)
router.delete('/by-user/:userId', (req, res) => {
  // Simulation de la suppression
  res.json({ message: 'Fichiers purgés pour cet utilisateur', user_id: req.params.userId, files_deleted: 0 });
});

// Montage du routeur sur le préfixe attendu par Nginx
app.use('/api/v1/media', router);

app.listen(PORT, () => {
  console.log(`[Media Simulator] Démarré sur le port ${PORT}`);
});