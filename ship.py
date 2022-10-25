from abc import abstractmethod
import math
from motion import Point, Velocity
import arcade
from flyingobject import FlyingObject as fo

class Ship(fo):
    """Ship object"""
    def __init__(self,radius,thrust):
        """Ship Initializer"""
        super().__init__()
        self.radius = radius
        self.rotation = 0
        self.rotation_speed = 3
        self.acceleration = thrust
        self.center.x = 400
        self.center.y = 300
        self.image = arcade.load_texture("images/ship.png")
        self.image_standard = arcade.load_texture("images/ship.png")
        self.thrusters = arcade.load_texture("images/ship_thrust.png")
        self.width = 48
        self.height = 48

    def rotate(self,direction):
        """Rotate the ship"""
        if direction == "LEFT":
            self.rotation += 3
        else:
            self.rotation -= 3

    def thrust(self,direction):
        """Accelerate the ship appropriately"""
        if direction == "UP":
            self.velocity.dx += math.cos(math.radians(self.rotation + 90)) * self.acceleration
            self.velocity.dy += math.sin(math.radians(self.rotation + 90)) * self.acceleration
        
        if direction == "DOWN":
            self.velocity.dx -= math.cos(math.radians(self.rotation + 90)) * self.acceleration
            self.velocity.dy -= math.sin(math.radians(self.rotation + 90)) * self.acceleration
    
    def stop(self):
        """Instantly stop the ship."""
        self.velocity.dx = 0.0
        self.velocity.dy = 0.0

    
    def draw(self):
        """Draw the ship."""
        super().draw()

    def crash(self):
        """If we crash we're dead."""
        self.alive = False
