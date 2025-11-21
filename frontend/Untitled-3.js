// routes/auth.js
const express = require('express');
const { body, validationResult } = require('express-validator');

module.exports = ({ DB, jwt, bcrypt, JWT_SECRET }) => {
  const router = express.Router();

  // register
  router.post('/register',
    body('username').isLength({min:3}),
    body('password').isLength({min:6}),
    body('role').optional().isIn(['student','vendor','admin']),
    async (req,res)=>{
      const err = validationResult(req);
      if (!err.isEmpty()) return res.status(400).json({ errors: err.array() });

      const { username, password, role='student', full_name, phone } = req.body;
      const existing = DB.get('SELECT id FROM users WHERE username = ?', [username]);
      if (existing) return res.status(409).json({ error: 'Username already taken' });

      const hashed = bcrypt.hashSync(password, 10);
      const info = DB.run('INSERT INTO users (username,password,role,full_name,phone) VALUES (?,?,?,?,?)',
        [username, hashed, role, full_name||'', phone||'']);
      const userId = info.lastInsertRowid;
      const token = jwt.sign({ id: userId, username, role }, JWT_SECRET, { expiresIn: '7d' });
      res.json({ token, user: { id: userId, username, role, full_name, phone } });
    });

  // login
  router.post('/login',
    body('username').exists(), body('password').exists(),
    (req,res)=>{
      const { username, password } = req.body;
      const user = DB.get('SELECT * FROM users WHERE username = ?', [username]);
      if (!user) return res.status(401).json({ error: 'Invalid credentials' });
      const ok = bcrypt.compareSync(password, user.password);
      if (!ok) return res.status(401).json({ error: 'Invalid credentials' });
      const token = jwt.sign({ id: user.id, username: user.username, role: user.role }, JWT_SECRET, { expiresIn: '7d' });
      res.json({ token, user: { id: user.id, username: user.username, role: user.role, full_name: user.full_name } });
    });

  // simple middleware to get user from token
  router.get('/me', (req,res)=>{
    const auth = req.headers.authorization || '';
    const token = auth.replace(/^Bearer\s+/i,'');
    if (!token) return res.status(401).json({ error: 'Missing token' });
    try {
      const payload = jwt.verify(token, JWT_SECRET);
      const user = DB.get('SELECT id,username,role,full_name,phone FROM users WHERE id=?', [payload.id]);
      return res.json({ user });
    } catch (e) {
      return res.status(401).json({ error: 'Invalid token' });
    }
  });

  return router;
};
