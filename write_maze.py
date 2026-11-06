"""迷路をファイルに出力するためのモジュール

迷路の盤面、スタート、ゴール、経路をoutput_maze.txtに書き込む。
"""
from maze_gen import generate_maze
from solve_maze import solve_maze


def write_maze(
        MAZE: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int],
        path: str
) -> None:
    """迷路の情報をoutput_maze.txtに書き込む

    各マスの値は16進数1文字で書き込む。

    Args:
        MAZE: 迷路の盤面
        start: 迷路のスタート位置
        end: 迷路のゴール
        path: スタートからゴールまでの経路
    """
    with open("output_maze.txt", "w", encoding="utf-8") as f:
        for row in MAZE:
            line = "".join(f"{cell:X}" for cell in row)
            f.write(f"{line}\n")

        # start
        f.write("\n")
        f.write(f"start: {start}  #(x, y)\n")
        f.write(f"end:   {end}  #(x, y)\n")
        f.write(f"path: {path}\n")


if __name__ == "__main__":
    maze = generate_maze(10, 10, (0, 0), (9, 9), 42)
    path = solve_maze(maze, (0, 0), (9, 9))
    write_maze(maze, (0, 0), (9, 9), path)
