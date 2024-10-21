import pygame

class MainMenu:
    def __init__(self, screen_width, screen_height):
        # Load the PixelifySans-Bold.ttf for the "Start" button
        self.font_big = pygame.font.Font('assets/pixelify_font/PixelifySans-Bold.ttf', 72)
        # Load the Pixelify-Regular.ttf for the "Exit Game" button
        self.font_small = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 48)
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Text for Start and Exit
        self.start_text = self.font_big.render("Start", True, (255, 255, 255))  # Black text
        self.exit_text = self.font_small.render("Exit Game", True, (255, 255, 255))  # Black text

        # Get positions for text (adjusted positions)
        self.start_rect = self.start_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))  # Adjusted Y-position
        self.exit_rect = self.exit_text.get_rect(center=(screen_width // 2, screen_height // 2))  # Adjusted Y-position

        self.game_started = False


    def draw(self, surface, game_instance):
        """Draw the main menu with a tiled background."""
        # Draw the tiled background
        game_instance.draw_tiled_background(surface)  # Only pass surface, not self

        # Draw the rest of the main menu elements
        # For example, drawing buttons, title, etc.
        title_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 72)
        # title_surface = title_font.render("Fortress of the Undead", True, (255, 255, 255))
        # title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        # surface.blit(title_surface, title_rect)

        # Draw "Start" button:
        surface.blit(self.start_text, self.start_rect)

        # Draw "Exit Game" button:
        surface.blit(self.exit_text, self.exit_rect)
        
        pygame.display.flip()  # Update the screen

    def handle_events(self, event):
        """Handle menu clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()

            # Check if the Start or Exit buttons are clicked
            if self.start_rect.collidepoint(mouse_pos):
                print("Start button clicked")  # Debugging line
                self.game_started = True  # Start the game when "Start" is clicked
            elif self.exit_rect.collidepoint(mouse_pos):
                print("Exit button clicked")  # Debugging line
                pygame.quit()
                exit()  # Quit the game when "Exit Game" is clicked

    def is_game_started(self):
        """Check if the game has started."""
        return self.game_started
