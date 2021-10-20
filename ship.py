                        #####CREATING A SHIP CLASS#####

import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self,ai_game): #ai_game references the AlienInvasion class

        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen    #screen is an attribute of Ship
        #allows us to place the ship in the correct location on the screen
        self.screen_rect = ai_game.screen.get_rect()   #rects = rectangles

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()   #allows us to access the ship surface's rect
                                            #attribute so we can later use it to place
                                            #the ship
        #returns  a surface representing the ship, which we assign to self.image

        #Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) #draws the image to the screen @ position specified by self.rect

        #RECT OBJECTS
        #use x- and y-coordinates of the top, bottom, left, and right edges of the rectangle,
            #as well as the center, to place the object. Use any of these values to est the current
            #position of the rect.'
        #when centering a game eement, work w the center, centerx, or centery attributes of a rect
        #when working at the edge of the screen, work w the top, bottom, left, or right attributes.
        #can also combine these properties: midbottom, midtop, midleft, and midright
        #when adgjusting the horizontal or vertical placement, you can use the x and y attributes

        #in Pygame, the origin (0,0) is at the top left corner
