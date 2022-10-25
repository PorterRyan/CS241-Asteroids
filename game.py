"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others

This program implements the asteroids game.

Additional Features:
- Background starscape
- Laser blast sounds
- Game Over screen
- Winner screen
- Background music
- Thruster effects
- Explosion particle effects
- Instant stop button
"""
import arcade
from motion import Point, Velocity
from ship import Ship
import asteroid
import flyingobject
import random
from bullet import Bullet

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2
  



class Game(arcade.View):
    """
    We are using Views instead of just a single window. This enables us to
    easily create a "Game Over" screen when the player dies or all asteroids
    are destroyed.
    """

    def __init__(self):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()
        self.background = None
        self.held_keys = set()
        self.asteroids = None
        self.player_list = None
        self.explosions = None
        self.player = None

        self.asteroids = []
        for i in range(0,5):
            self.asteroids.append(asteroid.LargeAsteroid())
        
        self.player = Ship(SHIP_RADIUS,SHIP_THRUST_AMOUNT)
        self.music = arcade.Sound("sounds/background_music.mp3")
        self.lasers = []     
       
    def setup(self):
        """Set up our starting field"""
        #Background image by Screaming Brain Studios
        self.background = arcade.load_texture("images/background.png")

        #Background Music by Abstraction: http://www.abstractionmusic.com/
        self.music = self.music.play(volume=0.8,loop=True)

        self.explosions = arcade.SpriteList()

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        #Draw the background
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)

        #Draw the asteroids
        for i in self.asteroids:
            i.draw()
        
        #Draw the explosions (if applicable)
        self.explosions.draw()

        #Draw the player. Only bother if the player is alive.
        if self.player.alive:
            self.player.draw()
        
        #Draw the lasers.
        for i in self.lasers:
            i.draw()
        
        

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        #Advance the asteroids
        for i in self.asteroids:
            i.advance()

        #Advance the lasers
        for i in self.lasers:
            i.advance()
        
        #Advance the player.
        self.player.advance()
        
        #Check for wrapping around the screen.
        self.check_wrap()

        #Get rid of dead sprites.
        self.cleanup_zombies()

        #Check if we've hit anything.
        self.check_collisions()
        
        #If the player dies, open the Game Over screen
        if not self.player.alive:
            game_over = GameOverView()
            self.window.show_view(game_over)
            arcade.stop_sound(self.music)
        
        #If the player wins, open the Winner screen
        if not self.asteroids:
            game_over = WinnerView()
            self.window.show_view(game_over)
            arcade.stop_sound(self.music)
        
        #Advance the explosion particles
        self.explosions.update()


    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.player.rotate("LEFT")

        if arcade.key.RIGHT in self.held_keys:
            self.player.rotate("RIGHT")

        if arcade.key.UP in self.held_keys:
            self.player.thrust("UP")
            self.player.image = self.player.thrusters

        if arcade.key.DOWN in self.held_keys:
            self.player.thrust("DOWN")
        
        if arcade.key.X in self.held_keys:
            self.player.stop() # Instantly stop the ship if the X key is pressed.

        #I decided to not implement a machine gun feature.


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.player.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                self.lasers.append(Bullet(self.player.rotation,
                self.player.velocity.dx,self.player.velocity.dy,
                self.player.center.x,self.player.center.y))
                Bullet.blast_sound() #PEW PEW
        
    def check_collisions(self):
        """Check for laser and asteroid collisions."""
        #Laser/Asteroid Collisions
        for laser in self.lasers:
            for rock in self.asteroids:
                if laser.alive and rock.alive:
                    strike = laser.radius + rock.radius

                    if (abs(laser.center.x - rock.center.x) < strike and
                        abs(laser.center.y - rock.center.y) < strike):
                        laser.hit()
                        if isinstance(rock, asteroid.LargeAsteroid) or isinstance(rock, asteroid.MediumAsteroid):
                            for chunk in rock.break_up():
                                self.asteroids.append(chunk)
                                for i in range(asteroid.particle_count):
                                    particle = asteroid.Particle(self.explosions)
                                    particle.position = rock.center.x,rock.center.y
                                    self.explosions.append(particle)
                        else:
                            particle = asteroid.Particle(self.explosions)
                            particle.position = rock.center.x,rock.center.y
                            self.explosions.append(particle)
                        rock.hit()
        
        #Asteroid/Ship Collisions
        for rock in self.asteroids:
            if self.player.alive and rock.alive:
                crash = self.player.radius + rock.radius

                if (abs(self.player.center.x - rock.center.x) < crash and
                    abs(self.player.center.y - rock.center.y) < crash):
                    self.player.crash()

        #Uncomment the following to monitor asteroid creation.
        #print(self.asteroids)     

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
        
        #Show the ship sprite with thrusters when thrusting up.
        if not arcade.key.UP in self.held_keys:
            self.player.image = self.player.image_standard

    def game_over(self):
        arcade.draw

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
        for laser in self.lasers:
            if not laser.alive:
                self.lasers.remove(laser)
    
    def check_wrap(self):
        self.player.wrap()
        for i in self.asteroids:
            i.wrap()
        for i in self.lasers:
            i.wrap()

class GameOverView(arcade.View):
    """Game Over Screen"""
    def __init__(self):
        """Initializer"""
        super().__init__()

    def on_show(self):
        """Set background color to black"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_texture_rectangle(400,300,448,109,arcade.load_texture("images/game_over.png"))
        arcade.draw_text("Click to restart", 310, 100, arcade.color.WHITE, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Restart the game when the user clicks."""
        game_view = Game()
        game_view.setup()
        self.window.show_view(game_view)

class WinnerView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_texture_rectangle(400,300,738,225,arcade.load_texture("images/winner2.png"))
        arcade.draw_text("Click to restart", 310, 100, arcade.color.WHITE, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.setup()
        self.window.show_view(game_view)

# Creates the game and starts it going
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,"Asteroids by Ryan Porter")
game = Game()
game.setup()
window.show_view(game)
arcade.run()