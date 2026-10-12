from collections import deque
from enum import Enum

from maze_gen import generate_maze

candidates: deque[tuple[tuple[int, int], str]] = deque()
visited: set[tuple] = set()


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    

def find_next_candidates(maze: list[list[int]], y: int, x: int, path: str) -> None:
    wall_direction = maze[y][x]

    if wall_direction >= Direction.WEST.value:
        wall_direction -= Direction.WEST.value
    elif (y, x - 1) not in visited:
        candidates.append([(y, x - 1), path + "W"])

    if wall_direction >= Direction.SOUTH.value:
        wall_direction -= Direction.SOUTH.value
    elif (y + 1, x) not in visited:
        candidates.append([(y + 1, x), path + "S"])

    if wall_direction >= Direction.EAST.value:
        wall_direction -= Direction.EAST.value
    elif (y, x + 1) not in visited:
        candidates.append([(y, x + 1), path + "E"])

    if wall_direction >= Direction.NORTH.value:
        wall_direction -= Direction.NORTH.value
    elif (y - 1, x) not in visited:
        candidates.append([(y - 1, x), path + "N"])


def solve_maze(maze: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> str:
    x, y = start
    candidates.append([start, ""])
    (y, x), path = candidates.popleft()
    visited.add(start)
    find_next_candidates(maze, y, x, path)
    while candidates:
        (y, x), path = candidates.popleft()
        visited.add((y, x))
        if (y, x) == end:
            return path
        find_next_candidates(maze, y, x, path)
    
    return "No path from start to goal"


if __name__ == "__main__":
    MAZE = generate_maze(3, 3)
    path = solve_maze(MAZE, (0, 0), (2, 2))
    print(f"path: {path}")