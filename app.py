from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class Client(db.Model):
    """Client model - stores customer information"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: one client can have many interactions
    interactions = db.relationship('Interaction', backref='client', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert client object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'email': self.email,
            'phone': self.phone,
            'amount': self.amount,
            'status': self.status,
            'priority': self.priority,
            'createdAt': self.created_at.isoformat(),
            'interactions': [interaction.to_dict() for interaction in self.interactions]
        }


class Interaction(db.Model):
    """Interaction model - stores interaction logs for each client"""
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert interaction object to dictionary"""
        return {
            'id': self.id,
            'date': self.date,
            'type': self.type,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat()
        }


# ==================== API ROUTES ====================

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)


@app.route('/api/database/view')
def view_database_web():
    """View database contents in browser"""
    clients = Client.query.all()
    interactions = Interaction.query.all()
    
    # Get statistics
    status_stats = db.session.query(
        Client.status, 
        db.func.count(Client.id)
    ).group_by(Client.status).all()
    
    priority_stats = db.session.query(
        Client.priority,
        db.func.count(Client.id)
    ).group_by(Client.priority).all()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CRM Database Viewer</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            h1 {{
                color: #667eea;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #764ba2;
                margin-top: 30px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            th {{
                background: rgb(71, 71, 255);
                border: 2px solid rgb(50, 50, 200);
                color: white;
                padding: 12px;
                text-align: left;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background: #f9f9f9;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .stat-box {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }}
            .badge {{
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
            }}
            .badge-high {{ background: #ffebee; color: #d32f2f; }}
            .badge-medium {{ background: #fff3e0; color: #f57c00; }}
            .badge-low {{ background: #e8f5e9; color: #388e3c; }}
            .badge-new {{ background: #e3f2fd; color: #1976d2; }}
            .badge-contacted {{ background: #fff3e0; color: #f57c00; }}
            .badge-uncontactable {{ background: #f3e5f5; color: #7b1fa2; }}
            .badge-undernego {{ background: #fce4ec; color: #c2185b; }}
            .badge-fullypaid {{ background: #e8f5e9; color: #388e3c; }}
            .badge-pullout {{ background: #ffebee; color: #d32f2f; }}
            .back-link {{
                display: inline-block;
                margin: 20px 0;
                padding: 10px 20px;
                background: rgb(71, 71, 255);
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }}
            .back-link:hover {{
                background: #764ba2;
            }}
            .empty {{
                text-align: center;
                padding: 40px;
                color: #999;
            }}
        </style>
    </head>
    <body>
        <h1>📊 CRM Database Viewer</h1>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0;">
            <a href="/" class="back-link" style="margin: 0;">← Back to CRM</a>
            <div>
                <span style="color: #666; margin-right: 15px;">Last updated: {datetime.now().strftime('%H:%M:%S')}</span>
                <button onclick="location.reload()" style="padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 600;">
                    🔄 Refresh Now
                </button>
            </div>
        </div>
        <div style="background: #fff3cd; padding: 10px; border-radius: 4px; margin-bottom: 20px; border-left: 4px solid #ffc107;">
            ℹ️ <strong>Auto-refresh:</strong> This page automatically updates every 5 seconds
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div>Total Clients</div>
                <div class="stat-number">{len(clients)}</div>
            </div>
            <div class="stat-box">
                <div>Total Interactions</div>
                <div class="stat-number">{len(interactions)}</div>
            </div>
        </div>
        
        <h2>📈 Statistics</h2>
        <div class="stats">
            <div class="stat-box">
                <strong>By Status:</strong><br>
                {'<br>'.join([f"{status}: {count}" for status, count in status_stats]) if status_stats else 'No data yet'}
            </div>
            <div class="stat-box">
                <strong>By Priority:</strong><br>
                {'<br>'.join([f"{priority}: {count}" for priority, count in priority_stats]) if priority_stats else 'No data yet'}
            </div>
        </div>
        
        <h2>👥 Clients ({len(clients)})</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Company</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Amount (AED)</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Created</th>
                    <th>Interactions</th>
                </tr>
            </thead>
            <tbody>
                {''.join([f'''
                <tr>
                    <td>{client.id}</td>
                    <td><strong>{client.name}</strong></td>
                    <td>{client.company or 'N/A'}</td>
                    <td>{client.email}</td>
                    <td>{client.phone or 'N/A'}</td>
                    <td>AED {client.amount:,.2f}</td>
                    <td><span class="badge badge-{client.status}">{client.status}</span></td>
                    <td><span class="badge badge-{client.priority}">{client.priority}</span></td>
                    <td>{client.created_at.strftime('%Y-%m-%d %H:%M')}</td>
                    <td>{len(client.interactions)}</td>
                </tr>
                ''' for client in clients]) if clients else '<tr><td colspan="10" class="empty">No clients found - Add some clients first!</td></tr>'}
            </tbody>
        </table>
        
        <h2>💬 Interactions ({len(interactions)})</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Client</th>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Notes</th>
                    <th>Created</th>
                </tr>
            </thead>
            <tbody>
                {''.join([f'''
                <tr>
                    <td>{interaction.id}</td>
                    <td><strong>{interaction.client.name}</strong></td>
                    <td>{interaction.date}</td>
                    <td>{interaction.type}</td>
                    <td>{interaction.notes}</td>
                    <td>{interaction.created_at.strftime('%Y-%m-%d %H:%M')}</td>
                </tr>
                ''' for interaction in interactions]) if interactions else '<tr><td colspan="6" class="empty">No interactions logged yet</td></tr>'}
            </tbody>
        </table>
        
        <a href="/" class="back-link">← Back to CRM</a>
    </body>
    </html>
    """
    
    return html


# CLIENT ENDPOINTS

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Get all clients"""
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients])


@app.route('/api/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Get a specific client by ID"""
    client = Client.query.get_or_404(client_id)
    return jsonify(client.to_dict())


@app.route('/api/clients', methods=['POST'])
def create_client():
    """Create a new client"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    
    new_client = Client(
        name=data['name'],
        company=data.get('company', ''),
        email=data['email'],
        phone=data.get('phone', ''),
        amount=data.get('amount', 0.0),
        status=data['status'],
        priority=data['priority']
    )
    
    db.session.add(new_client)
    db.session.commit()
    
    return jsonify(new_client.to_dict()), 201


@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Update an existing client"""
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    
    # Update fields
    client.name = data.get('name', client.name)
    client.company = data.get('company', client.company)
    client.email = data.get('email', client.email)
    client.phone = data.get('phone', client.phone)
    client.amount = data.get('amount', client.amount)
    client.status = data.get('status', client.status)
    client.priority = data.get('priority', client.priority)
    
    db.session.commit()
    
    return jsonify(client.to_dict())


@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Delete a client"""
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    
    return jsonify({'message': 'Client deleted successfully'}), 200


# INTERACTION ENDPOINTS

@app.route('/api/clients/<int:client_id>/interactions', methods=['POST'])
def create_interaction(client_id):
    """Add an interaction to a client"""
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    
    new_interaction = Interaction(
        client_id=client_id,
        date=data['date'],
        type=data['type'],
        notes=data['notes']
    )
    
    db.session.add(new_interaction)
    db.session.commit()
    
    return jsonify(new_interaction.to_dict()), 201


@app.route('/api/interactions/<int:interaction_id>', methods=['DELETE'])
def delete_interaction(interaction_id):
    """Delete an interaction"""
    interaction = Interaction.query.get_or_404(interaction_id)
    db.session.delete(interaction)
    db.session.commit()
    
    return jsonify({'message': 'Interaction deleted successfully'}), 200


# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized!")


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    # Create database tables if they don't exist
    init_db()
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)