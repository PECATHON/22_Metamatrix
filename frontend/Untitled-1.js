// server.js
const path = require('path');
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const multer = require('multer');
const { body, validationResult } = require('express-validator');

const DB = require('./db'); // simple wrapper around better-sqlite3
const auth = require('./routes/auth');
const api = require('./routes/api');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'replace_with_strong_secret';

// basic middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static: serve your uploaded front pages directly by referencing their paths.
// Copy the three files into the 'public' folder or symlink them to /mnt/data.
// We'll create express routes to send those exact files from your provided paths:
const landingPath = process.env.LANDING_PATH || '/mnt/data/Landing.html';
const studentPath = process.env.STUDENT_PATH || '/mnt/data/Student.html';
const vendorPath = process.env.VENDOR_PATH || '/mnt/data/Vendor.html';

app.get('/', (req, res) => res.sendFile(landingPath));
app.get('/landing', (req, res) => res.sendFile(landingPath));
app.get('/student', (req, res) => res.sendFile(studentPath));
app.get('/vendor', (req, res) => res.sendFile(vendorPath));

// static assets folder (if you add CSS / js / images)
app.use('/assets', express.static(path.join(__dirname, 'public', 'assets')));

// mount modular routes
app.use('/auth', auth({ DB, jwt, bcrypt, JWT_SECRET }));
app.use('/api', api({ DB, jwt, JWT_SECRET }));

// health
app.get('/health', (req, res) => res.json({ ok: true, ts: Date.now() }));

// fallback 404
app.use((req,res)=>res.status(404).json({ error: 'Not found' }));

app.listen(PORT, ()=>console.log(`Server listening on port ${PORT}`));
