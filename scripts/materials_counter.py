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

    def calculate_dps(self, fire_rate, damage_per_shot):
        """Calculate the average damage per second (DPS) the player is outputting."""
        return fire_rate * damage_per_shot

    def draw(self, surface, x, y, speed, fire_rate, damage, dps, sps, accuracy_offset):
        """Draw the materials, SPS, and accuracy range on the screen."""
        font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 24)
        
        # Draw materials (food, ammo, scrap) below the accuracy information
        food_text = font.render(f"Food: {self.food}", True, (255, 255, 255))
        ammo_text = font.render(f"Ammo: {self.ammo}", True, (255, 255, 255))
        scrap_text = font.render(f"Scrap: {self.scrap}", True, (255, 255, 255))

        # Display materials on the screen
        surface.blit(food_text, (x, y + 180))
        surface.blit(ammo_text, (x, y + 210))
        surface.blit(scrap_text, (x, y + 240))
            
        # Draw Speed, Fire Rate, Damage, DPS, SPS
        speed_text = font.render(f"Speed: {speed:.2f}", True, (255, 255, 255))
        fire_rate_text = font.render(f"Fire Rate: {fire_rate:.2f}", True, (255, 255, 255))
        damage_text = font.render(f"Damage: {damage}", True, (255, 255, 255))
        dps_text = font.render(f"DPS: {dps}", True, (255, 255, 255))
        sps_text = font.render(f"SPS: {sps}", True, (255, 255, 255))
        
        # Calculate the accuracy range (e.g., ±accuracy_offset)
        accuracy_range = f"Accuracy Range: ±{accuracy_offset:.2f}"

        # Render all text onto the screen
        surface.blit(speed_text, (x, y))
        surface.blit(fire_rate_text, (x, y + 30))
        surface.blit(damage_text, (x, y + 60))
        surface.blit(dps_text, (x, y + 90))
        surface.blit(sps_text, (x, y + 120))

        # Display the accuracy range below the SPS value
        accuracy_text = font.render(accuracy_range, True, (255, 255, 255))
        surface.blit(accuracy_text, (x, y + 150))





