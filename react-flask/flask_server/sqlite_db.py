import sqlite3
import os

class SQL_Util:
    def __init__(self, x):
        self.db_path = os.path.join(r'C:\Users\-----\OneDrive\Desktop\---------------', '------------')
        self.user_id = x

    def execute_query(self, query, values=None):
        result = None
        with sqlite3.connect(self.db_path) as conn:
            try:
                c = conn.cursor()
                if values:
                    c.execute(query, values)
                else:
                    c.execute(query)
                conn.commit()
                result = c.fetchone()
            except sqlite3.Error as e:
                print(f"An error occurred: {e.args[0]}")
        return result

    def user_validation(self):
        data = self.execute_query("SELECT * FROM users WHERE user_id = ?", (self.user_id,))
        return bool(data)

    def get_user_balance(self):
        data = self.execute_query("SELECT balance FROM users WHERE user_id=?", (self.user_id,))
        return data[0] if data else None

    def change_user_balance(self, x):
        self.execute_query("UPDATE users SET balance = ? WHERE user_id = ?", (x, self.user_id))

    def change_jackpot_val(self, val):
        self.execute_query("UPDATE curr_jackpot SET value = ?", (val,))

    def ret_jackpot_val(self):
        data = self.execute_query("SELECT value FROM curr_jackpot")
        return data[0] if data else None

