import tkinter as tk
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk
from constants import *
from aliens import create_aliens, move_aliens
from player import move_left, move_right, stop_left, stop_right, fire_bullet, move_player, move_bullets, move_missiles
from collision import check_collisions, update_score, check_block_collision
from stars import create_stars, animate_stars

# Game State
game_state = {
    'player_lives': 3,
    'score': 0,
    'game_over': False
}
aliens = []
bullets = []
missiles = []
player_movement = {"left": False, "right": False}
direction = 1  # Initial movement direction of aliens (1 for right, -1 for left)
move_down = False  # Flag to trigger downward movement when aliens hit the edge

# Set up the main window
root = tk.Tk()
root.title("Space Invaders")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Load images
alien_images = {
    "red": [ImageTk.PhotoImage(Image.open("assets/alien1_1.png")), ImageTk.PhotoImage(Image.open("assets/alien1_2.png"))],
    "green": [ImageTk.PhotoImage(Image.open("assets/alien2_1.png")), ImageTk.PhotoImage(Image.open("assets/alien2_2.png"))],
    "yellow": [ImageTk.PhotoImage(Image.open("assets/alien3_1.png")), ImageTk.PhotoImage(Image.open("assets/alien3_2.png"))],
}
missile_image = ImageTk.PhotoImage(Image.open("assets/missile.png"))

# Create player
player = canvas.create_rectangle(WIDTH // 2 - 15, HEIGHT - 50, WIDTH // 2 + 15, HEIGHT - 40, fill="blue")

# Function to create an image from text with a transparent background
def text_to_image_map(text, font_path, font_size, text_color):
    image_width = len(text) * font_size
    image_height = font_size
    image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text((0, 0), text, fill=text_color, font=font)
    return image

# Create the block image
block_image_pil = text_to_image_map(BLOCK_TEXT, "assets/arial.ttf", FONT_SIZE, "white")
block_image = ImageTk.PhotoImage(block_image_pil)

# Display the block image above the player
def create_block_image(canvas, block_image):
    block_x = WIDTH // 2  # Center horizontally
    block_y = HEIGHT - BLOCK_HEIGHT - 2 * ALIEN_HEIGHT  # Position above the player
    block_image_item = canvas.create_image(block_x, block_y, image=block_image, anchor="center")
    return block_image_item

def start_game():
    global bullets, missiles, player_movement, player, aliens, block_image_item, block_image_pil
    game_state['player_lives'] = 3
    game_state['score'] = 0
    game_state['game_over'] = False
    bullets = []
    missiles = []
    canvas.delete("all")  # Clear all canvas items
    create_stars(canvas)  # Draw the stars

    # Re-create the player (gun platform)
    player = canvas.create_rectangle(WIDTH // 2 - 15, HEIGHT - 50, WIDTH // 2 + 15, HEIGHT - 40, fill="blue")

    aliens = create_aliens(canvas, alien_images)  # Capture the returned aliens list
    block_image_item = create_block_image(canvas, block_image)  # Create block above player
    update_score(canvas, game_state)  # Update the score display
    root.after(1000, lambda: game_loop(aliens, alien_images, ALIEN_MOVE_SPEED, direction, move_down))  # Start game loop after 1 second

def restart_game(event=None):
    start_game()

def game_loop(aliens, alien_images, ALIEN_MOVE_SPEED, direction, move_down):
    if not game_state['game_over']:
        print(f"Game loop running. Aliens remaining: {len(aliens)}")

        # Move the player based on user input (left and right)
        move_player(canvas, player, player_movement)

        # Move aliens and update their speed if needed
        direction, move_down = move_aliens(canvas, aliens, missiles, ALIEN_MOVE_SPEED, missile_image, alien_images, direction, move_down)

        # Move bullets (player's missiles)
        move_bullets(canvas, bullets)

        # Move missiles (aliens' projectiles)
        move_missiles(canvas, missiles)

        # Check for collisions between bullets, missiles, and aliens
        check_collisions(canvas, bullets, missiles, aliens, player, game_state)

        # Check for block collisions (between missiles and block image)
        check_block_collision(canvas, missiles, block_image_item, block_image_pil)

        # Update score display on the screen
        update_score(canvas, game_state)

        # Schedule the next iteration of the game loop (runs every 50ms)
        root.after(50, lambda: game_loop(aliens, alien_images, ALIEN_MOVE_SPEED, direction, move_down))  # Pass direction and move_down to the next loop iteration
    else:
        print("Game Over or Victory condition reached.")
        # Optionally, display a 'Game Over' or 'Victory' message
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill="red", font=("Arial", 30))

# Bind keys for player movement, firing, and restarting the game
root.bind("<Left>", lambda event: move_left(event, player_movement))  # Left arrow key moves player left
root.bind("<Right>", lambda event: move_right(event, player_movement))  # Right arrow key moves player right
root.bind("<KeyRelease-Left>", lambda event: stop_left(event, player_movement))  # When left key is released, stop left movement
root.bind("<KeyRelease-Right>", lambda event: stop_right(event, player_movement))  # When right key is released, stop right movement
root.bind("<space>", lambda event: fire_bullet(event, canvas, bullets, missile_image, player))  # Spacebar to fire missile
root.bind("<r>", restart_game)  # Press 'r' to restart the game

animate_stars(canvas, root)
start_game()
root.mainloop()
