def _load_debug_grid(filename):
    with open(filename) as f:
        lines = f.readlines()

    lines = [l.replace("\n", "") for l in lines]
    return lines


def iter_grid_row(grid, row_idx):
    for i in range(len(grid[row_idx])):
        yield grid[row_idx][i]


def iter_grid_col(grid, col_idx):
    for x in range(len(grid)):
        yield grid[x][col_idx]


def iter_grid_cluster(grid, cluster_x, cluster_y):
    x_offset = cluster_x * 3
    y_offset = cluster_y * 3

    for y in range(3):
        for x in range(3):
            yield grid[y + y_offset][x + x_offset]


def print_grid(sudoku_grid):
    for ydx, line in enumerate(sudoku_grid):
        line = [c for c in line]
        for xdx, chr in enumerate(line):
            chr = str(chr) if chr is not None else "_"
            spacer = "   "
            if ((xdx + 1) % 3) == 0 and xdx != 0:
                spacer = " | "

            if xdx == 0:
                chr = " " + str(chr)
            print(chr + spacer, end="")

        print("\n", end="")
        if (ydx + 1) % 3 == 0:
            print((11 * "-" + "+") * 3)
            # print(4 * 9 * "-", end="\n")


def generate_solve_matrix():
    matrix = []
    for z in range(9):
        rows = []
        for y in range(9):
            row = []
            for x in range(9):
                row += [z + 1]
            rows += [row]
        matrix += [rows]
    return matrix


def iter_grid_coordinates():
    for y in range(9):
        for x in range(9):
            yield (x, y)


def get_value_in_grid(grid, x, y):
    return grid[y][x]


def set_value_in_grid(grid, x, y, value):
    grid[y][x] = value
    return grid


def get_solve_grid_z(solve_grid, x, y):
    depth_values = []

    for z in range(9):
        depth_values += [get_value_in_grid(solve_grid[z], x, y)]

    return depth_values


def is_cell_solved(solve_matrix, x, y):
    z = get_solve_grid_z(solve_matrix, x, y)
    values = [v for v in z if v]
    if len(values) == 1:
        return True
    return False


def is_solved(solve_matrix):
    for x, y in iter_grid_coordinates():
        if not is_cell_solved(solve_matrix, x, y):
            return False
    return True


def solve_matrix_cell(solve_matrix, x, y):
    """Attempts to solve a matrix column, returns the value for the solve, returns None if not solvable"""
    values = get_solve_grid_z(solve_matrix, x, y)
    values = [x for x in values if x]
    if len(values) == 1:
        return values[0]
    return None


def collapse_to_value(solve_matrix, x, y, value):
    other_values = range(9)
    other_values = [r for r in other_values if str(r + 1) != value]

    assert value not in other_values

    for v in other_values:
        solve_grid_v = solve_matrix[v]

        solve_grid_v = set_value_in_grid(solve_grid_v, x, y, "")
        solve_matrix[v] = solve_grid_v

    return solve_matrix


def remove_value_from_solve_matrix(solve_matrix, x, y, value):
    z_idx = value - 1
    solve_matrix[z_idx][y][x] = ""
    return solve_matrix


def get_cell_cluster(x, y):
    import math

    clus_x = math.floor(x / 3)
    clus_y = math.floor(y / 3)
    return clus_x, clus_y


def collapse_solve_matrix(solve_matrix):
    mem_grid = []
    for y in range(9):
        row = []
        for x in range(9):
            solved_value = solve_matrix_cell(solve_matrix, x, y)
            row += [solved_value]
        mem_grid += [row]
    return mem_grid


def main():
    grid = _load_debug_grid("./test_grid_1.txt")
    print_grid(grid)

    # print("Iterating over row %s" % 5)
    # chars = list(iter_grid_row(grid, 5))
    # print(chars)
    #
    # print("Iterating over col %s" % 5)
    # chars = list(iter_grid_col(grid, 5))
    # print(chars)
    #
    # print("Iterating over center cell")
    # chars = list(iter_grid_cell(grid, 1, 1))
    # print(chars)
    solve_matrix = generate_solve_matrix()

    # z = get_solve_grid_z(solve_matrix, 0, 0)
    # print(z)

    # collapse all values in test grid
    for x, y in iter_grid_coordinates():
        value = get_value_in_grid(grid, x, y)
        if value != " ":
            # print("Collapsing value %s at (%s %s)" % (value, x, y))
            solve_matrix = collapse_to_value(solve_matrix, x, y, value)

    for x in range(9):
        print_grid(solve_matrix[x])
        print("--" * 10)

    assert not is_solved(solve_matrix), "sudoku already solved?"
    # assert is_cell_solved(
    #     solve_matrix, 0, 0
    # ), "first cell (in test case) should not register as solved"

    max_attempts = 11
    attempt = 0
    while not is_solved(solve_matrix) and attempt < max_attempts:
        attempt += 1

        # construct a test_grid from the solve matrix, every cell that can be collapsed

        solved_grid = collapse_solve_matrix(solve_matrix)
        # print_grid(solved_grid)
        # print("--" * 20)

        for x, y in iter_grid_coordinates():
            if is_cell_solved(solve_matrix, x, y):
                continue
            cell_cluster = get_cell_cluster(x, y)
            # print(f"Solving Cell: {x}, {y} in cluster {cell_cluster}")

            row = [v for v in iter_grid_row(solved_grid, y)]
            row_taken_values = [v for v in row if v]

            col = [v for v in iter_grid_col(solved_grid, x)]
            col_taken_values = [v for v in col if v]

            cluster = [
                v
                for v in iter_grid_cluster(
                    solved_grid, cell_cluster[0], cell_cluster[1]
                )
            ]
            cluster_taken_values = [v for v in cluster if v]
            print(
                f"Cluster taken values for cluster {cell_cluster} : {cluster_taken_values}"
            )
            taken_values = row_taken_values + col_taken_values + cluster_taken_values
            taken_values = set(taken_values)
            taken_values = [v for v in taken_values if v]
            # if x == 4 and y == 4:
            #     print("Cell CANNOT contain any of these values: %s" % taken_values)

            for taken_value in taken_values:
                solve_matrix = remove_value_from_solve_matrix(
                    solve_matrix, x, y, taken_value
                )
            if is_cell_solved(solve_matrix, x, y):
                print(
                    f"Solved cell:({x},{y}) to {solve_matrix_cell(solve_matrix, x, y)}"
                )

        print("-" * 20)

        solved_grid = collapse_solve_matrix(solve_matrix)
        print("Solve iteration: %s" % attempt)
        print_grid(solved_grid)

        pass


if __name__ == "__main__":
    main()
