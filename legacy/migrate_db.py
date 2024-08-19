import sqlite3

def add_column():
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        
        # Add the appointment_date column if it doesn't exist
        cursor.execute("PRAGMA table_info(tokens)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'appointment_date' not in columns:
            cursor.execute("ALTER TABLE tokens ADD COLUMN appointment_date TEXT")
            print("Added 'appointment_date' column to the 'tokens' table.")
        else:
            print("'appointment_date' column already exists in the 'tokens' table.")

if __name__ == '__main__':
    add_column()
