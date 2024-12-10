from constants import *
from PIL import ImageDraw, ImageTk


def check_collisions(canvas, bullets, missiles, aliens, player, game_state):
    # Check for bullet collisions with aliens
    for bullet in bullets[:]:
        bullet_coords = canvas.bbox(bullet)
        if not bullet_coords:
            continue

        for alien_info in aliens[:]:
            alien_coords = canvas.bbox(alien_info["alien"])

            if not alien_coords or len(alien_coords) < 4:
                continue

            if (bullet_coords[2] > alien_coords[0] and bullet_coords[0] < alien_coords[2] and
                    bullet_coords[3] > alien_coords[1] and bullet_coords[1] < alien_coords[3]):
                canvas.delete(bullet)
                bullets.remove(bullet)
                canvas.delete(alien_info["alien"])
                aliens.remove(alien_info)
                game_state['score'] += 10
                break

    # Check for missile collisions with player
    for missile in missiles[:]:
        missile_coords = canvas.bbox(missile)
        if not missile_coords:
            continue

        player_coords = canvas.bbox(player)
        if (missile_coords[2] > player_coords[0] and missile_coords[0] < player_coords[2] and
                missile_coords[3] > player_coords[1] and missile_coords[1] < player_coords[3]):
            canvas.delete(missile)
            missiles.remove(missile)
            game_state['player_lives'] -= 1
            if game_state['player_lives'] <= 0:
                game_state['game_over'] = True
            break


def check_block_collision(canvas, missiles, block_image_item, block_image_pil):
    block_coords = canvas.bbox(block_image_item)
    for missile in missiles[:]:
        missile_coords = canvas.bbox(missile)

        if (missile_coords[2] > block_coords[0] and missile_coords[0] < block_coords[2] and
                missile_coords[3] > block_coords[1] and missile_coords[1] < block_coords[3]):

            # Update the PIL image by removing the damaged part
            draw = ImageDraw.Draw(block_image_pil)
            for x in range(int(missile_coords[0] - block_coords[0]), int(missile_coords[2] - block_coords[0])):
                for y in range(int(missile_coords[1] - block_coords[1]), int(missile_coords[3] - block_coords[1])):
                    draw.point((x, y), fill="black")

            # Convert updated PIL image to Tkinter image
            updated_block_image = ImageTk.PhotoImage(block_image_pil)
            canvas.itemconfig(block_image_item, image=updated_block_image)

            canvas.delete(missile)
            missiles.remove(missile)
            break


def update_score(canvas, game_state):
    score_text = f"Score: {game_state['score']}   Lives: {game_state['player_lives']}"
    canvas.delete("score")
    canvas.create_text(WIDTH - 80, 10, text=score_text, fill=COLOR, font=("Arial", 14), tag="score")
