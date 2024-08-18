from PIL import Image
import numpy as np

maps = []

for i in range(1):
    # Load the image
    image = Image.open(f'graphics/collision_maps/level_{i}.png').convert("RGBA")
    
    # Convert the image to a numpy array
    image_array = np.array(image)
    #Convert the image to a matrix
    image_array = image_array.tolist()
    #Append the matrix to the maps list
    maps.append(image_array)

class CollisionManager:
    def __init__(self, game_current_level_num):
        self.level_num: int = game_current_level_num #Set the level num class attribute to the current level num (made so changing the level num outside of the class changes the level num of the collision manager)

    def allow_movement(self, x, y):
        """" Function that given coordinates of a point on a 2D plane looks at the value of a matrix representing a collision maps and returns whether the player can move to that point or not, based on the color of the pixel at that point. """
        
        pixel_color = maps[self.level_num][y][x]
        if pixel_color[-1] == 0:
            return 'allowed'
        elif pixel_color == [0, 0, 0, 255]:
            return 'collision'

class PlayerCollisionManager(CollisionManager):
    def __init__(self, game_current_level_num):
        super().__init__(game_current_level_num)

    def allow_movement(self, x, y):
        """" Function that given coordinates of a point on a 2D plane looks at the value of a matrix representing a collision maps and returns whether the player can move to that point or not, based on the color of the pixel at that point. """

        try: #TODO: Fix this (remove try except)
            pixel_color: list[int] = maps[self.level_num][y][x]
        except IndexError:
            return 'collision'
        
        if pixel_color[-1] == 0: #Transparent pixel
            return 'allowed'
        elif pixel_color == [0, 0, 0, 255]: #Fully opaque black
            return 'collision'
        elif pixel_color == [0, 0, 255, 255]: #Fully opaque blue
            return 'changing level'
        elif pixel_color == [255, 0, 0, 255]: #Fully opaque red
            return 'death'