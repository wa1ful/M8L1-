import sqlite3

class Database:
    def __init__(self, db_file='support.db'):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                question TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_request(self, user_id, username, question):
        self.cursor.execute('''
            INSERT INTO requests (user_id, username, question) 
            VALUES (?, ?, ?)
        ''', (user_id, username, question))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def close(self):
        self.conn.close()