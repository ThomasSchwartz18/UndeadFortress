import random
import pygame

class MaterialsCounter:
    def __init__(self):
        self.food = 0
        self.ammo = 0
        self.scrap = 0

    def add_material(self, material_type):
        """Increase the count for the collected material."""
        if material_type == 'food':
            self.food += self.get_random_food()
        elif material_type == 'ammo':
            self.ammo += self.get_random_ammo()
        elif material_type == 'scrap':
            self.scrap += self.get_random_scrap()

    def get_random_food(self):
        """Generate a random amount of food with decreasing probability."""
        food_values = list(range(20, 101))  # Food drop range: 20-100
        weights = [100 - i for i in range(81)]  # Decreasing probability for higher values
        return random.choices(food_values, weights)[0]

    def get_random_ammo(self):
        """Generate a random amount of ammo with decreasing probability."""
        ammo_values = list(range(10, 21))  # Ammo drop range: 10-20
        weights = [21 - i for i in range(11)]  # Decreasing probability for higher values
        return random.choices(ammo_values, weights)[0]

    def get_random_scrap(self):
        """Generate a random amount of scrap with decreasing probability."""
        scrap_values = list(range(70, 101))  # Scrap drop range: 70-100
        weights = [101 - i for i in range(70, 101)]  # Decreasing probability for higher values
        return random.choices(scrap_values, weights)[0]

    def draw(self, surface, x, y, player_speed):
        """Draw the materials counter and player speed on the screen."""
        font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 20)
        food_text = font.render(f"Food: {self.food}", True, (0, 0, 0))
        ammo_text = font.render(f"Ammo: {self.ammo}", True, (0, 0, 0))
        scrap_text = font.render(f"Scrap: {self.scrap}", True, (0, 0, 0))
        speed_text = font.render(f"Speed: {player_speed:.1f} m/s", True, (0, 0, 0))

        # Display each material in a column
        surface.blit(food_text, (x, y))
        surface.blit(ammo_text, (x, y + 30))  # Offset for the next item
        surface.blit(scrap_text, (x, y + 60))  # Further offset
        surface.blit(speed_text, (x, y + 90))  # Show speed below scrap counter

