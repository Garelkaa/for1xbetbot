import sqlite3

class UserDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    
    def user_exists(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id,)).fetchall()
            return res
    
    def add_user(self, user_id):
        with self.conn:
            return self.cursor.execute("INSERT INTO user (user_id) VALUES (?)", (user_id,))
    