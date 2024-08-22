import random
import matplotlib.pyplot as plt
from collections import deque
import os

# Directions for movement: Down, Up, Right, Left
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def generate_maze_dfs_iterative(width, height):
    # Create a grid of walls
    maze = [[1] * (2 * width + 1) for _ in range(2 * height + 1)]

    # Start stack with the starting point
    stack = [(0, 0)]
    maze[1][1] = 0  # Mark the start point as part of the maze

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)  # Randomize the order of directions to move

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and maze[2 * nx + 1][2 * ny + 1] == 1:
                # Break the wall between the current cell and the new cell
                maze[2 * x + 1 + dx][2 * y + 1 + dy] = 0
                maze[2 * nx + 1][2 * ny + 1] = 0  # Mark the new cell as part of the maze
                stack.append((nx, ny))  # Add the new cell to the stack
                break
        else:
            stack.pop()  # Backtrack if no valid moves are available

    # Open the entrance and exit
    maze[1][0] = 0  # Entrance at the top-left corner
    maze[2 * height - 1][2 * width] = 0  # Exit at the bottom-right corner

    return maze

def solve_maze_bfs(maze):
    height = len(maze)
    width = len(maze[0])
    
    start = (1, 0)  # Entrance (top-left corner)
    end = (height - 2, width - 1)  # Exit (bottom-right corner)

    # Queue for BFS and a dictionary to track the path
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            break

        x, y = current

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and maze[nx][ny] == 0 and (nx, ny) not in came_from:
                queue.append((nx, ny))
                came_from[(nx, ny)] = current

    # Reconstruct the path from end to start
    path = []
    step = end
    while step:
        path.append(step)
        step = came_from[step]

    path.reverse()  # Reverse the path to get it from start to end

    return path

def save_maze(maze, save_path, dpi):
    plt.figure(figsize=(15, 15))
    plt.imshow(maze, cmap=plt.cm.binary)
    plt.xticks([]), plt.yticks([])  # Remove axis labels
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()

def save_solution(maze, path, save_path, dpi):
    maze_copy = [row[:] for row in maze]  # Copy the maze for visualization

    # Mark the solution path in the maze
    for (x, y) in path:
        maze_copy[x][y] = 2  # Use '2' to mark the solution path

    plt.figure(figsize=(15, 15))
    plt.imshow(maze_copy, cmap=plt.cm.binary)
    plt.xticks([]), plt.yticks([])  # Remove axis labels
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()

# Example usage
width, height = 50, 50  # Size of the maze
output_dir = 'mazes'
os.makedirs(output_dir, exist_ok=True)

for i in range(100):
    maze = generate_maze_dfs_iterative(width, height)
    solution_path = solve_maze_bfs(maze)

    # Save the maze and its solution
    maze_save_path = os.path.join(output_dir, f'maze_{i+1:03d}.png')
    solution_save_path = os.path.join(output_dir, f'solution_{i+1:03d}.png')
    
    save_maze(maze, maze_save_path, dpi=600)
    save_solution(maze, solution_path, solution_save_path, dpi=600)
    
    print(f'Saved maze {i+1} and its solution.')

print('All mazes and solutions have been saved.')