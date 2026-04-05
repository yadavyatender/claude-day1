import sqlite3
from datetime import datetime
from config import DATABASE_FILE

def create_database():
    """Create SQLite database and tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gold_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            price_usd REAL NOT NULL,
            change_percent REAL,
            source TEXT DEFAULT 'goldapi'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            email_to TEXT NOT NULL,
            subject TEXT NOT NULL,
            status TEXT DEFAULT 'sent'
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DATABASE_FILE}")

def insert_rate(price_usd, change_percent=None):
    """Insert a new gold rate record."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO gold_rates (price_usd, change_percent)
        VALUES (?, ?)
    ''', (price_usd, change_percent))
    
    conn.commit()
    conn.close()
    print(f"Rate inserted: ${price_usd:.2f} USD")

def get_latest_rate():
    """Get the most recent gold rate."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, timestamp, price_usd, change_percent
        FROM gold_rates
        ORDER BY timestamp DESC
        LIMIT 1
    ''')
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'id': result[0],
            'timestamp': result[1],
            'price_usd': result[2],
            'change_percent': result[3]
        }
    return None

def get_previous_rate():
    """Get the second most recent gold rate."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, timestamp, price_usd, change_percent
        FROM gold_rates
        ORDER BY timestamp DESC
        LIMIT 2 OFFSET 1
    ''')
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'id': result[0],
            'timestamp': result[1],
            'price_usd': result[2],
            'change_percent': result[3]
        }
    return None

def get_all_rates(limit=10):
    """Get recent gold rates."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, timestamp, price_usd, change_percent
        FROM gold_rates
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    rates = []
    for row in results:
        rates.append({
            'id': row[0],
            'timestamp': row[1],
            'price_usd': row[2],
            'change_percent': row[3]
        })
    return rates

def log_notification(email_to, subject):
    """Log sent notification."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO notifications (email_to, subject)
        VALUES (?, ?)
    ''', (email_to, subject))
    
    conn.commit()
    conn.close()

def get_notification_count(hours=24):
    """Get count of notifications sent in the last N hours."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM notifications
        WHERE datetime(timestamp) > datetime('now', '-' || ? || ' hours')
    ''', (hours,))
    
    count = cursor.fetchone()[0]
    conn.close()
    return count
