import pygame
import random
import time

class Character:
    def __init__(self, start_x, start_y, width=20, height=40, speed=1.2, health=100, accuracy=10, player_stats=None):
        self.x = start_x  # Player's x position
        self.y = start_y  # Player's y position
        self.base_width = width  # Store base width for scaling
        self.base_height = height  # Store base height for scaling
        self.speed = speed  # Base speed of movement (upgradable)
        self.max_health = health
        self.current_health = health
        self.color = (0, 0, 255)  # Character color (blue for now)
        self.velocity_x = 0  # Horizontal movement velocity
        self.velocity_y = 0  # Vertical movement velocity
        self.in_house = True  # Start the player inside the house and invisible
        self.is_visible = False  # Player is invisible when inside the house
        self.shooting_automatic = False  # For machine gunner ability (automatic shooting)

        # Reference to player stats for real-time upgrades (optional)
        self.player_stats = player_stats or {}

        # Abilities attributes (initial state with no bonuses)
        self.accuracy_bonus = 0.0  # Accuracy bonus for snipers
        self.damage_bonus = 0  # Damage bonus for machine gunners
        self.health_regen_rate = 0  # Health regeneration rate for medics
        self.accuracy_offset = accuracy  # Lower value = more accurate, higher value = less accurate

        # Track time for medic healing and automatic shooting
        self.last_health_regen_time = time.time()
        self.last_auto_shot_time = time.time()

    # Method to dynamically update the character's stats when upgraded
    def update_stat(self, stat_name, new_value):
        """Update the character's stat dynamically."""
        if stat_name == "Speed":
            self.speed = new_value  # Dynamically update speed
            print(f"Speed updated to {self.speed}")
        elif stat_name == "Accuracy":
            self.accuracy_bonus = new_value  # Dynamically update accuracy
            print(f"Accuracy updated to {self.accuracy_bonus}")
        elif stat_name == "Health Regen Rate":
            self.health_regen_rate = new_value  # Dynamically update health regen rate
            print(f"Health Regen Rate updated to {self.health_regen_rate}")

    def handle_movement(self, keys_pressed):
        # Retrieve the total speed (base + boost) from player stats if available
        speed = self.player_stats.get('Speed', (self.speed, 0, self.speed))[2]

        # Calculate direction modifiers based on keys pressed
        move_x = 0
        move_y = 0

        if keys_pressed[pygame.K_w]:
            move_y -= speed
        if keys_pressed[pygame.K_s]:
            move_y += speed
        if keys_pressed[pygame.K_a]:
            move_x -= speed
        if keys_pressed[pygame.K_d]:
            move_x += speed

        # If moving diagonally, normalize the movement vector
        if move_x != 0 and move_y != 0:
            move_x /= 1.414  # Divide by sqrt(2) to normalize diagonal speed
            move_y /= 1.414

        # Apply the movement to the character's position
        self.x += move_x
        self.y += move_y

    def toggle_in_house(self):
        """Toggle the player's status between inside and outside the house."""
        self.in_house = not self.in_house
        self.is_visible = not self.in_house  # Player is visible when outside the house

    def take_damage(self, damage):
        """Reduce the character's health."""
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0  # Prevent health from going negative

    def is_dead(self):
        """Check if the character's health is 0 or below."""
        return self.current_health <= 0

    def regenerate_health(self, delta_time):
        """Regenerate health over time if the health_regen_rate is greater than 0."""
        if self.health_regen_rate > 0 and self.current_health < self.max_health:
            self.current_health += self.health_regen_rate * delta_time  # Regenerate health based on delta_time
            if self.current_health > self.max_health:
                self.current_health = self.max_health

    def heal_over_time(self):
        """For Medic: Regenerate health every second if not at max health."""
        current_time = time.time()
        if self.current_health < self.max_health and current_time - self.last_health_regen_time >= 1:
            self.current_health += 1
            if self.current_health > self.max_health:
                self.current_health = self.max_health
            self.last_health_regen_time = current_time

    def draw(self, surface, zoom_level):
        """Draw the character on the screen if they are visible with zoom."""
        if self.is_visible:
            # Scale the character based on the zoom level
            scaled_width = int(self.base_width * zoom_level)
            scaled_height = int(self.base_height * zoom_level)
            # Adjust the character's position to account for zooming
            scaled_x = self.x - (scaled_width - self.base_width) // 2
            scaled_y = self.y - (scaled_height - self.base_height) // 2

            # Draw the character
            pygame.draw.rect(surface, self.color, (scaled_x, scaled_y, scaled_width, scaled_height))
            
    def draw_health_bar_bottom(self, surface, screen_width, screen_height):
        """Draw the character's health bar across the bottom of the screen."""
        bar_height = 30
        health_bar_width = int((self.current_health / self.max_health) * screen_width)
        
        # Create a transparent surface for the health bar
        bar_surface = pygame.Surface((screen_width, bar_height), pygame.SRCALPHA)
        bar_surface.fill((255, 0, 0, 150))  # Red with 150 alpha for transparency

        # Foreground (Green) for remaining health
        health_surface = pygame.Surface((health_bar_width, bar_height), pygame.SRCALPHA)
        health_surface.fill((0, 255, 0, 150))  # Green with 150 alpha for transparency

        # Draw the health bar background and foreground on the screen
        surface.blit(bar_surface, (0, screen_height - bar_height))
        surface.blit(health_surface, (0, screen_height - bar_height))

        # Draw the text label "Character Health" above the health bar
        font = pygame.font.Font(None, 36)
        label_surface = font.render("Character Health", True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(screen_width // 2, screen_height - bar_height - 20))
        surface.blit(label_surface, label_rect)
        
    def shoot(self, mouse_x, mouse_y):
        """Return the information needed to create a bullet with slight randomness."""
        
        # Debugging to ensure `self.base_width` is correct
        if not isinstance(self.base_width, (int, float)):
            print(f"Error: self.base_width is {type(self.base_width)} instead of int or float!")
            self.base_width = 20  # Safeguard value in case it gets corrupted

        # Introduce randomness for shooting inaccuracy
        random_offset_x = random.uniform(-self.accuracy_offset, self.accuracy_offset)
        random_offset_y = random.uniform(-self.accuracy_offset, self.accuracy_offset)

        # Adjust the shooting target with the random offset and accuracy bonus
        adjusted_mouse_x = mouse_x + random_offset_x + self.accuracy_bonus
        adjusted_mouse_y = mouse_y + random_offset_y + self.accuracy_bonus

        # Return the shooting coordinates, ensuring `self.base_width` is valid
        return self.x + self.base_width // 2, self.y + self.base_height // 2, adjusted_mouse_x, adjusted_mouse_y

    def auto_shoot(self, mouse_x, mouse_y):
        """For Machine Gunner: Automatically shoot at a regular interval."""
        current_time = time.time()
        if current_time - self.last_auto_shot_time >= 0.1:  # Shoot every 100ms
            self.last_auto_shot_time = current_time
            return self.shoot(mouse_x, mouse_y)
        return None
