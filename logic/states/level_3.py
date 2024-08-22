from settings import pg, PAUSE_KEY

def handle_level_three_events(game, event):
    """Function that handles events for the level three game state"""
    
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()

def update_level_three(game):
    
    player = game.player #Rename player to make code easier to read

    #Player
    player.handle_input() #Handle player input
    player.move() #Move the player
    player.update_animation() #Update the player animation
    
    #Environment
    game.update_portal_animation() #Update the portal animation
    [effect.update_animation() for effect in game.effects] #Update all the effects

def render_level_three(game):
    screen = game.screen

    screen.blit(game.level_three_ground_surf, game.level_three_ground_rect) #Draw the ground
    #TODO: Draw interactibles
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    [screen.blit(effect.sprite, effect.rect) for effect in game.effects] #Draw all the effects
    screen.blit(game.player.sprite, game.player.rect) #Draw the player

    if game.should_draw_cursor: screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor
