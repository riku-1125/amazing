"""迷路を生成して解き、画面に表示するメインモジュール

迷路を生成し、スタートからゴールまでの経路を求めて、ターミナルに描画する。
"""
import sys

from maze_gen import generate_maze
from solve_maze import solve_maze
from render_maze import render_maze
from read_conf import read_conf
from write_maze import write_maze
from constants import WALL_COLORS


def set_path_flg(
        path: str,
        entry: tuple[int, int],
        width: int,
        height: int
) -> list[list[int]]:
    """経路の文字列をたどり、経路上のマスに1を立てた二次元リストを返す

    スタートとゴールのマスは0のままにする(描画側で s と g を表示するため)。

    Args:
        path: 進む方向(N, E, S, W)をつなげた経路の文字列
        entry: 迷路のスタート位置(x, y)
        width: 迷路の横幅
        height: 迷路の縦幅

    Returns:
        経路上のマスが1、それ以外が0の二次元リスト。is_path[y][x]でアクセスする。
    """
    is_path = [[0] * width for _ in range(height)]
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

    if len(sys.argv) != 2:
        raise Exception("引数は一つだけ指定してください")
    if sys.argv[1] != "config.txt":
        raise Exception("引数の名称が正しくありません")

    conf = read_conf(sys.argv[1])
    width = conf.width
    height = conf.height
    entry = conf.entry
    exit = conf.exit
    output_file = conf.output_file
    perfect = conf.perfect
    seed = conf.seed

    input_num = ""
    color_idx = 0
    print_path_flg = False

    maze = generate_maze(width, height, entry, exit, seed, perfect)
    path = solve_maze(maze, entry, exit)
    is_path = set_path_flg(path, entry, width, height)
    write_maze(maze, entry, exit, path, output_file)
    render_maze(
        maze, is_path, entry, exit, print_path_flg, width, height
    )

    while True:
        if input_num == "1":
            maze = generate_maze(width, height, entry, exit, seed, perfect)
            path = solve_maze(maze, entry, exit)
            is_path = set_path_flg(path, entry, width, height)
            print_path_flg = False
            write_maze(maze, entry, exit, path, output_file)
            render_maze(
                maze, is_path, entry, exit, print_path_flg, width, height
            )
        elif input_num == "2":
            print_path_flg = not print_path_flg
            render_maze(
                maze, is_path, entry, exit, print_path_flg, width, height
            )
        elif input_num == "3":
            color_idx += 1
            render_maze(
                maze,
                is_path,
                entry,
                exit,
                print_path_flg,
                width,
                height,
                WALL_COLORS[color_idx % 5]
            )
        elif input_num == "4":
            print("Done.")
            break
        else:
            print("Please enter a number between 1 and 4.")

        print("")
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colour")
        print("4. Quit")
        input_num = input("Choice? (1-4): ")
        print("")


if __name__ == "__main__":
    main()
