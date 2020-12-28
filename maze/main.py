"""
There should only be console printing in main.py. Remember to comment out ALL
debug/test printing in your other python files.
"""

import sys
import random;

import config
from pymaze import *
from Problem import *
from Fringe import *
from ClosedList import *
from Bot import RandomBot
from view import View
from view import EdgeView
from graph_search import graph_search
from SearchNode import SearchNode
from State import MazeState

seed = input("enter random seed: ")
random.seed(seed)

#==============================================================================
# DO NOT CHANGE ANYTHING IN THIS SECTION.
# Create maze
#==============================================================================
ROWS = config.ROWS
COLS = config.COLS
PUNCHES = config.PUNCHES
option = input("0-random maze or 1-stored maze: ")
maze = DFSMazeWithCycles(ROWS, COLS, PUNCHES)
if option == 1:
    maze.restore('maze.json')

#==============================================================================
# DO NOT CHANGE ANYTHING IN THIS SECTION.
#==============================================================================
NUMBOTS = 1
r0 = input("initial row: ")
c0 = input("initial column: ")
initial_state = (r0, c0)
r1 = input("goal row: ")
c1 = input("goal column: ")
goal_state = (r1, c1)
search = raw_input("bfs, dfs, ucs, iddfs, gbfs, or A*: ")

#==============================================================================
# NEW 2018
# gui == True iff use graphical animation. For now set this to True.
#==============================================================================
#gui = raw_input('graphical animation? (y/n): ')
#if gui in 'yY':
#    gui = True
#else:
#    gui = False
gui = True

#==============================================================================
# DO NOT CHANGE ANYTHING IN THIS SECTION.
# Create view of maze and bot
#==============================================================================
if gui:
    from view import CELLWIDTH # ADDED 2020/09/29
    view0 = View(width=(COLS) * CELLWIDTH,
                 height=(ROWS) * CELLWIDTH,
                 delay=1)
    mazeview = view0.add_maze(maze, name='maze')
    edgeview = view0.add_edges(mazeview, name='edgeview')
    
    bots = []
    for i in range(NUMBOTS):
        bot = RandomBot(maze, start=(r0, c0))
        bots.append(bot)
        name = 'bot%s' % i
        view0.add_bot(bot,
                      mazeview,
                      color=config.BOT_COLOR,
                      name=name)
else:
    view0 = None

#===========================================================
# TODO: Compute solution using graph search.
# Select the correct fringe object.
#===========================================================
view0['maze'].background[initial_state] = (0,255,0)
view0.run()
problem = MazeProblem(maze=maze,
                      initial_state=(r0,c0),
                      goal_states=[(r1,c1)],
                      search=search
                      )

if search == 'bfs':
    fringe = FSQueue()
elif search == 'dfs':
    fringe = FSStack()
elif search == 'ucs' or search == 'A*' or search == 'gbfs':
    dangerous_rooms = {} #dictionary of (state, path_cost)
    new_room = raw_input("Dangerous Room r c cost: ")
    while new_room:
        dr, dc, dcost = new_room.split()
        dangerous_rooms[(int(dr),int(dc))] = dcost
        new_room = raw_input("Dangerous Room r c cost: ")
    problem.dangerous_rooms = dangerous_rooms
    fringe = UCSFringe()
elif search == 'iddfs':
    fringe = IDDFS(max_depth=maze.rows * maze.cols)
else:
    raise Exception('invalid search')

closed_list = SetClosedListWithCompression()
initial_node = SearchNode(initial_state)
if search == 'iddfs':
    initial_node.path_cost = 0
    fringe.initial_node = initial_node
    fringe.closed_list = closed_list
    fringe.view0 = view0
fringe.put(initial_node)


solution = graph_search(problem=problem,
                        Node=initial_node,
                        fringe=fringe,
                        closed_list=closed_list,
                        view0=view0)

#==============================================================================
# DO NOT CHANGE ANYTHING IN THIS SECTION.
#==============================================================================
print("solution: %s" % solution)
print("len(solution): %s" % len(solution))
print("len(closed_list): %s" % len(closed_list))
print("len(fringe): %s" % len(fringe))

# Compute path from solution for drawing.
maze = problem.maze
(r, c) = initial_state
path = [initial_state]
for action in solution:
    (r, c) = maze.get_adj_tuple((r, c), action)
    path.append((r, c))
#print("path: %s" % path)
for bot in bots:
    bot.set_path(path)

if gui:
    while 1:
        view0.run()
