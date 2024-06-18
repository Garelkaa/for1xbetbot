import sqlite3
from datetime import datetime

class UserDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def __del__(self):
        self.conn.close()

    def user_exists(self, user_id):
        """Check if a user exists in the database."""
        with self.conn:
            res = self.cursor.execute("SELECT 1 FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return bool(res)
        
    def get_all_users(self):
        """Retrieve all user IDs from the database."""
        with self.conn:
            return [row[1] for row in self.cursor.execute("SELECT * FROM user").fetchall()]
    
    def add_user(self, user_id):
        """Add a new user to the database."""
        with self.conn:
            self.cursor.execute("INSERT INTO user (user_id) VALUES (?)", (user_id,))
        
    def get_stats_add_balance(self, user_id):
        """Get the balance addition history for a user."""
        with self.conn:
            res = self.cursor.execute("SELECT * FROM success_payments WHERE user_id = ?", (user_id,)).fetchall()
            if res:
                return "\n\n".join(f"Дата: {ret[3]}\nСумма: {ret[2]}" for ret in res)
            return "Ваша история пуста!"
            
    def get_stats_withdraw_balance(self, user_id):
        """Get the balance withdrawal history for a user."""
        with self.conn:
            res = self.cursor.execute("SELECT * FROM success_withdraw_balance WHERE user_id = ?", (user_id,)).fetchall()
            if res:
                return "\n\n".join(f"Дата: {ret[3]}\nСумма: {ret[2]}" for ret in res)
            return "Ваша история пуста!"
    
    def add_balance_stats(self, user_id, sum, date):
        """Add a record to the balance addition history."""
        with self.conn:
            self.cursor.execute("INSERT INTO success_payments (user_id, sum, date) VALUES (?,?,?)", (user_id, sum, date,))
    
    def add_withdraw_stats(self, user_id, date):
        """Add a record to the balance withdrawal history."""
        with self.conn:
            self.cursor.execute("INSERT INTO success_withdraw_balance (user_id, date) VALUES (?,?)", (user_id, date,))
    
    def change_req(self, new_req):
        """Update the bank request details."""
        with self.conn:
            self.cursor.execute("UPDATE bank_req SET req = ?", (new_req,))
    
    def add_ban(self, user_id, time):
        """Ban a user."""
        with self.conn:
            self.cursor.execute("INSERT INTO banned_users (user_id, time) VALUES (?,?)", (user_id, time,))
    
    def add_suspicious(self, user_id):
        """Mark a user as suspicious."""
        with self.conn:
            self.cursor.execute("UPDATE user SET suspicious = 1 WHERE user_id = ?", (user_id,))
    
    def add_balance(self, user_id, value_sum):
        """Add balance to a user's account."""
        with self.conn:
            self.cursor.execute("UPDATE user SET balance = balance + ? WHERE user_id = ?", (value_sum, user_id,))
    
    def update_user_ranking_and_bonus(self, user_id, ranking, bonus):
        """Update a user's ranking and bonus."""
        with self.conn:
            self.cursor.execute("UPDATE user SET ranking = ?, bonus = ? WHERE id = ?", (ranking, bonus, user_id,))
    
    def update_ranking(self):
        """Update the ranking and bonus for all users based on their balance."""
        cursor = self.cursor
        cursor.execute("SELECT id, balance FROM user ORDER BY balance DESC")
        users = cursor.fetchall()

        for idx, (user_id, balance) in enumerate(users):
            ranking = idx + 1
            bonus = self.calculate_bonus(ranking)
            self.update_user_ranking_and_bonus(user_id, ranking, bonus)
    
    def calculate_bonus(self, ranking):
        """Calculate bonus based on ranking."""
        if ranking <= 3:
            return 3.0
        elif ranking <= 20:
            return 2.0
        elif ranking <= 50:
            return 1.0
        return 0.0
    
    def get_rank_user(self, user_id):
        """Get the ranking of a user."""
        with self.conn:
            res = self.cursor.execute("SELECT ranking FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return res[0] if res else None
        
    def get_bonus_user(self, user_id):
        """Get the bonus of a user."""
        with self.conn:
            res = self.cursor.execute("SELECT bonus FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return res[0] if res else None
    
    def change_replanish_status(self, value):
        """Change the status of bank replenishment."""
        with self.conn:
            self.cursor.execute("UPDATE bank_req SET status = ?", (value,))
        
    def get_stats_suspicious(self):
        """Get the list of suspicious users."""
        with self.conn:
            res = self.cursor.execute("SELECT * FROM user WHERE suspicious = 1").fetchall()
            if res:
                return "\n\n".join(f"Chat_id: {ret[1]}" for ret in res)
            return "Ваша история пуста!"
    
    def remove_ban(self, user_id):
        """Remove a ban from a user."""
        with self.conn:
            self.cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
        
    def get_today_profit(self):
        """Get today's profit from successful payments."""
        with self.conn:
            today_date = datetime.today().strftime('%Y-%m-%d')
            self.cursor.execute("SELECT SUM(sum) FROM success_payments WHERE date = ?", (today_date,))
            result = self.cursor.fetchone()[0]
            return result if result else 0

    def get_total_profit(self):
        """Get the total profit from successful payments."""
        self.cursor.execute("SELECT SUM(sum) FROM success_payments")
        result = self.cursor.fetchone()[0]
        return result if result else 0
    
    def is_admin(self, user_id):
        """Check if a user is an admin."""
        with self.conn:
            res = self.cursor.execute("SELECT admin FROM user WHERE user_id = ?", (user_id,)).fetchone()
            return bool(res[0]) if res else False
        
    def get_req(self):
        """Get the current bank request if active."""
        with self.conn:
            res = self.cursor.execute("SELECT req FROM bank_req WHERE status = 1").fetchone()
            return str(res[0]) if res else None
