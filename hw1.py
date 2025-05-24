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
            if (color == -1):
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
    
def countEmptySpaces(grid):
    emptySpaces = 0
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == -1:
                emptySpaces = emptySpaces + 1
    return emptySpaces

def moveBrushPosition(row, col):
    while True:
        shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
        cur_col, cur_row = shapePos
        # print(f"Desired position: ({row}, {col})")
        # print(f"Current position: ({cur_row}, {cur_col})")

        if cur_col < col:
            game.execute('right')
        elif cur_col > col:
            game.execute('left')
        elif cur_row < row:
            game.execute('down')
        elif cur_row > row:
            game.execute('up')
        else:
            break  # We're at the target position

# Loop through each square
while (not done):
    for row in range(len(grid)):
        for col in range(len(grid)):
            minEmptySpacesLeft = len(grid) * len(grid)

            # Check if it is empty and loop through the brush type and color to find local optima
            if grid[row][col] == -1:
                # print(f"Checking position ({row}, {col})")
                bestBrush = None
                bestColor = None

                # Move brush position
                switchToSpecifiedBrushIndex(0)
                moveBrushPosition(row, col)
                shapePos, currentShapeIndex, currentColorIndex, gridBeforePlacing, placedShapes, done = game.execute('export')
                gridBeforePlacing = np.copy(gridBeforePlacing)

                # Iterate through each brush pattern
                for brushIndex in range(9):
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
                    
                    # Try each color for this brush
                    for colorIndex in range(4):

                        switchToSpecifiedColorIndex(colorIndex)
                        
                        # Try to place and check if the grid has changed
                        shapePos, currentShapeIndex, currentColorIndex, gridAfterPlacing, placedShapes, done = game.execute('place')
                        gridAfterPlacing = np.copy(gridAfterPlacing)

                        if (not (gridBeforePlacing == gridAfterPlacing).all()):
                            if adjacencyRulePasses(gridAfterPlacing):
                                emptySpacesLeftWithNewPlacement = countEmptySpaces(gridAfterPlacing)
                                # print(f"Trying brush {brushIndex} with color {colorIndex}")

                                if (emptySpacesLeftWithNewPlacement < minEmptySpacesLeft):
                                    minEmptySpacesLeft = emptySpacesLeftWithNewPlacement
                                    bestBrush = brushIndex
                                    bestColor = colorIndex
                                    # print(f"New best Brush: {brushIndex}")
                                    # print(f"New best Color: {colorIndex}")
                                    # print(f"ShapePos: {shapePos[1]} , {shapePos[0]}")
                                    # print(gridAfterPlacing)

                            # Undo since we are not sure that this is the best local solution
                            # print("Undo")
                            game.execute('undo')

                if bestBrush is not None and bestColor is not None:
                    #print(f"Placing working shape ({row}, {col})")
                    switchToSpecifiedBrushIndex(bestBrush)
                    switchToSpecifiedColorIndex(bestColor)
                    moveBrushPosition(row, col)
                    #print(f"{bestBrush}, {bestColor}")
                    shapePos, currentShapeIndex, currentColorIndex, gridAfterPlacing, placedShapes, done = game.execute('place')
                    #print(f"shape position: {shapePos[1]}, {shapePos[0]}")
                    #print(f"Current shape index: {currentShapeIndex}")
                    #print(gridAfterPlacing)




########################################

# Do not modify any of the code below. 

########################################

end=time.time()

np.savetxt('grid.txt', grid, fmt="%d")
with open("shapes.txt", "w") as outfile:
    outfile.write(str(placedShapes))
with open("time.txt", "w") as outfile:
    outfile.write(str(end-start))
