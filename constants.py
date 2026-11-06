from enum import IntEnum


class Direction(IntEnum):
    """壁の方向を表すビットの値

    マスの値は、閉じている壁の値の合計で表す。
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
