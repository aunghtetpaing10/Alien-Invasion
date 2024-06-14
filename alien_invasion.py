import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""

        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_fleet()
        self.stats = GameStats(self)
        self.button = Button(self, "Play")
        self.sb = Scoreboard(self)
        self.game_active = False
        pygame.display.set_caption("Alien Invasion")

    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.check_events()

            if self.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()
            self.clock.tick(60)

    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        
        self.check_aliens_hit_bottom()


    def create_fleet(self):
        """Create a fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - alien_height * 3):
            while current_x < (self.settings.screen_width - alien_width * 2):
                self.create_alien(current_x, current_y)
                current_x += alien_width * 2
            current_x = alien_width
            current_y += alien_height * 2

    def create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
    def update_bullets(self):
        """Update the bullets and delete the old bullets"""        
        self.bullets.update()

        # Get rid of bullets that have disappered
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_collisions()

        

    def check_collisions(self):
        """Check if bullets hit aliens and remove them"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)



    def check_aliens_hit_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.ship_hit()
                break

    def check_play_button(self, mouse_pos):
        if self.button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.start_game()

    def start_game(self):
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_ships()
        self.game_active = True
        self.bullets.empty()
        self.aliens.empty()
        self.create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)
                

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_p:
            self.start_game()
        
            

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    
    def update_screen(self):
        """Update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.game_active:
            self.button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    app = AlienInvasion()
    app.run_game()