N, S, E, W = 1, 2, 4, 8
HORIZONTAL, VERTICAL = 0, 1

def divide(grid, mx, my, ax, ay):
    dx = ax - mx
    dy = ay - my
    if dx < 2 or dy < 2:
        # make a hallway
        if dx > 1:
            y = my
            for x in xrange(mx, ax-1):
                grid[y][x] |= E
                grid[y][x+1] |= W
        elif dy > 1:
            x = mx
            for y in xrange(my, ay-1):
                grid[y][x] |= S
                grid[y+1][x] |= N
        return

    wall = HORIZONTAL if dy > dx else (VERTICAL if dx > dy else random.randrange(2))

    xp = random.randrange(mx, ax-(wall == VERTICAL))
    yp = random.randrange(my, ay-(wall == HORIZONTAL))

    x, y = xp, yp
    if wall == HORIZONTAL:
        ny = y + 1
        grid[y][x] |= S
        grid[ny][x] |= N

        divide(grid, mx, my, ax, ny)
        divide(grid, mx, ny, ax, ay)
    else:
        nx = x + 1
        grid[y][x] |= E
        grid[y][nx] |= W

        divide(grid, mx, my, nx, ay)
        divide(grid, nx, my, ax, ay)