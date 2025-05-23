import time
import numpy as np
from gridgame import *

##############################################################################################################################

# You can visualize what your code is doing by setting the GUI argument in the following line to true.
# The render_delay_sec argument allows you to slow down the animation, to be able to see each step more clearly.

# For your final submission, please set the GUI option to False.

# The gs argument controls the grid size. You should experiment with various sizes to ensure your code generalizes.
# Please do not modify or remove lines 18 and 19.

##############################################################################################################################

game = ShapePlacementGrid(GUI=True, render_delay_sec=0.5, gs=6, num_colored_boxes=5)
shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
np.savetxt('initial_grid.txt', grid, fmt="%d")

##############################################################################################################################

# Initialization

# shapePos is the current position of the brush.

# currentShapeIndex is the index of the current brush type being placed (order specified in gridgame.py, and assignment instructions).

# currentColorIndex is the index of the current color being placed (order specified in gridgame.py, and assignment instructions).

# grid represents the current state of the board. 
    
    # -1 indicates an empty cell
    # 0 indicates a cell colored in the first color (indigo by default)
    # 1 indicates a cell colored in the second color (taupe by default)
    # 2 indicates a cell colored in the third color (veridian by default)
    # 3 indicates a cell colored in the fourth color (peach by default)

# placedShapes is a list of shapes that have currently been placed on the board.
    
    # Each shape is represented as a list containing three elements: a) the brush type (number between 0-8), 
    # b) the location of the shape (coordinates of top-left cell of the shape) and c) color of the shape (number between 0-3)

    # For instance [0, (0,0), 2] represents a shape spanning a single cell in the color 2=veridian, placed at the top left cell in the grid.

# done is a Boolean that represents whether coloring constraints are satisfied. Updated by the gridgames.py file.

##############################################################################################################################

shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')

print(shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done)


####################################################
# Timing your code's execution for the leaderboard.
####################################################

start = time.time()  # <- do not modify this.



##########################################
# Write all your code in the area below. 
##########################################

# The intuition: Try to minimize the number of shapes and colors used by starting with a bigger shape and trying to fit shapes of smaller and smaller sizes within
# the gaps while maintaining the constraint of no adjacent cells of the same color so we must loop through the different shapes as well as the colors at each stage
# objective function should choose the paint and brush option that results in the least remaining empty spaces

# Method used: Steepest ascent hill climbing

# while loop to stay looping

'''

YOUR CODE HERE



'''

# Switch to specified brush pattern
def switchToSpecifiedBrushIndex(desiredIndex):
    shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
    while (currentShapeIndex != desiredIndex):
        shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('switchshape')

def switchToSpecifiedColorIndex(desiredIndex):
    shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
    while (currentColorIndex != desiredIndex):
        shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('switchcolor')

def adjacencyRulePasses(grid):
    # Check that no adjacent cells have the same color
    gridSize = len(grid)
    for i in range(gridSize):
        for j in range(gridSize):
            color = grid[i, j]
            if i > 0 and grid[i - 1, j] == color:
                return False
            if i < gridSize - 1 and grid[i + 1, j] == color:
                return False
            if j > 0 and grid[i, j - 1] == color:
                return False
            if j < gridSize - 1 and grid[i, j + 1] == color:
                return False

    return True
    
def countEmptySpaces(grid):
    emptySpaces = 0
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == -1:
                emptySpaces = emptySpaces + 1
    return emptySpaces

def moveBrushPosition(x, y):
    shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
    while (shapePos[0] != x or shapePos[1] != y):
        if (shapePos[0] < x):
            shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('right')
        elif (shapePos[0] > x):
            shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('left')
        if (shapePos[1] < y):
            shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('up')
        elif (shapePos[1] > y):
            shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('down')
    return grid


# Loop through each square
for row in range(len(grid)):
    for col in range(len(grid)):
        minEmptySpacesLeft = len(grid) * len(grid)

        # Check if it is empty and loop through the brush type and color to find local optima
        if grid[row][col] == -1:
            brushIterator = 9
            bestBrush = None
            bestColor = None

            # Move brush position
            gridBeforePlacing = moveBrushPosition(row, col)

            # Iterate through each brush pattern
            while (brushIterator):

                # Try to place and if the grid has changed, check for adjacency: if it does not pass the adjacency rule then switch color
                shapePos, currentShapeIndex, currentColorIndex, gridAfterPlacing, placedShapes, done = game.execute('place')

                if not (gridBeforePlacing == gridAfterPlacing).all():

                    if adjacencyRulePasses(gridAfterPlacing):
                        emptySpacesLeftWithNewPlacement = countEmptySpaces(gridAfterPlacing)
                        print("Trying new configuration since adjacency rule passes")

                        if (emptySpacesLeftWithNewPlacement < minEmptySpacesLeft):
                            minEmptySpacesLeft = emptySpacesLeftWithNewPlacement
                            bestBrush = currentShapeIndex
                            bestColor = currentColorIndex

                            shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('switchshape')
                            brushIterator = brushIterator - 1
                            print("New best Brush: " + str(currentShapeIndex))
                            print("New best Color: " + str(currentColorIndex))
                    else:
                        print("Grid fits but color does not work")
                        shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('switchcolor')

                    # Undo since we are not sure that this is the best local solution
                    shapePos, currentShapeIndex, currentColorIndex, gridAfterPlacing, placedShapes, done = game.execute('undo')
                    
                else:
                    print("Shape does not fit")
                    shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('switchshape')
                    brushIterator = brushIterator - 1

            print("Place working shape")
            switchToSpecifiedBrushIndex(bestBrush)
            switchToSpecifiedColorIndex(bestColor)
            shapePos, currentShapeIndex, currentColorIndex, gridAfterPlacing, placedShapes, done = game.execute('place')



########################################

# Do not modify any of the code below. 

########################################

end=time.time()

np.savetxt('grid.txt', grid, fmt="%d")
with open("shapes.txt", "w") as outfile:
    outfile.write(str(placedShapes))
with open("time.txt", "w") as outfile:
    outfile.write(str(end-start))
