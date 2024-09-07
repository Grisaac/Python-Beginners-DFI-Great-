import sqlite3

def setup_database():
    conn = sqlite3.connect('hotel_reservation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guest_name TEXT,
        room_number INTEGER,
        room_type TEXT,
        check_in_date TEXT,
        check_out_date TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        room_number INTEGER PRIMARY KEY,
        room_type TEXT,
        status TEXT
    )
    ''')
    
    room_types = ['Single', 'Double', 'Suite', 'Deluxe', 'Penthouse']
    room_data = [(101, 'Single', 'Available'),
                 (102, 'Double', 'Available'),
                 (103, 'Suite', 'Available'),
                 (201, 'Deluxe', 'Available'),
                 (202, 'Penthouse', 'Available')]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO rooms (room_number, room_type, status)
    VALUES (?, ?, ?)
    ''', room_data)
    
    conn.commit()
    conn.close()

setup_database()