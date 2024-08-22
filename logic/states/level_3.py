from settings import pg, PAUSE_KEY

def handle_level_three_events(game, event):
    """Function that handles events for the level three game state"""
    
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()

def update_level_three(game):
    pass

def render_level_three(game):
    pass
