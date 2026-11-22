*This project has been created as part of the 42 curriculum by rinshiba, rnagai.*

# A-Maze-ing

## Description

A-Maze-ingは、設定ファイルから迷路を生成し、入口から出口までの最短経路を
求めるPythonプログラムです。壁・入口・出口・経路をターミナルに表示し、
迷路と最短経路を指定されたファイルに保存します。
盤面に余裕がある場合は、四方を壁で閉じたマスで「42」を描きます。

## Instructions

Python 3.10以上が必要です。ターミナル版を実行するための追加ライブラリは
ありません。リポジトリ直下で次を実行します。

```sh
python3 a_maze_ing.py config.txt
```

### Makefileを使う場合

リポジトリ直下で `make` コマンドを実行できます。最初に仮想環境を作成し、
必要な開発用ライブラリをインストールします。

```sh
make install
```

利用できる主なターゲットは次のとおりです。

| コマンド | 操作 |
| --- | --- |
| `make install` | `.venv`を作成し、`requirements.txt`からライブラリをインストールする |
| `make run` | `.venv`のPythonで`config.txt`を使って実行する |
| `make debug` | `pdb`でデバッグ実行する |
| `make clean` | `__pycache__`と`.mypy_cache`を削除する |
| `make lint` | flake8と通常のmypyチェックを実行する |
| `make lint-strict` | flake8と`mypy --strict`を実行する |

通常の実行は次のとおりです。

```sh
make install
make run
```

引数は設定ファイルへのパス一つです。別のファイル名でも実行できます。
起動すると迷路が表示され、次のメニューを操作できます。

| 入力 | 操作 |
| --- | --- |
| `1` | 迷路を再生成し、最短経路を求め直して表示・保存する |
| `2` | 最短経路の表示・非表示を切り替える |
| `3` | 壁の色を切り替える |
| `4` | 終了する |

同じ設定と固定シードを使うと同じ盤面が再現されます。
操作 `1` で別の盤面を試すには、`SEED` の指定を省いて起動します。

### 設定ファイル

UTF-8のテキストで、1行に一つの `KEY=VALUE` を書きます。
空行と `#` から始まるコメント行は無視されます。
キー名は大文字で指定します。重複・未知のキーや必須項目の不足はエラーです。

```ini
# 10×10の完全迷路を再現する例
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

| キー | 必須 | 値 |
| --- | --- | --- |
| `WIDTH` | はい | 横のマス数。正の整数 |
| `HEIGHT` | はい | 縦のマス数。正の整数 |
| `ENTRY` | はい | 入口の座標。`x,y` 形式 |
| `EXIT` | はい | 出口の座標。`x,y` 形式 |
| `OUTPUT_FILE` | はい | 出力先のファイルパス |
| `PERFECT` | はい | `True` なら完全迷路、`False` なら輪のある迷路 |
| `SEED` | いいえ | 再現に使う整数。省略すると固定しない |

座標は左上を `(0, 0)` とし、右が `x` の正方向、下が `y` の正方向です。
入口と出口は盤面内の異なるマスを指定し、「42」のマスとの重複も避けます。
幅9未満または高さ7未満では、「42」を省略してメッセージを表示します。
相対パスは実行時の作業ディレクトリが基準です。

出力ファイルには、壁をマスごとに16進数1文字で書きます。
盤面の後に空行を挟み、入口座標・出口座標・最短経路を1行ずつ書きます。
経路は北・東・南・西を表す `N`、`E`、`S`、`W` の文字列です。

## Algorithms

生成には、ランダムに隣マスを選ぶ**深さ優先探索（DFS）とバックトラッキング**
を使います。すべての壁が閉じた盤面から始め、まだ訪問していない隣マスへ
進むときだけ、両側の壁を開けます。進める場所がなくなったら、一つ前のマスに
戻って探索を続けます。「42」に使うマスは候補から除外します。

この方法を選んだのは、訪問済みの集合と戻り先のリストで手順を表せ、
未訪問のマスにだけ通路を足すことで、輪のない迷路を作れるためです。
`PERFECT=False` の場合は、行き止まりから追加の通路を開き、輪を増やします。
内部の壁がすべて開いた3×3領域があれば、中央と東隣の間の壁を閉じます。

最短経路は**幅優先探索（BFS）**で求めます。各移動は1マス分なので、
入口から近い順に探索し、初めて出口に着いた経路を使います。

## Reusable maze generator

迷路生成と経路探索は `MazeGenerator` から別のPythonプロジェクトでも使えます。
設定ファイルの読み込み、ターミナル表示、結果の保存はアプリ側が担当します。

### インストール

Python 3.10以上を使います。リポジトリ直下で、仮想環境を作って
提出用wheelをインストールします。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ./mazegen-0.1.0-py3-none-any.whl
```

