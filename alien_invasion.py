import sys
from time import sleep  #pauses the game momentarily when ship is hit

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

#Create class AlienInvasion
class AlienInvasion:

    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.scree_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #this is the paramater that gives Ship access to the game's resources
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() 
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # Set the background color. Light Gray
        self.bg_color = (230, 230, 230)

        # Make the Play button.
        self.play_button = Button(self, "Play")

    #this method controls the game
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()  #calls the ship's update() method on each pass through the loop
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
        
    #detects relevant events (keypresses, keyreleases)    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():    #this function returns a list of events that've taken 
                                            #place since the last time this function was called
            if event.type == pygame.QUIT:  
                sys.exit()  #exits the game
            #responds when Pygame detects a KEYDOWN event
            #we use elifs bcs each event's only connected to one key
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:    
                self._check_keyup_events(event)
            #detects when a player clicks anywhere on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:  
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""

        #button_clicked stores a True OR False; game restarts only if Play is clicked & 
        #game is not currently active
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings() #resets the speed
            self.stats.reset_stats()    #giving player 3 new ships
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT: #event.key checks whether the RIGHT arrow key was pressed
            self.ship.moving_right = True   #when the player presses the RIGHT arrow key
                                                    #moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True    #if a KEYDOWN event occurs for K_LEFT key, moving_left = True
        #ends the game when the player presses "Q"
        elif event.key == pygame.K_q:
            sys.exit()
        #calls _fire_bullet() when the SPACEBAR is pressed
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT: #when player releases RIGHT arrow key, moving_right = False
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:    #if a KEYUP event occurs for K_LEFT key, moving_left = False
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        #Limits the player to 3 bullets at a time.
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()   #calls bullet.update() for each bullet placed in the group of bullets

        # Get rid of (delete) bullets that have disappeared.
        for bullet in self.bullets.copy():  #enables us to modify bullets inside the loop
            if bullet.rect.bottom <= 0:     #check if bulet has gone off the screen
                self.bullets.remove(bullet) #if yes, remove from bullets

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.

        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
                #groupcollide-returns a dictionary; key = bullet and value = alien that was hit
        collisions = pygame.sprite.groupcollide(    #compares the positions of all the bullets in self.bullets
                                                    #and all the aliens in self.aliens, and IDs any that overlap   
                self.bullets, self.aliens, True, True)  #the Trues tell Pygame to delete the bullets&aliens that collided
        
        #updates score each time an alien is shot down
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()    #creates a new image for the updated score

        #check whether the aliens group is empty
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()    #Removes existing bullets
            self._create_fleet()    #Repopulates the alien fleet
            self.settings.increase_speed()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
            then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()    #checks fleet's edges before updating aliens' positions
        self.aliens.update()

        # Look for alien-ship collisions.
            #spritecollideany() loops through the group aliens & returns the 1st alien that
            #collides w/ a sprite (bullet)
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing beteween each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size #get the aliens width from rect attribute
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            #creates the aliens in one row
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""    
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        #loops thorugh the fleet; calls check_edges() on each alien
        for alien in self.aliens.sprites():
            if alien.check_edges(): #if check_edges() = True, alien is at edge & needs to change direction
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        #loop through all aliens & drop each one using fleet_drop_speed
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 #change value of fleet direction (mult. current value by -1)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause. -- gives player time to see that their ship has been hit
            sleep(0.5)
        else:
            #game_active = False when player has used up all their ships
            self.stats.game_active = False
            #makes cursor visible once the game ends (so player can click PLAY again)
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            #an alien has reached the bottom when its rect.bottom >= the screen's rect.bottom
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()    #called when alien reaches the bottom
                break

    #Redraws the screen on each pass through the main loop
    def _update_screen(self): 
        '''Update images on the screen, and flip to the new screen.'''
        self.screen.fill(self.settings.bg_color)    #fill bckgrd using fill() method
        self.ship.blitme()  #draws the ship on the screen
                            #it appears on top of the background
        #returns a list of all sprites in the group "bullets" & loop through the sprites
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #draws alien to the screen
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
