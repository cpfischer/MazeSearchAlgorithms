#==============================================================================
# Maze
#==============================================================================
ROWS = 40                  # number of rows in maze
COLS = 40                  # number of columns in maze

PUNCHES = (ROWS * COLS) * 0.1   # number of punches in wall after maze is generated
                           # (to create loops).
                         
CELLWIDTH = 32             # assume each cell is a square

WALLWIDTH =  CELLWIDTH / 8 # Approximately CELLWIDTH/8
if WALLWIDTH <= 1:
    WALLWIDTH = 2

X,Y = 0,0                  # relative top-left for whole maze

#==============================================================================
# Bot
#==============================================================================
#BOT_RADIUS = 4 # Approx slightly less than (CELLWIDTH - WALLWIDTH)/2
BOT_RADIUS = (CELLWIDTH - WALLWIDTH)/2 - 1
if BOT_RADIUS < 2:
    BOT_RADIUS = 2
    
SPEED = 2        # radius of bot. If too large, will fail tolerance test.
BOT_COLOR = (200, 0, 200)
