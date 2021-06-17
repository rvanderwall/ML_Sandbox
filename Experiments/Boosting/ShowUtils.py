
#
#  Data will come in tuples of the form (x, y), label
#  range from 0 to max_x, inclusive
#
def show_data(data_set):
    grid = []

    for y in range(data_set.max_y + 1):
        row = []
        for x in range(data_set.max_x + 1):
            row.append(".")
        grid.append(row)

    for d in data_set.data:
        (x, y), v = d
        if v > 0:
            mark = "+"
        else:
            mark = "-"
        grid[data_set.max_y - y][x] = mark
    for row in grid:
        print row
