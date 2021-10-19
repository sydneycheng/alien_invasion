                        #####STARTING THE GAME PROJECT#####
#when RUN, this py file: returns an empty Pygame

#import sys and pygame modules
import sys
import pygame
from settings import Settings

#Create class AlienInvasion
class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  #we've created an insance of Settings
                                                                        #   & assigned it to self.settings
        #(1200,800) is a Tuple - defines the dimensions of the game window.
        #self.screen is an Attribute - will be available in all methods in the class

        #the Object we assigned to self.screen is called a Surface
            #SURFACE - a part of the screen where a game element can be displayed
            #each element in the game (ex: alien,ship) is its own surface
            #the surface returned by display.set_mode() represents the entire game window
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        # Set the background color. Light Gray
        self.bg_color = (230, 230, 230)

    #this method controls the game
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            #EVENT - an action that the user performs while plaing the game, such as pressing a key or moving the mouse
            #EVENT LOOP - makes our program respond to events by listening for events and performing appropriate 
            #   tasks depending on the kinds of events that occur
            for event in pygame.event.get():    #this function returns a list of events that've taken 
                                                #place since the last time this function was called
                if event.type == pygame.QUIT:  
                    sys.exit()                  #exits the game
            
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color) #fill bckgrd using fill() method, which acts on a surface and only
                                            #   takes one argument: a color

            # Make the most recently drawn screen visible.
            pygame.display.flip() 

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

