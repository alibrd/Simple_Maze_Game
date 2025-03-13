import pygame
import random
import sys

# Constants
MAZE_ROWS = 7  # Number of rows/columns
CELL_SIZE = 40    # Size (in pixels) of each cell.
SEED = 8     # Deterministic seed for maze generation.

def generate_maze(n):
    """
    Generate a perfect maze using recursive backtracking.
    
    The maze is represented as a grid of size (2*n + 1) x (2*n + 1):
      - 1 indicates a wall.
      - 0 indicates an open cell.
    
    Starting at (1,1), the algorithm carves out passages by jumping two cells at a time,
    ensuring exactly one path exists between any two open cells.
    """
    width = n + 2 # + 2 to add the walls around the board
    height = n + 2
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve(x, y):
        maze[y][x] = 0  # Mark the current cell as open.
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)  # Randomize carving order.
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                # Remove wall between current and neighbor cells.
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)
    
    carve(1, 1)
    maze[width-2][height-2] = 0 # make sure the cheese is accesible
    return maze

def handle_events(mouse_pos, maze, maze_width, maze_height, won):
    """
    Process pygame events and update the mouse's position.
    
    Only allow movement if the game has not been won.
    Returns the (possibly updated) mouse position and a running flag.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return mouse_pos, False
        elif event.type == pygame.KEYDOWN and not won:
            new_x, new_y = mouse_pos[0], mouse_pos[1]
            if event.key == pygame.K_UP:
                new_y -= 1
            elif event.key == pygame.K_DOWN:
                new_y += 1
            elif event.key == pygame.K_LEFT:
                new_x -= 1
            elif event.key == pygame.K_RIGHT:
                new_x += 1
            
            # Check bounds and whether the new cell is an open space.
            if 0 <= new_x < maze_width and 0 <= new_y < maze_height:
                if maze[new_y][new_x] == 0:
                    mouse_pos = [new_x, new_y]
    return mouse_pos, True

def draw_maze(screen, maze, cell_size):
    """
    Draw the maze grid on the pygame screen.
    
    Walls are white and open cells are black.
    """
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, (255, 255, 255), rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect)

def draw_entities(screen, mouse_pos, cheese_pos, cell_size):
    """
    Draw the mouse and the cheese on the screen.
    
    The cheese is drawn in gold and the mouse in red.
    """
    # Draw cheese (gold).
    cheese_rect = pygame.Rect(cheese_pos[0] * cell_size, cheese_pos[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, (255, 215, 0), cheese_rect)
    
    # Draw mouse (red).
    mouse_rect = pygame.Rect(mouse_pos[0] * cell_size, mouse_pos[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, (255, 0, 0), mouse_rect)

def display_win(screen, font, window_width, window_height):
    """
    Display the winning message on the screen.
    """
    text = font.render("You Win!", True, (0, 255, 0))
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    screen.blit(text, text_rect)

def main():
    # Seed the random number generator.
    random.seed(SEED)
    
    # Generate the maze.
    maze = generate_maze(MAZE_ROWS)
    maze_width = len(maze[0])
    maze_height = len(maze)
    
    # Calculate window dimensions based on the maze size.
    window_width = maze_width * CELL_SIZE
    window_height = maze_height * CELL_SIZE
    
    # Initialize pygame.
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Maze Game: Mouse and Cheese")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    
    # Set initial positions.
    mouse_pos = [1, 1]  # Mouse starts at the top left open cell.
    cheese_pos = (maze_width - 2, maze_height - 2)  # Cheese is at the bottom right open cell.
    
    running = True
    won = False
    
    # Main game loop.
    while running:
        mouse_pos, running = handle_events(mouse_pos, maze, maze_width, maze_height, won)
        
        # Check if the mouse has reached the cheese.
        if mouse_pos[0] == cheese_pos[0] and mouse_pos[1] == cheese_pos[1]:
            won = True
        
        # Draw the maze and game entities.
        draw_maze(screen, maze, CELL_SIZE)
        draw_entities(screen, mouse_pos, cheese_pos, CELL_SIZE)
        
        # Display winning message if applicable.
        if won:
            display_win(screen, font, window_width, window_height)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
