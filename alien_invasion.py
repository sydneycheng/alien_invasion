import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

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
        #this is the paramater that gives Ship access to the game's resources
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() 

        # Set the background color. Light Gray
        self.bg_color = (230, 230, 230)

    #this method controls the game
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()  #calls the ship's update() method on each pass through the loop
            self._update_bullets()
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

    #Redraws the screen on each pass through the main loop
    def _update_screen(self): 
            '''Update images on the screen, and flip to the new screen.'''
            self.screen.fill(self.settings.bg_color)    #fill bckgrd using fill() method
            self.ship.blitme()  #draws the ship on the screen
                                #it appears on top of the background
            #returns a list of all sprites in the group "bullets" & loop through the sprites
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # Make the most recently drawn screen visible.
            pygame.display.flip() 

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
