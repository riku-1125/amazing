"""ランダム迷路生成のためのモジュール

壁をビットで表し、未訪問の隣マスをランダムに選んで探索する。
迷路生成位置は(0, 0)固定

todo:
    * config.txtから読み取った設定を反映する機能の追加
    * スタートゴールが迷路の範囲外のエラーは未実装config.txtを読むファイルでvalidateする？？
"""
import random
import sys


def get_candidate(
    candidates: list[tuple[int, int]],
    arrived: set[tuple[int, int]],
    blocked: set[tuple[int, int]],
    x: int, y: int, width: int,
    height: int
) -> None:
    """範囲内で、未訪問の隣マスを候補に追加する

    Args:
        candidates: 候補の座標を追加するリスト
        arrived: すでに通った座標の集合（＊変更しない）
        blocked: "42"の文字があるためアクセスしてはいけない場所
        x: 現在地のx座標
        y: 現在地のy座標
        width: 迷路の横幅
        height: 迷路の縦幅
    """
    if (
        x + 1 < width
        and (x + 1, y) not in arrived
        and (x + 1, y) not in blocked
    ):
        candidates.append((x + 1, y))
    if (
        x - 1 >= 0
        and (x - 1, y) not in arrived
        and (x - 1, y) not in blocked
    ):
        candidates.append((x - 1, y))
    if (
        y + 1 < height
        and (x, y + 1) not in arrived
        and (x, y + 1) not in blocked
    ):
        candidates.append((x, y + 1))
    if (
        y - 1 >= 0
        and (x, y - 1) not in arrived
        and (x, y - 1) not in blocked
    ):
        candidates.append((x, y - 1))


def open_wall(
    maze: list[list[int]],
    x: int,
    y: int,
    next_x: int,
    next_y: int
) -> None:
    """壁を開ける処理

    Args:
        maze: 迷路の盤面
        x: 現在地のx座標
        y: 現在地のy座標
        next_x: 次のx座標
        next_y: 次のy座標
    """
    north = 1
    east = 2
    south = 4
    west = 8

    if x == next_x and y > next_y:
        maze[y][x] &= ~north
        maze[next_y][next_x] &= ~south
    if x < next_x and y == next_y:
        maze[y][x] &= ~east
        maze[next_y][next_x] &= ~west
    if x == next_x and y < next_y:
        maze[y][x] &= ~south
        maze[next_y][next_x] &= ~north
    if x > next_x and y == next_y:
        maze[y][x] &= ~west
        maze[next_y][next_x] &= ~east


def get_deadend_candidate(
    deadend_candidates: list[tuple[int, int]],
    maze: list[list[int]],
    blocked: set[tuple[int, int]],
    x: int,
    y: int,
    width: int,
    height: int
) -> None:
    """範囲内で行き止まりの候補を探す

    Args:
        deadend_candidates: 候補を追加するリスト
        maze: 迷路の盤面
        blocked: 到達禁止座標
        x: 現在地のx座標
        y: 現在地のy座標
        width: 生成する迷路の横幅
        height: 生成する迷路の縦幅

    """
    north = 1
    east = 2
    south = 4
    west = 8
    if (
        x + 1 < width
        and (x + 1, y) not in blocked
        and maze[y][x] & east
    ):
        deadend_candidates.append((x + 1, y))
    if (
        x - 1 >= 0
        and (x - 1, y) not in blocked
        and maze[y][x] & west
    ):
        deadend_candidates.append((x - 1, y))
    if (
        y + 1 < height
        and (x, y + 1) not in blocked
        and maze[y][x] & south
    ):
        deadend_candidates.append((x, y + 1))
    if (
        y - 1 >= 0
        and (x, y - 1) not in blocked
        and maze[y][x] & north
    ):
        deadend_candidates.append((x, y - 1))


def is_3x3_space(maze: list[list[int]], top: int, left: int) -> bool:
    """3*3のスペースがあるか判断する

    Args:
        maze: 生成された迷路の盤面
        top: 調べる領域の左上のy座標
        left: 調べる領域の左上のx座標

    Returns:
        左上の視点から右下に3*3の空白があればTrue、なければFalse
    """
    east = 2
    south = 4
    for dy in range(3):
        for dx in range(2):
            if maze[top + dy][left + dx] & east:
                return False
    for dy in range(2):
        for dx in range(3):
            if maze[top + dy][left + dx] & south:
                return False
    return True


