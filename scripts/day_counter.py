# day_counter.py

import pygame
import time

class DayCounter:
    def __init__(self, initial_day=1):
        # Load PixelifySans-Regular font for both the timer and button
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 30)
        self.button_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 28)  # Same font for button
        self.button_color = (70, 130, 180)  # Blue for the button
        self.button_hover_color = (100, 149, 237)
        self.button_text_color = (255, 255, 255)
        self.show_next_day_button = False

        # Timer for the "Next Day" button
        self.timer_duration = 90  # 90 seconds (1:30)
        self.time_left = self.timer_duration
        self.timer_start_time = None

        # Position of the "Next Day" button
        self.button_rect = pygame.Rect(0, 0, 200, 70)
        self.button_rect.centerx = pygame.display.get_surface().get_width() // 2
        self.button_rect.top = 20

    def start_timer(self):
        """Start the countdown timer when the button appears."""
        if not self.timer_start_time:  # Ensure the timer starts only once
            self.timer_start_time = time.time()

    def update_timer(self):
        """Update the countdown timer."""
        if self.timer_start_time:
            elapsed_time = time.time() - self.timer_start_time
            self.time_left = max(0, self.timer_duration - int(elapsed_time))  # Ensure time doesn't go negative

    def draw(self, surface):
        """Draw the day counter and button with a countdown timer if needed."""
        # Display the current day
        day_text = self.font.render(f"Day {self.current_day}", True, (0, 0, 0))
        surface.blit(day_text, (20, 20))

        # Display the "Start Next Day" button if all zombies are killed
        if self.show_next_day_button:
            pygame.draw.rect(surface, self.button_color, self.button_rect)

            # Draw "Start Next Day" text using the button font
            button_text = self.button_font.render("Start Next Day", True, self.button_text_color)
            surface.blit(button_text, (self.button_rect.x + 20, self.button_rect.y + 10))

            # Update and draw the countdown timer using the same font
            self.update_timer()
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            timer_text = f"({minutes}:{seconds:02d})"
            timer_rendered = self.button_font.render(timer_text, True, self.button_text_color)
            surface.blit(timer_rendered, (self.button_rect.x + 50, self.button_rect.y + 40))  # Position below button text

    def advance_day(self):
        """Increase the day counter and hide the button."""
        self.current_day += 1
        self.show_next_day_button = False
        self.time_left = self.timer_duration  # Reset the timer for the next time
        self.timer_start_time = None  # Reset the timer

    def check_button_click(self, event):
        """Check if the next day button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.show_next_day_button and self.button_rect.collidepoint(mouse_pos):
                return True
        return False

    def is_timer_done(self):
        """Check if the timer has reached zero and automatically advance the day."""
        return self.time_left == 0

    def auto_advance_day_if_needed(self):
        """Automatically advance the day if the timer reaches zero."""
        if self.is_timer_done():
            self.advance_day()
