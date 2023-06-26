import random
import pygame
from itertools import groupby
total_pay = 0
JACKPOT = 10000.0
symbols = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Ace', 'Jack', 'Queen', 'King', 'Joker']
bet_size = [0.20, 0.50, 1, 2, 5, 10, 20, 50, 100, 200]
paylines = [
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
payouts = {
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
symbol_weights = {symbol: 1 / max(payout.values() if payout else [1]) for symbol, payout in payouts.items() if symbol != 'Ace'}

symbol_weights['Ace'] = (symbol_weights['Queen'] + symbol_weights['Jack']) / 2.25
symbol_weights['Joker'] = (symbol_weights['King'] + symbol_weights['Queen']) / 2.25

total_weight = sum(symbol_weights.values())
symbol_weights = {symbol: weight / total_weight for symbol, weight in symbol_weights.items()}

weighted_symbols = [symbol for symbol, weight in symbol_weights.items() for _ in range(int(weight * 10000))]

WIDTH, HEIGHT = 1600, 900
SYMBOL_WIDTH, SYMBOL_HEIGHT = 100, 140
GAP = 20
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 24)
window = pygame.display.set_mode((WIDTH, HEIGHT))
images = {symbol: pygame.transform.scale(pygame.image.load(symbol + '.png').convert_alpha(), (SYMBOL_WIDTH, SYMBOL_HEIGHT)) for symbol in symbols}


class Button:
    def __init__(self, x, y, width, height, color, text='', text_color=(255,255,255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        if self.text != '':
            font = pygame.font.Font(None, 50)
            text = font.render(self.text, True, self.text_color)
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


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

    def spin(self):

        if self.balance < self.bet_size:
            return

        self.balance -= self.bet_size
        self.reels = []
        for _ in range(3):
            row = []
            for i in range(5):
                if i <= 2 and 'Joker' in row:
                    self.joker_multiplier *= 1.5
                    self.weighted_symbols = [symbol for symbol, weight in symbol_weights.items()
                                             for _ in range(int(weight * 10000 * (self.joker_multiplier if symbol == 'Joker' else 1)))]
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
                print(f"Winning payline: {symbols_in_line}\n{payline}")
                winning_lines.append(symbols_in_line)
            total_payout += payout

        self.balance += total_payout

        print("Reels:")
        for row in self.reels:
            print(row)
        print(f"Total payout: {total_payout}")
        print(f"Balance: {self.balance}")

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

    def bonus(self, bonus_spins):
        global total_pay
        print(f"Bonus activated!")
        multi = 1
        bonus_symbols = ['Ace', '2', '5', '10', 'Jack', 'Queen', 'King', 'Joker']
        bonus_payouts = {
            'Joker': 500,
            'King': 250,
            'Queen': 50,
            'Jack': 25,
            '10': 10,
            '5': 5,
            '2': 2,
            'Ace': 1
        }
        pygame.font.init()
        font = pygame.font.SysFont(None, 24)
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        images = {symbol: pygame.transform.scale(pygame.image.load(symbol + '.png').convert_alpha(),
                                                 (SYMBOL_WIDTH, SYMBOL_HEIGHT)) for symbol in bonus_symbols}
        spin_button = Button(WIDTH - 200, HEIGHT // 2, 100, 50, (0, 255, 0), 'SPIN')
        spin_button.draw(window)
        pygame.display.update()
        running = True
        while running and bonus_spins >= 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if spin_button.is_over(pos):
                        bonus_weights = {symbol: 1 / bonus_payouts[symbol] for symbol in bonus_symbols}
                        total_weight = sum(bonus_weights.values())
                        bonus_weights = {symbol: weight / total_weight for symbol, weight in bonus_weights.items()}
                        weighted_bonus_symbols = [symbol for symbol, weight in bonus_weights.items() for _ in
                                                  range(int(weight * 10000))]
                        result = []
                        bonus_text = font.render("Bonus Spins Left: " + str(bonus_spins) + "    Multiplier: " + str(multi) + "x", True, (255, 255, 255))
                        window.fill((0, 0, 0))
                        window.blit(bonus_text, (10, 10))
                        spin_button.draw(window)
                        pygame.display.update()
                        total_content_width = (3 * GAP) + (3 * SYMBOL_WIDTH)
                        total_content_height = (3 * GAP) + (3 * SYMBOL_HEIGHT)
                        start_x = (WIDTH // 2) - (total_content_width // 2)
                        start_y = (HEIGHT // 2) - (total_content_height // 2)

                        for i in range(3):
                            symbol = random.choice(weighted_bonus_symbols)
                            result.append(symbol)
                            x = start_x + i * (SYMBOL_WIDTH + GAP)
                            y = start_y
                            window.blit(images[symbol], (x, y))
                            if i == 0:
                                bonus_weights[symbol] *= 2
                            if i == 1:
                                bonus_weights[symbol] *= 2
                            total_weight = sum(bonus_weights.values())
                            bonus_weights = {symbol: weight / total_weight for symbol, weight in bonus_weights.items()}
                            weighted_bonus_symbols = [symbol for symbol, weight in bonus_weights.items() for _ in
                                                      range(int(weight * 10000))]
                        bonus_spins -= 1
                        if result[0] == result[1] == result[2]:
                            if result[0] == 'Joker':
                                total_pay += JACKPOT
                                self.balance += JACKPOT
                                win_text = font.render("You Won " + str(JACKPOT) + " !", True, (255, 255, 255))
                                window.blit(win_text, ((WIDTH // 2) - 75, 10))
                                JACKPOT = 10000.
                            else:
                                win = bonus_payouts[result[0]] * multi * self.bet_size
                                total_pay += win
                                self.balance += win
                                win_text = font.render("You Won " + str(win) + " !", True, (255, 255, 255))
                                window.blit(win_text, ((WIDTH // 2) - 75, 10))
                                multi += 1
                                if multi > 5:
                                    multi = 5

                        pygame.display.flip()
                        result.clear()


chosen_balance = 1000
chosen_bet_size = 10
slot_machine = SlotMachine(symbols, paylines, payouts, balance=chosen_balance, bet_size=chosen_bet_size, weighted_symbols=weighted_symbols)
spin_button = Button(WIDTH - 150, HEIGHT-100, 100, 50, (0, 255, 0), 'SPIN')
quit_button = Button(50, HEIGHT-100, 100, 50, (255, 0, 0), 'QUIT')
bet_size_buttons = [Button(WIDTH/2 + i*60 - (len(bet_size)*60)/2, HEIGHT - 50, 50, 30, (0, 0, 255), str(bet)) for i, bet in enumerate(bet_size)]
for button in bet_size_buttons:
    button.draw(window)
spin_button.draw(window)
quit_button.draw(window)
pygame.display.update()

return_pressed = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if quit_button.is_over(pos):
                pygame.quit()

            for i, button in enumerate(bet_size_buttons):
                if button.is_over(pos):
                    slot_machine.bet_size = bet_size[i]

            if spin_button.is_over(pos):
                JACKPOT += 0.01 * float(chosen_bet_size)
                payout, winning_lines = slot_machine.spin()

                balance_text = font.render("Balance: " + str(round(slot_machine.balance)), True, (255, 255, 255))
                jackpot_text = font.render("Jackpot: " + str(round(JACKPOT, 2)), True, (255, 255, 255))
                window.fill((0, 0, 0))
                window.blit(balance_text, (10, 10))
                window.blit(jackpot_text, (750, 10))
                spin_button.draw(window)
                quit_button.draw(window)
                for button in bet_size_buttons:
                    button.draw(window)
                pygame.display.update()

                total_content_width = len(slot_machine.reels[0]) * SYMBOL_WIDTH + (len(slot_machine.reels[0]) - 1) * GAP
                total_content_height = len(slot_machine.reels) * SYMBOL_HEIGHT + (len(slot_machine.reels) - 1) * GAP

                start_x = (WIDTH - total_content_width) // 2
                start_y = (HEIGHT - total_content_height) // 2

                for i, row in enumerate(slot_machine.reels):
                    for j, symbol in enumerate(row):
                        # Calculate the position for the symbol
                        x = start_x + j * (SYMBOL_WIDTH + GAP)
                        y = start_y + i * (SYMBOL_HEIGHT + GAP)
                        window.blit(images[symbol], (x, y))

                prev_window = window.copy()
                win_count = len(winning_lines)
                if win_count > 0:
                    window.fill((0, 0, 0))
                    for i, payline in enumerate(winning_lines):
                        for j, symbol in enumerate(payline):
                            x = start_x + j * (SYMBOL_WIDTH + GAP)
                            y = start_y + i * (SYMBOL_HEIGHT + GAP)
                            window.blit(images[symbol], (x, y-100))

                    pay_text = font.render("YOU WON $" + str(payout) + "!", True, (255, 255, 255))
                    window.blit(pay_text, (750, HEIGHT - 100))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    window.blit(prev_window, (0, 0))
                    pygame.display.update()

                pygame.display.flip()
                joker_count = 0
                for row in slot_machine.reels:
                    for symbol in row:
                        if symbol == 'Joker':
                            joker_count += 1

                if joker_count in [3, 4, 5]:

                    font = pygame.font.Font(None, 36)
                    text = font.render('Bonus Game Activated', True, (255, 255, 255), (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (WIDTH // 2, HEIGHT // 2)

                    window.blit(text, textRect)
                    pygame.display.flip()
                    pygame.time.delay(2000)

                    window.fill((0, 0, 0))
                    bonus_rules = ["In order to win all 3 cards must be the same.", "With each win the multiplier is increased by 1x(excludes Jackpot)", "Ace = 1x, 2 = 2x, 5 = 5x, 10 = 10x, Jack = 25x, Queen = 50x, King = 250x, Joker = JACKPOT"]
                    for i, rule in enumerate(bonus_rules):
                        rule_text = font.render(rule, True, (255, 255, 255), (0, 0, 0))
                        rule_text_rect = rule_text.get_rect()
                        rule_text_rect.center = (WIDTH // 2, HEIGHT // 2 + i * 40)  # Adjust the y-value as needed
                        window.blit(rule_text, rule_text_rect)

                    pygame.display.flip()
                    ready_button = Button((WIDTH // 2)-100, HEIGHT - 200, 200, 100, (0, 255, 0), 'READY')
                    ready_button.draw(window)
                    pygame.display.update()

                    bonus_ready = False
                    while not bonus_ready:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                bonus_ready = True
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                if ready_button.is_over(pos):
                                    if joker_count == 5:
                                        slot_machine.bonus(15)
                                    if joker_count == 4:
                                        slot_machine.bonus(12)
                                    if joker_count == 3:
                                        slot_machine.bonus(10)
                                    bonus_ready = True

                    window.fill((0, 0, 0))
                    spin_button.draw(window)
                    quit_button.draw(window)
                    pygame.display.update()
                    text = font.render('Total Bonus Win: $' + str(total_pay) + "!", True, (255, 255, 255), (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (WIDTH // 2, HEIGHT // 2)
                    window.blit(text, textRect)
                    total_pay = 0
                    pygame.display.flip()

pygame.quit()
