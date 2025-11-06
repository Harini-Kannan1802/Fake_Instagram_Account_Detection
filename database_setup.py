import sqlite3
import hashlib

def setup_database():
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create username_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS username_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            old_username TEXT,
            new_username TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert sample data
    sample_data = [
        ('john_doe_123', 'john@email.com', '+1234567890'),
        ('sarah_smith', 'sarah@email.com', '+0987654321'),
        ('mike_jones', 'mike@email.com', '+1122334455'),
        ('user123', 'john@email.com', '+1234567890'),  # Same email as john_doe
        ('user456', 'sarah@email.com', '+0987654321'), # Same phone as sarah
        ('fake_account1', 'fake1@email.com', '+1111111111'),
        ('fake_account2', 'fake1@email.com', '+1111111111'),
        ('fake_account3', 'fake1@email.com', '+1111111111'),
    ]
    
    username_changes = [
        (1, 'john_original', 'john_doe_123'),
        (1, 'john_doe_123', 'john_new'),
        (2, 'sarah_old', 'sarah_smith'),
        (3, 'mike_original', 'mike_jones'),
    ]
    
    for username, email, phone in sample_data:
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO users (username, email, phone) VALUES (?, ?, ?)',
                (username, email, phone)
            )
        except:
            pass
    
    for user_id, old_username, new_username in username_changes:
        cursor.execute(
            'INSERT INTO username_history (user_id, old_username, new_username) VALUES (?, ?, ?)',
            (user_id, old_username, new_username)
        )
    
    conn.commit()
    conn.close()
    print("✅ Database setup completed successfully!")
    print("📊 Sample data inserted with:")
    print("   - 8 user accounts")
    print("   - 4 username change records")
    print("   - Multiple accounts linked to same email/phone")

if __name__ == "__main__":
    setup_database()