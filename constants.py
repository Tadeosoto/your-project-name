SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
LINE_WIDTH = 2

# Player movement
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200

# asteroids
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

# Added: background / stars tuning for the new scrolling starfield effect
# STAR_COUNT controls how many stars are rendered.
# STAR_SPEED_MIN/MAX control the vertical drift speed range to create parallax-like motion.
STAR_COUNT = 120
STAR_SPEED_MIN = 30
STAR_SPEED_MAX = 120

# Added: lives/respawn/invulnerability and explosion timing
PLAYER_START_LIVES = 3  # how many hits allowed before game over
PLAYER_RESPAWN_TIME = 2.0  # seconds to wait before respawn
PLAYER_INVULNERABLE_TIME = 2.0  # post-respawn safety window
EXPLOSION_DURATION = 0.5  # how long explosion animation runs