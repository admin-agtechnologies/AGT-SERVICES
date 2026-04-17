-- Script d'initialisation PostGIS pour le service Geolocation AGT
-- Exécuté automatiquement par Docker lors du premier démarrage du conteneur PostgreSQL

-- Activation de l'extension PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Vérification
SELECT PostGIS_Version();
