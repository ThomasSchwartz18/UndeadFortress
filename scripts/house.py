import pygame
import time

class House:
    def __init__(self):
        # Basic properties of the house
        self.base_size = 200
        self.health = 100  # Current health of the house
        self.max_health = 100  # Maximum health

        # Load the house image
        try:
            self.house_image = pygame.image.load('assets/starterhouseIMG.png').convert_alpha()
            self.house_image = pygame.transform.scale(self.house_image, (self.base_size, self.base_size))
        except pygame.error as e:
            print(f"Unable to load house image: {e}")
            self.house_image = pygame.Surface((self.base_size, self.base_size))
            self.house_image.fill((100, 100, 100))  # Default to grey if image not found

        # Load rubble image (replace with an actual rubble image if available)
        self.rubble_image = pygame.Surface((self.base_size, self.base_size))
        self.rubble_image.fill((139, 69, 19))  # Brown color to represent rubble

        # Time tracking for house health regeneration (Engineer)
        self.last_health_regen_time = time.time()

    def take_damage(self, damage):
        """Reduce the house's health."""
        self.health -= damage
        if self.health < 0:
            self.health = 0  # Prevent health from going negative

    def is_destroyed(self):
        """Check if the house is destroyed."""
        return self.health <= 0

    def repair(self, amount):
        """Repair the house by increasing health."""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health  # Ensure it doesn't exceed max health

    def engineer_repair(self):
        """For Engineer: Regenerate house health over time based on Building Regen Rate."""
        current_time = time.time()
        if current_time - self.last_health_regen_time >= 3:
            if self.health < self.max_health:
                self.health += self.building_regen_rate  # Use the building regen rate
                if self.health > self.max_health:
                    self.health = self.max_health
            self.last_health_regen_time = current_time

    def draw(self, surface, zoom_level, screen_width, screen_height):
        """Draw the house or rubble on the given surface."""
        # Scale the house based on the zoom level
        scaled_size = int(self.base_size * zoom_level)
        house_x = (screen_width // 2) - (scaled_size // 2)
        house_y = (screen_height // 2) - (scaled_size // 2)

        if self.is_destroyed():
            # Draw rubble when the house is destroyed
            scaled_rubble = pygame.transform.scale(self.rubble_image, (scaled_size, scaled_size))
            surface.blit(scaled_rubble, (house_x, house_y))
        else:
            # Draw the house image
            scaled_house = pygame.transform.scale(self.house_image, (scaled_size, scaled_size))
            surface.blit(scaled_house, (house_x, house_y))

    def draw_health_bar_bottom(self, surface, screen_width, screen_height):
        """Draw the house's health bar across the bottom of the screen."""
        bar_height = 30
        health_bar_width = int((self.health / self.max_health) * screen_width)

        # Create a transparent surface for the health bar
        bar_surface = pygame.Surface((screen_width, bar_height), pygame.SRCALPHA)
        bar_surface.fill((255, 0, 0, 150))  # Red with 150 alpha for transparency

        # Foreground (Green) for remaining health
        health_surface = pygame.Surface((health_bar_width, bar_height), pygame.SRCALPHA)
        health_surface.fill((0, 255, 0, 150))  # Green with 150 alpha for transparency

        # Draw the health bar background and foreground on the screen
        surface.blit(bar_surface, (0, screen_height - bar_height))
        surface.blit(health_surface, (0, screen_height - bar_height))

        # Draw the text label "House Health" above the health bar
        font = pygame.font.Font(None, 36)
        label_surface = font.render("House Health", True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(screen_width // 2, screen_height - bar_height - 20))
        surface.blit(label_surface, label_rect)
