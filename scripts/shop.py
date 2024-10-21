import pygame

class Shop:
    def __init__(self, screen_width, screen_height, house, materials_counter, stat_window, money_counter):
        # Set up fonts
        self.font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 25)
        self.tab_font = pygame.font.Font('assets/pixelify_font/PixelifySans-Regular.ttf', 28)

        # Reference to house, materials counter, stat window, and money counter
        self.house = house
        self.materials_counter = materials_counter
        self.stat_window = stat_window
        self.money_counter = money_counter

        # Load the shop button image
        try:
            self.shop_button_image = pygame.image.load('assets/ShoppingIMG.png').convert_alpha()
        except pygame.error as e:
            print(f"Unable to load image: {e}")

        # Resize the shop button image to fit the button area
        self.shop_button_width, self.shop_button_height = 80, 50
        self.shop_button_image = pygame.transform.scale(self.shop_button_image, (self.shop_button_width, self.shop_button_height))

        # Shop button rectangle for click detection
        self.shop_button_rect = self.shop_button_image.get_rect(topright=(screen_width - 20, 20))

        # Shop menu tabs (Buy, Upgrade, Craft, Repairs)
        self.tabs = ['Buy', 'Upgrade', 'Craft', 'Repairs']
        self.active_tab = 'Upgrade'  # Default active tab
        self.tab_rects = []  # List of tab rects for tab buttons
        self.upgrade_button_rects = []  # List of upgrade button rects

        # Shop dimensions (cover almost the entire screen)
        margin = 20  # Gap around the edges
        self.shop_width = screen_width - margin * 2
        self.shop_height = screen_height - margin * 2
        self.tab_area = pygame.Rect(margin, margin, self.shop_width, self.shop_height)

        # Close shop button
        self.close_button_rect = pygame.Rect(self.tab_area.x + 20, self.tab_area.bottom - 60, self.shop_width - 40, 40)
        self.close_button_color = (220, 20, 60)
        self.close_button_text_color = (255, 255, 255)

        # Flags to control shop state
        self.shop_open = False

        # Repair cost per health point
        self.scrap_per_repair = 5

        # Variable to store the repair button's rect
        self.repair_button = None

        # Upgrade prices for each stat
        self.upgrade_prices = {
            'Speed': 50,
            'Accuracy': 70,
            'Health Regen Rate': 80,
            'Building Regen Rate': 100
        }

    def draw_shop_button(self, surface):
        """Draw the shop button on the screen."""
        surface.blit(self.shop_button_image, self.shop_button_rect)

    def open_shop_menu(self, surface):
        """Display the shop menu with a transparent black background and styled buttons."""
        self.tab_rects.clear()
        self.upgrade_button_rects.clear()

        # Draw a transparent black background
        transparent_black = pygame.Surface((self.shop_width, self.shop_height), pygame.SRCALPHA)
        transparent_black.fill((0, 0, 0, 180))  # Black with alpha value for transparency
        surface.blit(transparent_black, (self.tab_area.x, self.tab_area.y))

        # Draw the tabs with improved visuals
        tab_height = 60
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(self.tab_area.x + 10, 20 + i * tab_height, 360, 50)
            self.tab_rects.append(tab_rect)

            if tab == self.active_tab:
                pygame.draw.rect(surface, (70, 130, 180), tab_rect, border_radius=8)  # Active tab with rounded corners
            else:
                pygame.draw.rect(surface, (160, 160, 160), tab_rect, border_radius=8)  # Inactive tab with rounded corners

            tab_text = self.tab_font.render(tab, True, (255, 255, 255))
            surface.blit(tab_text, (tab_rect.x + 30, tab_rect.y + 10))

        # Display the tab contents
        self.display_tab_contents(surface, content_y=20 + len(self.tabs) * tab_height + 40)

        # Draw the close shop button with gradient effect
        self.draw_gradient_button(surface, self.close_button_rect, self.close_button_color, (255, 80, 80), "Close Shop")

    def draw_gradient_button(self, surface, rect, color1, color2, text):
        """Draw a button with a gradient background and rounded corners."""
        button_surface = pygame.Surface((rect.width, rect.height))
        for i in range(rect.height):
            r = color1[0] + (color2[0] - color1[0]) * i // rect.height
            g = color1[1] + (color2[1] - color1[1]) * i // rect.height
            b = color1[2] + (color2[2] - color1[2]) * i // rect.height
            pygame.draw.line(button_surface, (r, g, b), (0, i), (rect.width, i))
        button_surface.set_alpha(220)  # Make the button slightly transparent
        surface.blit(button_surface, rect)

        # Draw the text on the button
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def display_repairs(self, surface, x, y):
        """Display the Repairs tab content."""
        repair_text = self.font.render("Repairs:", True, (255, 255, 255))
        surface.blit(repair_text, (x, y))

        house_image = pygame.image.load('assets/starterhouseIMG.png')
        house_image = pygame.transform.scale(house_image, (60, 60))
        surface.blit(house_image, (x, y + 50))

        health_bar_width = 120
        health_percentage = self.house.health / self.house.max_health
        pygame.draw.rect(surface, (255, 0, 0), (x + 70, y + 60, health_bar_width, 20))
        pygame.draw.rect(surface, (0, 255, 0), (x + 70, y + 60, int(health_bar_width * health_percentage), 20))

        health_text = self.font.render(f"{self.house.health}/{self.house.max_health}", True, (255, 255, 255))
        surface.blit(health_text, (x + 200, y + 55))

        if self.house.health < self.house.max_health:
            repair_cost = self.scrap_per_repair * (self.house.max_health - self.house.health)
            repair_cost_text = self.font.render(f"Cost: {repair_cost} scrap", True, (255, 255, 255))
            surface.blit(repair_cost_text, (x, y + 120))

            repair_button = pygame.Rect(x + 200, y + 120, 100, 40)
            self.draw_gradient_button(surface, repair_button, (70, 130, 180), (100, 150, 210), "Repair")
            return repair_button

        return None

    def display_upgrade_items(self, surface, x, y):
        """Display the Upgrade tab content."""
        upgrade_text = self.font.render("Upgrade abilities:", True, (255, 255, 255))
        surface.blit(upgrade_text, (x, y))

        self.upgrade_button_rects.clear()

        for i, (stat_name, price) in enumerate(self.upgrade_prices.items()):
            upgrade_item_text = f"Upgrade {stat_name}: {price} money"
            upgrade_item_surface = self.font.render(upgrade_item_text, True, (255, 255, 255))
            surface.blit(upgrade_item_surface, (x, y + 40 * (i + 1)))

            upgrade_button = pygame.Rect(x + 400, y + 40 * (i + 1), 120, 30)
            self.draw_gradient_button(surface, upgrade_button, (70, 130, 180), (100, 150, 210), "Upgrade")
            self.upgrade_button_rects.append((stat_name, upgrade_button))

    def display_tab_contents(self, surface, content_y):
        """Display content based on the active tab."""
        content_x = self.tab_area.x + 20
        if self.active_tab == 'Buy':
            self.display_buy_items(surface, content_x, content_y)
        elif self.active_tab == 'Upgrade':
            self.display_upgrade_items(surface, content_x, content_y)
        elif self.active_tab == 'Craft':
            self.display_craft_items(surface, content_x, content_y)
        elif self.active_tab == 'Repairs':
            self.repair_button = self.display_repairs(surface, content_x, content_y)

    def handle_events(self, event):
        """Handle events for shop button, menu, and close button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # If the shop button is clicked, this is already handled separately
            # Handle internal shop interactions only if the shop is open
            if self.shop_open:
                # Handle tab switching
                for tab, rect in zip(self.tabs, self.tab_rects):
                    if rect.collidepoint(mouse_pos):
                        self.active_tab = tab

                # Handle close shop button
                if self.close_button_rect.collidepoint(mouse_pos):
                    self.shop_open = False

                # Handle upgrade events
                if self.active_tab == 'Upgrade':
                    for stat_name, upgrade_button in self.upgrade_button_rects:
                        if upgrade_button.collidepoint(mouse_pos):
                            self.upgrade_stat(stat_name)

                # Handle repair events
                if self.active_tab == 'Repairs' and self.repair_button and self.repair_button.collidepoint(mouse_pos):
                    self.repair_house()
                    
    def handle_shop_button_click(self, event):
        """Handle the click event for the shop button to open/close the shop."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # If the shop button is clicked, toggle the shop open state
            if self.shop_button_rect.collidepoint(mouse_pos):
                self.shop_open = not self.shop_open

    def upgrade_stat(self, stat_name):
        """Upgrade the selected stat if the player has enough money."""
        stat_boost_amounts = {
            'Speed': 0.25,               # Character speed boost
            'Accuracy': 0.05,            # Character accuracy boost
            'Health Regen Rate': 0.02,   # Character health regen boost
            'Building Regen Rate': 0.01  # House health regen boost
        }

        price = self.upgrade_prices[stat_name]

        if self.money_counter.money >= price:
            # Deduct money for the upgrade
            self.money_counter.money -= price
            boost_amount = stat_boost_amounts.get(stat_name, 0.1)

            # Apply the boost to the corresponding stat
            if stat_name == 'Building Regen Rate':
                self.house.building_regen_rate += boost_amount  # Increase house regen rate
            else:
                self.stat_window.apply_stat_boost(stat_name, boost_amount)  # Apply character upgrades

            print(f"{stat_name} upgraded by {boost_amount}! Money left: {self.money_counter.money}")
            
            # Increase the upgrade price for the next time
            self.upgrade_prices[stat_name] = int(price * 1.2)
            print(f"New price for {stat_name} upgrade: {self.upgrade_prices[stat_name]}")
        else:
            print(f"Not enough money to upgrade {stat_name}.")

    def repair_house(self):
        """Repair the house if enough scrap is available."""
        repair_cost = self.scrap_per_repair * (self.house.max_health - self.house.health)
        if self.materials_counter.scrap >= repair_cost:
            self.materials_counter.scrap -= repair_cost
            self.house.health = self.house.max_health
            print(f"House repaired! Scrap left: {self.materials_counter.scrap}")
        else:
            print("Not enough scrap to repair the house.")

    def is_shop_open(self):
        """Return whether the shop is currently open."""
        return self.shop_open
