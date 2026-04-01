import pygame  # input and drawing
from shot import Shot  # projectile entity

from constants import (PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_RESPAWN_TIME, PLAYER_INVULNERABLE_TIME)  # player + timing constants
from circleshape import CircleShape  # base class
from sound import play_shoot  # Added: play shoot sfx

class Player(CircleShape):
  def __init__(self, x, y):
    super().__init__(x, y, PLAYER_RADIUS)  # set up position/velocity/radius
    self.cooldown = 0  # time until next allowed shot
    
    self.rotation = 0  # current facing in degrees
    # Added: life/death & timers
    self.alive = True  # whether the ship can act/draw
    self.respawn_timer = 0  # countdown while dead
    self.invulnerable_timer = 0  # brief safety after respawn
  def draw(self, screen):
    if not self.alive:
      return  # do not draw when dead
    # blink while invulnerable
    if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
      return  # skip some frames to blink
    pygame.draw.polygon(screen, "blue", self.triangle(), LINE_WIDTH)  # draw triangle ship
    # in the Player class
  def triangle(self):
    forward = pygame.Vector2(0, 1).rotate(self.rotation)  # ship forward vector
    right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # right vector for base width
    a = self.position + forward * self.radius  # nose point
    b = self.position - forward * self.radius - right  # left base
    c = self.position - forward * self.radius + right  # right base
    return [a, b, c]  # triangle vertices
  def rotate(self, dt):
    self.rotation += PLAYER_TURN_SPEED * dt  # continuous rotation by input
    
  def update(self, dt):
    self.cooldown -=dt  # tick down shoot cooldown
    # handle respawn countdown
    if not self.alive:
      self.respawn_timer -= dt  # progress toward respawn
      if self.respawn_timer <= 0:
        # come back to life with brief invulnerability
        self.alive = True  # re-enable input/drawing
        self.invulnerable_timer = PLAYER_INVULNERABLE_TIME  # start safety window
      return  # skip normal input while dead

    # update invulnerability timer if alive
    if self.invulnerable_timer > 0:
      self.invulnerable_timer -= dt  # tick down safety
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        self.rotate(-dt)  # rotate left
    if keys[pygame.K_d]:
        self.rotate(dt)  # rotate right
    if keys[pygame.K_w]:
        self.move(dt)  # thrust forward
    if keys[pygame.K_s]:
        self.move(-dt)  # reverse thrust
        
    if keys[pygame.K_SPACE]:
        
        self.shoot()  # fire shot if cooldown ready
        
  def move(self, dt):
      unit_vector = pygame.Vector2(0, 1)  # up vector
      rotated_vector = unit_vector.rotate(self.rotation)  # face direction
      rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt  # scale by speed
      self.position += rotated_with_speed_vector  # move ship
  
  def shoot(self):
    if not self.alive:
      return  # cannot shoot when dead
    if self.cooldown > 0:
      return  # still cooling down
    else:
      self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS  # reset cooldown
    shot = Shot(self.position.x, self.position.y)  # create projectile at ship
    shot_start = pygame.Vector2(0, 1)  # base forward
    rotate_shot = shot_start.rotate(self.rotation)  # aim by ship rotation
    shot.velocity = rotate_shot * PLAYER_SHOOT_SPEED  # set projectile speed
    play_shoot()  # play sfx
  
  # Added: trigger a death and start respawn countdown
  def die(self):
    self.alive = False  # mark dead
    self.respawn_timer = PLAYER_RESPAWN_TIME  # start countdown
    # place player at center (caller may adjust)
    # visual handled by explosion sprite in main
  
  # Added: safely reset player position/rotation on respawn start
  def reset_position(self, x, y):
    self.position.x = x  # set X
    self.position.y = y  # set Y
    self.rotation = 0  # face up
  
  