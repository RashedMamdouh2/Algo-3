from collections import deque
dx = [-1, -1, -1, 0, 1, 1, 1, 0]
dy = [-1, 0, 1, 1, 1, 0, -1, -1]

def validIndix(r, c, n, m):
    return 0 <= r < n and 0 <= c < m

def bfs(x, y, grid):
    q = deque()
    n = len(grid)
    m = len(grid[0])
    q.append((x, y))
    visited = [[0 for _ in range(m)] for _ in range(n)]

    visited[x][y] = 1
    level = 2

    while len(q):
        sz = len(q)

        level += 1

        while sz:
            sz -= 1
            parent = q.popleft()
            for i in range(8):
                r = parent[0] + dx[i]
                c = parent[1] + dy[i]
                if validIndix(r, c, n, m):
                    if not visited[r][c] and (grid[r][c] == 0 or grid[r][c] == 2):
                        visited[r][c] = 1
                        q.append((r, c))
                        grid[r][c] = level

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



