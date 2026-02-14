"""
View CRM Database Contents
This script displays all data stored in the SQLite database
"""

import sqlite3
from datetime import datetime

def view_database():
    # Connect to the database (Flask stores it in 'instance' folder)
    conn = sqlite3.connect('instance/crm.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("📊 CRM DATABASE CONTENTS")
    print("=" * 80)
    print()
    
    # ==================== CLIENTS TABLE ====================
    print("👥 CLIENTS")
    print("-" * 80)
    
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    
    if not clients:
        print("   No clients found.")
    else:
        print(f"   Total Clients: {len(clients)}")
        print()
        
        for client in clients:
            print(f"   ID: {client[0]}")
            print(f"   Name: {client[1]}")
            print(f"   Company: {client[2] or 'N/A'}")
            print(f"   Email: {client[3]}")
            print(f"   Phone: {client[4] or 'N/A'}")
            print(f"   Status: {client[5]}")
            print(f"   Priority: {client[6]}")
            print(f"   Created: {client[7]}")
            print("   " + "-" * 76)
    
    print()
    print()
    
    # ==================== INTERACTIONS TABLE ====================
    print("💬 INTERACTIONS")
    print("-" * 80)
    
    cursor.execute("""
        SELECT i.id, i.client_id, c.name, i.date, i.type, i.notes, i.created_at
        FROM interactions i
        JOIN clients c ON i.client_id = c.id
        ORDER BY i.created_at DESC
    """)
    interactions = cursor.fetchall()
    
    if not interactions:
        print("   No interactions found.")
    else:
        print(f"   Total Interactions: {len(interactions)}")
        print()
        
        for interaction in interactions:
            print(f"   ID: {interaction[0]}")
            print(f"   Client: {interaction[2]} (ID: {interaction[1]})")
            print(f"   Date: {interaction[3]}")
            print(f"   Type: {interaction[4]}")
            print(f"   Notes: {interaction[5]}")
            print(f"   Created: {interaction[6]}")
            print("   " + "-" * 76)
    
    print()
    print()
    
    # ==================== SUMMARY STATISTICS ====================
    print("📈 SUMMARY STATISTICS")
    print("-" * 80)
    
    # Count by status
    cursor.execute("SELECT status, COUNT(*) FROM clients GROUP BY status")
    status_counts = cursor.fetchall()
    
    print("   Clients by Status:")
    for status, count in status_counts:
        print(f"      {status}: {count}")
    
    print()
    
    # Count by priority
    cursor.execute("SELECT priority, COUNT(*) FROM clients GROUP BY priority")
    priority_counts = cursor.fetchall()
    
    print("   Clients by Priority:")
    for priority, count in priority_counts:
        print(f"      {priority}: {count}")
    
    print()
    
    # Recent activity
    cursor.execute("SELECT COUNT(*) FROM interactions WHERE date >= date('now', '-7 days')")
    recent = cursor.fetchone()[0]
    print(f"   Interactions in last 7 days: {recent}")
    
    print()
    print("=" * 80)
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    try:
        view_database()
    except sqlite3.OperationalError as e:
        print("❌ Error: Database file not found!")
        print("   Make sure 'crm.db' exists in the same folder.")
        print("   Run 'python app.py' first to create the database.")
    except Exception as e:
        print(f"❌ Error: {e}")