# =============================================
# IMPORTS AND INITIALIZATION
# =============================================

# pygame: Main library for creating the game window and handling graphics
# deque: Used for implementing the BFS (Breadth-First Search) algorithm efficiently
# time: Used for adding delays in animations to make moves visible
import pygame
from collections import deque
import time

# Initialize all pygame modules
pygame.init()

# Game board configuration
S = 8    # Board size (8x8 chess board)
T = 80   # Tile size in pixels (each square is 80x80 pixels)
BOARD_SIZE = S * T  # Chess board dimensions (640x640 pixels)
BAR_HEIGHT = 60     # Height of the bottom UI panel
W = BOARD_SIZE      # Window width (640 pixels)
H = BOARD_SIZE + BAR_HEIGHT  # Window height (700 pixels)

# Create the game window
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Black Bishop Hunt")  # Window title
font = pygame.font.Font(None, 40)  # Font for text display (size 40)

# =============================================
# COLOR DEFINITIONS
# =============================================
# All colors are defined as RGB tuples (Red, Green, Blue)
# Some colors include alpha channel (transparency) as fourth value
WHITE = (255, 255, 255)          # Pure white
BLACK = (0, 0, 0)                # Pure black
LIGHT_SQ = (240, 217, 181)       # Light square color (beige)
DARK_SQ = (181, 136, 99)         # Dark square color (brown)
HIGHLIGHT = (247, 247, 105, 150) # Yellow highlight with transparency
MOVE_HIGHLIGHT = (124, 252, 0, 150)    # Green highlight for possible moves
CAPTURE_HIGHLIGHT = (220, 20, 60, 150) # Red highlight for capture moves

# =============================================
# ASSET LOADING
# =============================================
# Load and scale all chess piece images to fit the tile size
# Each image is scaled to T x T pixels (80x80)
bishop = pygame.transform.scale(pygame.image.load("assets/images/black bishop.png"), (T, T))
piece_images = {
    "pawn": pygame.transform.scale(pygame.image.load("assets/images/white pawn.png"), (T, T)),
    "knight": pygame.transform.scale(pygame.image.load("assets/images/white knight.png"), (T, T)),
    "bishop": pygame.transform.scale(pygame.image.load("assets/images/white bishop.png"), (T, T)),
    "rook": pygame.transform.scale(pygame.image.load("assets/images/white rook.png"), (T, T)),
    "queen": pygame.transform.scale(pygame.image.load("assets/images/white queen.png"), (T, T)),
    "king": pygame.transform.scale(pygame.image.load("assets/images/white king.png"), (T, T))
}

# =============================================
# GAME CONFIGURATION
# =============================================
# Define piece priorities and values for targeting
# Format: "piece_name": (priority, value)
# Lower priority number = higher priority
# Higher value = more valuable piece
piece_priority = {
    "king": (1, 0),    # Highest priority (1), but value 0 (not captured)
    "queen": (2, 9),   # Second priority, highest value (9)
    "rook": (3, 5),    # Third priority, medium-high value (5)
    "bishop": (4, 3),  # Fourth priority, medium value (3)
    "knight": (4, 3),  # Same priority as bishop, same value (3)
    "pawn": (5, 1)     # Lowest priority, lowest value (1)
}

# =============================================
# GAME STATE VARIABLES
# =============================================
# Initialize all game state variables
b_pos = None           # Black bishop's position [row, col]
pieces = []            # List of white pieces on the board
path = []              # Current path being followed
started = False        # Whether the game has started
highlighted_cells = [] # Cells to highlight
last_move = None       # Last move made by the bishop

# =============================================
# PIECE SELECTION SETTINGS
# =============================================
# Configuration for piece placement
selected_type = "pawn"  # Currently selected piece type
# Maximum number of each piece type allowed on the board
allowed_counts = {
    "king": 1,    # Only one king
    "queen": 1,   # Only one queen
    "rook": 2,    # Two rooks
    "bishop": 2,  # Two bishops
    "knight": 2,  # Two knights
    "pawn": 8     # Eight pawns
}
# Current count of each piece type on the board
counts = {k: 0 for k in allowed_counts}
# Keyboard shortcuts for piece selection (1-6 keys)
key_to_piece = {
    pygame.K_1: "pawn",
    pygame.K_2: "knight",
    pygame.K_3: "bishop",
    pygame.K_4: "rook",
    pygame.K_5: "queen",
    pygame.K_6: "king"
}

