from flask import Flask, jsonify, request
from sqlite_db import SQL_Util
from server_settings import set_routes
from slot_machine import set_reels
""" 
07.01  -  When server.py is updated the front-end spins the same reel until it breaks and the user is forced to login again
    Test Key: y12p0EyLeqKWc6N
"""

class GameInstance:
    def __init__(self):
        self.app = Flask(__name__)
        set_routes(self.app, self)
        self.bet_size = 1

    def get_balance(self):
        self.balance = self.user_sql.get_user_balance()
        return jsonify(self.balance)
    
    def get_jackpot(self):
        self.jackpot = self.user_sql.ret_jackpot_val()
        return jsonify(self.jackpot)
    
    def get_reels(self):
        self.balance, self.jackpot = self.balance - self.bet_size, self.jackpot + (0.01 * self.bet_size)
        self.user_sql.change_user_balance(self.balance), self.user_sql.change_jackpot_val(self.jackpot)
        return jsonify(set_reels())
    
    def login(self):
        self.user_sql = SQL_Util(request.get_json().get('user_id'))
        self.jackpot, self.balance = self.user_sql.ret_jackpot_val(), self.user_sql.get_user_balance()
        return jsonify({'success': self.user_sql.user_validation()})


if __name__ == "__main__":
    user = GameInstance()
    user.app.run(debug=True)
