import pygame
import math

class Bullet:
    def __init__(self, start_x, start_y, target_x, target_y, zoom_level, speed=10):
        self.x = start_x
        self.y = start_y
        self.zoom_level = zoom_level
        self.speed = speed

        # Load the bullet image and set its base size (adjust as needed)
        self.bullet_image = pygame.image.load('assets/5.56Ammo.png').convert_alpha()
        self.base_width, self.base_height = 10, 30  # Adjust width and height based on the image size
        self.bullet_image = pygame.transform.scale(self.bullet_image, (self.base_width, self.base_height))

        # Calculate direction of the bullet
        delta_x = target_x - start_x
        delta_y = target_y - start_y

        # Adjust angle calculation by adding 90 degrees to align the top correctly
        self.angle = math.degrees(math.atan2(-delta_y, delta_x)) - 90  # Subtract 90 degrees to fix orientation

        # Calculate distance and velocity
        distance = math.hypot(delta_x, delta_y)
        self.velocity_x = (delta_x / distance) * self.speed
        self.velocity_y = (delta_y / distance) * self.speed

    def update(self):
        """Update the bullet's position."""
        self.x += self.velocity_x
        self.y += self.velocity_y

    def is_off_screen(self, screen_width, screen_height):
        """Check if the bullet is off the screen."""
        return self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height

    def draw(self, surface, zoom_level):
        """Draw the bullet on the screen."""
        # Scale the bullet image based on the zoom level
        scaled_image = pygame.transform.scale(self.bullet_image, (int(self.base_width * zoom_level), int(self.base_height * zoom_level)))

        # Rotate the bullet image to face the direction of movement
        rotated_image = pygame.transform.rotate(scaled_image, self.angle)

        # Get the rectangle of the rotated image and center it on the bullet's current position
        rect = rotated_image.get_rect(center=(self.x, self.y))

        # Draw the rotated bullet image
        surface.blit(rotated_image, rect.topleft)
