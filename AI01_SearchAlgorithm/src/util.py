from math import *


def find_next(pos, matrix):
    next = []
    if (pos[0] - 1 >= 0 and matrix[pos[0]-1][pos[1]] != 'x'):
        next.append((pos[0]-1, pos[1]))
    if (pos[0] + 1 < len(matrix) and matrix[pos[0]+1][pos[1]] != 'x'):
        next.append((pos[0]+1, pos[1]))
    if (pos[1] + 1 < len(matrix[0]) and matrix[pos[0]][pos[1] + 1] != 'x'):
        next.append((pos[0], pos[1] + 1))
    if (pos[1] - 1 >= 0 and matrix[pos[0]][pos[1]-1] != 'x'):
        next.append((pos[0], pos[1]-1))
    return next


def heuristic_distance(node, end):
    return sqrt((node[0] - end[0])**2 + (node[1] - end[1])**2)


def heuristic_distance_bonus(node, end, bonus_points):
    for _, points in enumerate(bonus_points):
        if node == (points[0], points[1]):
            return points[2] + sqrt((node[0] - end[0])**2 + (node[1] - end[1])
                                    ** 2)
    return sqrt((node[0] - end[0])**2 + (node[1] - end[1])**2)


def actual_distance(node, start):
    return sqrt((node[0] - start[0])**2 + (node[1] - start[1])**2)
