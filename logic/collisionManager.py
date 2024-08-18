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
    def __init__(self, level_num):
        self.level_num = level_num

    def allow_movement(self, x, y):
        """" Function that given coordinates of a point on a 2D plane looks at the value of a matrix representing a collision maps and returns whether the player can move to that point or not, based on the color of the pixel at that point. """
        
        pixel_color = maps[self.level_num][y][x]
        if pixel_color[-1] == 0:
            return 'allowed'
        elif pixel_color == [0, 0, 0, 255]:
            return 'collision'

class PlayerCollisionManager(CollisionManager):
    def __init__(self, level_num):
        super().__init__(level_num)

    def allow_movement(self, x, y):
        """" Function that given coordinates of a point on a 2D plane looks at the value of a matrix representing a collision maps and returns whether the player can move to that point or not, based on the color of the pixel at that point. """

        pixel_color = maps[self.level_num][y][x]
        if pixel_color[-1] == 0: #If the pixel is transparent
            return 'allowed'
        elif pixel_color == [0, 0, 0, 255]:
            return 'collision'
        elif pixel_color == [255, 0, 0, 255]:
            return 'death'
        #Add level switching color
        
