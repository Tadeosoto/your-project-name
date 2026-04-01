import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from shot import Shot
import sys
from background import Starfield  # Added: scrolling starfield background
from constants import ASTEROID_MIN_RADIUS  # Added: used to compute score by asteroid size
from constants import PLAYER_START_LIVES, PLAYER_INVULNERABLE_TIME, SCREEN_WIDTH, SCREEN_HEIGHT  # Added: lives and screen constants
from explosion import Explosion  # Added: explosion animations
from sound import play_explosion  # Added: explosion SFX
from highscore import load_high_score, save_high_score  # Added: persistent high score helpers


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    # Added: create starfield first so it draws underneath all gameplay elements
    Starfield(updatable, drawable)  # background manager plugged into engine groups
    Player.containers = (updatable, drawable)
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2 )
    asteroids =  pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    AsteroidField()
    shots = pygame.sprite.Group()
    Shot.containers = (shots, drawable, updatable)

    # Added: scoring state + font for HUD
    score = 0  # current run score
    font = pygame.font.SysFont(None, 28)  # small font for HUD text
    # Added: lives and game state
    lives = PLAYER_START_LIVES  # how many hits we can take
    game_over = False  # whether game over overlay is active
    # Added: load persistent high score at start
    high_score = load_high_score()  # read best score from disk

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)  # updates now also advance the starfield
        if not game_over:  # skip gameplay when game over overlay is shown
            for asteroid in asteroids:
                # player collision
                if player.alive and player.invulnerable_timer <= 0 and player.collides_with(asteroid):  # valid hit?
                    log_event("player_hit")  # analytics/log
                    # spawn explosion at player pos
                    Explosion(player.position.x, player.position.y, 10, 60, (255, 255, 255), drawable, updatable)  # player boom
                    play_explosion()  # play boom
                    lives -= 1  # lose a life
                    player.die()  # start respawn timer
                    player.reset_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # move to center for respawn
                    if lives < 0:  # when we drop below zero, end the run
                        game_over = True  # trigger overlay
                # shots collision
                for shot in list(shots):
                    if shot.collides_with(asteroid):  # projectile hit
                        log_event("asteroid_shot")  # analytics/log
                        # Added: award points based on asteroid size (smaller gives more)
                        kind = max(1, round(asteroid.radius / ASTEROID_MIN_RADIUS))  # derive asteroid size index
                        if kind <= 1:
                            score += 100  # small = hardest
                        elif kind == 2:
                            score += 50  # medium
                        else:
                            score += 20  # large
                        # explosion at asteroid pos
                        Explosion(asteroid.position.x, asteroid.position.y, 6, 40, (255, 255, 255), drawable, updatable)  # asteroid boom
                        play_explosion()  # play boom
                        asteroid.split()  # split or remove asteroid
                        shot.kill()  # remove projectile
        # player.draw(screen)
        for draw in drawable:  # background draws first; player/asteroids/shots on top
            draw.draw(screen)
        # Added: draw HUD (score) top-left
        score_surf = font.render(f"Score: {score}", True, pygame.Color("white"))  # build score surface
        screen.blit(score_surf, (12, 10))  # draw score
        # Added: show high score on HUD
        hs_surf = font.render(f"Highest Score: {high_score}", True, pygame.Color("white"))  # build high score surface
        screen.blit(hs_surf, (12, 58))  # draw high score
        # Added: draw lives
        lives_text = "Lives: " + (str(max(0, lives)) if lives >= 0 else "0")  # avoid negative display
        lives_surf = font.render(lives_text, True, pygame.Color("white"))  # build lives surface
        screen.blit(lives_surf, (12, 36))  # draw lives

        # Added: game over screen overlay
        if game_over:
            # update and persist high score once at game over
            if score > high_score:  # if we set a record
                high_score = score  # update local value
                save_high_score(high_score)  # persist to disk
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # semi-opaque backdrop
            overlay.fill((0, 0, 0, 180))  # darken the screen
            screen.blit(overlay, (0, 0))  # draw overlay
            title = pygame.font.SysFont(None, 64).render("GAME OVER", True, pygame.Color("white"))  # big title
            prompt = pygame.font.SysFont(None, 32).render("Press R to restart or ESC to quit", True, pygame.Color("white"))  # help text
            final = pygame.font.SysFont(None, 32).render(f"Final Score: {score}", True, pygame.Color("white"))  # run score
            best = pygame.font.SysFont(None, 28).render(f"Best: {high_score}", True, pygame.Color("white"))  # best score
            screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - 80))  # center title
            screen.blit(final, (SCREEN_WIDTH/2 - final.get_width()/2, SCREEN_HEIGHT/2 - 20))  # center run score
            screen.blit(best, (SCREEN_WIDTH/2 - best.get_width()/2, SCREEN_HEIGHT/2 + 6))  # center best score
            screen.blit(prompt, (SCREEN_WIDTH/2 - prompt.get_width()/2, SCREEN_HEIGHT/2 + 30))  # center prompt

            # handle restart/quit keys without advancing the game state
            keys = pygame.key.get_pressed()  # read keys while paused
            if keys[pygame.K_r]:
                return main()  # restart fresh
            if keys[pygame.K_ESCAPE]:
                return  # exit to OS
        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
