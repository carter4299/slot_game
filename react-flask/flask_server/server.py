from flask import Flask, jsonify, request
import numpy as np
import random
from sqlite_db import SQL_Util

"""
needed fixes: if server.py is altered then saved  |  self.user_sql.get_user_balance() -> AttributeError: 'NoneType' object has no attribute 'get_user_balance'
    another GameInstance is loaded where self.user_sql = None
    the user_id is gathered only when user enters game using 'login', since the balance is updated in 'get_reels' 'login' is never called
    after server.py the user can keep spinning but it will make no changes to their account

        'reshuffle' still works after updating server.py
"""

class GameInstance:
    def __init__(self):
        """ initiate app  | initiate user_id  |   intiate balance  |  initiate deck ( np.array ), then fill it  """
        self.app = Flask(__name__)
        self.user_id = ''
        self.balance = 0
        self.user_sql = None
        self.bet_size = 1
        self.card_img_names = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        self.probabilities = np.array([0.13326752221125374, 0.13326752221125374, 0.13326752221125374, 0.08884501480750248,
                          0.08884501480750248, 0.08884501480750248, 0.06663376110562687, 0.06663376110562687,
                          0.06663376110562687, 0.04442250740375124, 0.026653504442250744, 0.013326752221125372,
                          0.031589338598223105, 0.017769002961500496])
        self.deck = self.reshuffle_deck()
        """ App Routes """
        self.app.add_url_rule('/reels', 'get_reels', self.get_reels)
        self.app.add_url_rule('/reshuffle', 'reshuffle', self.reshuffle, methods=['POST'])
        self.app.add_url_rule('/get_balance', 'get_balance', self.get_balance)
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST'])

        self.reshuffle_deck()

    def get_reels(self):
        """ selects 15 + 10*i random cards from deck and returns list as dtype json, See 'App.js' 
        extra game rule: if a card lands on joker, it increases the chances of getting another joker"""
        self.balance -= self.bet_size
        self.user_sql.change_user_balance(self.balance)
        reels  = []
        flag = False
        joker_chance = 0
        for i in range(5):
            reel = np.random.choice(list(self.deck), size=(15 + (10 * i))).tolist()
            for i in range(3):
                if reel[-(i+1)] == 14:
                    if flag == False:
                        joker_chance = self.probabilities[13] * 1.5
                        flag = True
                    else:
                        joker_chance *= 1.5
                elif random.random() < joker_chance:
                    reel[-(i+1)] = 14
            reels.append(reel)
        return jsonify(reels)

    def reshuffle_deck(self):
        """ Fills intitial deck, then reshuffles every 10 min to provide new probabilites """
        self.deck = np.random.choice(self.card_img_names, p=self.probabilities, size=100000)

    def reshuffle(self):
        """ Post method to reshuffle when called from App.js """
        self.reshuffle_deck()
        return jsonify({'success': True})

    def get_balance(self):
        """ Return user balance to useGameLogic.js """
        self.balance = self.user_sql.get_user_balance()
        return jsonify(self.balance)
    
    def login(self):
        """ Fetch user balance based on user_id """
        data = request.get_json()
        self.user_id = data.get('user_id')
        self.user_sql = SQL_Util(self.user_id)
        self.balance = self.user_sql.get_user_balance()
        return jsonify({'success': self.user_sql.user_validation()})

    def start_run(self):
        """ Start app and create deck """
        self.app.run(debug=True)



if __name__ == "__main__":
    user = GameInstance()
    user.start_run()
