"""迷路を解くためのモジュール

幅優先探索(BFS)で、スタートからゴールまでの最短経路を求める。
経路は進む方向の文字(N, E, S, W)をつなげた文字列で表す。

"""
from collections import deque
from enum import Enum

from maze_gen import generate_maze


class Direction(Enum):
    """壁の方向を表すビットの値

    マスの値は、閉じている壁の値の合計で表す。
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


def find_next_candidates(
        candidates: deque[tuple[tuple[int, int], str]],
        visited: set[tuple[int, int]],
        maze: list[list[int]],
        y: int,
        x: int,
        path: str
) -> None:
    """壁がなく、未訪問の隣マスを候補に追加する

    Args:
        candidates: 未訪問の隣接マス
        visited: 訪問済みのマス
        maze: 迷路の盤面
        y: 現在地のy座標
        x: 現在地のx座標
        path: スタートから現在地までの経路
    """
    wall_direction = maze[y][x]

    if wall_direction >= Direction.WEST.value:
        wall_direction -= Direction.WEST.value
    elif (y, x - 1) not in visited:
        candidates.append(((y, x - 1), path + "W"))

    if wall_direction >= Direction.SOUTH.value:
        wall_direction -= Direction.SOUTH.value
    elif (y + 1, x) not in visited:
        candidates.append(((y + 1, x), path + "S"))

    if wall_direction >= Direction.EAST.value:
        wall_direction -= Direction.EAST.value
    elif (y, x + 1) not in visited:
        candidates.append(((y, x + 1), path + "E"))

    if wall_direction >= Direction.NORTH.value:
        wall_direction -= Direction.NORTH.value
    elif (y - 1, x) not in visited:
        candidates.append(((y - 1, x), path + "N"))


def solve_maze(
        maze: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int]
) -> str:
    """スタートからゴールまでの最短経路を求める

    Args:
        maze: 迷路の盤面
        start: 迷路のスタート位置
        end: 迷路のゴール

    Returns:
        進む方向(N, E, S, W)をつなげた経路の文字列。
        ゴールにたどり着けなければ"No path from start to goal"
    """
    candidates: deque[tuple[tuple[int, int], str]] = deque()
    visited: set[tuple[int, int]] = set()

    start_x, start_y = start
    start_point: tuple[int, int] = (start_y, start_x)
    end_x, end_y = end
    end_point: tuple[int, int] = (end_y, end_x)
    candidates.append((start_point, ""))
    (y, x), path = candidates.popleft()
    visited.add(start_point)
    find_next_candidates(candidates, visited, maze, y, x, path)
    while candidates:
        (y, x), path = candidates.popleft()
        visited.add((y, x))
        if (y, x) == end_point:
            return path
        find_next_candidates(candidates, visited, maze, y, x, path)

    return "No path from start to goal"


if __name__ == "__main__":
    MAZE = generate_maze(10, 10, (0, 0), (9, 9))
    path = solve_maze(MAZE, (0, 0), (0, 2))
    print(f"path: {path}")
