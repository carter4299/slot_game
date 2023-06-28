import random
import pygame
from Settings import Settings
from Button import Button
from SlotMachine import SlotMachine


class SlotGame:
    def __init__(self):
        self.settings = Settings()
        self.deck = []
        self.bonus_deck = []
        self.spin_button = None
        self.quit_button = None
        self.bet_size_buttons = []
        self.bet_size = 1
        self.JACKPOT = 10000.0
        self.balance = 1000
        self.bonus_win = 0
        self.WIDTH, self.HEIGHT = 1600, 900
        self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT = 100, 140
        self.GAP = 20
        self.font = pygame.font.SysFont(None, 24)
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.images = {
            symbol: pygame.transform.scale(pygame.image.load(symbol + '.png').convert_alpha(),
                                           (self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT)) for symbol in self.settings.symbols
        }

    def fill_deck(self):
        symbol_weights = {
            symbol: 1 / max(payout.values() if payout else [1]) for symbol,
            payout in self.settings.payouts.items() if symbol != 'Ace'
        }
        
        symbol_weights['Ace'] = (symbol_weights['Queen'] + symbol_weights['Jack']) / 2.25
        symbol_weights['Joker'] = (symbol_weights['King'] + symbol_weights['Queen']) / 2.25
        total_weight = sum(symbol_weights.values())
        symbol_weights = {symbol: weight / total_weight for symbol, weight in symbol_weights.items()}

        self.deck = [symbol for symbol, weight in symbol_weights.items() for _ in range(int(weight * 100000))]

    def fill_bonus_deck(self):
        bonus_weights = {
            symbol: 1 / self.settings.bonus_odds[symbol] for symbol in self.settings.bonus_symbols
        }

        total_weight = sum(bonus_weights.values())
        bonus_weights = {symbol: weight / total_weight for symbol, weight in bonus_weights.items()}
        
        self.bonus_deck = [symbol for symbol, weight in bonus_weights.items() for _ in range(int(weight * 10000))]

    def draw_buttons(self):
        self.spin_button = Button(self.WIDTH - 150, self.HEIGHT - 100, 100, 50, (0, 255, 0), 'SPIN')
        self.quit_button = Button(50, self.HEIGHT - 100, 100, 50, (255, 0, 0), 'QUIT')
        self.bet_size_buttons = [
            Button(self.WIDTH / 2 + i * 60 - (len(self.settings.bet_size) * 60) / 2,
                   self.HEIGHT - 50, 50, 30, (0, 0, 255),
                   str(bet)) for i, bet in enumerate(self.settings.bet_size)
        ]
        
        for button in self.bet_size_buttons:
            button.draw(self.window)
        self.spin_button.draw(self.window)
        self.quit_button.draw(self.window)
        
        pygame.display.update()

    def bonus(self, bonus_spins):
        multi = 1
        pygame.font.init()
        font = pygame.font.SysFont(None, 24)
        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        images = {
            symbol: pygame.transform.scale(pygame.image.load(symbol + '.png').convert_alpha(),
            (self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT)) for symbol in self.settings.bonus_symbols
        }
        spin_button = Button(self.WIDTH - 200, self.HEIGHT // 2, 100, 50, (0, 255, 0), 'SPIN')
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
                        result = []
                        bonus_text = font.render("Bonus Spins Left: " + str(bonus_spins) + "    Multiplier: "
                                                 + str(multi) + "x", True, (255, 255, 255))
                        window.fill((0, 0, 0))
                        window.blit(bonus_text, (10, 10))
                        spin_button.draw(window)
                        pygame.display.update()
                        total_content_width = (3 * self.GAP) + (3 * self.SYMBOL_WIDTH)
                        total_content_height = (3 * self.GAP) + (3 * self.SYMBOL_HEIGHT)
                        start_x = (self.WIDTH // 2) - (total_content_width // 2)
                        start_y = (self.HEIGHT // 2) - (total_content_height // 2)

                        repeater_bonus = 0
                        for i in range(3):
                            symbol = random.choice(self.bonus_deck)
                            if i == 0:
                                repeater_bonus = (self.bonus_deck.count(symbol) / len(self.bonus_deck)) * 2
                            if i == 1 and symbol == result[0]:
                                repeater_bonus *= 2

                            if random.random() < repeater_bonus and i != 0:
                                symbol = result[0]

                            result.append(symbol)

                            x = start_x + i * (self.SYMBOL_WIDTH + self.GAP)
                            y = start_y
                            window.blit(images[symbol], (x, y))
                        bonus_spins -= 1
                        
                        if result[0] == result[1] == result[2]:
                            if result[0] == 'Joker':
                                self.bonus_win += self.JACKPOT
                                self.balance += self.JACKPOT
                                
                                win_text = font.render("You Won " + str(self.JACKPOT) + " !", True, (255, 255, 255))
                                window.blit(win_text, ((self.WIDTH // 2) - 75, 10))
                                
                                self.JACKPOT = 10000.
                            else:
                                win = self.settings.bonus_payouts[result[0]] * multi * self.bet_size
                                self.bonus_win += win
                                self.balance += win
                                
                                win_text = font.render("You Won " + str(win) + " !", True, (255, 255, 255))
                                window.blit(win_text, ((self.WIDTH // 2) - 75, 10))
                                multi += 1
                                if multi > 5:
                                    multi = 5

                        pygame.display.flip()
                        result.clear()

    def run_game(self):
        self.fill_deck()
        self.fill_bonus_deck()
        self.draw_buttons()
        slot_machine = SlotMachine(
            self.settings.symbols, self.settings.paylines, self.settings.payouts, balance=self.balance,
            bet_size=self.bet_size, weighted_symbols=self.deck
        )
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.quit_button.is_over(pos):
                        pygame.quit()

                    for i, button in enumerate(self.bet_size_buttons):
                        if button.is_over(pos):
                            self.bet_size = self.settings.bet_size[i]
                            slot_machine.bet_size = self.bet_size

                    if self.spin_button.is_over(pos):
                        self.JACKPOT += 0.01 * float(self.bet_size)
                        payout, winning_lines = slot_machine.spin()

                        balance_text = self.font.render("Balance: " + str(round(slot_machine.balance)), True,
                                                        (255, 255, 255))
                        jackpot_text = self.font.render("Jackpot: " + str(round(self.JACKPOT, 2)), True,
                                                        (255, 255, 255))
                        self.window.fill((0, 0, 0))
                        self.window.blit(balance_text, (10, 10))
                        self.window.blit(jackpot_text, (750, 10))
                        self.spin_button.draw(self.window)
                        self.quit_button.draw(self.window)
                        for button in self.bet_size_buttons:
                            button.draw(self.window)
                            
                        pygame.display.update()

                        total_content_width = len(slot_machine.reels[0]) * self.SYMBOL_WIDTH + \
                                              (len(slot_machine.reels[0]) - 1) * self.GAP
                        total_content_height = len(slot_machine.reels) * self.SYMBOL_HEIGHT + \
                                               (len(slot_machine.reels) - 1) * self.GAP

                        start_x = (self.WIDTH - total_content_width) // 2
                        start_y = (self.HEIGHT - total_content_height) // 2

                        for i, row in enumerate(slot_machine.reels):
                            for j, symbol in enumerate(row):
                                # Calculate the position for the symbol
                                x = start_x + j * (self.SYMBOL_WIDTH + self.GAP)
                                y = start_y + i * (self.SYMBOL_HEIGHT + self.GAP)
                                self.window.blit(self.images[symbol], (x, y))

                        prev_window = self.window.copy()
                        
                        win_count = len(winning_lines)
                        if win_count > 0:
                            self.window.fill((0, 0, 0))
                            for i, payline in enumerate(winning_lines):
                                for j, symbol in enumerate(payline):
                                    x = start_x + j * (self.SYMBOL_WIDTH + self.GAP)
                                    y = start_y + i * (self.SYMBOL_HEIGHT + self.GAP)
                                    self.window.blit(self.images[symbol], (x, y - 100))

                            pay_text = self.font.render("YOU WON $" + str(payout) + "!", True, (255, 255, 255))
                            self.window.blit(pay_text, (750, self.HEIGHT - 100))
                            pygame.display.update()
                            pygame.time.delay(2000)
                            self.window.blit(prev_window, (0, 0))
                            
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
                            textRect.center = (self.WIDTH // 2, self.HEIGHT // 2)

                            self.window.blit(text, textRect)
                            pygame.display.flip()
                            pygame.time.delay(2000)

                            self.window.fill((0, 0, 0))
                            bonus_rules = ["In order to win all 3 cards must be the same.",
                                           "With each win the multiplier is increased by 1x(excludes Jackpot)",
                                           "Ace = 1x, 2 = 2x, 5 = 5x, 10 = 10x, Jack = 25x, Queen = 50x, King = 250x, Joker = JACKPOT"]
                            for i, rule in enumerate(bonus_rules):
                                rule_text = font.render(rule, True, (255, 255, 255), (0, 0, 0))
                                rule_text_rect = rule_text.get_rect()
                                rule_text_rect.center = (
                                    self.WIDTH // 2, self.HEIGHT // 2 + i * 40)  # Adjust the y-value as needed
                                self.window.blit(rule_text, rule_text_rect)

                            pygame.display.flip()
                            ready_button = Button((self.WIDTH // 2) - 100, self.HEIGHT - 200, 200, 100, (0, 255, 0),
                                                  'READY')
                            ready_button.draw(self.window)
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
                                                self.bonus(15)
                                            if joker_count == 4:
                                                self.bonus(12)
                                            if joker_count == 3:
                                                self.bonus(10)
                                            bonus_ready = True

                            self.window.fill((0, 0, 0))
                            self.spin_button.draw(self.window)
                            self.quit_button.draw(self.window)
                            pygame.display.update()
                            text = font.render('Total Bonus Win: $' + str(self.bonus_win) + "!", True, (255, 255, 255),
                                               (0, 0, 0))
                            textRect = text.get_rect()
                            textRect.center = (self.WIDTH // 2, self.HEIGHT // 2)
                            self.window.blit(text, textRect)
                            self.bonus_win = 0
                            pygame.display.flip()


def start_game():
    pygame.init()
    pygame.font.init()


def end_game():
    pygame.quit()


if __name__ == "__main__":
    start_game()
    slot = SlotGame()
    slot.run_game()
    end_game()


