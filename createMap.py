dx = [+0, +1, -1, +0, +1, +1, -1, -1]
dy = [-1, +0, +0, +1, -1, +1, +1, -1]
def validIndix(r, c, n, m):
    return 0 <= r < n and 0 <= c < m

def bfs(x, y, grid):
    q = []
    n = len(grid)
    m = len(grid[0])
    q.append((x, y))
    visited = [[0 for _ in range(m)] for _ in range(n)]
    front = 0
    visited[x][y] = 1
    level = 2

    while len(q) - front:
        sz = len(q) - front
        level += 1

        while sz:
            sz -= 1
            parent = q[front]
            front += 1

            for i in range(8):
                r = parent[0] + dx[i]
                c = parent[1] + dy[i]
                if validIndix(r, c, n, m):
                    if not visited[r][c] and (grid[r][c] == 0 or grid[r][c] == 2):
                        visited[r][c] = 1
                        q.append((r, c))
                        grid[r][c] = level


def track_the_path(grid, start, goal):
    path = []
    n = len(grid)
    m = len(grid[0])
    path.append(start)
    cur = start
    minimum_neighbour = None
    minimum_cost = float('inf')

    while cur != goal:
        for i in range(8):
            r = cur[0] + dx[i]
            c = cur[1] + dy[i]
            if validIndix(r, c, n, m):
                if grid[r][c] != 1 and grid[r][c] < minimum_cost:
                    minimum_cost = grid[r][c]
                    minimum_neighbour = (r, c)
        cur = minimum_neighbour
        path.append(cur)

    return path


def solve():
    n, m = 14, 20
    x, y = map(int, input().split())
    goalX, goalY = x, y
    grid = []
    for i in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
        for j in range(m):
            if grid[i][j] == 2:
                x, y = i, j

    bfs(x, y, grid)
    for r in grid:
        for c in r:
            print(c, end=" ")
        print()

    path = track_the_path(grid, (goalX, goalY), (x, y))
    for p in path:
        print(p[0], p[1])




solve()
