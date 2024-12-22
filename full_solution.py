import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors



def visualize_path(map_data, trajectory):
    """
    Visualizes the environment and the planned trajectory
    
    Args:
        map_data (list): 2D list representing the environment
        trajectory (list): List of coordinates representing the path
    """
    plt.figure(figsize=(12, 8))
    plt.imshow(map_data, cmap='binary')
    
    # Plot trajectory
    traj_y, traj_x = zip(*trajectory)
    plt.plot(traj_x, traj_y, 'r-', linewidth=2, label='Trajectory')
    
    plt.grid(True)
    plt.legend()
    plt.title('Wavefront Planner Path')
    plt.show()

def plot_map(matrix):
    # Define the colors for the cells
    # 0 -> white, 1 -> grey, 2 -> green, other -> red
    cmap = mcolors.ListedColormap(['grey', 'green', 'red', 'white'])

    masked_matrix = np.where((matrix == 0) | (matrix == 1) | (matrix == 2), matrix, 3)

    
    fig, ax = plt.subplots()

  
    cax = ax.imshow(masked_matrix, cmap=cmap, interpolation='nearest')

    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, str(int(matrix[i, j])), ha='center', va='center', color='black', fontsize=8)

    ax.axis('off')
    # Show the plot without axes and color bar
    plt.show()



#Dirictions in x and y axis
dx = [+0, +1, -1, +0, +1, +1, -1, -1]
dy = [-1, +0, +0, +1, -1, +1, +1, -1]
def valid_indix(r, c, n, m):
    return 0 <= r < n and 0 <= c < m

def bfs(x, y, grid):
    '''
    The Breadth first search algorithm is a level by level search algorithm on the graph
    (the map cells are verticies and the neighbouring relation is the edges)
    '''
    #initial list to store the neighbours of the free space cells
    q = []
    n = len(grid)
    m = len(grid[0])

    #add the initial position
    q.append((x, y))
    #boolean map to mark each cell if it has been visited or not yet to avoid infinite loops
    visited = [[0 for _ in range(m)] for _ in range(n)]
    
    #front variable to determine the index of the coming cell of q list in each iteration
    front = 0

    visited[x][y] = 1
    #the level variable to mark the level of neighbourhood of each cell from the start x,y point (the goal point value is 2)
    level = 2
    
    while len(q) - front:
        
        #The real size of non looped cells (because we're not poping the looped cells we can use deque and popleft to hundle this)
        sz = len(q) - front

        #increase the level of neighbouring the initial position each iteration
        level += 1

        while sz:
            sz -= 1
            parent = q[front]
            front += 1

            #loop in the 8th dirictions of neighbours
            for i in range(8):
                r = parent[0] + dx[i]
                c = parent[1] + dy[i]

                #valid_indix function that ensures that we're not exceeding the borders of the map
                if valid_indix(r, c, n, m):
                    #if it's a free space cell or the goal point we can access it 
                    if not visited[r][c] and (grid[r][c] == 0 or grid[r][c] == 2):
                        visited[r][c] = 1
                        q.append((r, c))
                        grid[r][c] = level


def track_the_path(grid, start, goal):
    '''
    looping on the neighbours of the current cell to determine the minimum cost cell to move to
    (if more than one cell has the minimum cost we follows the priority such as :[upper, Right, Lower, Left, Upper right, lower
        right, Lower Left, Upper Left])
    '''
    path = []
    n = len(grid)
    m = len(grid[0])
    path.append(start)
    cur = start
    minimum_neighbour = None
    minimum_cost = float('inf')

    #Checking if we reach the goal or not yet 
    while cur != goal:
        for i in range(8):
            r = cur[0] + dx[i]
            c = cur[1] + dy[i]
            if valid_indix(r, c, n, m):
                if grid[r][c] != 1 and grid[r][c] < minimum_cost:
                    minimum_cost = grid[r][c]
                    minimum_neighbour = (r, c)
        cur = minimum_neighbour
        path.append(cur)

    return path

def planner(map, start_row, start_column):
    #convert the start point from 1-based to 0-based (to be a valid indix in the map)
    start_row-=1
    start_column-=1

    goal_x,goal_y=0,0
    #Looping on the map to find the position of the goal point
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 2:
                goal_x, goal_y = i, j
                break
    #take a copy of the original map to edit on 
    value_map=map
    #Use the bfs algorithm to mark each cell with it's level of neighboring from the goal point (it's edit on the passed value_map)
    bfs(goal_x,goal_y,value_map)

    #Use the track_the_path function that gets the optimal path 
    trajectory=track_the_path(value_map,(start_row,start_column),(goal_x,goal_y))

    #Visualize the path and the map
    visualize_path(value_map, trajectory)
    plot_map(np.array(value_map))

    return value_map,trajectory
    

def test():
    '''
    This function for testing and taking input map and start position from the user in the Terminal
    
    '''
    n, m = 14, 20
    print('Enter the start position')
    x, y = map(int, input().split())
    grid = []
    print("Enter the map: ")
    for i in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
       
        
    test_map,path =planner(grid,x,y)
 
   
