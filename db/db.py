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
        
    def get_stats_add_balance(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT * FROM success_payments WHERE user_id = ?", (user_id,)).fetchall()
            if res:
                form_answ = [f"Дата: {ret[3]}\nСумма: {ret[2]}" for ret in res]
                return "\n\n".join(form_answ)
            else:
                return "Ваша история пуста!"
            
            
    def get_stats_widthraw_balance(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT * FROM success_withdraw_balance WHERE user_id = ?", (user_id,)).fetchall()
            if res:
                form_answ = [f"Дата: {ret[3]}\nСумма: {ret[2]}" for ret in res]
                return "\n\n".join(form_answ)
            else:
                return "Ваша история пуста!"
    
    
    def add_balance_stats(self, user_id, sum, date):
        with self.conn:
            return self.cursor.execute("INSERT INTO success_payments (user_id, sum, date) VALUES (?,?,?)", (user_id, sum, date,))
    
    
    def add_widthraw_stats(self, user_id, date):
        with self.conn:
            return self.cursor.execute("INSERT INTO success_withdraw_balance (user_id, date) VALUES (?,?)", (user_id, date,))
    