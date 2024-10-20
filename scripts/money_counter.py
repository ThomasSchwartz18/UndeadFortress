# money_counter.py

import pygame

class MoneyCounter:
    def __init__(self, initial_money=0, money_per_kill=10):
        self.money = initial_money
        self.money_per_kill = money_per_kill
        self.font = pygame.font.Font(None, 36)
        
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)

    def add_money(self):
        """Increase the money for each zombie kill."""
        self.money += self.money_per_kill

    def draw(self, surface, x, y):
        """Draw the money counter on the screen at the specified position."""
        money_text = self.font.render(f"Money: ${self.money}", True, (0, 0, 0))
        surface.blit(money_text, (x, y))