def fix_3x3_space(maze: list[list[int]]) -> None:
    """3*3の空白が迷路に存在した時、その領域の中心の右側の位置の壁を立てる
    渡されたmazeを直接変更する

    Args:
        maze: 生成された迷路の盤面
    """
    east = 2
    west = 8
    height = len(maze)
    width = len(maze[0])
    for top in range(height - 2):
        for left in range(width - 2):
            if is_3x3_space(maze, top, left):
                maze[top + 1][left + 1] |= east
                maze[top + 1][left + 2] |= west


def generate_maze(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
    seed: int | None = None,
    perfect: bool = True
) -> list[list[int]]:
    """迷路生成関数

    Args:
        width: 生成する迷路の横幅
        height: 生成する迷路の縦幅
        entry: 迷路のスタート位置
        exit: 迷路のゴール
        seed: シード値.Noneならランダムで、同じシード値なら同じ迷路が生成されるはず
        perfect: True->完全迷路、False->不完全迷路

    Returns:
        生成した迷路の二次元リスト

    Raises:
        ValueError: スタートまたはゴールが”42”のます上だと例外を投げる。
    """
    # 壁の値は北=1、東=2、南=4、西=8。15は全方向の壁が閉じた状態。
    # 座標は(x, y)で表し、迷路のマスにはmaze[y][x]でアクセスする。
    maze = [[15] * width for _ in range(height)]
    # routeは現在地までの探索経路。リストの最後(route[-1])が現在地で、行き止まりなら戻る。
    route = [(0, 0)]
    # arrivedは訪問済みの座標。戻ったときも取り除かず、再訪を防ぐ.
    arrived = {(0, 0)}
    # 引数のseedからランダムジェネレーターを生成
    random_generator = random.Random(seed)
    # "42"パターン(仮) 7*5
    pattern = [
        "#...###",
        "#.....#",
        "###.###",
        "..#.#..",
        "..#.###",
    ]
    # patternを中央に配置するためのoffset
    offset_x = (width - len(pattern[0])) // 2
    offset_y = (height - len(pattern)) // 2
    # "42"の文字があるためアクセスしてはいけない場所
    blocked: set[tuple[int, int]] = set()
    # "42"パターンの周りに道ができる最低の大きさ以下では"42"を表示しない。
    if width < 9 or height < 7:
        print("迷路が小さいので'42'の表示が出来ません。", file=sys.stderr)
    # "42"パターンをblockedに追加
    else:
        for pattern_y, row in enumerate(pattern):
            for pattern_x, cell in enumerate(row):
                if cell == '#':
                    blocked.add(
                        # 中心に配置
                        (offset_x + pattern_x, offset_y + pattern_y)
                    )
    if entry in blocked or exit in blocked:
        raise ValueError("スタートとゴールを'42'のマスの上に配置出来ません。")

    # 戻って探索できるマスがなくなるまで、進む・戻るを繰り返す
    while route:
        # 現在地を取得
        x, y = route[-1]
        # 現在地が変わるたびに、候補を空から集め直す。
        candidates: list[tuple[int, int]] = []
        get_candidate(candidates, arrived, blocked, x, y, width, height)
        if not candidates:
            # 未訪問の隣マスがなければ、現在地を取り除いて一つ前へ戻る。
            route.pop()
        else:
            # 候補からランダムに行き先を選び、経路と訪問済みの記録に追加する。
            next_x, next_y = random_generator.choice(candidates)
            route.append((next_x, next_y))
            arrived.add((next_x, next_y))
            open_wall(maze, x, y, next_x, next_y)
    if not perfect:
        for y in range(height):
            for x in range(width):
                if maze[y][x].bit_count() == 3:
                    deadend_candidates: list[tuple[int, int]] = []
                    get_deadend_candidate(
                        deadend_candidates,
                        maze,
                        blocked,
                        x,
                        y,
                        width,
                        height
                    )
                    if deadend_candidates:
                        next_x, next_y = random_generator.choice(
                            deadend_candidates
                        )
                        open_wall(maze, x, y, next_x, next_y)
        fix_3x3_space(maze)

    return maze


if __name__ == "__main__":
    maze = generate_maze(49, 49, (0, 0), (48, 48), perfect=False)

    for row in maze:
        line = ""
        for cell in row:
            line += format(cell, "X")
        print(line)
