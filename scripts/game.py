# game.py

import pygame
import sys
import random
from scripts.house import House
from scripts.settings import Settings
from scripts.bullet import Bullet
from scripts.zombie import Zombie
from scripts.day_counter import DayCounter
from scripts.money_counter import MoneyCounter
from scripts.main_menu import MainMenu
from scripts.character import Character
from scripts.startup_selections import IntroStep, FamilySelectionStep, TeamSelectionStep
from scripts.drop import Drop
from scripts.materials_counter import MaterialsCounter
from scripts.shop import Shop
from scripts.stat_window import StatWindow

WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        self.initialize_game_elements()

    def initialize_game_elements(self):
        self.screen = pygame.display.set_mode((1280, 720))  # Windowed mode for testing
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_surface().get_size()
        pygame.display.set_caption("Fortress of the Undead")
        self.clock = pygame.time.Clock()

        # Load the PixelifySans font
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 36)  # Default size 36

        # Load grass image for tiling
        self.grass_image = pygame.image.load('assets/grass.png').convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (64, 64))  # Resize to 64x64 tiles, adjust as necessary

        # Game elements
        self.house = House()
        self.settings = Settings(self.screen)
        self.day_counter = DayCounter()
        self.money_counter = MoneyCounter()
        self.materials_counter = MaterialsCounter()

        # Create the stat window for displaying player stats
        self.player_stats = {
            'Speed': (1.2, 0.0, 1.2),  # Base, Boost, Total
            'Health': (100, 0.0, 100),
            'Accuracy': (0, 0.0, 0.0),
            'Rate of Fire': (3.0, 0.0, 3.0),
            'Health Regen Rate': (0, 0.0, 0),
            'Building Regen Rate': (0, 0.0, 0)
        }

        # Initialize the stat window before the shop
        self.stat_window = StatWindow(self.screen, self.player_stats)

        # Other game element initialization...
        self.team_selection_step = TeamSelectionStep(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.stat_window)

        # Placeholder for character initialization, it will be initialized after team selection
        self.character = None

        self.player_speed = 0.0  # Initialize player speed
        self.previous_position = (0, 0)  # Track the previous position of the player
        self.speed_history = []  # List to store recent speed values
        self.speed_history_size = 10  # Number of frames to average over
        self.damage_done_in_last_second = 0  # Track total damage done per second
        self.dps_timer = pygame.time.get_ticks() / 1000.0  # Start timer for DPS calculation

        self.shots_fired = 0
        self.sps_timer = pygame.time.get_ticks() / 1000.0  # Timer for SPS calculation

        self.shots_in_last_interval = 0  # Track how many shots fired in the last 0.5 seconds
        self.sps = 0  # Shots per second

        # Initialize the shop after creating the stat window
        self.shop = Shop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.house, self.materials_counter, self.stat_window, self.money_counter)

        self.main_menu = MainMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Game steps
        self.intro_step = IntroStep(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.family_selection_step = FamilySelectionStep(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.team_selection_step = TeamSelectionStep(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.stat_window)

        # Game state variables
        self.bullets = []
        self.zombies = []
        self.drops = []
        self.zoom_level = 1.0
        self.current_step = "main_menu"
        self.last_drop_spawn_time = 0
        self.drop_spawn_interval = 5000
        self.spawn_drops(5)

        # Automatic shooting variables
        self.shooting_interval = 1 / 3  # 3 bullets per second
        self.last_shot_time = 0  # Track the time of the last shot
        self.is_shooting = False  # Track if the player is holding Mouse1 (left-click)

    def start_game_after_team_selection(self):
        """Initialize the game with the selected roles."""
        selected_roles = self.team_selection_step.selected_roles  # Get the selected roles
        print(f"Selected roles: {selected_roles}")  # Debugging line to ensure roles are selected

        # Pass selected roles to the Character class
        self.character = Character(
            self.SCREEN_WIDTH // 2,
            self.SCREEN_HEIGHT // 2,
            player_stats=self.player_stats,
            selected_roles=selected_roles  # Pass selected roles to the character
        )

        self.spawn_zombies(5)
        self.day_counter.current_day = 1
        self.current_step = "game"
    
    def apply_stat_boost(self, stat_name, boost_value):
        """Apply a boost to the given stat and update its total."""
        if stat_name in self.player_stats:
            # Increment the boost value
            base, current_boost, total = self.player_stats[stat_name]
            new_boost = current_boost + boost_value
            self.player_stats[stat_name] = (base, new_boost, base + new_boost)

            # Apply the boost to relevant character attributes
            if stat_name == "Speed":
                self.character.update_stat("Speed", self.player_stats['Speed'][2])  # Update speed
            elif stat_name == "Accuracy":
                self.character.update_stat("Accuracy", self.player_stats['Accuracy'][2])  # Update accuracy
            elif stat_name == "Health Regen Rate":
                self.character.update_stat("Health Regen Rate", self.player_stats['Health Regen Rate'][2])  # Update health regen
            elif stat_name == "Building Regen Rate":
                self.house.building_regen_rate = self.player_stats['Building Regen Rate'][2]  # Update building regen rate
                
    def run(self):
        while True:
            self.handle_events()
            self.update_game()
            self.render_game()
            self.clock.tick(60)

    # -------- Event Handling --------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Always check for the shop button click first
            self.shop.handle_shop_button_click(event)

            # Then handle other events based on the current step
            self.handle_event_by_step(event)

    
    def handle_game_events(self, event):
        # Check for the shop button click first to allow opening/closing the shop
        self.shop.handle_shop_button_click(event)

        # If the shop is open, handle only shop interactions
        if self.shop.is_shop_open():
            self.shop.handle_events(event)
        else:
            # Only handle game actions when the shop is not open
            self.handle_in_game_actions(event)
            self.settings.handle_events(event)
            self.check_day_progression(event)
            
    def handle_event_by_step(self, event):
        # Handle shop open state first
        if self.shop.is_shop_open():
            # If the shop is open, only handle shop interactions
            self.shop.handle_events(event)
        else:
            # If the shop is not open, handle other game events
            if self.current_step == "main_menu":
                self.handle_main_menu_events(event)
            elif self.current_step == "intro":
                self.handle_intro_events(event)
            elif self.current_step == "family_selection":
                self.handle_family_selection_events(event)
            elif self.current_step == "team_selection":
                self.handle_team_selection_events(event)
            elif self.current_step == "game":
                self.handle_game_events(event)

    def handle_main_menu_events(self, event):
        """Handle events in the main menu, like button clicks."""
        self.main_menu.handle_events(event)  # Process events in the main menu
        
        # Check if the game has started by clicking "Start"
        if self.main_menu.is_game_started():
            print("Transitioning to Intro")
            self.current_step = "intro"  # Transition to the intro phase

    def handle_intro_events(self, event):
        # Check if the "Continue" button in the intro step was clicked or if the user presses Enter/Space
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("Continue button clicked in Intro Step.")  # Debugging line
            self.current_step = "family_selection"  # Move to the next phase
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print("Enter key pressed in Intro Step.")  # Debugging line
            self.current_step = "family_selection"

    def handle_family_selection_events(self, event):
        # Check if a family has been selected and transition to team selection
        if self.family_selection_step.handle_events(event) == "team_selection":
            print("Transitioning to Team Selection")  # Debugging line
            self.current_step = "team_selection"

    def handle_team_selection_events(self, event):
        """Handle the transition from team selection to game start."""
        if self.team_selection_step.handle_events(event) == "game_start":
            print("Transitioning to the Game")
            self.team_selection_step.apply_team_boosts(self.team_selection_step.selected_roles)  # Apply boosts
            self.start_game_after_team_selection()  # Initialize the character with selected roles

    def handle_in_game_actions(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Mouse1 (left-click)
                self.is_shooting = True  # Start automatic shooting when Mouse1 is pressed
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Mouse1 (left-click)
                self.is_shooting = False  # Stop automatic shooting when Mouse1 is released
        elif event.type == pygame.KEYDOWN:
            self.handle_key_event(event)
        elif event.type == pygame.KEYUP:
            self.handle_key_release(event)

    def handle_mouse_event(self, event):
        if event.button == 4:  # Scroll up
            self.zoom_level += 0.1
        elif event.button == 5:  # Scroll down
            self.zoom_level = max(0.1, self.zoom_level - 0.1)

    def handle_key_event(self, event):
        if event.key == pygame.K_e:
            self.check_house_interaction()
        elif event.key == pygame.K_TAB:
            self.stat_window.set_visibility(True)  # Show stat window on Tab key press
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def handle_key_release(self, event):
        if event.key == pygame.K_TAB:
            self.stat_window.set_visibility(False)  # Hide stat window on Tab key release

    # -------- Game Logic --------
    def start_game(self):
        """Transition to the game state."""
        self.current_step = "game"
        self.spawn_zombies(5)
        self.day_counter.current_day = 1

    def shoot_bullet(self):
        """Handle shooting bullets based on player location and ammo count."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # If the player is inside the house, allow shooting freely
        if self.character.in_house:
            bullet_info = self.character.shoot(mouse_x, mouse_y)
            bullet = Bullet(*bullet_info, self.zoom_level)
            self.bullets.append(bullet)
            self.shots_fired += 1  # Track number of shots fired
            print(f"Bullet shot at: ({mouse_x}, {mouse_y}) | Player inside the house")
        
        # If the player is outside the house, check for ammo
        else:
            if self.materials_counter.ammo > 0:
                bullet_info = self.character.shoot(mouse_x, mouse_y)
                bullet = Bullet(*bullet_info, self.zoom_level)
                self.bullets.append(bullet)
                self.materials_counter.ammo -= 1
                self.shots_fired += 1  # Track number of shots fired
                print(f"Bullet shot at: ({mouse_x}, {mouse_y}) | Ammo left: {self.materials_counter.ammo}")
            else:
                print("No ammo left!")  # Notify that the player is out of ammo

    def check_house_interaction(self):
        house_center_x = self.SCREEN_WIDTH // 2
        house_center_y = self.SCREEN_HEIGHT // 2
        distance_to_house = ((self.character.x - house_center_x) ** 2 + (self.character.y - house_center_y) ** 2) ** 0.5
        if self.character.in_house:
            self.character.toggle_in_house()
        elif distance_to_house < 50:
            self.character.toggle_in_house()

    # -------- Updates --------
    def update_game(self):
        if self.current_step != "game":
            return
        
        # Calculate the current time and reset DPS every second
        current_time = pygame.time.get_ticks() / 1000.0  # Time in seconds
        # Reset SPS every second
        if current_time - self.sps_timer >= 1.0:
            self.sps = self.shots_fired  # Store the number of bullets fired in 1 second
            self.shots_fired = 0  # Reset the shot count for the next second
            self.sps_timer = current_time
        
        if current_time - self.dps_timer >= 0.25:
            # Calculate the DPS as total damage done in the last second
            self.dps = self.damage_done_in_last_second
            self.damage_done_in_last_second = 0  # Reset the damage tracker
            self.dps_timer = current_time  # Reset the DPS timer

        # Calculate player speed based on position change
        current_position = (self.character.x, self.character.y)
        distance_moved = ((current_position[0] - self.previous_position[0]) ** 2 +
                        (current_position[1] - self.previous_position[1]) ** 2) ** 0.5
        current_speed = distance_moved / (self.clock.get_time() / 1000)  # Speed in pixels per second

        if current_speed < 0.1:  # If the player speed is very low, consider it as not moving
            current_speed = 0.0
            
        delta_time = self.clock.get_time() / 1000  # Convert milliseconds to seconds

        # Pass the calculated DPS and accuracy_offset to materials_counter.draw
        self.materials_counter.draw(
            self.screen, 20, 100, 
            self.player_speed, 
            self.character.fire_rate, 
            self.character.damage_bonus, 
            self.dps, 
            self.sps,
            self.character.accuracy_offset  # Pass accuracy_offset here
        )

        # Update speed history with the current speed
        self.speed_history.append(current_speed)
        # Regenerate health for character and house
        self.character.regenerate_health(delta_time)
        self.house.regenerate_health(delta_time)

        # Keep the speed history size limited
        if len(self.speed_history) > self.speed_history_size:
            self.speed_history.pop(0)

        # Calculate the average speed from the history
        self.player_speed = sum(self.speed_history) / len(self.speed_history)

        # Update the previous position
        self.previous_position = current_position

        # Update other game elements
        self.character.handle_movement(pygame.key.get_pressed())
        self.auto_shoot()
        self.update_bullets()
        self.update_zombies()
        self.check_for_drop_collection()

        if not self.zombies:
            if not self.day_counter.timer_start_time:
                self.day_counter.start_timer()
            self.day_counter.show_next_day_button = True

    def update_bullets(self):
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.update()
            if bullet.is_off_screen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT):
                bullets_to_remove.append(bullet)
            else:
                print(f"Checking bullet collisions for bullet at ({bullet.x}, {bullet.y})")  # Debugging
                self.check_bullet_collisions(bullet, bullets_to_remove)

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

    def check_bullet_collisions(self, bullet, bullets_to_remove):
        damage = self.character.damage_bonus if hasattr(self.character, 'damage_bonus') else 0  # Ensure damage is initialized
        print(f"Damage bonus: {damage}")  # Debugging line

        for zombie in self.zombies[:]:
            if zombie.check_collision(bullet):
                zombie.take_damage(damage)  # Apply damage to the zombie
                bullets_to_remove.append(bullet)
                self.damage_done_in_last_second += damage  # Add damage to the DPS tracker
                print(f"Zombie hit! Health: {zombie.current_health}, Damage dealt: {damage}")
                if zombie.is_dead():
                    self.zombies.remove(zombie)
                    self.money_counter.add_money()


    def update_zombies(self):
        for zombie in self.zombies:
            if zombie.update(self.clock.get_time(), self.character, self.house):
                self.house.take_damage(5)

    def check_for_drop_collection(self):
        for drop in self.drops[:]:
            if drop.check_collection(self.character):
                self.materials_counter.add_material(drop.type_of_drop)
                self.drops.remove(drop)
                
    def auto_shoot(self):
        """Automatically shoot bullets if Mouse1 is held down, with an interval adjusted by selected roles."""
        current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds
        mouse_buttons = pygame.mouse.get_pressed()

        # If Mouse1 (left-click) is held down, shoot bullets automatically
        if mouse_buttons[0]:
            self.is_shooting = True
        else:
            self.is_shooting = False

        # Calculate the shooting interval based on the character's fire rate and bonus
        shooting_interval = self.character.shooting_interval

        if self.is_shooting and current_time - self.last_shot_time >= shooting_interval:
            self.shoot_bullet()  # Shoot a bullet
            
            # Check if Machine Gunner is selected and apply a faster shooting interval
            if "Machine Gunner" in self.team_selection_step.selected_roles:
                print("Machine Gunner active, reducing shooting interval")  # Debugging
                shooting_interval = max(0.1, shooting_interval - 0.1)  # Reduce interval, e.g., by 0.1 seconds
            
            self.last_shot_time = current_time  # Update the last shot time


    # -------- Handle Day Progression --------
    def check_day_progression(self, event):
        """Handle the logic for starting the next day."""
        if self.day_counter.show_next_day_button:
            self.day_counter.auto_advance_day_if_needed()

            # Check for button click to advance the day manually
            if self.day_counter.check_button_click(event):
                self.advance_day_logic()

    # -------- Render Game Background --------
    def draw_tiled_background(self, surface):
        """Tile the grass image across the given surface."""
        tile_width, tile_height = self.grass_image.get_size()
        screen_width, screen_height = surface.get_size()
        
        for x in range(0, screen_width, tile_width):
            for y in range(0, screen_height, tile_height):
                surface.blit(self.grass_image, (x, y))

    # -------- Rendering --------
    def render_game(self):
        if self.current_step == "main_menu":
            self.main_menu.draw(self.screen, self)  # Pass self as game_instance
        elif self.current_step == "intro":
            self.intro_step.draw(self.screen, self)  # Ensure intro_step takes game_instance too if needed
        elif self.current_step == "family_selection":
            self.family_selection_step.draw(self.screen, self)  # Pass self as game_instance here
        elif self.current_step == "team_selection":
            self.team_selection_step.draw(self.screen, self)  # Pass self as game_instance here
        elif self.current_step == "game":
            self.render_gameplay()

            
    def render_gameplay(self):
        # First, draw the tiled background
        self.draw_tiled_background(self.screen)  # Pass self.screen as the argument

        # Then, draw all game elements (house, character, etc.)
        self.house.draw(self.screen, self.zoom_level, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.character.draw(self.screen, self.zoom_level)

        for zombie in self.zombies:
            zombie.draw(self.screen, self.zoom_level)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.zoom_level)

        for drop in self.drops:
            drop.draw(self.screen)

        self.day_counter.draw(self.screen)
        self.money_counter.draw(self.screen, 20, 60)

        # Check if the character is inside the house
        if self.character.in_house:
            # Draw the house's health bar at the bottom of the screen
            self.house.draw_health_bar_bottom(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        else:
            # Draw the character's health bar at the bottom of the screen
            self.character.draw_health_bar_bottom(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Add the DPS value when calling the draw method, along with accuracy_offset
        self.materials_counter.draw(
            self.screen, 20, 100, 
            self.player_speed, 
            self.character.fire_rate, 
            self.character.damage_bonus, 
            self.dps, 
            self.sps, 
            self.character.accuracy_offset  # Add accuracy_offset here
        )

        self.shop.draw_shop_button(self.screen)
        if self.shop.is_shop_open():
            self.shop.open_shop_menu(self.screen)

        # Add the settings logo here so it's drawn after everything else
        self.settings.draw_logo()

        # Display house interaction message
        self.draw_house_interaction_message()

        self.stat_window.draw()  # Draw the stats window if it's visible

        # Check if the settings window should be drawn
        if self.settings.show_settings_window:
            self.settings.draw_settings_window()

        # Update display
        pygame.display.flip()



    def draw_house_interaction_message(self):
        """Display a message when the player is inside or near the house for the first 4 seconds, then fade out."""
        # Do not show indicators if the shop is open
        if self.shop.is_shop_open():
            return  # Skip drawing the indicator if the shop is open

        current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds

        # If the player is inside the house
        if self.character.in_house:
            time_in_house = current_time - self.character.house_entry_time  # Time spent in the house

            # Only show the message for the first 4 seconds inside the house
            if time_in_house > 4:
                return  # Stop showing the message after 4 seconds

            message = "Press E to exit house"
        else:
            # If the player is near the house but not inside
            house_center_x = self.SCREEN_WIDTH // 2
            house_center_y = self.SCREEN_HEIGHT // 2
            distance_to_house = ((self.character.x - house_center_x) ** 2 + (self.character.y - house_center_y) ** 2) ** 0.5

            if distance_to_house < 50:  # Define an arbitrary threshold for "near" the house
                # If the player is near the house, track time since they became near
                if not hasattr(self.character, 'near_house_time') or self.character.near_house_time is None:
                    self.character.near_house_time = current_time  # Start the timer when the player is near the house

                time_near_house = current_time - self.character.near_house_time  # Time spent near the house

                # Show the message for 4 seconds after the player is near the house
                if time_near_house > 4:
                    return  # Stop showing the message after 4 seconds

                message = "Press E to enter house"
            else:
                # If the player is not near the house, reset the timer
                self.character.near_house_time = None
                return  # No message if not near or in the house

        # Font settings for the message
        regular_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 36)
        e_font = pygame.font.Font('assets/pixelify_font/Monofett-Regular.ttf', 36)

        # Split the message to render "E" separately
        parts = message.split("E")
        text_surface_before_e = regular_font.render(parts[0], True, (255, 255, 255))
        text_surface_after_e = regular_font.render(parts[1], True, (255, 255, 255)) if len(parts) > 1 else None
        e_surface = e_font.render("E", True, (255, 255, 255))

        before_e_width = text_surface_before_e.get_width()
        e_width = e_surface.get_width()
        after_e_width = text_surface_after_e.get_width() if text_surface_after_e else 0

        total_width = before_e_width + e_width + after_e_width
        base_x = self.SCREEN_WIDTH // 2 - total_width // 2
        base_y = self.SCREEN_HEIGHT // 2 + 100

        # Determine fade out effect for the last 2 seconds
        if self.character.in_house:
            alpha = 255 if time_in_house <= 2 else max(0, 255 - int(255 * (time_in_house - 2) / 2))
        else:
            alpha = 255 if time_near_house <= 2 else max(0, 255 - int(255 * (time_near_house - 2) / 2))

        # Apply alpha transparency to surfaces
        text_surface_before_e.set_alpha(alpha)
        e_surface.set_alpha(alpha)
        if text_surface_after_e:
            text_surface_after_e.set_alpha(alpha)

        # Draw the message parts on the screen
        self.screen.blit(text_surface_before_e, (base_x, base_y))
        self.screen.blit(e_surface, (base_x + before_e_width, base_y))
        if text_surface_after_e:
            self.screen.blit(text_surface_after_e, (base_x + before_e_width + e_width, base_y))

        pygame.display.flip()  # Update the screen



    # -------- Helper Functions --------
    def spawn_zombies(self, num_zombies):
        house_center_x = self.SCREEN_WIDTH // 2
        house_center_y = self.SCREEN_HEIGHT // 2
        for _ in range(num_zombies):
            zombie = Zombie(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, house_center_x, house_center_y)
            self.zombies.append(zombie)

    def spawn_drops(self, num_drops=None):
        if num_drops is None:
            num_drops = random.randint(3, 7)
        for _ in range(num_drops):
            drop_type = random.choice(['food', 'ammo', 'scrap'])
            drop = Drop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, drop_type)
            self.drops.append(drop)

    def check_day_progression(self, event):
        if self.day_counter.show_next_day_button:
            self.day_counter.start_timer()
            if self.day_counter.check_button_click(event) or self.day_counter.is_timer_done():
                self.day_counter.advance_day()
                self.spawn_zombies(5 * self.day_counter.current_day)
                self.spawn_drops()


if __name__ == "__main__":
    game = Game()
    game.run()
