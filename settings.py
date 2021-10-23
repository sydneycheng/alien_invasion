class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_speed = 1.5 #when ship moves, its position is adjusted by 1.5 pixels
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0

        #creates settings for fleet direction
        self.fleet_drop_speed = 10  #controls how quickly the fleet drops down each time alien hits edge
        # fleet_direction of 1 represents right; -1 represnets left.
        self.fleet_direction = 1
        