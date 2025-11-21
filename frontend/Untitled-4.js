// routes/api.js
const express = require('express');

module.exports = ({ DB, jwt, JWT_SECRET }) => {
  const router = express.Router();

  // helper auth middleware
  function authMiddleware(req, res, next) {
    const auth = (req.headers.authorization || '').replace(/^Bearer\s+/i,'');
    if (!auth) return res.status(401).json({ error: 'No token' });
    try {
      req.user = jwt.verify(auth, JWT_SECRET);
      next();
    } catch (e) { return res.status(401).json({ error: 'Invalid token' }); }
  }

  // --- PUBLIC: list menu items / search
  router.get('/menu', (req,res)=>{
    const q = (req.query.q || '').trim();
    if (q) {
      const items = DB.all("SELECT * FROM menu_items WHERE name LIKE ? OR description LIKE ? LIMIT 200", [`%${q}%`,`%${q}%`]);
      return res.json({ items });
    }
    const items = DB.all("SELECT * FROM menu_items ORDER BY created_at DESC LIMIT 500");
    res.json({ items });
  });

  // get item by id
  router.get('/menu/:id', (req,res)=>{
    const item = DB.get("SELECT * FROM menu_items WHERE id = ?", [req.params.id]);
    if (!item) return res.status(404).json({ error: 'Not found' });
    res.json({ item });
  });

  // --- VENDOR: add/edit menu (auth + vendor role)
  router.post('/vendor/menu', authMiddleware, (req,res)=>{
    if (req.user.role !== 'vendor') return res.status(403).json({ error: 'Vendor-only' });
    const { name, description, category, price, photo, has_offer } = req.body;
    // ensure vendor record exists
    let vendor = DB.get('SELECT * FROM vendors WHERE user_id=?', [req.user.id]);
    if (!vendor) {
      const info = DB.run('INSERT INTO vendors (user_id, vendor_name) VALUES (?,?)', [req.user.id, `Vendor ${req.user.username}`]);
      vendor = DB.get('SELECT * FROM vendors WHERE id=?', [info.lastInsertRowid]);
    }
    const info = DB.run('INSERT INTO menu_items (vendor_id,name,description,category,price,photo,has_offer) VALUES (?,?,?,?,?,?,?)',
      [vendor.id, name, description||'', category||'Meals', price||0, photo||'', has_offer?1:0]);
    res.json({ ok: true, id: info.lastInsertRowid });
  });

  // vendor list own items
  router.get('/vendor/menu', authMiddleware, (req,res)=>{
    if (req.user.role !== 'vendor') return res.status(403).json({ error: 'Vendor-only' });
    const vendor = DB.get('SELECT * FROM vendors WHERE user_id=?', [req.user.id]);
    if (!vendor) return res.json({ items: [] });
    const items = DB.all('SELECT * FROM menu_items WHERE vendor_id=?', [vendor.id]);
    res.json({ items });
  });

  // --- ORDERS (create by student)
  router.post('/orders', authMiddleware, (req,res)=>{
    if (req.user.role !== 'student') return res.status(403).json({ error: 'Student-only' });
    const { vendor_id, items, total, delivery_address, contact_phone, payment_method } = req.body;
    const info = DB.run('INSERT INTO orders (student_id,vendor_id,items_json,total,delivery_address,contact_phone,payment_method) VALUES (?,?,?,?,?,?,?)',
      [req.user.id, vendor_id||null, JSON.stringify(items||[]), total||0, delivery_address||'', contact_phone||'', payment_method||'']);
    // In a real system here you'd push a notification to vendor (websocket/push)
    res.json({ ok:true, order_id: info.lastInsertRowid });
  });

  // student order list
  router.get('/orders/mine', authMiddleware, (req,res)=>{
    const rows = DB.all('SELECT * FROM orders WHERE student_id=? ORDER BY created_at DESC', [req.user.id]);
    res.json({ orders: rows });
  });

  // vendor inbound orders
  router.get('/orders/vendor', authMiddleware, (req,res)=>{
    if (req.user.role !== 'vendor') return res.status(403).json({ error: 'Vendor-only' });
    const vendor = DB.get('SELECT * FROM vendors WHERE user_id=?', [req.user.id]);
    if (!vendor) return res.json({ orders: [] });
    const rows = DB.all('SELECT * FROM orders WHERE vendor_id=? ORDER BY created_at DESC', [vendor.id]);
    res.json({ orders: rows });
  });

  // vendor mark order complete
  router.post('/orders/:id/complete', authMiddleware, (req,res)=>{
    if (req.user.role !== 'vendor') return res.status(403).json({ error: 'Vendor-only' });
    const order = DB.get('SELECT * FROM orders WHERE id=?', [req.params.id]);
    if (!order) return res.status(404).json({ error: 'Order not found' });
    const vendor = DB.get('SELECT * FROM vendors WHERE user_id=?', [req.user.id]);
    if (!vendor || vendor.id !== order.vendor_id) return res.status(403).json({ error: 'Not your order' });
    DB.run('UPDATE orders SET status = ? WHERE id = ?', ['completed', order.id]);
    res.json({ ok: true });
  });

  // --- REVIEWS
  router.post('/reviews', authMiddleware, (req,res)=>{
    const { vendor_id, item_id, rating, text } = req.body;
    DB.run('INSERT INTO reviews (student_id,vendor_id,item_id,rating,text) VALUES (?,?,?,?,?)',
      [req.user.id, vendor_id||null, item_id||null, rating||5, text||'']);
    res.json({ ok:true });
  });

  router.get('/reviews/vendor/:vendorId', (req,res)=>{
    const rows = DB.all('SELECT * FROM reviews WHERE vendor_id=? ORDER BY created_at DESC', [req.params.vendorId]);
    res.json({ reviews: rows });
  });

  return router;
};