def draw_board():
    """
    Draw the complete game board including:
    - Chess board squares
    - All pieces
    - Highlights for moves and captures
    - UI elements
    - Reset button
    """
    # Draw the chess board squares
    for r in range(S):
        for c in range(S):
            # Alternate between light and dark squares
            # (r + c) % 2 == 0 creates the checkerboard pattern
            color = LIGHT_SQ if (r + c) % 2 == 0 else DARK_SQ
            pygame.draw.rect(screen, color, (c * T, r * T, T, T))

    # Highlight the last move made
    if last_move:
        s = pygame.Surface((T, T), pygame.SRCALPHA)  # Create transparent surface
        s.fill(MOVE_HIGHLIGHT)
        screen.blit(s, (last_move[1] * T, last_move[0] * T))

    # Highlight the current path and possible moves
    for i, cell in enumerate(highlighted_cells):
        s = pygame.Surface((T, T), pygame.SRCALPHA)
        # Use different color for capture moves (last cell in path)
        if i == len(highlighted_cells) - 1 and any(p["pos"] == cell for p in pieces):
            s.fill(CAPTURE_HIGHLIGHT)  # Red for capture
        else:
            s.fill(MOVE_HIGHLIGHT)     # Green for normal moves
        screen.blit(s, (cell[1] * T, cell[0] * T))

    # Draw all white pieces
    for p in pieces:
        screen.blit(piece_images[p["type"]], (p["pos"][1] * T, p["pos"][0] * T))

    # Draw the black bishop with a pulsing effect
    if b_pos:
        # Create pulsing effect based on time
        pulse = int(10 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
        bishop_scaled = pygame.transform.scale(bishop, (T + pulse, T + pulse))
        screen.blit(bishop_scaled, (b_pos[1] * T - pulse // 2, b_pos[0] * T - pulse // 2))

    # Draw the UI panel below the board
    pygame.draw.rect(screen, WHITE, (0, BOARD_SIZE, W, BAR_HEIGHT))

    # Show selected piece and count
    info_text = f"Selected: {selected_type} ({counts[selected_type]}/{allowed_counts[selected_type]})"
    text_surface = font.render(info_text, True, BLACK)
    screen.blit(text_surface, (20, BOARD_SIZE + 16))

    # Draw reset button if game has started
    if started:
        btn = pygame.Rect(W - 120, BOARD_SIZE + 12, 100, 36)
        pygame.draw.rect(screen, (200, 50, 50), btn)  # Red button
        reset_text = font.render("Reset", True, WHITE)
        screen.blit(reset_text, reset_text.get_rect(center=btn.center))

def is_path_clear(start, end):
    """
    Check if the path between two points is clear of other pieces
    Args:
        start: Starting position [row, col]
        end: Ending position [row, col]
    Returns:
        bool: True if path is clear, False if blocked
    """
    # Calculate direction of movement
    dx = 1 if end[0] > start[0] else -1
    dy = 1 if end[1] > start[1] else -1

    # Check each square along the path
    x, y = start[0] + dx, start[1] + dy
    while x != end[0] and y != end[1]:
        # If any piece is found along the path, it's blocked
        if any(p["pos"] == [x, y] for p in pieces):
            return False
        x += dx
        y += dy
    return True

def get_valid_moves(b_pos, pieces):
    """
    Get all valid moves for the bishop from its current position
    Args:
        b_pos: Bishop's current position [row, col]
        pieces: List of all pieces on the board
    Returns:
        list: List of valid move positions
    """
    moves = []
    # All possible diagonal directions for a bishop
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Check each direction
    for dr, dc in directions:
        # Check each square in that direction
        for i in range(1, 8):
            r, c = b_pos[0] + dr * i, b_pos[1] + dc * i
            # Check if within board bounds
            if 0 <= r < S and 0 <= c < S:
                # Check if there's a piece at this position
                piece_at_pos = next((p for p in pieces if p["pos"] == [r, c]), None)

                if piece_at_pos:
                    # Do not allow capturing or stepping onto the king
                    if piece_at_pos["type"] != "king" and is_path_clear(b_pos, [r, c]):
                        moves.append((r, c))
                    break  # Can't move further in this direction
                else:
                    # If path is clear, can move to empty square
                    if is_path_clear(b_pos, [r, c]):
                        moves.append((r, c))
            else:
                break  # Out of board bounds
    return moves

def bfs(s, e, pieces):
    """
    Breadth-First Search to find the shortest path to a target piece
    Args:
        s: Start position [row, col]
        e: End position [row, col]
        pieces: List of all pieces on the board
    Returns:
        list: Shortest path from start to end, or empty list if no path exists
    """
    # Initialize visited and parent arrays
    visited = [[False] * S for _ in range(S)]
    parent = [[None] * S for _ in range(S)]
    queue = deque([s])
    visited[s[0]][s[1]] = True

    # BFS main loop
    while queue:
        x, y = queue.popleft()
        # If reached target, reconstruct and return path
        if [x, y] == e:
            path = []
            while [x, y] != s:
                path.append([x, y])
                x, y = parent[x][y]
            return path[::-1]  # Reverse path to get start->end order

        # Check all valid moves from current position
        for move in get_valid_moves([x, y], pieces):
            nx, ny = move
            if not visited[nx][ny]:
                visited[nx][ny] = True
                parent[nx][ny] = (x, y)
                queue.append((nx, ny))
    return []  # No path found

def auto_move():
    """
    Make one move with the black bishop, avoiding the king
    This function:
    1. Finds all reachable pieces
    2. Sorts them by priority and value
    3. Makes one move towards the highest priority target
    4. Updates the game state
    """
    global b_pos, pieces, highlighted_cells, last_move

    # Find all reachable pieces with their priority and path
    targets = []
    for piece in pieces:
        # Skip if the piece is a king
        if piece["type"] == "king":
            continue
        path = bfs(b_pos, piece["pos"], pieces)
        if path:
            priority, value = piece_priority[piece["type"]]
            targets.append((piece, priority, value, path))

    if not targets:
        return  # No valid targets found

    # Sort targets by:
    # 1. Priority (lower number = higher priority)
    # 2. Value (higher number = more valuable)
    # 3. Path length (shorter path preferred)
    targets.sort(key=lambda x: (x[1], -x[2], len(x[3])))

    # Get the best target and its path
    target_piece, _, _, path = targets[0]
    highlighted_cells = path.copy()

    # Make the move
    if path:
        step = path[0]  # Take only the first step
        last_move = b_pos  # Remember the last position
        b_pos = step      # Update bishop position

        # Check if this move captures a piece
        captured = next((p for p in pieces if p["pos"] == step), None)
        if captured:
            pieces.remove(captured)  # Remove captured piece
            draw_board()
            pygame.display.flip()
            time.sleep(1.0)  # Pause to show capture

        # Update display
        draw_board()
        pygame.display.flip()
        time.sleep(1.0)  # Pause to show move

    # Clear highlights
    highlighted_cells = []
    draw_board()
    pygame.display.flip()
    time.sleep(1.0)

# =============================================
# MAIN GAME LOOP
# =============================================
clock = pygame.time.Clock()
running = True

while running:
    # Handle all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Handle reset button click
            if started and W - 120 <= x <= W - 20 and BOARD_SIZE + 12 <= y <= BOARD_SIZE + 48:
                # Reset all game state
                b_pos = None
                pieces = []
                counts = {k: 0 for k in allowed_counts}
                started = False
                last_move = None
                continue

            # Ignore clicks on the bottom UI panel
            if y >= BOARD_SIZE:
                continue

            r, c = y // T, x // T  # Convert pixel position to board coordinates

            # Handle piece placement
            if not started:
                if not b_pos:
                    b_pos = [r, c]  # Place black bishop
                else:
                    # Place white piece if:
                    # 1. Not on bishop's position
                    # 2. Not on another piece
                    # 3. Haven't exceeded piece limit
                    if [r, c] != b_pos and not any(p["pos"] == [r, c] for p in pieces):
                        if counts[selected_type] < allowed_counts[selected_type]:
                            pieces.append({"type": selected_type, "pos": [r, c]})
                            counts[selected_type] += 1

        elif event.type == pygame.KEYDOWN:
            # Start game with space bar
            if event.key == pygame.K_SPACE and b_pos and pieces and not started:
                started = True
                auto_move()
            # Change selected piece type with number keys
            elif event.key in key_to_piece:
                selected_type = key_to_piece[event.key]

    # Update display
    draw_board()
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS

# Clean up
pygame.quit()