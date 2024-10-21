import pygame

class StatWindow:
    def __init__(self, screen, player_stats):
        self.screen = screen
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)
        self.show_window = False
        self.player_stats = player_stats  # Dictionary holding base stats, boosts, and totals

        # Window dimensions
        self.window_width = 900  # Adjust if necessary
        self.window_height = len(player_stats) * 50 + 300
        self.window_rect = pygame.Rect((self.screen.get_width() // 2) - (self.window_width // 2),
                                       (self.screen.get_height() // 2) - (self.window_height // 2),
                                       self.window_width, self.window_height)

    def set_visibility(self, visible):
        self.show_window = visible

    def apply_stat_boost(self, stat_name, boost_value):
        """Apply a boost to the given stat."""
        if stat_name in self.player_stats:
            base_value, boost, total = self.player_stats[stat_name]
            new_boost = boost + boost_value
            self.player_stats[stat_name] = (base_value, new_boost, base_value + new_boost)
            print(f"Applied {boost_value} boost to {stat_name}. New value: {self.player_stats[stat_name]}")

    def draw(self):
        if self.show_window:
            # Create a semi-transparent surface
            window_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            window_surface.fill((0, 0, 0, 180))  # Black with 180/255 transparency

            # Draw the semi-transparent window
            self.screen.blit(window_surface, (self.window_rect.x, self.window_rect.y))

            # Draw the stat titles
            x_offset = 20
            y_offset = 20

            # Adjust the width of the first column only
            first_column_width = 300  # Adjust this to make the first column wider
            other_column_width = 100  # Width for other columns

            # Add column headers
            headers = ['Stat', 'Base', 'Boost', 'Total']
            for i, header in enumerate(headers):
                header_surface = self.font.render(header, True, (255, 255, 255))  # White text
                if i == 0:
                    self.screen.blit(header_surface, (self.window_rect.x + x_offset, self.window_rect.y + y_offset))  # First column
                else:
                    self.screen.blit(header_surface, (self.window_rect.x + x_offset + first_column_width + (i - 1) * other_column_width, self.window_rect.y + y_offset))  # Other columns

            y_offset += 40  # Move down for the stat rows

            for stat_name, stat_values in self.player_stats.items():
                base_value, boost_value, total_value = stat_values  # Unpack tuple

                # Render the stat name and values
                stat_text = f"{stat_name}:"
                base_text = f"{base_value:.1f}"
                boost_text = f"+{boost_value:.1f}"
                total_text = f"{total_value:.1f}"

                # Display each stat with base value, boost (in green), and total
                stat_surface = self.font.render(stat_text, True, (255, 255, 255))  # White text
                base_surface = self.font.render(base_text, True, (255, 255, 255))  # White text
                boost_surface = self.font.render(boost_text, True, (0, 255, 0))  # Green for boost value
                total_surface = self.font.render(total_text, True, (255, 255, 255))  # White text

                # Adjust the horizontal spacing: first column wider
                self.screen.blit(stat_surface, (self.window_rect.x + x_offset, self.window_rect.y + y_offset))  # First column
                self.screen.blit(base_surface, (self.window_rect.x + x_offset + first_column_width, self.window_rect.y + y_offset))  # Second column (Base)
                self.screen.blit(boost_surface, (self.window_rect.x + x_offset + first_column_width + other_column_width, self.window_rect.y + y_offset))  # Third column (Boost)
                self.screen.blit(total_surface, (self.window_rect.x + x_offset + first_column_width + other_column_width * 2, self.window_rect.y + y_offset))  # Fourth column (Total)

                y_offset += 40  # Move down for next stat
