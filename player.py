import pygame
from shot import Shot

from constants import (PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS)
from circleshape import CircleShape

class Player(CircleShape):
  def __init__(self, x, y):
    super().__init__(x, y, PLAYER_RADIUS)
    self.cooldown = 0
    
    self.rotation = 0
  def draw(self, screen):
    pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    # in the Player class
  def triangle(self):
    forward = pygame.Vector2(0, 1).rotate(self.rotation)
    right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
    a = self.position + forward * self.radius
    b = self.position - forward * self.radius - right
    c = self.position - forward * self.radius + right
    return [a, b, c]
  def rotate(self, dt):
    self.rotation += PLAYER_TURN_SPEED * dt
    
  def update(self, dt):
    self.cooldown -=dt
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        self.rotate(-dt)
    if keys[pygame.K_d]:
        self.rotate(dt)
    if keys[pygame.K_w]:
        self.move(dt)
    if keys[pygame.K_s]:
        self.move(-dt)
        
    if keys[pygame.K_SPACE]:
        
        self.shoot()
        
  def move(self, dt):
      unit_vector = pygame.Vector2(0, 1)
      rotated_vector = unit_vector.rotate(self.rotation)
      rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
      self.position += rotated_with_speed_vector
  
  def shoot(self):
    if self.cooldown > 0:
      return
    else:
      self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
    shot = Shot(self.position.x, self.position.y)
    shot_start = pygame.Vector2(0, 1)
    rotate_shot = shot_start.rotate(self.rotation)
    shot.velocity = rotate_shot * PLAYER_SHOOT_SPEED
  
  