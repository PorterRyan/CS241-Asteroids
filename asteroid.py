from motion import Point, Velocity
from abc import ABC, abstractmethod
import random
import math
import arcade
from flyingobject import FlyingObject as fo

class Asteroid(fo):
    """Asteroid class"""
    def __init__(self):
        """Initializer"""
        super().__init__()
        
        self.center.x = random.uniform(0,800)
        self.center.y = random.uniform(0,600)

        self.direction = random.uniform(0,360)
        self.rotation = 0 #Current rotational degree
        self.speed = 0 #Movement speed
        self.spin = 0 #Degrees to spin per frame
        self.radius = 0 #Collision radius
        self.velocity = Velocity()
        self.alive = True
        self.width = 0
        self.height = 0

    def advance(self):
        """Perform this action every frame."""
        super().advance()
        self.rotation += self.spin #Rotate
    
    def hit(self):
        """If the asteroid it hit by a laser it is dead."""
        self.alive = False

    def wrap(self):
        """We must warp around the screen!"""
        super().wrap()
    
    def draw(self):
        """Each asteroid must have a draw function!"""
        arcade.draw_texture_rectangle(self.center.x,self.center.y,self.width,self.height,self.image,self.rotation)

class LargeAsteroid(Asteroid):
    """Large Asteroid class"""
    def __init__(self):
        """Initializer"""
        super().__init__()
        self.speed = 1.5
        self.spin = 1
        self.radius = 15
        self.image = arcade.load_texture("images/meteorGrey_big1.png")
        self.width = 101
        self.height = 84

        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.direction)) * self.speed
    
    def draw(self):
        """Draw the asteroid."""
        super().draw()

    def hit(self):
        """End the asteroid when it gets hit."""
        self.alive = False
    
    def break_up(self):
        """Break the asteroid into smaller chunks"""
        first_chunk = MediumAsteroid(self.center.x,self.center.y,self.velocity.dy+2,self.velocity.dx)
        second_chunk = MediumAsteroid(self.center.x,self.center.y,self.velocity.dy-2,self.velocity.dx)
        third_chunk = SmallAsteroid(self.center.x,self.center.y,self.velocity.dx+5,self.velocity.dy)
        return first_chunk, second_chunk, third_chunk # This probably won't work, gonna have to work on it some more

    def advance(self):
        """Update every frame"""
        super().advance()
    
    def wrap(self):
        """Wrap around the screen"""
        super().wrap()

class MediumAsteroid(Asteroid):
    """Medium Asteroid class"""
    def __init__(self, centerX, centerY, speedY, speedX):
        """Initializer"""
        super().__init__()

        self.center.x = centerX
        self.center.y = centerY
        self.angle = 0
        self.spin = -2
        self.radius = 5
        self.width = 43
        self.height = 43
        self.image = arcade.load_texture("images/meteorGrey_med1.png")
        self.velocity.dy = speedY
        self.velocity.dx = speedX
    
    def draw(self):
        """Draw the asteroid."""
        arcade.draw_texture_rectangle(self.center.x,self.center.y,self.width,self.height,self.image,self.rotation)

    def advance(self):
        """Advance the asteroid"""
        super().advance()
    
    def wrap(self):
        """Warp around the screen!"""
        super().wrap()
    
    def break_up(self):
        """The asteroid breaks into smaller chunks when hit by a laser"""
        first_chunk = SmallAsteroid(self.center.x,self.center.y,self.velocity.dx+1.5,self.velocity.dy+1.5)
        second_chunk = SmallAsteroid(self.center.x,self.center.y,self.velocity.dx-1.5,self.velocity.dy-1.5)
        return first_chunk, second_chunk

    def hit(self):
        """What to do when the asteroid is hit"""
        self.alive = False

class SmallAsteroid(Asteroid):
    """Small asteroid class"""
    def __init__(self, centerX, centerY, speedX, speedY):
        """Initializer"""
        super().__init__()

        self.center.x = centerX
        self.center.y = centerY
        self.radius = 2
        self.spin = 5
        self.width, self.height = 28, 28
        self.image = arcade.load_texture("images/meteorGrey_small1.png")

        self.velocity.dx = speedX
        self.velocity.dy = speedY

    def hit(self):
        """What to do when the asteroid is hit"""
        
        arcade.draw_texture_rectangle(self.center.x,self.center.y,80,80,self.image)
        self.alive = False
    
    def wrap(self):
        """Wrap around the screen"""
        super().wrap()
    
    def advance(self):
        """Advance the asteroid"""
        super().advance()
    
    def draw(self):
        """Draw the asteroid"""
        arcade.draw_texture_rectangle(self.center.x,self.center.y,self.width,self.height,self.image,self.rotation)
    
    def break_up(self):
        """We don't break up the small asteroids, we delete them."""
        pass

# Explosion Properties
#Courtesy of Arcade library
particle_gravity = 0 #No gravity because we're in SPAAAAACE
particle_fade_rate = 8
particle_min_speed = 2.5
particle_speed_range = 2.5
particle_count = 20
particle_radius = 3
particle_colors = [arcade.color.ALIZARIN_CRIMSON,
                   arcade.color.COQUELICOT,
                   arcade.color.LAVA,
                   arcade.color.KU_CRIMSON,
                   arcade.color.DARK_TANGERINE]
particle_sparkle_chance = 0.02

class Particle(arcade.SpriteCircle):
    """Explosion particle"""
    def __init__(self, my_list):
        color = random.choice(particle_colors)
        super().__init__(particle_radius, color)
        self.normal_texture = self.texture
        self.my_list = my_list
        speed = random.random() * particle_speed_range + particle_min_speed
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed
        self.my_alpha = 255
        
    def update(self):
        """Update the explosion"""
        if self.my_alpha <= particle_fade_rate:
            self.remove_from_sprite_lists()
        else:
            self.my_alpha -= particle_fade_rate
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= particle_gravity #This does nothing because we're in space.

            if random.random() <= particle_sparkle_chance:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width),arcade.color.WHITE)
            else:
                self.texture = self.normal_texture
    



    
