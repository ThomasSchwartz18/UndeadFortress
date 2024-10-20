import pygame
import random

class Drop:
    def __init__(self, screen_width, screen_height, type_of_drop):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type_of_drop = type_of_drop

        # Load images for different types of drops
        if self.type_of_drop == 'ammo':
            self.image = pygame.image.load('assets/AmmoCrateIMG.png').convert_alpha()
        elif self.type_of_drop == 'food':
            self.image = pygame.image.load('assets/FoodBagIMG.png').convert_alpha()
        elif self.type_of_drop == 'scrap':
            self.image = pygame.image.load('assets/scrapIMG.png').convert_alpha()
        elif self.type_of_drop == 'rare_speed':
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 255, 0))  # Yellow box for rare speed drop

        # Set the default width and height for all drops (adjust as needed)
        self.width, self.height = 30, 30
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Randomly place the drop on the map
        self.x = random.randint(0, self.screen_width - self.width)
        self.y = random.randint(0, self.screen_height - self.height)

    def draw(self, surface):
        """Draw the drop on the screen."""
        surface.blit(self.image, (self.x, self.y))

    def check_collection(self, character):
        """Check if the character collides with the drop."""
        character_rect = pygame.Rect(character.x, character.y, character.base_width, character.base_height)
        drop_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return character_rect.colliderect(drop_rect)

    def apply_effect(self, character):
        """Apply the effect of the drop when collected."""
        if self.type_of_drop == 'rare_speed':
            if random.random() < 1:  # 50% chance to increase speed
                character.increase_speed()
                print("Speed increased!")
            else:
                print("No speed increase this time.")
