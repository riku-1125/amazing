"""迷路の設定ファイルを読み、型付きの設定値に変換するモジュール"""


class Config:
    """迷路生成・経路探索・出力で共有する設定値。"""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        output_file: str,
        seed: int | None = None,
    ) -> None:
        """受け取った設定値を属性に保存する。"""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.output_file = output_file
        self.seed = seed


def _read_values(filename: str) -> dict[str, str]:
    """空行とコメントを飛ばし、設定を文字列の辞書として返す。"""
    values: dict[str, str] = {}
    with open(filename, encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, separator, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if not separator or not key or not value:
                raise ValueError(f"{number}行目: KEY=VALUE で指定してください。")
            if key in values:
                raise ValueError(f"{number}行目: {key} が重複しています。")
            values[key] = value
    return values


def _parse_int(key: str, value: str) -> int:
    """設定値を整数に変換し、失敗時は項目名を伝える。"""
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{key} は整数で指定してください。")


def _parse_point(
    key: str, value: str, width: int, height: int
) -> tuple[int, int]:
    """盤面の範囲内にある座標を返す。"""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} は x,y の形式で指定してください。")
    x = _parse_int(f"{key} の x 座標", parts[0])
    y = _parse_int(f"{key} の y 座標", parts[1])
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"{key} の座標 ({x}, {y}) は迷路の範囲外です。")
    return x, y


def read_conf(filename: str) -> Config:
    """指定されたファイルを読み、検証済みの設定を返す。

    Args:
        filename: 設定ファイルのパス。

    Returns:
        各設定値を利用する型に変換した Config。

    Raises:
        OSError: ファイルを開けない、または読み込めない場合。
        ValueError: 書式や設定値が不正な場合。
    """

    _REQUIRED_KEYS = (
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "PERFECT",
        "OUTPUT_FILE"
    )
    values = _read_values(filename)
    missing = [key for key in _REQUIRED_KEYS if key not in values]
    if missing:
        raise ValueError(f"必須項目がありません: {', '.join(missing)}")

    width = _parse_int("WIDTH", values["WIDTH"])
    height = _parse_int("HEIGHT", values["HEIGHT"])
    if width < 1 or height < 1:
        raise ValueError("WIDTH と HEIGHT は1以上にしてください。")

    entry = _parse_point("ENTRY", values["ENTRY"], width, height)
    exit_point = _parse_point("EXIT", values["EXIT"], width, height)
    if entry == exit_point:
        raise ValueError("ENTRY と EXIT は異なる座標にしてください。")

    perfect = values["PERFECT"].lower()
    if perfect not in ("true", "false"):
        raise ValueError("PERFECT は True または False で指定してください。")

    seed = _parse_int("SEED", values["SEED"]) if "SEED" in values else None
    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_point,
        perfect=perfect == "true",
        output_file=values["OUTPUT_FILE"],
        seed=seed,
    )


if __name__ == "__main__":
    try:
        conf = read_conf("./config.txt")
        print(conf.width)
        print(conf.height)
        print(conf.entry)
        print(conf.exit)
        print(conf.perfect)
        print(conf.output_file)
        print(conf.seed)
    except ValueError as e:
        print(e)
