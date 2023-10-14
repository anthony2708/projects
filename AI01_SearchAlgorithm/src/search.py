from util import *


# BFS
def BFS(matrix, start, end):
    open_list, visited = [start], [start]
    closed_list = []
    while open_list:
        current = open_list.pop(0)
        closed_list.append(current)
        if current == end:
            return closed_list
        for neighbor in find_next(current, matrix):
            if neighbor not in visited:
                open_list.append(neighbor)
                visited.append(neighbor)
    return None


# DFS
def DFS(matrix, start, end):
    stack, visited = [start], [start]
    route = []
    while (stack):
        n = stack.pop()
        route.append(n)
        if n == end:
            return route
        for x in find_next(n, matrix):
            if x not in visited:
                visited.append(x)
                stack.append(x)
    return None


# Greedy
def Greedy(matrix, start, end, bonus_points):
    open_list = [start]
    closed_list = []
    while open_list:
        current = open_list.pop(0)
        closed_list.append(current)
        if current == end:
            return closed_list
        for neighbor in find_next(current, matrix):
            if (neighbor not in closed_list):
                open_list.append(neighbor)
        open_list.sort(key=lambda x: heuristic_distance_bonus(
            x, end, bonus_points))
    return None


# A*
def AStar(matrix, start, end):
    F, G, camefrom = {}, {}, {}
    G[start] = 0
    F[start] = heuristic_distance(start, end)
    opened, closed = [start], []

    while opened:
        current, currentF = None, None
        for pos in opened:
            if current is None or F[pos] < currentF:
                currentF = F[pos]
                current = pos
        if current == end:
            route = [current]
            while current in camefrom:
                current = camefrom[current]
                route.append(current)
            route.reverse()
            return route
        opened.remove(current)
        closed.append(current)

        for neighbor in find_next(current, matrix):
            if neighbor in closed:
                continue
            candidateG = G[current] + actual_distance(current, start)
            if neighbor not in opened:
                opened.append(neighbor)
            elif candidateG >= G[neighbor]:
                continue
            camefrom[neighbor] = current
            G[neighbor] = candidateG
            H = heuristic_distance(neighbor, end)
            F[neighbor] = G[neighbor] + H
    return None
