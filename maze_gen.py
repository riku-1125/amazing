"""ランダム迷路生成のためのモジュール

壁をビットで表し、未訪問の隣マスをランダムに選んで探索する。

todo:
    * config.txtから読み取った設定を反映する機能の追加
"""
import random


def get_candidate(
    candidates: list[tuple[int, int]],
    arrived: set[tuple[int, int]],
    x: int, y: int, width: int,
    height: int
) -> None:
    """範囲内で、未訪問の隣マスを候補に追加する

    Args:
        candidates: 候補の座標を追加するリスト
        arrived: すでに通った座標の集合（＊変更しない）
        x: 現在地のx座標
        y: 現在地のy座標
        width: 迷路の横幅
        height: 迷路の縦幅
    """
    if x + 1 < width and (x + 1, y) not in arrived:
        candidates.append((x + 1, y))
    if x - 1 >= 0 and (x - 1, y) not in arrived:
        candidates.append((x - 1, y))
    if y + 1 < height and (x, y + 1) not in arrived:
        candidates.append((x, y + 1))
    if y - 1 >= 0 and (x, y - 1) not in arrived:
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


def generate_maze(width: int, height: int) -> list[list[int]]:
    """迷路生成関数

    Args:
        width: 生成する迷路の横幅
        height: 生成する迷路の縦幅

    Returns: 生成した迷路の二次元リスト
    """
    # 壁の値は北=1、東=2、南=4、西=8。15は全方向の壁が閉じた状態。
    # 座標は(x, y)で表し、迷路のマスにはmaze[y][x]でアクセスする。
    maze = [[15] * width for _ in range(height)]
    # routeは現在地までの探索経路。リストの最後(route[-1])が現在地で、行き止まりなら戻る。
    route = [(0, 0)]
    # arrivedは訪問済みの座標。戻ったときも取り除かず、再訪を防ぐ.
    arrived = {(0, 0)}

    # 戻って探索できるマスがなくなるまで、進む・戻るを繰り返す
    while route:
        # 現在地を取得
        x, y = route[-1]
        # 現在地が変わるたびに、候補を空から集め直す。
        candidates = []
        get_candidate(candidates, arrived, x, y, width, height)
        if not candidates:
            # 未訪問の隣マスがなければ、現在地を取り除いて一つ前へ戻る。
            route.pop()
        else:
            # 候補からランダムに行き先を選び、経路と訪問済みの記録に追加する。
            next_x, next_y = random.choice(candidates)
            route.append((next_x, next_y))
            arrived.add((next_x, next_y))
            open_wall(maze, x, y, next_x, next_y)
    return maze


maze = generate_maze(10, 10)

for row in maze:
    line = ""
    for cell in row:
        line += format(cell, "X")
    print(line)
