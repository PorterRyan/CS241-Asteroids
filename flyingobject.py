from motion import Point, Velocity
from abc import ABC, abstractmethod
import arcade
class FlyingObject(ABC):
    """FlyingObject abstract class"""
    def __init__(self):
        """FlyingObject Initializer"""
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True
        self.rotation = 0.0
        self.acceleration = 0.0
        self.image = arcade.load_texture("images/placeholder.png")
        self.width = 30
        self.height = 30
    
    def advance(self):
        """Advance the flying object"""
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    
    def wrap(self):
        """Warp objects to the opposite side of the screen if they leave the screen."""
        if self.center.x > 800:
            self.center.x = 0
        
        if self.center.x < 0:
            self.center.x = 800
        
        if self.center.y > 600:
            self.center.y = 0
        
        if self.center.y < 0:
            self.center.y = 600

    def draw(self):
        """Draw the object."""
        arcade.draw_texture_rectangle(self.center.x, self.center.y,self.width,self.height,self.image,self.rotation,255)