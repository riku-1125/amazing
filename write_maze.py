from maze_gen import generate_maze
from solve_maze import solve_maze


def write_maze(MAZE: list[list[int]], start: tuple[int, int], end: tuple[int, int], path: str) -> None:
    
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