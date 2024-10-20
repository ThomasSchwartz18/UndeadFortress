import pygame

class MainMenu:
    def __init__(self, screen_width, screen_height):
        # Load the PixelifySans-Bold.ttf for the "Start" button
        self.font_big = pygame.font.Font('assets/pixelify_font/PixelifySans-Bold.ttf', 72)
        # Load the Pixelify-Regular.ttf for the "Exit Game" button
        self.font_small = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 48)
        
        # Text for Start and Exit
        self.start_text = self.font_big.render("Start", True, (0, 0, 0))  # Black text
        self.exit_text = self.font_small.render("Exit Game", True, (0, 0, 0))  # Black text

        # Get positions for text (adjusted positions)
        self.start_rect = self.start_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))  # Adjusted Y-position
        self.exit_rect = self.exit_text.get_rect(center=(screen_width // 2, screen_height // 2))  # Adjusted Y-position

        self.game_started = False

    def draw(self, surface):
        """Draw the menu."""
        surface.fill((255, 255, 255))  # Fill the screen with white
        surface.blit(self.start_text, self.start_rect)
        surface.blit(self.exit_text, self.exit_rect)
        pygame.display.flip()  # Ensure the display is updated

    def handle_events(self, event):
        """Handle menu clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse clicked at {mouse_pos}")  # Debugging line

            # Print button positions
            print(f"Start button rect: {self.start_rect}")
            print(f"Exit button rect: {self.exit_rect}")

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
