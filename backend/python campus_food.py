import webbrowser
from threading import Timer
from flask import Flask, Response

# Initialize the Flask Application
app = Flask(__name__)

# This function opens the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

# --- THE EXACT HTML CONTENT ---
# We use a raw string (r""") to ensure Python doesn't mess up the HTML/JS formatting
HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Food Hub - Final</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <style>
        body { font-family: 'system-ui', sans-serif; }
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background-color: rgba(139, 92, 246, 0.3); border-radius: 20px; }
        .fade-in { animation: fadeIn 0.3s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        /* Modal Animation */
        .modal-enter { animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        @keyframes popIn { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
    </style>
</head>
<body class="bg-purple-50 text-purple-900 h-screen overflow-hidden">
    <div id="root" class="h-full"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        // --- ICONS (SVG Components) ---
        const Icon = ({ path, className }) => (
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
                {path}
            </svg>
        );
        const Icons = {
            Database: (props) => <Icon {...props} path={<><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></>} />,
            Server: (props) => <Icon {...props} path={<><rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/></>} />,
            ShoppingCart: (props) => <Icon {...props} path={<><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></>} />,
            Plus: (props) => <Icon {...props} path={<><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></>} />,
            Trash: (props) => <Icon {...props} path={<><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></>} />,
            Check: (props) => <Icon {...props} path={<><polyline points="20 6 9 17 4 12"/></>} />,
            MapPin: (props) => <Icon {...props} path={<><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></>} />
        };

        // --- MOCK BACKEND / DATABASE ---
        const initialDb = {
            users: [
                { id: 'u1', username: 'student', password: '123', role: 'student', name: 'Alex Student' },
                { id: 'u2', username: 'vendor', password: '123', role: 'vendor', name: 'Campus Bites' },
                { id: 'u3', username: 'admin', password: '123', role: 'admin', name: 'System Admin' }
            ],
            menuItems: [
                { id: 'm1', vendorId: 'u2', name: 'Veg Cheese Burger', price: 80, category: 'Meals', description: 'Loaded with cheese and fresh veggies' },
                { id: 'm2', vendorId: 'u2', name: 'Cold Coffee', price: 60, category: 'Beverages', description: 'Creamy, strong, and refreshing' },
                { id: 'm3', vendorId: 'u2', name: 'Spicy Paneer Wrap', price: 100, category: 'Snacks', description: 'Grilled paneer cubes with spicy mint chutney' },
                { id: 'm4', vendorId: 'u2', name: 'Chicken Biryani', price: 150, category: 'Meals', description: 'Aromatic basmati rice with tender chicken' },
                { id: 'm5', vendorId: 'u2', name: 'Masala Chai', price: 20, category: 'Beverages', description: 'Hot tea brewed with ginger and cardamom' },
                { id: 'm6', vendorId: 'u2', name: 'Peri-Peri Fries', price: 70, category: 'Snacks', description: 'Crispy fries tossed in spicy seasoning' },
                { id: 'm7', vendorId: 'u2', name: 'Choco Lava Cake', price: 90, category: 'Desserts', description: 'Warm chocolate cake with a molten core' },
                { id: 'm8', vendorId: 'u2', name: 'Red Pasta', price: 110, category: 'Meals', description: 'Penne pasta in tangy tomato garlic sauce' }
            ],
            orders: []
        };

        // --- COMPONENT: LANDING / AUTH ---
        const LandingPage = ({ onLogin, onSignup }) => {
            const [view, setView] = useState('login');
            const [role, setRole] = useState('student');
            const [formData, setFormData] = useState({ username: '', password: '', email: '', fullname: '' });
            const [msg, setMsg] = useState('');

            const handleSubmit = (e) => {
                e.preventDefault();
                setMsg('Processing...');
                setTimeout(() => {
                    if (view === 'login') {
                        const success = onLogin(formData.username, formData.password, role);
                        if (!success) setMsg('Invalid credentials or role.');
                    } else {
                        onSignup({ ...formData, role });
                        setMsg('Account created! Logging in...');
                        setTimeout(() => onLogin(formData.username, formData.password, role), 800);
                    }
                }, 600);
            };

            return (
                <div className="h-full w-full bg-gradient-to-br from-purple-600 via-purple-500 to-pink-400 flex items-center justify-center p-4 relative overflow-hidden">
                    <div className="absolute inset-0 opacity-10 pointer-events-none">
                        <svg width="100%" height="100%"><pattern id="p" width="50" height="50" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="2" fill="white"/></pattern><rect width="100%" height="100%" fill="url(#p)"/></svg>
                    </div>
                    <div className="w-full max-w-md bg-white/95 backdrop-blur-md rounded-3xl shadow-2xl border border-purple-200 px-8 py-10 text-purple-900 z-10 fade-in">
                        <header className="mb-8 text-center">
                            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 shadow-lg text-2xl">🍔</div>
                            <h1 className="text-2xl font-semibold tracking-tight">{view === 'login' ? 'Campus Food Hub' : 'Create Account'}</h1>
                            <p className="mt-1 text-sm text-purple-600">Order · Review · Enjoy</p>
                        </header>
                        <div className="mb-6 flex rounded-full bg-purple-100 p-1 text-xs font-medium">
                            {['student', 'vendor', 'admin'].map(r => (
                                <button key={r} onClick={() => setRole(r)} className={`flex-1 rounded-full py-2 capitalize transition-all ${role === r ? 'bg-purple-600 text-white shadow-sm' : 'text-purple-700'}`}>
                                    {r}
                                </button>
                            ))}
                        </div>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {view === 'signup' && (
                                <>
                                    <div><label className="block text-xs font-bold uppercase text-purple-700 mb-1">Full Name</label><input className="w-full rounded-2xl border border-purple-300 bg-purple-50 px-3 py-2 text-sm focus:ring-2 focus:ring-pink-300 outline-none" required value={formData.fullname} onChange={e => setFormData({...formData, fullname: e.target.value})} /></div>
                                    <div><label className="block text-xs font-bold uppercase text-purple-700 mb-1">Email</label><input type="email" className="w-full rounded-2xl border border-purple-300 bg-purple-50 px-3 py-2 text-sm focus:ring-2 focus:ring-pink-300 outline-none" required value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} /></div>
                                </>
                            )}
                            <div><label className="block text-xs font-bold uppercase text-purple-700 mb-1">Username</label><input className="w-full rounded-2xl border border-purple-300 bg-purple-50 px-3 py-2 text-sm focus:ring-2 focus:ring-pink-300 outline-none" required value={formData.username} onChange={e => setFormData({...formData, username: e.target.value})} /></div>
                            <div><label className="block text-xs font-bold uppercase text-purple-700 mb-1">Password</label><input type="password" className="w-full rounded-2xl border border-purple-300 bg-purple-50 px-3 py-2 text-sm focus:ring-2 focus:ring-pink-300 outline-none" required value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} /></div>
                            {msg && <div className="text-center text-xs font-medium text-pink-600 bg-pink-50 py-2 rounded-lg">{msg}</div>}
                            <button type="submit" className="w-full rounded-2xl bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-2.5 text-sm font-bold text-white shadow-lg hover:scale-[1.02] transition-transform">
                                {view === 'login' ? 'Login' : 'Sign Up'}
                            </button>
                        </form>
                        <div className="mt-6 border-t border-purple-200 pt-4 text-center">
                            <button onClick={() => { setView(view === 'login' ? 'signup' : 'login'); setMsg(''); }} className="text-xs font-semibold text-purple-700 hover:underline">
                                {view === 'login' ? "Don't have an account? Sign Up" : "Already have an account? Login"}
                            </button>
                        </div>
                         <div className="mt-4 text-[10px] text-gray-400 text-center">
                            Try: student/123, vendor/123, admin/123
                        </div>
                    </div>
                </div>
            );
        };

        // --- COMPONENT: VENDOR DASHBOARD ---
        const VendorDashboard = ({ user, db, updateDb, onLogout }) => {
            const [tab, setTab] = useState('menu');
            const [isAdding, setIsAdding] = useState(false);
            const [newItem, setNewItem] = useState({ name: '', price: '', category: '', description: '' });
            const myItems = db.menuItems.filter(i => i.vendorId === user.id);
            const myOrders = db.orders.filter(o => o.vendorId === user.id);

            const handleAddItem = (e) => {
                e.preventDefault();
                const item = { ...newItem, id: 'm' + Date.now(), vendorId: user.id };
                updateDb('menuItems', [...db.menuItems, item]);
                setIsAdding(false);
                setNewItem({ name: '', price: '', category: '', description: '' });
            };

            const handleDeleteItem = (id) => {
                updateDb('menuItems', db.menuItems.filter(i => i.id !== id));
            };

            const updateOrderStatus = (orderId, status) => {
                const updatedOrders = db.orders.map(o => o.id === orderId ? { ...o, status } : o);
                updateDb('orders', updatedOrders);
            };

            return (
                <div className="h-full flex flex-col bg-purple-50">
                    <header className="bg-white border-b border-purple-200 px-6 py-3 flex justify-between items-center shadow-sm">
                        <div className="flex items-center gap-2"><span className="text-2xl">🍔</span><h1 className="font-bold text-purple-900">Vendor Portal</h1></div>
                        <div className="flex items-center gap-4">
                            <span className="text-sm text-purple-600">Welcome, {user.name}</span>
                            <button onClick={onLogout} className="bg-pink-500 hover:bg-pink-600 text-white px-3 py-1 rounded-full text-xs font-bold transition-colors">Logout</button>
                        </div>
                    </header>
                    <main className="flex-1 p-4 flex gap-4 overflow-hidden">
                        <aside className="w-52 bg-white border border-purple-200 rounded-2xl p-3 flex flex-col gap-2 shadow-lg">
                            <div className="text-xs font-bold text-purple-400 uppercase tracking-wider px-2 mb-2">Dashboard</div>
                            <button onClick={() => setTab('menu')} className={`text-left px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 ${tab === 'menu' ? 'bg-purple-600 text-white' : 'text-purple-700 hover:bg-purple-50'}`}>🍕 Manage Menu</button>
                            <button onClick={() => setTab('orders')} className={`text-left px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 ${tab === 'orders' ? 'bg-purple-600 text-white' : 'text-purple-700 hover:bg-purple-50'}`}>
                                📦 Orders {myOrders.filter(o => o.status === 'Pending').length > 0 && <span className="bg-pink-500 text-white text-[10px] px-1.5 py-0.5 rounded-full ml-auto">{myOrders.filter(o => o.status === 'Pending').length}</span>}
                            </button>
                        </aside>
                        <section className="flex-1 bg-white border border-purple-200 rounded-2xl p-6 overflow-y-auto shadow-lg relative">
                            {tab === 'menu' && (
                                <div className="space-y-6 fade-in">
                                    <div className="flex justify-between items-center">
                                        <h2 className="text-xl font-bold text-purple-900">Menu Items</h2>
                                        <button onClick={() => setIsAdding(!isAdding)} className="bg-purple-500 text-white px-4 py-2 rounded-full text-sm font-bold flex items-center gap-2 shadow hover:bg-purple-600 transition">{isAdding ? 'Cancel' : '＋ Add New Item'}</button>
                                    </div>
                                    {isAdding && (
                                        <form onSubmit={handleAddItem} className="bg-purple-50 p-4 rounded-xl border border-purple-200 space-y-3 animate-pulse-once">
                                            <div className="grid grid-cols-2 gap-4">
                                                <input placeholder="Item Name" required className="p-2 rounded-lg border border-purple-200 text-sm" value={newItem.name} onChange={e => setNewItem({...newItem, name: e.target.value})} />
                                                <input placeholder="Price (₹)" type="number" required className="p-2 rounded-lg border border-purple-200 text-sm" value={newItem.price} onChange={e => setNewItem({...newItem, price: e.target.value})} />
                                            </div>
                                            <select className="w-full p-2 rounded-lg border border-purple-200 text-sm" value={newItem.category} onChange={e => setNewItem({...newItem, category: e.target.value})} required>
                                                <option value="">Select Category</option><option>Snacks</option><option>Meals</option><option>Beverages</option><option>Desserts</option>
                                            </select>
                                            <textarea placeholder="Description" className="w-full p-2 rounded-lg border border-purple-200 text-sm" value={newItem.description} onChange={e => setNewItem({...newItem, description: e.target.value})} />
                                            <button type="submit" className="bg-green-500 text-white px-4 py-1.5 rounded-lg text-xs font-bold shadow">Save Item</button>
                                        </form>
                                    )}
                                    <div className="grid gap-4">
                                        {myItems.length === 0 ? <p className="text-gray-400 text-sm text-center py-10">No items yet.</p> : myItems.map(item => (
                                            <div key={item.id} className="flex items-center justify-between p-4 border border-purple-100 rounded-xl bg-purple-50/50 hover:bg-white transition shadow-sm">
                                                <div>
                                                    <h3 className="font-bold text-purple-900">{item.name}</h3>
                                                    <p className="text-xs text-purple-600">{item.category} • ₹{item.price}</p>
                                                </div>
                                                <button onClick={() => handleDeleteItem(item.id)} className="text-red-400 hover:text-red-600"><Icons.Trash className="w-4 h-4" /></button>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                            {tab === 'orders' && (
                                <div className="space-y-6 fade-in">
                                    <h2 className="text-xl font-bold text-purple-900">Incoming Orders</h2>
                                    <div className="space-y-4">
                                        {myOrders.length === 0 ? <p className="text-gray-400 text-sm text-center py-10">No orders received yet.</p> : 
                                        myOrders.slice().reverse().map(order => (
                                            <div key={order.id} className="border border-purple-200 rounded-xl p-4 flex justify-between items-start bg-white shadow-sm">
                                                <div>
                                                    <div className="flex items-center gap-2 mb-2">
                                                        <span className="font-mono font-bold text-purple-600">#{order.id.slice(-4)}</span>
                                                        <span className={`text-[10px] px-2 py-0.5 rounded-full border ${order.status === 'Pending' ? 'bg-yellow-50 border-yellow-200 text-yellow-700' : 'bg-green-50 border-green-200 text-green-700'}`}>{order.status}</span>
                                                    </div>
                                                    <div className="text-sm text-gray-700 font-medium">{order.items.map(i => `${i.quantity}x ${i.name}`).join(', ')}</div>
                                                    <div className="text-xs text-gray-500 mt-1">Total: ₹{order.total} • Address: {order.address}</div>
                                                </div>
                                                {order.status === 'Pending' && (
                                                    <button onClick={() => updateOrderStatus(order.id, 'Ready')} className="bg-purple-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-purple-700">Mark Ready</button>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </section>
                    </main>
                </div>
            );
        };

        // --- COMPONENT: STUDENT DASHBOARD ---
        const StudentDashboard = ({ user, db, updateDb, onLogout }) => {
            const [cart, setCart] = useState([]);
            const [view, setView] = useState('browse');
            const [address, setAddress] = useState('');
            const [showSuccessModal, setShowSuccessModal] = useState(false);

            const addToCart = (item) => {
                setCart(prev => {
                    const existing = prev.find(i => i.id === item.id);
                    if (existing) return prev.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
                    return [...prev, { ...item, quantity: 1 }];
                });
            };

            const removeFromCart = (itemId) => {
                 setCart(prev => prev.filter(i => i.id !== itemId));
            };

            const placeOrder = () => {
                if (cart.length === 0) return;
                if (!address.trim()) {
                    alert("Please enter a delivery address.");
                    return;
                }

                const vendorGroups = {};
                cart.forEach(item => {
                    if (!vendorGroups[item.vendorId]) vendorGroups[item.vendorId] = [];
                    vendorGroups[item.vendorId].push(item);
                });

                const newOrders = [];
                Object.keys(vendorGroups).forEach(vId => {
                    const items = vendorGroups[vId];
                    const total = items.reduce((sum, i) => sum + (i.price * i.quantity), 0);
                    newOrders.push({
                        id: crypto.randomUUID(),
                        studentId: user.id,
                        studentName: user.name,
                        vendorId: vId,
                        items: items,
                        total: total,
                        address: address,
                        status: 'Pending',
                        timestamp: new Date().toISOString()
                    });
                });

                updateDb('orders', [...db.orders, ...newOrders]);
                setCart([]);
                setAddress('');
                setShowSuccessModal(true);
            };

            const myOrders = db.orders.filter(o => o.studentId === user.id);
            const cartTotal = cart.reduce((sum, i) => sum + (i.price * i.quantity), 0);

            return (
                <div className="h-full flex flex-col bg-gray-50">
                    {/* Header */}
                    <header className="bg-white border-b border-purple-200 px-6 py-3 flex justify-between items-center sticky top-0 z-20 shadow-sm">
                        <div className="flex items-center gap-2 cursor-pointer" onClick={() => setView('browse')}><span className="text-2xl">🍔</span><h1 className="font-bold text-purple-900">Student Hub</h1></div>
                        <div className="flex items-center gap-6">
                             <button onClick={() => setView('browse')} className={`text-sm font-medium transition hover:text-purple-600 ${view === 'browse' ? 'text-purple-600' : 'text-gray-500'}`}>Browse</button>
                             <button onClick={() => setView('cart')} className={`relative text-sm font-medium transition hover:text-purple-600 ${view === 'cart' ? 'text-purple-600' : 'text-gray-500'}`}>
                                Cart
                                {cart.length > 0 && <span className="absolute -top-2 -right-3 bg-pink-500 text-white text-[10px] w-4 h-4 flex items-center justify-center rounded-full">{cart.length}</span>}
                             </button>
                             <button onClick={() => setView('orders')} className={`text-sm font-medium transition hover:text-purple-600 ${view === 'orders' ? 'text-purple-600' : 'text-gray-500'}`}>My Orders</button>
                             <div className="h-4 w-px bg-gray-300"></div>
                             <button onClick={onLogout} className="text-xs text-red-500 font-medium hover:underline">Logout</button>
                        </div>
                    </header>

                    <main className="flex-1 overflow-y-auto p-6 max-w-6xl mx-auto w-full">
                        {/* Success Modal */}
                        {showSuccessModal && (
                            <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center fade-in">
                                <div className="bg-white rounded-3xl p-8 shadow-2xl max-w-sm w-full text-center modal-enter transform">
                                    <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                        <Icons.Check className="w-8 h-8" />
                                    </div>
                                    <h2 className="text-xl font-bold text-gray-900 mb-2">Order Confirmed!</h2>
                                    <p className="text-gray-500 mb-6 text-sm">Your food is being prepared and will be delivered to your address.</p>
                                    <button onClick={() => {setShowSuccessModal(false); setView('orders');}} className="w-full bg-purple-600 text-white py-3 rounded-xl font-bold hover:bg-purple-700 transition">View Status</button>
                                </div>
                            </div>
                        )}

                        {view === 'browse' && (
                            <div className="fade-in">
                                <h2 className="font-bold text-xl text-gray-800 mb-6">Available Menu</h2>
                                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {db.menuItems.length === 0 ? <p>No items available.</p> : db.menuItems.map(item => (
                                    <div key={item.id} className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col justify-between hover:shadow-lg hover:-translate-y-1 transition duration-300">
                                        <div>
                                            <div className="flex justify-between items-start mb-2">
                                                <h3 className="font-bold text-lg text-gray-800">{item.name}</h3>
                                                <span className="text-[10px] bg-purple-50 text-purple-600 px-2 py-1 rounded-full font-medium">{item.category}</span>
                                            </div>
                                            <p className="text-xs text-gray-500 leading-relaxed">{item.description}</p>
                                        </div>
                                        <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-50">
                                            <p className="text-lg font-bold text-purple-600">₹{item.price}</p>
                                            <button onClick={() => addToCart(item)} className="bg-purple-100 text-purple-700 p-2.5 rounded-xl hover:bg-purple-200 hover:scale-105 transition active:scale-95">
                                                <Icons.Plus className="w-5 h-5" />
                                            </button>
                                        </div>
                                    </div>
                                ))}
                                </div>
                            </div>
                        )}

                        {view === 'cart' && (
                            <div className="fade-in max-w-2xl mx-auto">
                                <h2 className="font-bold text-xl text-gray-800 mb-6">Your Cart</h2>
                                {cart.length === 0 ? (
                                    <div className="bg-white rounded-2xl p-10 text-center border border-gray-200">
                                        <div className="bg-gray-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                            <Icons.ShoppingCart className="w-6 h-6 text-gray-400" />
                                        </div>
                                        <p className="text-gray-500">Your cart is empty.</p>
                                        <button onClick={() => setView('browse')} className="mt-4 text-purple-600 font-bold hover:underline">Browse Menu</button>
                                    </div>
                                ) : (
                                    <div className="bg-white rounded-2xl shadow-sm border border-purple-100 overflow-hidden">
                                        <div className="p-6 space-y-6">
                                            {cart.map((item, idx) => (
                                                <div key={idx} className="flex items-center justify-between">
                                                    <div className="flex items-center gap-4">
                                                        <div className="bg-purple-50 w-12 h-12 rounded-lg flex items-center justify-center text-purple-600 font-bold">{item.quantity}x</div>
                                                        <div>
                                                            <h4 className="font-bold text-gray-800">{item.name}</h4>
                                                            <p className="text-xs text-gray-500">₹{item.price} each</p>
                                                        </div>
                                                    </div>
                                                    <div className="flex items-center gap-4">
                                                        <span className="font-bold text-gray-800">₹{item.price * item.quantity}</span>
                                                        <button onClick={() => removeFromCart(item.id)} className="text-red-400 hover:text-red-600"><Icons.Trash className="w-4 h-4"/></button>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                        
                                        <div className="bg-gray-50 p-6 space-y-4">
                                            <div className="flex justify-between text-lg font-bold text-purple-900">
                                                <span>Total Amount</span>
                                                <span>₹{cartTotal}</span>
                                            </div>
                                            
                                            <div className="pt-2">
                                                <label className="block text-xs font-bold uppercase text-gray-500 mb-2 flex items-center gap-2">
                                                    <Icons.MapPin className="w-3 h-3" /> Delivery Address
                                                </label>
                                                <textarea 
                                                    value={address}
                                                    onChange={(e) => setAddress(e.target.value)}
                                                    placeholder="Room Number, Hostel Block..."
                                                    className="w-full p-3 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400 resize-none h-24 bg-white"
                                                />
                                            </div>

                                            <button onClick={placeOrder} className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-bold shadow-lg hover:shadow-xl hover:opacity-95 transition transform active:scale-[0.98]">
                                                Confirm Order
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        {view === 'orders' && (
                            <div className="space-y-4 fade-in max-w-3xl mx-auto">
                                <h2 className="font-bold text-xl text-gray-800 mb-6">My Order History</h2>
                                {myOrders.length === 0 ? <p className="text-gray-400 text-center py-10">No orders placed yet.</p> : 
                                myOrders.slice().reverse().map(order => (
                                    <div key={order.id} className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition">
                                        <div className="flex justify-between mb-4 border-b pb-3">
                                            <div>
                                                <div className="font-bold text-purple-900 text-lg">Order #{order.id.slice(0,8)}</div>
                                                <div className="text-xs text-gray-400 mt-1">{new Date(order.timestamp).toLocaleString()}</div>
                                            </div>
                                            <span className={`h-fit px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${order.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'}`}>{order.status}</span>
                                        </div>
                                        <div className="space-y-2 mb-4">
                                            {order.items.map((item, i) => (
                                                <div key={i} className="flex justify-between text-sm text-gray-600">
                                                    <span>{item.quantity}x {item.name}</span>
                                                    <span className="font-medium">₹{item.price * item.quantity}</span>
                                                </div>
                                            ))}
                                        </div>
                                        <div className="flex justify-between items-center pt-3 border-t border-gray-100">
                                            <div className="text-xs text-gray-500">
                                                <span className="font-bold">To:</span> {order.address}
                                            </div>
                                            <div className="text-lg font-bold text-purple-900">₹{order.total}</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </main>
                </div>
            );
        };

        // --- COMPONENT: ADMIN / BACKEND DOCS ---
        const BackendDocs = ({ onLogout, systemStatus }) => {
            const Section = ({ title, icon: IconComp, children }) => (
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 border-2 border-purple-200 mb-6 shadow-sm">
                    <h3 className="text-xl font-bold text-purple-900 mb-4 flex items-center gap-2">
                        {IconComp && <IconComp className="w-6 h-6" />} {title}
                    </h3>
                    {children}
                </div>
            );
            return (
                <div className="h-full flex flex-col">
                    <header className="bg-slate-900 text-white px-6 py-3 flex justify-between items-center">
                        <div className="flex items-center gap-2 font-mono"><Icons.Server className="text-green-400"/> System Admin Console</div>
                        <button onClick={onLogout} className="text-xs bg-red-600 hover:bg-red-500 px-3 py-1 rounded">Shutdown Session</button>
                    </header>
                    <div className="flex-1 overflow-y-auto p-6 bg-slate-50">
                         <div className="max-w-6xl mx-auto">
                            <div className="grid md:grid-cols-3 gap-4 mb-8">
                                {[
                                    { label: 'Database', val: 'Connected', icon: Icons.Database, color: 'text-green-600' },
                                    { label: 'Active Orders', val: systemStatus.totalOrders, icon: Icons.ShoppingCart, color: 'text-blue-600' },
                                    { label: 'API Status', val: 'Online', icon: Icons.Server, color: 'text-purple-600' },
                                ].map((stat, i) => (
                                    <div key={i} className="bg-white p-4 rounded-xl shadow-sm border border-purple-100 flex items-center gap-4">
                                        <stat.icon className={`w-8 h-8 ${stat.color}`} />
                                        <div>
                                            <div className="text-xs text-gray-500 uppercase">{stat.label}</div>
                                            <div className="text-lg font-bold text-slate-800">{stat.val}</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <Section title="Database Schema Design" icon={Icons.Database}>
                                <div className="grid md:grid-cols-2 gap-4">
                                     <div className="bg-white rounded-lg p-4 shadow-sm border border-purple-200">
                                        <h4 className="font-bold text-purple-900 mb-3">👥 Users Table</h4>
                                        <div className="font-mono text-xs space-y-2 text-gray-600">
                                            <div className="flex justify-between border-b pb-1"><span>id</span><span className="text-purple-600">UUID (PK)</span></div>
                                            <div className="flex justify-between border-b pb-1"><span>username</span><span className="text-purple-600">VARCHAR</span></div>
                                            <div className="flex justify-between border-b pb-1"><span>role</span><span className="text-purple-600">ENUM</span></div>
                                        </div>
                                     </div>
                                     <div className="bg-white rounded-lg p-4 shadow-sm border border-purple-200">
                                        <h4 className="font-bold text-purple-900 mb-3">📦 Orders Table</h4>
                                        <div className="font-mono text-xs space-y-2 text-gray-600">
                                            <div className="flex justify-between border-b pb-1"><span>id</span><span className="text-purple-600">UUID (PK)</span></div>
                                            <div className="flex justify-between border-b pb-1"><span>student_id</span><span className="text-purple-600">FK > Users</span></div>
                                            <div className="flex justify-between border-b pb-1"><span>total</span><span className="text-purple-600">DECIMAL</span></div>
                                        </div>
                                     </div>
                                </div>
                            </Section>
                            <Section title="Backend API Routes" icon={Icons.Server}>
                                <div className="space-y-2 font-mono text-xs">
                                    <div className="flex gap-2 bg-white p-2 rounded border"><span className="bg-green-500 text-white px-1 rounded">POST</span> /api/auth/login</div>
                                    <div className="flex gap-2 bg-white p-2 rounded border"><span className="bg-blue-500 text-white px-1 rounded">GET</span> /api/vendors/menu</div>
                                    <div className="flex gap-2 bg-white p-2 rounded border"><span className="bg-green-500 text-white px-1 rounded">POST</span> /api/orders/create</div>
                                </div>
                            </Section>
                         </div>
                    </div>
                </div>
            );
        };

        // --- MAIN APP ORCHESTRATOR ---
        const App = () => {
            const [db, setDb] = useState(initialDb);
            const [currentUser, setCurrentUser] = useState(null);
            
            const updateDb = (collection, newData) => {
                setDb(prev => ({ ...prev, [collection]: newData }));
            };

            const handleLogin = (username, password, role) => {
                const user = db.users.find(u => u.username === username && u.password === password && u.role === role);
                if (user) {
                    setCurrentUser(user);
                    return true;
                }
                return false;
            };

            const handleSignup = (data) => {
                const newUser = { 
                    id: 'u' + Date.now(), 
                    username: data.username, 
                    password: data.password, 
                    role: data.role, 
                    name: data.fullname 
                };
                updateDb('users', [...db.users, newUser]);
            };

            const handleLogout = () => setCurrentUser(null);

            if (!currentUser) return <LandingPage onLogin={handleLogin} onSignup={handleSignup} />;
            if (currentUser.role === 'vendor') return <VendorDashboard user={currentUser} db={db} updateDb={updateDb} onLogout={handleLogout} />;
            if (currentUser.role === 'student') return <StudentDashboard user={currentUser} db={db} updateDb={updateDb} onLogout={handleLogout} />;
            if (currentUser.role === 'admin') return <BackendDocs onLogout={handleLogout} systemStatus={{ totalOrders: db.orders.length }} />;
            return <div>Unknown Role</div>;
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# --- FLASK ROUTE ---
@app.route('/')
def index():
    # Return the HTML string directly with the correct mime type
    return Response(HTML_CONTENT, mimetype='text/html')

if __name__ == '__main__':
    # Start the timer to open the browser after 1 second
    Timer(1, open_browser).start()
    # Run the Flask app
    app.run(port=5000)