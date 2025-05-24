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

game = ShapePlacementGrid(GUI=True, render_delay_sec=0, gs=10, num_colored_boxes=5)
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

'''

YOUR CODE HERE



'''
# Method used: Steepest Ascent Hill Climbing
# Try to minimize the number of shapes used by finding the biggest valid brush shape that fits.
# In order to minimize the number of colors used, always iterate through the colors in the same manner (e.g. Indigo, Taupe, Viridian...)

# Switches to specified brush pattern
def switchToSpecifiedBrushIndex(desiredIndex):
    shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
    while (currentShapeIndex != desiredIndex):
        shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('switchshape')

# Switches to specificed color index
def switchToSpecifiedColorIndex(desiredIndex):
    shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
    while (currentColorIndex != desiredIndex):
        shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('switchcolor')

# Checks that we are not violating any color adjacency rules
def adjacencyRulePasses(grid):
    gridSize = len(grid)
    for i in range(gridSize):
        for j in range(gridSize):
            color = grid[i, j]
            if (color == -1): # Ignore empty spaces
                continue
            if i > 0 and grid[i - 1, j] == color:
                return False
            if i < gridSize - 1 and grid[i + 1, j] == color:
                return False
            if j > 0 and grid[i, j - 1] == color:
                return False
            if j < gridSize - 1 and grid[i, j + 1] == color:
                return False
    return True
    
# Counts the empty spaces remaining on the given board
def countEmptySpaces(grid):
    emptySpaces = 0
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == -1:
                emptySpaces = emptySpaces + 1
    return emptySpaces

# Moves the brush position to the given row and column
def moveBrushPosition(row, col):
    while True:
        shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
        cur_col, cur_row = shapePos

        if cur_col < col:
            game.execute('right')
        elif cur_col > col:
            game.execute('left')
        elif cur_row < row:
            game.execute('down')
        elif cur_row > row:
            game.execute('up')
        else:
            break # We arrived at the correct position

# Don't stop until we are done
while (not done):

    # Loop through each square on the grid
    for row in range(len(grid)):
        for col in range(len(grid)):

            # This has to be the max empty spaces given a certain grid
            minEmptySpacesLeft = len(grid) * len(grid)

            # Check if it is empty and loop through the brush type and color to find local optima
            if grid[row][col] == -1:
                bestBrush = None
                bestColor = None

                # Initialize brush position to smallest so we don't have any issues moving brush postion
                switchToSpecifiedBrushIndex(0)
                moveBrushPosition(row, col)
                shapePos, currentShapeIndex, currentColorIndex, gridBeforePlacing, placedShapes, done = game.execute('export')
                gridBeforePlacing = np.copy(gridBeforePlacing)

                # Iterate through each brush pattern
                for brushIndex in range(9):

                    # Maintain boundaries so we can skip some computations towards the edges of the grid
                    if (col == len(grid) - 1 and brushIndex > 0):
                        continue
                    elif (col == len(grid) - 2 and brushIndex >= 5):
                        continue
                    elif (col == len(grid) - 3 and (brushIndex == 5 or brushIndex == 6)):
                        continue
                    if (row == len(grid) - 1 and brushIndex > 0):
                        continue
                    elif (row >= len(grid) - 3 and (brushIndex == 3 or brushIndex == 4)):
                        continue
                    
                    switchToSpecifiedBrushIndex(brushIndex)
                    
                    # Try each color for this brush and always in the same order to minimize colors used
                    for colorIndex in range(4):
                        switchToSpecifiedColorIndex(colorIndex)
                        shapePos, currentShapeIndex, currentColorIndex, gridAfterPlacing, placedShapes, done = game.execute('place')
                        gridAfterPlacing = np.copy(gridAfterPlacing)

                        # We know that the brush pattern and position was valid if the grid changes after it was placed
                        if (not (gridBeforePlacing == gridAfterPlacing).all()):

                            # Check that we pass the color adjacency rule since placing doesn't check for this
                            if adjacencyRulePasses(gridAfterPlacing):
                                emptySpacesLeftWithNewPlacement = countEmptySpaces(gridAfterPlacing)

                                # We have arrived at a new best shape and color if we are minimizing the number of empty spaces left
                                if (emptySpacesLeftWithNewPlacement < minEmptySpacesLeft):
                                    minEmptySpacesLeft = emptySpacesLeftWithNewPlacement
                                    bestBrush = brushIndex
                                    bestColor = colorIndex
                            
                            game.execute('undo') # Due to Steepest-Ascent Hill Climbing, we do not know that the current shape and color is the best suited yet

                # We have tested and arrived at the best shape and color
                if bestBrush is not None and bestColor is not None:
                    switchToSpecifiedBrushIndex(bestBrush)
                    switchToSpecifiedColorIndex(bestColor)
                    moveBrushPosition(row, col)
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
