import sqlite3
import os
your_path = ''
your_databse_name = '.db'
class SQL_Util:
    def __init__(self, x):
        self.db_path = os.path.join({your_path}, your_databse_name)
        self.user_id = x

    def user_validation(self):
        there = None
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM users WHERE user_id = ?", (self.user_id,)) 
            data = c.fetchone()
            if data is not None:
                there = True
            else:
                there = False
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            there = False
        finally:
            conn.close()

        return there
    
    def get_user_balance(self):
        bal = None
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("SELECT balance FROM users WHERE user_id=?", (self.user_id,))
            data = c.fetchone()
            if data is None:
                bal = None
            else:
                bal = data[0]
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            bal = None
        finally:
            conn.close()

        return bal
    
    def change_user_balance(self, x):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (x, self.user_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
        finally:
            conn.close()
