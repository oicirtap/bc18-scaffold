import heapq
import numpy as np

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
    path.reverse()  # optional
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
