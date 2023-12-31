class Settings:
    def __init__(self):
        self.paylines = [
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
            [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],
            [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],
            [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],
            [(1, 0), (0, 1), (0, 2), (0, 3), (1, 4)],
            [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)],
            [(1, 0), (1, 1), (0, 2), (1, 3), (1, 4)],
        ]
        self.payouts = {
            'Joker': {},
            'King': {5: 200, 4: 20, 3: 10},
            'Queen': {5: 100, 4: 16, 3: 8},
            'Jack': {5: 60, 4: 12, 3: 6},
            '10': {5: 40, 4: 8, 3: 3},
            '9': {5: 40, 4: 8, 3: 3},
            '8': {5: 40, 4: 8, 3: 3},
            '7': {5: 30, 4: 6, 3: 2},
            '6': {5: 30, 4: 6, 3: 2},
            '5': {5: 30, 4: 6, 3: 2},
            '4': {5: 20, 4: 4, 3: 1},
            '3': {5: 20, 4: 4, 3: 1},
            '2': {5: 20, 4: 4, 3: 1},
            'Ace': {}
        }
        self.symbols = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Ace', 'Jack', 'Queen', 'King', 'Joker']
        self.bet_size = [0.20, 0.50, 1, 2, 5, 10, 20, 50, 100, 200]
        self.bonus_symbols = ['Ace', '2', '5', '10', 'Jack', 'Queen', 'King', 'Joker']
        self.bonus_payouts = {
            'Joker': 100,
            'King': 75,
            'Queen': 50,
            'Jack': 25,
            '10': 10,
            '5': 5,
            '2': 2,
            'Ace': 1
        }
        self.bonus_odds = {
            'Joker': 75,
            'King': 50,
            'Queen': 25,
            'Jack': 10,
            '10': 5,
            '5': 2,
            '2': 1,
            'Ace': 1
        }