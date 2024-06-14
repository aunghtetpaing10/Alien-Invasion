import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to manage an alien"""

    def __init__(self, ai_game):
        """Initialize the alien and starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return true if alien hit the edge"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x