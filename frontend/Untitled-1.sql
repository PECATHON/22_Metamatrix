// db.js
const Database = require('better-sqlite3');
const path = require('path');
const dbPath = process.env.DB_PATH || path.join(__dirname, 'data', 'campus-food.db');

const db = new Database(dbPath);

// Ensure foreign keys on
db.pragma('foreign_keys = ON');

module.exports = {
  run: (sql, params=[]) => db.prepare(sql).run(...params),
  get: (sql, params=[]) => db.prepare(sql).get(...params),
  all: (sql, params=[]) => db.prepare(sql).all(...params),
  db,
  initIfNeeded() {
    // create tables if not exist
    db.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT CHECK(role IN ('student','vendor','admin')) DEFAULT 'student',
        full_name TEXT,
        phone TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS vendors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        vendor_name TEXT,
        contact TEXT,
        location TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
      );

      CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        name TEXT,
        description TEXT,
        category TEXT,
        price INTEGER,
        photo TEXT,
        has_offer INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE CASCADE
      );

      CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        vendor_id INTEGER,
        items_json TEXT,
        total INTEGER,
        status TEXT DEFAULT 'pending',
        delivery_address TEXT,
        contact_phone TEXT,
        payment_method TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES users(id),
        FOREIGN KEY (vendor_id) REFERENCES vendors(id)
      );

      CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        vendor_id INTEGER,
        item_id INTEGER,
        rating INTEGER,
        text TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES users(id)
      );
    `);
  }
};
