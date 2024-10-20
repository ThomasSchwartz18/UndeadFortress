import pygame
import math
import random

class Zombie:
    def __init__(self, screen_width, screen_height, house_x, house_y, width=20, height=50, health=100, speed=1):
        self.base_width = width
        self.base_height = height
        self.max_health = health
        self.current_health = health
        self.speed = speed

        # Randomly spawn outside the screen
        self.x, self.y = self.random_spawn_location(screen_width, screen_height)

        # Calculate movement direction toward the house
        self.house_x = house_x
        self.house_y = house_y
        self.calculate_movement_direction()

        self.reached_house = False  # Tracks if the zombie has reached the house
        self.damage_timer = 0  # Timer to track when the zombie deals damage

    def random_spawn_location(self, screen_width, screen_height):
        """Spawn randomly outside the screen."""
        spawn_buffer = 100  # Extra space outside the screen to spawn the zombies
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return random.randint(-spawn_buffer, screen_width + spawn_buffer), -spawn_buffer
        elif side == "bottom":
            return random.randint(-spawn_buffer, screen_width + spawn_buffer), screen_height + spawn_buffer
        elif side == "left":
            return -spawn_buffer, random.randint(-spawn_buffer, screen_height + spawn_buffer)
        elif side == "right":
            return screen_width + spawn_buffer, random.randint(-spawn_buffer, screen_height + spawn_buffer)

    def calculate_movement_direction(self, target_x=None, target_y=None):
        """Calculate movement direction toward the house or the character."""
        if target_x is None:
            delta_x = self.house_x - self.x
            delta_y = self.house_y - self.y
        else:
            delta_x = target_x - self.x
            delta_y = target_y - self.y
        
        distance = math.hypot(delta_x, delta_y)

        # Normalize the direction and multiply by speed
        self.velocity_x = (delta_x / distance) * self.speed if distance != 0 else 0
        self.velocity_y = (delta_y / distance) * self.speed if distance != 0 else 0

    def update(self, delta_time, character, house):
        """Update the zombie's position or apply damage if it has reached its target."""
        # Calculate the distance to the character
        distance_to_character = math.hypot(character.x - self.x, character.y - self.y)

        if distance_to_character < 100 and not character.is_dead() and not character.in_house:  # Within 100 pixels, target the character if outside
            self.calculate_movement_direction(character.x, character.y)
        else:  # Otherwise, target the house
            self.calculate_movement_direction()

        # Move the zombie
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check if the zombie should attack the character or house
        if distance_to_character < 20 and not character.is_dead() and not character.in_house:  # Attack character
            self.damage_timer += delta_time
            if self.damage_timer >= 1000:  # 1 second interval for damage
                self.damage_timer = 0
                character.take_damage(5)  # Deal 5 damage to the character
        elif ((self.x - self.house_x) ** 2 + (self.y - self.house_y) ** 2) ** 0.5 < 20:  # Close to the house, attack it
            self.damage_timer += delta_time
            if self.damage_timer >= 1000:  # 1 second interval for damage
                self.damage_timer = 0
                return True  # Indicate to deal damage to the house

        return False  # No damage to the house

    def take_damage(self, damage):
        """Reduce the zombie's health by the given damage."""
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

    def is_dead(self):
        """Check if the zombie's health is 0 or below."""
        return self.current_health <= 0

    def check_collision(self, bullet):
        """Check if a bullet has collided with the zombie."""
        # Use the image size to create the bullet rectangle
        bullet_width = bullet.bullet_image.get_width() * bullet.zoom_level
        bullet_height = bullet.bullet_image.get_height() * bullet.zoom_level

        # Create a rectangle for the bullet based on its current position and size
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet_width, bullet_height)

        # Create a rectangle for the zombie
        zombie_rect = pygame.Rect(self.x, self.y, self.base_width, self.base_height)

        return zombie_rect.colliderect(bullet_rect)
    
    def draw(self, surface, zoom_level):
        """Draw the zombie and its health bar on the given surface."""
        # Scale the zombie based on the zoom level
        scaled_width = int(self.base_width * zoom_level)
        scaled_height = int(self.base_height * zoom_level)

        # Draw the zombie
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, scaled_width, scaled_height))

        # Draw the health bar
        health_bar_width = int((self.current_health / self.max_health) * scaled_width)
        health_bar_x = self.x
        health_bar_y = self.y + scaled_height + 5  # Position health bar below the zombie
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, scaled_width, 5))  # Red for background
        pygame.draw.rect(surface, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width, 5))  # Green for health
