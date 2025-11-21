// scripts/init_db.js
const fs = require('fs');
const path = require('path');
const DB = require('../db');

const dataDir = path.join(__dirname, '..', 'data');
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

DB.initIfNeeded();
console.log('DB initialized at', process.env.DB_PATH || path.join(__dirname, '..', 'data', 'campus-food.db'));
