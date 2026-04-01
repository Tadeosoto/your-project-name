import random  # used to randomize star positions/speeds
import pygame  # pygame primitives for vectors/drawing
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STAR_COUNT, STAR_SPEED_MIN, STAR_SPEED_MAX  # screen and star settings


class Star(pygame.sprite.Sprite):  # represents a single background star
    # New: represents a single background star that scrolls down and wraps to the top
    def __init__(self, group):  # group so we can manage many stars together
        super().__init__(group)  # add this star to the provided sprite group
        self.position = pygame.Vector2(  # use a vector for easy movement
            random.uniform(0, SCREEN_WIDTH),  # random initial X across the width
            random.uniform(0, SCREEN_HEIGHT),  # random initial Y across the height
        )
        self.speed = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)  # variable speed to add depth
        # slightly vary star size/brightness
        self.radius = random.choice([1, 1, 1, 2])  # mostly small
        self.color = "white"  # white stars for classic space look

    def update(self, dt):  # move star each frame
        self.position.y += self.speed * dt  # move star downward each frame
        if self.position.y > SCREEN_HEIGHT:  # when past bottom edge
            self.position.y = -2  # wrap to the top when going off-screen
            self.position.x = random.uniform(0, SCREEN_WIDTH)  # re-randomize X
            self.speed = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)  # and speed

    def draw(self, screen):  # render the star
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)  # draw a tiny circle


class Starfield(pygame.sprite.Sprite):  # manages a collection of stars
    # New: lightweight manager that owns a group of stars and forwards update/draw
    def __init__(self, updatable_group, drawable_group):  # groups to plug into game loop
        super().__init__()  # not auto-adding to star group; this object is its own entity
        self._stars = pygame.sprite.Group()  # internal group holding all star sprites
        self._drawable = drawable_group  # reference to global drawable group
        self._updatable = updatable_group  # reference to global updatable group
        for _ in range(STAR_COUNT):  # seed the field with many stars
            star = Star(self._stars)  # create and add to internal star group
            # chain-adding to the shared groups by proxy (iterate when drawing/updating)
        # Register this manager object to the engine groups so its update/draw are called under others
        self.add(self._updatable)  # allow game loop to call update() on this manager
        self.add(self._drawable)  # allow game loop to call draw() on this manager

    def update(self, dt):  # called by the game loop each frame
        self._stars.update(dt)  # advance all stars

    def draw(self, screen):  # called by the game loop to render
        for star in self._stars:  # render stars behind gameplay objects
            star.draw(screen)  # each star knows how to draw itself