インストールしたwheelを試すには、仮想環境を有効にしたまま
リポジトリの外に移動し、次のコードを実行します。

```python
from maze_gen import MazeGenerator

generator = MazeGenerator(
    width=10,
    height=10,
    entry=(0, 0),
    exit=(9, 9),
    seed=42,
    perfect=True,
)

walls = generator.maze   # walls[y][x] でマスを取得
path = generator.solve   # 入口から出口までの最短経路
```

`width`・`height` でサイズ、`entry`・`exit` で座標、
`seed` で再現に使う値、`perfect` で生成モードを変更できます。
盤面の値は整数で、閉じている壁を北=1、東=2、南=4、西=8のビットで表します。
`help(MazeGenerator)` でも使い方を確認できます。

### wheelの再ビルド

リポジトリ直下で、Python 3.10以上の仮想環境を有効にして実行します。

```sh
python -m pip wheel --no-deps --wheel-dir dist .
```

`pyproject.toml` の設定を使い、`dist/` にwheelを生成します。
ビルドには `setuptools` が必要で、初回はpipが取得する場合があります。
提出済みのwheelを更新するときは、新しく生成したファイルを直下に置きます。
ライセンスは [LICENSE.md](LICENSE.md) を参照してください。

## Team and project management

| メンバー | 担当 |
| --- | --- |
| `rinshiba` | 迷路生成、設定読み込み、wheelの作成、README |
| `rnagai` | 最短経路探索、ファイル出力、ターミナル表示、メイン処理、Makefile |

当初は、迷路生成と最短経路探索を分担し、それぞれが単体で動く状態を
目指しました。その後、設定読み込みを追加して、生成・探索・保存・表示を
メイン処理から呼ぶ形にまとめました。終盤に生成と探索を別のプロジェクトから
使えるようにし、wheelとして配布できる形にしました。

生成と探索で盤面の形式を共有したことで、それぞれの担当が並行して進められました。
改善点は、設定と生成・表示のつなぎ目で起きる動作を、統合前から共有することです。
特に固定シードでの再生成や、設定値を変えた場合の挙動を早めに確認できると、
レビューで意図を説明しやすくなります。

作業の管理にはGitのブランチとGitHubのIssues・Pull Requestsを使いました。
迷路の検証には課題付属の `maze_analyzer.py`、書式・型の確認には
flake8とmypy、wheelの動作確認にはPythonの仮想環境を使いました。

## Resources

- [Python: random](https://docs.python.org/3/library/random.html)
  — 候補のランダム選択とシードの扱い
- [Python: collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
  — 幅優先探索の待ち行列
- [Python: venv](https://docs.python.org/3/library/venv.html)
  — テスト用の仮想環境
- [pip wheel](https://pip.pypa.io/en/stable/cli/pip_wheel/)
  — ソースからwheelを再ビルドする手順

AIは、課題要件の整理、迷路生成と検証の考え方の説明、設定読み込みの
初稿作成とレビュー、メイン処理のレビュー、wheel化の手順確認、
このREADMEの下書きに使いました。設定読み込みの初稿は、チームで読める形に
直し、不正な入力や例外処理を手元で確認しました。
