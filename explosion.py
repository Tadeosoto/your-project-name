import pygame  # drawing and timing
from constants import EXPLOSION_DURATION, LINE_WIDTH  # how long the animation lasts and line width

# Added: simple expanding-circle explosion animation
class Explosion(pygame.sprite.Sprite):  # standalone sprite that animates then removes itself
    def __init__(self, x, y, start_radius=6, end_radius=40, color=(255, 255, 255), *groups):  # position, size range, color
        super().__init__(*groups)  # attach to any sprite groups passed in
        self.position = pygame.Vector2(x, y)  # center of the explosion
        self.elapsed = 0.0  # time since spawned
        self.duration = EXPLOSION_DURATION  # how long to animate before removing
        self.start_radius = start_radius  # initial circle radius
        self.end_radius = end_radius  # final circle radius when finished
        self.color = color  # draw color (white to match vector art)

    def update(self, dt):  # advance animation timer
        self.elapsed += dt  # accumulate delta time
        if self.elapsed >= self.duration:  # once finished
            self.kill()  # remove from all groups to stop drawing/updating

    def draw(self, screen):  # render the current frame
        t = max(0.0, min(1.0, self.elapsed / self.duration))  # normalize progress 0..1
        radius = int(self.start_radius + (self.end_radius - self.start_radius) * t)  # interpolate radius
        alpha = int(255 * (1.0 - t))  # fade out over time
        # draw with fading alpha by creating a temporary surface
        surf = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)  # transparent surface around circle
        pygame.draw.circle(surf, (*self.color, alpha), (radius + 2, radius + 2), radius, LINE_WIDTH)  # circle with alpha
        screen.blit(surf, (self.position.x - radius - 2, self.position.y - radius - 2))  # center the surface on position

