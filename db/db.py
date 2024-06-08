from datetime import datetime
import sqlite3

class UserDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    
    def user_exists(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id,)).fetchall()
            return res
        
        
    def get_all_users(self):
        with self.conn:
            return [row[1] for row in self.cursor.execute("SELECT * FROM user").fetchall()]
    
    
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
    
    def change_req(self, new_req):
        with self.conn:
            return self.cursor.execute("UPDATE bank_req SET req = ?", (new_req,))
    
    
    def add_ban(self, user_id, time):
        with self.conn:
            return self.cursor.execute("INSERT INTO banned_users (user_id, time) VALUES (?,?)", (user_id, time,))
    
    
    def add_suspicious(self, user_id):
        with self.conn:
            return self.cursor.execute("UPDATE user SET suspicious = 1 WHERE user_id = ?", (user_id,))
    
    
    def add_balance(self, user_id, value_sum):
        with self.conn:
            return self.cursor.execute("UPDATE user SET balance = balance + ? WHERE user_id = ?", (value_sum, user_id,))
    
    
    def update_user_ranking_and_bonus(self, user_id, ranking, bonus):
        with self.conn:
            self.cursor.execute("UPDATE user SET ranking = ?, bonus = ? WHERE id = ?", (ranking, bonus, user_id,))
    
    
    def update_ranking(self):
        cursor = self.cursor
        cursor.execute("SELECT id, balance FROM user ORDER BY balance DESC")
        users = cursor.fetchall()

        for idx, (user_id, balance) in enumerate(users):
            ranking = idx + 1
            if ranking <= 3:
                bonus = 3.0
            elif ranking <= 20:
                bonus = 2.0
            elif ranking <= 50:
                bonus = 1.0
            else:
                bonus = 0.0
            
            self.update_user_ranking_and_bonus(user_id, ranking, bonus,)
            
    
    def get_rank_user(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT ranking, bonus FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return res[0]
        

    def get_bonus_user(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT bonus FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return res[0] 
        
                   
    def get_rank_user(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT ranking FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return res[0]            
    
    
    def change_replanis(self, value):
        with self.conn:
            return self.cursor.execute("UPDATE bank_req SET status = ?", (value,))
        
        
    def get_stats_suspicious(self):
        with self.conn:
            res = self.cursor.execute("SELECT * FROM user WHERE suspicious = ?", (1,)).fetchall()
            if res:
                form_answ = [f"Chat_id: {ret[1]}" for ret in res]
                return "\n\n".join(form_answ)
            else:
                return "Ваша история пуста!"
            
    
    def remove_ban(self, user_id):
        with self.conn:
            return self.cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
        
    
    def get_today_profit(self):
        with self.conn:
            today_date = datetime.today().strftime('%Y-%m-%d')
            self.cursor.execute("SELECT SUM(sum) FROM success_payments WHERE date = ?", (today_date,))
            result = self.cursor.fetchone()[0]
            return result if result else 0


    def get_total_profit(self):
        self.cursor.execute("SELECT SUM(sum) FROM success_payments")
        result = self.cursor.fetchone()[0]
        return result if result else 0
    
    
    def is_admin(self, user_id):
        with self.conn:
            res = self.cursor.execute("SELECT admin FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return bool(res[0]) if res else False
        
    
    def get_req(self):
        with self.conn:
            res = self.cursor.execute("SELECT req FROM bank_req WHERE status = 1").fetchone()
            return str(res[0]) if res else False
        