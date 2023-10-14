import os
import sys
from search import *
from UI import *

# Global variables
BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/..'
MAPS_DIR = BASE_DIR + '/test'

# Usage: python main.py [algorithm] [mazefile]
if (len(sys.argv) < 3):
    raise SyntaxError('Invalid syntax')
else:
    algorithm = sys.argv[1].lower()
    map_name = sys.argv[2].lower()
    try:
        bonus_points, matrix = readfile(MAPS_DIR + '/' + map_name)
    except FileNotFoundError as e:
        print('File not found: ' + map_name)
        exit(1)

    # Print the information of the matrix
    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'S':
                start = (i, j)
            elif matrix[i][j] == ' ':
                if (i == 0) or (i == len(matrix)-1) or (j == 0) or (j == len(matrix[0])-1):
                    end = (i, j)
            else:
                pass

    # Check the correct algorithm
    if (algorithm == 'dfs'):
        route = DFS(matrix, start, end)
        pass
    elif (algorithm == 'bfs'):
        route = BFS(matrix, start, end)
        pass
    elif (algorithm == 'astar'):
        route = AStar(matrix, start, end)
        pass
    elif (algorithm == 'greedy'):
        route = Greedy(matrix, start, end, bonus_points)
        pass
    else:
        print('Wrong algorithm')  # Exit when receiving wrong algorithm
        exit(1)

    if route is None:  # No route was found
        visualize_maze(matrix, bonus_points, start, end)
        print('No route to found from starting point to ending point')
        exit(2)
    else:  # A route is found
        visualize_maze(matrix, bonus_points, start, end, route)
