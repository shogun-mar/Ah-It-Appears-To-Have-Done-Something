SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
MAX_FPS = 5

PLAYER_SPEED = 2
MAX_PLAYER_JUMP_HEIGHT = PLAYER_SPEED * 100
PLAYER_ANIMATION_SWITCHING_DELAY = MAX_FPS#max(1, 5 * (MAX_FPS // 30))  #After how many frames the animation of the player should progress


MAX_SPEED = 10
FALLLING_SPEED = 1
PLAYER_GRAVITY_PULL_DELAY = max(1, 1 * (MAX_FPS // 30))
BASE_GRAVITY_PULL = FALLLING_SPEED
MAX_FALL_SPEED = 16
MAX_JUMP_SPEED = -10  # Negative value for jumping up