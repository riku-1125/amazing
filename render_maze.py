"""迷路を画面に表示するためのモジュール

壁を+---+と|で、スタートをs、ゴールをg、経路を*、"42"を###で描画する。
"""
from constants import Direction, RESET
from maze_gen import generate_maze
from solve_maze import solve_maze


def print_line(width: int, wall_color: str) -> None:
    """迷路の一番下の壁の線を表示する

    Args:
        width: 迷路の横幅
    """
    line = "+"

    for _ in range(width):
        line += "---+"
    print(f"{wall_color}{line}{RESET}")


def render_maze(
        MAZE: list[list[int]],
        is_path: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        print_path_flg: bool,
        width: int,
        height: int,
        wall_color: str = "\033[37m",  # 白
) -> None:
    """迷路を左上から1行ずつターミナルに表示する

    各マスの北と西の壁を描き、一番東と一番南の壁は行末と最後に描く。

    Args:
        MAZE: 迷路の盤面
        is_path: 経路上のマスが1、それ以外が0の二次元リスト
        entry: 迷路のスタート位置(x, y)
        exit: 迷路のゴール(x, y)
        print_path_flg: Trueなら経路を表示する
        width: 迷路の横幅
        height: 迷路の縦幅
        wall_color: 壁の色を表すANSIエスケープシーケンス(デフォルトは白)
    """
    for y in range(height):
        for x in range(width):
            if MAZE[y][x] & Direction.NORTH:
                print(f"{wall_color}+---{RESET}", end="")
            else:
                print(f"{wall_color}+   {RESET}", end="")
        print(f"{wall_color}+{RESET}")

        for x in range(width):
            if MAZE[y][x] & Direction.WEST:
                print(f"{wall_color}|{RESET}", end="")
            else:
                print(" ", end="")

            if (x, y) == entry:
                print(" s ", end="")
            elif (x, y) == exit:
                print(" g ", end="")
            elif MAZE[y][x] == 15:
                print("###", end="")
            elif print_path_flg and is_path[y][x] == 1:
                print(" * ", end="")
            else:
                print("   ", end="")
        print(f"{wall_color}|{RESET}")
    print_line(width, wall_color)


if __name__ == "__main__":
    WIDTH = 10
    HEIGHT = 10
    ENTRY = (0, 0)
    EXIT = (9, 9)

    def set_path_flg(
            path: str,
            entry: tuple[int, int]
    ) -> list[list[int]]:
        """経路の文字列をたどり、経路上のマスに1を立てた二次元リストを返す

        Args:
            path: 進む方向(N, E, S, W)をつなげた経路の文字列
            entry: 迷路のスタート位置(x, y)

        Returns:
            経路上のマスが1、それ以外が0の二次元リスト
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

    MAZE = generate_maze(WIDTH, HEIGHT, ENTRY, EXIT)
    path = solve_maze(MAZE, ENTRY, EXIT)
    is_path = set_path_flg(path, ENTRY)
    print_path_flg = True
    render_maze(MAZE, is_path, ENTRY, EXIT, print_path_flg, WIDTH, HEIGHT)
