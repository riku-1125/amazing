"""迷路を生成して解き、画面に表示するメインモジュール

迷路を生成し、スタートからゴールまでの経路を求めて、ターミナルに描画する。
"""
from maze_gen import generate_maze
from solve_maze import solve_maze
from render_maze import render_maze

WIDTH = 10
HEIGHT = 10
ENTRY = (0, 0)
EXIT = (9, 9)


def set_path_flg(path: str, entry: tuple[int, int]) -> list[list[int]]:
    """経路の文字列をたどり、経路上のマスに1を立てた二次元リストを返す

    スタートとゴールのマスは0のままにする(描画側で s と g を表示するため)。

    Args:
        path: 進む方向(N, E, S, W)をつなげた経路の文字列
        entry: 迷路のスタート位置(x, y)

    Returns:
        経路上のマスが1、それ以外が0の二次元リスト。is_path[y][x]でアクセスする。
    """
    is_path = [[0] * WIDTH for _ in range(HEIGHT)]
    x, y = entry

    for direction in path:
        match direction:
            case "N":
                y -= 1
                is_path[y][x] = 1
            case "E":
                x += 1
                is_path[y][x] = 1
            case "S":
                y += 1
                is_path[y][x] = 1
            case "W":
                x -= 1
                is_path[y][x] = 1
    is_path[y][x] = 0
    return is_path


def main() -> None:
    """迷路を生成し、経路を求めて画面に表示する"""
    MAZE = generate_maze(WIDTH, HEIGHT, ENTRY, EXIT)
    path = solve_maze(MAZE, ENTRY, EXIT)
    is_path = set_path_flg(path, ENTRY)
    print_path_flg = True

    render_maze(MAZE, is_path, ENTRY, EXIT, print_path_flg, WIDTH, HEIGHT)
    print(f"path: {path}")


if __name__ == "__main__":
    main()
