import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self,ai_game): #ai_game references the AlienInvasion class

        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #allows us to place the ship in the correct location on the screen
        self.screen_rect = ai_game.screen.get_rect()   #rects = rectangles

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False   #means the ship is motionless
        self.moving_left = False

    #moves the ship right and left (updating the position of the ship) if the flag is True
    def update(self):
        """Update the ship's position based on the movement flags."""
        #2 if blocks used rather than an elif - allows ship's rect.x value to be increased & decreased when
        #both arrow keys ar held down: results in ship standing still

        # Update the ship's x value, not the rect.
        #limits the ship's range (prevents ship from disappearing of the edge of the screen)
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x    #controls the position of the ship

    #draws the ship to the screen
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) #draws the image to the screen @ position specified by self.rect

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x) #tracks ship's exact position
