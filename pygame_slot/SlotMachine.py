import random
from itertools import groupby


class SlotMachine:
    def __init__(self, symbols, paylines, payouts, balance, bet_size, weighted_symbols):
        self.symbols = symbols
        self.paylines = paylines
        self.payouts = payouts
        self.balance = balance
        self.bet_size = bet_size
        self.weighted_symbols = weighted_symbols
        self.joker_multiplier = 1
        self.reels = []
        self.joker_count = self.weighted_symbols.count('Joker') / len(self.weighted_symbols)

    def spin(self):

        if self.balance < self.bet_size:
            return

        self.balance -= self.bet_size
        self.reels = []
        for _ in range(3):
            row = []
            for i in range(5):
                joker_chance = 0
                if i <= 3 and 'Joker' in row:
                    self.joker_multiplier *= 1.75
                    joker_chance = self.joker_count * self.joker_multiplier
                if random.random() < joker_chance:
                    symbol = 'Joker'
                else:
                    symbol = random.choice(self.weighted_symbols)
                row.append(symbol)
            self.reels.append(row)
        self.joker_multiplier = 1

        total_payout = 0
        winning_lines = []

        for payline in self.paylines:
            symbols_in_line = [self.reels[coord[0]][coord[1]] for coord in payline]
            payout = self.check_payout(symbols_in_line)
            if payout > 0:
                winning_lines.append(symbols_in_line)
            total_payout += payout

        self.balance += total_payout

        return total_payout, winning_lines

    def check_payout(self, symbols):
        if symbols.count('Ace') > 0:
            filtered_symbols = [s for s in set(symbols) if s not in ['Ace', 'Joker']]
            if filtered_symbols:
                most_common_symbol = max(filtered_symbols, key=symbols.count)
            else:
                most_common_symbol = None

            symbols = [symbol if symbol != 'Ace' else most_common_symbol for symbol in symbols]

        groups = [(symbol, len(list(group))) for symbol, group in groupby(symbols)]

        if groups[0][0] != symbols[0]:
            return 0

        symbol, count = groups[0]

        return self.payouts.get(symbol, {}).get(count, 0) * self.bet_size