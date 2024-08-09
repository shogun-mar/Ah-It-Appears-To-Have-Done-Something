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
        if maps[self.level_num][y][x] == (0, 0, 0, 0):
            return True
        elif maps[self.level_num][y][x] == (0, 0, 0, 255):
            return False

class PlayerCollisionManager(CollisionManager):
    def __init__(self, level_num):
        super().__init__(level_num)

    def allow_movement(self, x, y):
        print(f"coords: {x, y} color: {maps[self.level_num][y][x]}")
        if maps[self.level_num][y][x] == (0, 0, 0, 0):
            return True
        elif maps[self.level_num][y][x] == (0, 0, 0, 255):
            return False
        elif maps[self.level_num][y][x] == (255, 0, 0, 255):
            return 'death'
        #Add level switching color
        
