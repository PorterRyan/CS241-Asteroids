import flyingobject, arcade
import math
class Bullet(flyingobject.FlyingObject):
    """Bullet object"""
    def __init__(self, angle, velocityX, velocityY, centerX, centerY):
        super().__init__()
        self.center.x = centerX
        self.center.y = centerY
        self.ship_velocityX = velocityX
        self.ship_velocityY = velocityY
        self.rotation = angle + 90
        self.radius = 30
        self.speed = 10
        self.image = arcade.load_texture("images/laserBlue01.png")
        self.alive = True
        self.count = 60
        self.velocity.dx = math.cos(math.radians(self.rotation)) * self.speed  + self.ship_velocityX
        self.velocity.dy = math.sin(math.radians(self.rotation)) * self.speed + self.ship_velocityY
        self.width = 25
        self.height = 6
        self.hit_sound = arcade.load_sound("sounds/explosion.wav")
        
    def advance(self):
        """Advance the bullet"""
        super().advance()
        self.count -= 1
        if self.count <= 0:
            self.alive = False
    
    def draw(self):
        """Draw the bullet"""
        arcade.draw_texture_rectangle(self.center.x, self.center.y,self.width,self.height,self.image,self.rotation)

    def hit(self):
        """What happens if the bullet hits an asteroid."""
        self.alive = False
        arcade.sound.play_sound(self.hit_sound)
    
    def wrap(self):
        """Wrap the bullet"""
        super().wrap()
    
    def blast_sound():
        """Sound effects!"""
        sound = arcade.sound.load_sound("sounds/laser 5.mp3")
        #Sound from https://mrpoxl.itch.io/laser-sounds

        arcade.sound.play_sound(sound)
