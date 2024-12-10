from constants import *

def move_left(event, player_movement):
    player_movement["left"] = True

def move_right(event, player_movement):
    player_movement["right"] = True

def stop_left(event, player_movement):
    player_movement["left"] = False

def stop_right(event, player_movement):
    player_movement["right"] = False

# Fire missile (player side)
def fire_bullet(event, canvas, bullets, missile_image, player):
    try:
        if canvas.coords(player):  # Ensure the player exists
            x1, y1, x2, y2 = canvas.coords(player)

            # Create a new missile (bullet) just above the player
            bullet = canvas.create_image((x1 + x2) // 2, y1 - 10, image=missile_image, anchor="n")

            # Ensure the missile is added to the bullets list
            bullets.append(bullet)

            # Print statement for debugging
            print(f"Bullet fired at: {x1}, {y1}")
    except Exception as e:
        print(f"Error firing bullet: {e}")

def move_player(canvas, player, player_movement):
    if player_movement["left"]:
        canvas.move(player, -PLAYER_SPEED, 0)
        x1, y1, x2, y2 = canvas.coords(player)
        if x1 < 0:  # Prevent moving off the left edge
            canvas.move(player, -x1, 0)

    if player_movement["right"]:
        canvas.move(player, PLAYER_SPEED, 0)
        x1, y1, x2, y2 = canvas.coords(player)
        if x2 > WIDTH:  # Prevent moving off the right edge
            canvas.move(player, WIDTH - x2, 0)

def move_bullets(canvas, bullets):
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -BULLET_SPEED)
        x1, y1 = canvas.coords(bullet)
        if y1 < 0:  # If missile goes off-screen, delete it
            canvas.delete(bullet)
            bullets.remove(bullet)

def move_missiles(canvas, missiles):
    for missile in missiles[:]:
        canvas.move(missile, 0, MISSILE_SPEED)
        x1, y1 = canvas.coords(missile)
        if y1 > HEIGHT:
            canvas.delete(missile)
            missiles.remove(missile)
