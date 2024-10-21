# startup_selections.py
from scripts.team_boosts import TEAM_BOOSTS  # Import the boost dictionary
import pygame

# Step 1: Intro Step
class IntroStep:
    def __init__(self, screen_width, screen_height):
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)
        self.continue_button_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)
        
        # Explanation text
        self.story_text = [
            "In a post-zombie-infested world, you are part of a hired",
            "security team. Your job is to protect a wealthy family",
            "from the remaining zombie threat."
        ]
        
        # Button to proceed
        self.continue_text = self.continue_button_font.render("Continue", True, (0, 0, 0))
        self.continue_rect = self.continue_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))

    def draw(self, surface):
        """Draw the intro story and continue button."""
        surface.fill((255, 255, 255))  # Clear the screen

        # Draw the story text
        y_offset = 100
        for line in self.story_text:
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += 40

        # Draw the continue button
        surface.blit(self.continue_text, self.continue_rect)
        pygame.display.flip()

    def handle_events(self, event):
        """Handle click on the continue button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.continue_rect.collidepoint(mouse_pos):
                print("Continue button clicked")  # Debugging line
                return "continue"
        return None

# Step 2: Family Selection Step
class FamilySelectionStep:
    def __init__(self, screen_width, screen_height):
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)
        self.button_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)

        # Families to choose from
        self.families = ["The Wellingtons", "The Andersons", "The Harpers"]
        self.family_buttons = []
        self.selected_family = None

        # Create family buttons
        for index, family in enumerate(self.families):
            button_text = self.button_font.render(family, True, (0, 0, 0))
            button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + index * 60))
            self.family_buttons.append((button_text, button_rect))

    def draw(self, surface):
        """Draw the family selection buttons."""
        surface.fill((255, 255, 255))

        # Draw the family selection text
        header = self.font.render("Select the family you are protecting:", True, (0, 0, 0))
        header_rect = header.get_rect(center=(surface.get_width() // 2, surface.get_height() // 4))
        surface.blit(header, header_rect)

        # Draw family buttons
        for button_text, button_rect in self.family_buttons:
            surface.blit(button_text, button_rect)
        pygame.display.flip()

    def handle_events(self, event):
        """Handle family selection clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            for family_text, rect in self.family_buttons:
                if rect.collidepoint(mouse_pos):
                    self.selected_family = family_text
                    print(f"Selected family: {self.selected_family}")  # Debugging line
                    return "team_selection"  # Proceed to the next step
        return None


# Step 3: Team Selection Step
class TeamSelectionStep:
    TEAM_BOOSTS = {
        "Sniper": {"Accuracy": 5},  # Sniper boosts Accuracy by +5
        "Machine Gunner": {"Damage": 10, "Fire Rate": -0.05},  # Machine Gunner improves fire rate (lower interval)
        "Medic": {"Health Regen Rate": 0.1},  # Medic increases health regeneration rate
        "Engineer": {"Building Regen Rate": 0.05}  # Engineer increases building regeneration rate
    }

    def __init__(self, screen_width, screen_height, stat_window):
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)
        self.button_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)

        # Team roles
        self.roles = ["Sniper", "Machine Gunner", "Medic", "Engineer"]
        self.role_buttons = []
        self.selected_roles = []

        # Reference to the stat window (for applying boosts)
        self.stat_window = stat_window  # The stat window to apply stat boosts

        # Create role buttons
        for index, role in enumerate(self.roles):
            button_text = self.button_font.render(role, True, (0, 0, 0))
            button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + index * 60))
            self.role_buttons.append((role, button_text, button_rect))

        # Counter text
        self.counter_text = self.font.render("0/2 selected", True, (0, 0, 0))
        self.counter_rect = self.counter_text.get_rect(center=(screen_width // 2, screen_height // 4 - 50))

        # Continue button (initially hidden)
        self.continue_text = self.button_font.render("Continue", True, (0, 0, 0))
        self.continue_rect = self.continue_text.get_rect(center=(screen_width // 2, screen_height - 100))
        self.show_continue_button = False

    def draw(self, surface):
        """Draw the team role selection buttons and counter."""
        surface.fill((255, 255, 255))

        # Draw the team selection text
        header = self.font.render("Select your security team members:", True, (0, 0, 0))
        header_rect = header.get_rect(center=(surface.get_width() // 2, surface.get_height() // 4))
        surface.blit(header, header_rect)

        # Draw role buttons
        for role, button_text, button_rect in self.role_buttons:
            surface.blit(button_text, button_rect)

        # Draw the counter
        self.counter_text = self.font.render(f"{len(self.selected_roles)}/2 selected", True, (0, 0, 0))
        surface.blit(self.counter_text, self.counter_rect)

        # Draw the continue button if 2 selections are made
        if self.show_continue_button:
            surface.blit(self.continue_text, self.continue_rect)

        pygame.display.flip()

    def handle_events(self, event):
        """Handle role selection clicks and continue button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()

            # Check if the user clicked on a role button
            for role, _, button_rect in self.role_buttons:
                if button_rect.collidepoint(mouse_pos):
                    if role in self.selected_roles:
                        self.selected_roles.remove(role)  # Deselect if already selected
                    elif len(self.selected_roles) < 2:
                        self.selected_roles.append(role)  # Select if less than 2 selected

            # Update continue button visibility
            if len(self.selected_roles) == 2:
                self.show_continue_button = True
            else:
                self.show_continue_button = False

            # Check if the user clicked the continue button
            if self.show_continue_button and self.continue_rect.collidepoint(mouse_pos):
                print("Continue button clicked, applying boosts.")  # Debugging line
                self.apply_team_boosts(self.selected_roles)  # Apply boosts
                return "game_start"

        return None

    def apply_team_boosts(self, selected_team):
        """Apply the stat boosts based on the selected team members."""
        for member in selected_team:
            boosts = self.TEAM_BOOSTS.get(member, {})
            for stat, boost_value in boosts.items():
                self.stat_window.apply_stat_boost(stat, boost_value)
                print(f"Boost applied for {member}: {stat} increased by {boost_value}")
