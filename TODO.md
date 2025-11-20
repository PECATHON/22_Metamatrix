# Campus Food Ordering and Review System - TODO (Web App Only)

## Task Division Among 4 People

The project is divided into 4 main tasks, assigned to 4 team members for parallel development where possible, with sequential dependencies.

- **Person 1: Backend Development (Task 1)** - Handles server-side logic, data models, and APIs. Focus on building the core backend infrastructure.
- **Person 2: Frontend Integration (Task 2)** - Builds the client-side UI and connects to the backend. Depends on Task 1 completion.
- **Person 3: Bonus Features (Task 3)** - Adds advanced, optional features after core functionality. Can start after Tasks 1-2 are mostly done.
- **Person 4: Testing and Deployment (Task 4)** - Ensures quality and deploys the app. Starts after Tasks 1-3 are complete.

### How Tasks Link Later
Tasks link sequentially: Person 1 provides APIs for Person 2 to consume. Person 2 integrates with Person 1's work via HTTP/WebSocket calls. Person 3 extends Person 1-2's setup. Person 4 verifies and deploys the integrated system from all.

- **Integration Steps**:
  1. Person 1 completes backend, tests APIs.
  2. Person 2 replaces demo data with API calls.
  3. Person 3 adds endpoints/UI to existing setup.
  4. Person 4 tests full flow and deploys.
- **Potential Issues**: Update interfaces if changes occur. Use Git for version control and pull requests for merges.

This ensures modularity and prevents silos.

## Task 1: Backend Development
- [ ] Set up MongoDB models (User, Vendor, MenuItem, Order, Review)
  - Install mongoose if not already.
  - Create models/ directory.
  - Define User model: fields like name, email, password (hashed), role (enum: 'student', 'vendor', 'admin').
  - Define Vendor model: extends User or separate, with additional fields like vendorName, description, location.
  - Define MenuItem model: name, description, price, category, vendor (ref to Vendor), image (optional), availability.
  - Define Order model: student (ref to User), items (array of {menuItem ref, quantity}), total, status (enum: 'received', 'preparing', 'ready', 'delivered'), createdAt, updatedAt.
  - Define Review model: student (ref to User), menuItem (ref to MenuItem), rating (1-5), comment, createdAt.
- [ ] Implement authentication (JWT, roles: Student, Vendor, Admin)
  - Install jsonwebtoken and bcryptjs.
  - Create middleware/auth.js for JWT verification and role checking.
  - Create routes/auth.js: POST /register (hash password, save user), POST /login (verify password, return JWT).
  - Add role-based middleware: e.g., requireStudent, requireVendor.
- [ ] Create API routes for vendors (CRUD menu items)
  - Create routes/menu.js.
  - GET /menu: Get all menu items (public or authenticated).
  - POST /menu: Create new menu item (requireVendor, validate fields).
  - PUT /menu/:id: Update menu item (requireVendor, check ownership).
  - DELETE /menu/:id: Delete menu item (requireVendor, check ownership).
  - Use multer for image uploads if needed.
- [ ] Create API routes for students (browse menu, place orders, reviews)
  - In routes/menu.js: Add GET /menu with query params for search (name, category) and filter (vendor).
  - Create routes/orders.js: POST /orders: Place order (requireStudent, validate cart, create order).
  - GET /orders: Get user's orders (requireStudent).
  - PUT /orders/:id/status: Update status (requireVendor, for their items).
  - Create routes/reviews.js: POST /reviews: Submit review (requireStudent, after order).
  - GET /reviews/:menuItemId: Get reviews for item.
- [ ] Implement order tracking (statuses: Received, Preparing, Ready)
  - In Order model, add status field.
  - In routes/orders.js, add PUT /orders/:id/status for vendors to update.
  - Optionally, add WebSocket for real-time updates (install socket.io).
- [ ] Add search and filter endpoints
  - Enhance GET /menu with query params: ?search=term&category=cat&vendor=id&minPrice=&maxPrice=.
  - Use MongoDB aggregation or regex for search.

## Task 2: Frontend Integration
- [ ] Convert Student.html to React components
  - Create components/ directory in client/src.
  - Extract sections: BrowseMenu, Cart, Orders, Reviews, ReviewModal.
  - Use state for cart, orders, reviews (initially local, later from API).
  - Replace vanilla JS with React hooks (useState, useEffect).
  - Style with Tailwind CSS (install if needed).
- [ ] Build Vendor dashboard in React
  - Create VendorDashboard component: Manage menu items (add, edit, delete), view orders, update statuses.
  - Use forms for CRUD operations.
  - Connect to vendor-specific APIs.
- [ ] Implement authentication UI
  - Create Login/Register components.
  - Use JWT from localStorage.
  - Add protected routes (e.g., with react-router-dom).
  - Redirect based on role.
- [ ] Connect frontend to backend APIs
  - Install axios for HTTP requests.
  - Create api/ directory with functions for each endpoint.
  - Replace demo data with API calls.
  - Handle loading states and errors.
- [ ] Add real-time order updates (WebSockets or polling)
  - Install socket.io-client.
  - Connect to server WebSocket.
  - Listen for order status changes, update UI.
  - Alternative: Poll GET /orders periodically.

## Phase 3: Bonus Features
- [ ] Personalized recommendations
  - Based on past orders/reviews, suggest menu items.
  - Add endpoint GET /recommendations/:userId.
  - Display in BrowseMenu.
- [ ] Real-time notifications
  - Use WebSockets for order updates, new reviews, etc.
  - Show toast notifications (e.g., with react-toastify).
- [ ] Chatbot assistant
  - Integrate a simple chatbot (e.g., Dialogflow or custom).
  - Add chat UI, handle queries like "recommend pizza".

## Task 4: Testing and Deployment
- [ ] Unit and integration tests
  - For backend: Use Jest/Supertest for API tests.
  - For frontend: Use React Testing Library for components.
  - Test auth, CRUD, order flow.
- [ ] Deploy web app (Vercel/Netlify)
  - Build client: npm run build.
  - Deploy to Vercel/Netlify.
  - Set up environment variables for MongoDB, JWT secret.
  - Ensure CORS for frontend-backend.
