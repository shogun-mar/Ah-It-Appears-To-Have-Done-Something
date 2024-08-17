#Graphical representation settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
MAX_FPS = 60 #60

#Physics simulation settings
MAX_ENTITY_SPEED = 10 #The maximum speed of any entity in pixels per frame
FALLING_SPEED_INCR = 1 #The speed at which the player falls in pixels per frame
PLAYER_GRAVITY_PULL_DELAY = 2 #The delay in frames between gravity pulls
BASE_GRAVITY_PULL = FALLING_SPEED_INCR #The base gravity pull any entity with simulated physics
MAX_DOWN_VELOCITY = 16 #The maximum speed the player can fall at in pixels per frame (should be multiple of FALLING_SPEED)

#Player movement settings
PLAYER_SPEED = 2 #The speed of the player in pixels per frame
PLAYER_ANIMATION_SWITCHING_DELAY = 12  #After how many frames the animation of the player should progress
BASE_JUMP_SPEED = -10 #Initial player jump speed in pixel per frame (negative value for jumping up)

INITIAL_COORDS_PLAYER = [(50, 400)] #Initial coordinates the player should have in each level (midbottom)