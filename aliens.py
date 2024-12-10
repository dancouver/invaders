import random
from constants import *

# Create aliens and place them on the canvas
def create_aliens(canvas, alien_images):
    aliens = []
    rows = 3
    cols = 8
    space_between_aliens = 50
    starting_x = 50
    starting_y = 60

    for row in range(rows):
        for col in range(cols):
            alien_type = random.choice(list(alien_images.keys()))  # Randomly choose alien type
            alien_image = random.choice(alien_images[alien_type])  # Randomly choose one of the alien images for this type
            x = starting_x + col * space_between_aliens
            y = starting_y + row * space_between_aliens

            alien = canvas.create_image(x, y, image=alien_image)
            alien_info = {
                "alien": alien,
                "type": alien_type,
                "image": alien_image,
                "missile": None,
                "animation_state": 0  # Initialize animation_state
            }
            aliens.append(alien_info)

    print(f"Aliens created: {len(aliens)}")
    return aliens

# Move aliens and make them fire missiles
def move_aliens(canvas, aliens, missiles, ALIEN_MOVE_SPEED, missile_image, alien_images, direction, move_down):
    for alien_info in aliens:
        # Alternate between alien images for animation
        alien_info["animation_state"] = (alien_info["animation_state"] + 1) % 2  # Toggle between 0 and 1
        alien_info["image"] = alien_images[alien_info["type"]][alien_info["animation_state"]]
        canvas.itemconfig(alien_info["alien"], image=alien_info["image"])  # Update the alien image on the canvas

        # Randomly decide if the alien will fire a missile
        if random.random() < 0.01:  # Random chance for alien to fire
            fire_alien_missile(canvas, alien_info, missiles, missile_image)

        # Check if any alien has reached the left or right edge of the canvas
        x1, y1 = canvas.coords(alien_info["alien"])
        if x1 + ALIEN_MOVE_SPEED * direction < 0 or x1 + ALIEN_MOVE_SPEED * direction > WIDTH:
            move_down = True  # Set move_down to True when edge is reached

    if move_down:
        # Move aliens down after reaching the edge
        print("Aliens reached the edge, moving down.")
        for alien_info in aliens[:]:
            # Move aliens down by one step
            canvas.move(alien_info["alien"], 0, ALIEN_HEIGHT)  # Move down

            # Ensure aliens don't move past the bottom of the screen
            coords = canvas.coords(alien_info["alien"])
            if coords[1] + ALIEN_HEIGHT > HEIGHT:  # Prevent them from going past the bottom
                canvas.move(alien_info["alien"], 0, HEIGHT - coords[1] - ALIEN_HEIGHT)

        direction *= -1  # Reverse horizontal direction (left to right or right to left)
        move_down = False  # Reset move_down flag after moving down
    else:
        # Move aliens horizontally
        for alien_info in aliens[:]:
            canvas.move(alien_info["alien"], ALIEN_MOVE_SPEED * direction, 0)  # Move horizontally

    return direction, move_down  # Return updated direction and move_down state

# Fire a missile from an alien
def fire_alien_missile(canvas, alien_info, missiles, missile_image):
    x1, y1 = canvas.coords(alien_info["alien"])
    missile = canvas.create_image(x1, y1 + ALIEN_HEIGHT, image=missile_image, anchor="n")
    missiles.append(missile)
    alien_info["missile"] = missile  # Store missile information in alien data
