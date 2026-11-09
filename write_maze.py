"""迷路をファイルに出力するためのモジュール

迷路の盤面、スタート、ゴール、経路をoutput_maze.txtに書き込む。
"""
from maze_gen import generate_maze
from solve_maze import solve_maze


def write_maze(
        MAZE: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        path: str,
        output: str
) -> None:
    """迷路の情報をoutput_maze.txtに書き込む

    各マスの値は16進数1文字で書き込む。

    Args:
        MAZE: 迷路の盤面
        entry: 迷路のスタート位置
        exit: 迷路のゴール
        path: スタートからゴールまでの経路
        output: 結果を出力する拡張子含むファイル名

    Raises:
        OSError: 出力ファイルを作成・書き込みできない場合
    """
    with open(output, "w", encoding="utf-8") as f:
        for row in MAZE:
            line = "".join(f"{cell:X}" for cell in row)
            f.write(f"{line}\n")

        entry_x, entry_y = entry
        exit_x, exit_y = exit
        f.write("\n")
        f.write(f"{entry_x},{entry_y}\n")
        f.write(f"{exit_x},{exit_y}\n")
        f.write(f"{path}\n")


if __name__ == "__main__":
    maze = generate_maze(10, 10, (0, 0), (9, 9), 42)
    path = solve_maze(maze, (0, 0), (9, 9))
    write_maze(maze, (0, 0), (9, 9), path, "maze.txt")
