import heapq
import random
import numpy as np
import battlecode as bc

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.height, self.width = grid.shape

    def neighbors(self, loc):
        (x, y) = loc
        neighbor_list = []

        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                else:
                    nx = x + dx
                    ny = y + dy
                    if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height and self.grid[ny][nx] >= 0:
                        neighbor_list.append((nx,ny))
        return neighbor_list


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    return path


def a_star(grid, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return None

def fuzzy_a_star(grid, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        for next in grid.neighbors(current):
            if random.random() > 0.75:
                new_cost = cost_so_far[current] + 1 + np.random.normal(1, 0.1, 1)[0]
            else:
                new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return None

rotate_right = {}
rotate_right[bc.Direction.North] = bc.Direction.Northeast
rotate_right[bc.Direction.East] = bc.Direction.Southeast
rotate_right[bc.Direction.South] = bc.Direction.Southwest
rotate_right[bc.Direction.West] = bc.Direction.Northwest
rotate_right[bc.Direction.Northeast] = bc.Direction.East
rotate_right[bc.Direction.Northwest] = bc.Direction.North
rotate_right[bc.Direction.Southeast] = bc.Direction.South
rotate_right[bc.Direction.Southwest] = bc.Direction.West
rotate_right[bc.Direction.Center] = bc.Direction.Center

rotate_left = {}
rotate_left[bc.Direction.North] = bc.Direction.Northwest
rotate_left[bc.Direction.East] = bc.Direction.Northeast
rotate_left[bc.Direction.South] = bc.Direction.Southeast
rotate_left[bc.Direction.West] = bc.Direction.Southwest
rotate_left[bc.Direction.Northeast] = bc.Direction.North
rotate_left[bc.Direction.Northwest] = bc.Direction.West
rotate_left[bc.Direction.Southeast] = bc.Direction.East
rotate_left[bc.Direction.Southwest] = bc.Direction.South
rotate_left[bc.Direction.Center] = bc.Direction.Center
