SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
MAX_FPS = 60 #60

PLAYER_SPEED = 120 // MAX_FPS #The speed of the player in pixels per frame
MAX_PLAYER_JUMP_HEIGHT = 200
PLAYER_ANIMATION_SWITCHING_DELAY = max(1, 5 * (MAX_FPS // 30))  #After how many frames the animation of the player should progress
MAX_SPEED = 10
FALLLING_SPEED = 1
PLAYER_GRAVITY_PULL_DELAY = max(1, 1 * (MAX_FPS // 30))
BASE_GRAVITY_PULL = FALLLING_SPEED
MAX_FALL_SPEED = 16
MAX_JUMP_SPEED = -10  # Negative value for jumping up