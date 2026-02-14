# CRM System with Python Flask Backend

A Customer Relationship Manager with a Python Flask backend and SQLite database - perfect for learning full-stack development!

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)
    ↓ API Calls (HTTP)
Backend (Python Flask)
    ↓ SQL Queries
Database (SQLite - crm.db)
```

## 📁 Project Structure

```
crm-flask/
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── index.html          # Frontend HTML
├── style.css           # Frontend styles
├── script.js           # Frontend JavaScript (API calls)
├── crm.db             # SQLite database (auto-created)
└── README.md          # This file
```

## 🚀 Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install with the --break-system-packages flag if needed:

```bash
pip install -r requirements.txt --break-system-packages
```

### 2. Run the Flask Server

```bash
python app.py
```

The server will start at: `http://localhost:5000`

### 3. Open the Application

Open your browser and go to:
```
http://localhost:5000
```

## 🔧 How It Works

### Backend (app.py)

**Database Models:**
- `Client` - Stores customer information
- `Interaction` - Stores interaction logs (linked to clients)

**API Endpoints:**

**Clients:**
- `GET /api/clients` - Get all clients
- `GET /api/clients/<id>` - Get specific client
- `POST /api/clients` - Create new client
- `PUT /api/clients/<id>` - Update client
- `DELETE /api/clients/<id>` - Delete client

**Interactions:**
- `POST /api/clients/<id>/interactions` - Add interaction to client
- `DELETE /api/interactions/<id>` - Delete interaction

### Frontend (script.js)

The JavaScript now makes HTTP requests to the Flask API instead of using localStorage:

**Before (localStorage):**
```javascript
clients = JSON.parse(localStorage.getItem('crmClients')) || [];
```

**After (API):**
```javascript
const response = await fetch('http://localhost:5000/api/clients');
clients = await response.json();
```

## 📊 Database Schema

### Clients Table
```sql
CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company VARCHAR(100),
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Interactions Table
```sql
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    date VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL,
    notes TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

## 🔑 Key Learning Concepts

### 1. **RESTful API Design**
- GET for reading data
- POST for creating data
- PUT for updating data
- DELETE for removing data

### 2. **Database Relationships**
- One-to-Many: One client can have many interactions
- Foreign Keys: `client_id` links interactions to clients
- Cascade Delete: Deleting a client deletes all their interactions

### 3. **ORM (Object-Relational Mapping)**
- SQLAlchemy converts Python objects to database rows
- No need to write raw SQL queries
- Automatic database schema creation

### 4. **CORS (Cross-Origin Resource Sharing)**
- Allows frontend to communicate with backend
- Required when frontend and backend are on different ports

### 5. **Async/Await in JavaScript**
- Modern way to handle asynchronous API calls
- Better error handling with try/catch

## 🎓 What You've Learned

✅ How to build a REST API with Flask  
✅ Database design and relationships  
✅ SQL queries through SQLAlchemy ORM  
✅ Frontend-backend communication  
✅ HTTP methods (GET, POST, PUT, DELETE)  
✅ Error handling on both frontend and backend  
✅ Database migrations and initialization  

## 🔄 Next Steps to Improve

1. **Add User Authentication**
   - Login/Register system
   - Password hashing
   - Session management

2. **Add Pagination**
   - Limit clients per page
   - Better performance with large datasets

3. **Add Search Filters on Backend**
   - Move filtering logic to SQL queries
   - More efficient than filtering in JavaScript

4. **Deploy to Production**
   - Use PostgreSQL instead of SQLite
   - Deploy to Heroku, Railway, or AWS
   - Add environment variables

5. **Add Data Validation**
   - Email format validation
   - Required field checks
   - Input sanitization

## 🐛 Troubleshooting

**"Connection refused" error:**
- Make sure the Flask server is running (`python app.py`)
- Check the server is on `http://localhost:5000`

**Database errors:**
- Delete `crm.db` file and restart the server
- Database will be recreated automatically

**CORS errors:**
- Check Flask-CORS is installed
- Verify `CORS(app)` is in app.py

## 📚 Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- REST API Guide: https://restfulapi.net/
- MDN Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

**Happy Learning! 🚀**