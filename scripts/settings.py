import pygame
import sys

class Settings:
    def __init__(self, screen):
        self.screen = screen
        
        # Load the settings logo image
        try:
            self.settings_logo_original = pygame.image.load('assets/settingsIMG.png')
        except pygame.error as e:
            print(f"Unable to load image: {e}")
        
        # Scale the settings logo based on the screen size (e.g., 5% of screen height)
        logo_scale_factor = 0.05  # 5% of screen height
        self.logo_width = int(self.screen.get_height() * logo_scale_factor)
        self.logo_height = int(self.logo_width)  # Keep the aspect ratio
        self.settings_logo = pygame.transform.scale(self.settings_logo_original, (self.logo_width, self.logo_height))

        self.show_settings_window = False

        # Settings window dimensions
        self.window_width = 400
        self.window_height = 300

        # Button properties
        # Load the PixelifySans-Regular font for buttons
        self.button_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 36)
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 149, 237)
        self.button_text_color = (255, 255, 255)

        # Return to game button
        self.return_button_rect = pygame.Rect(0, 0, 200, 50)
        self.return_button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 - 30)

        # Quit game button
        self.quit_button_rect = pygame.Rect(0, 0, 200, 50)
        self.quit_button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 30)

    def draw_logo(self):
        """Draw the settings logo in the bottom-right corner."""
        x = self.screen.get_width() - self.logo_width - 10  # 10 pixels from right
        y = self.screen.get_height() - self.logo_height - 10  # 10 pixels from bottom
        self.screen.blit(self.settings_logo, (x, y))

    def draw_settings_window(self):
        """Draw the settings window with buttons."""
        pygame.draw.rect(self.screen, (200, 200, 200), 
                         ((self.screen.get_width() - self.window_width) // 2, 
                          (self.screen.get_height() - self.window_height) // 2, 
                          self.window_width, self.window_height))

        # Draw "Return to Game" button
        pygame.draw.rect(self.screen, self.button_color, self.return_button_rect)
        return_text = self.button_font.render("Return to game", True, self.button_text_color)
        self.screen.blit(return_text, (self.return_button_rect.x + 25, self.return_button_rect.y + 10))

        # Draw "Quit Game" button
        pygame.draw.rect(self.screen, self.button_color, self.quit_button_rect)
        quit_text = self.button_font.render("Quit game", True, self.button_text_color)
        self.screen.blit(quit_text, (self.quit_button_rect.x + 50, self.quit_button_rect.y + 10))

    def handle_events(self, event):
        """Handle click events for settings icon and window buttons."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if the settings logo is clicked to toggle the settings window
            x = self.screen.get_width() - self.logo_width - 10
            y = self.screen.get_height() - self.logo_height - 10
            if not self.show_settings_window and pygame.Rect(x, y, self.logo_width, self.logo_height).collidepoint(mouse_pos):
                self.show_settings_window = True

            # Check if buttons in the settings window are clicked
            if self.show_settings_window:
                if self.return_button_rect.collidepoint(mouse_pos):
                    self.show_settings_window = False  # Close settings
                elif self.quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # Quit the game
