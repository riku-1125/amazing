from enum import IntEnum


class Direction(IntEnum):
    """壁の方向を表すビットの値

    マスの値は、閉じている壁の値の合計で表す。
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


RESET = "\033[0m"
WALL_COLORS = [
    "\033[37m",   # 白
    "\033[31m",   # 赤
    "\033[32m",   # 緑
    "\033[34m",   # 青
    "\033[33m",   # 黄
]
