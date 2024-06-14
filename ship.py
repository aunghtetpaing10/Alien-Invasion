import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """To manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # Movement
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """Update the ship's position"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x


    def blitme(self):
        self.screen.blit(self.image, self.rect)

    
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)