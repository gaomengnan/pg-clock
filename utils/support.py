from PIL import Image
import pygame as pg

player_scaled = 1.5


def load_animation(path):
    frames = []
    gif_image = Image.open(path)
    try:
        while True:
            frame = gif_image.convert("RGBA")
            pg_frame = pg.image.fromstring(
                frame.tobytes(), frame.size, "RGBA"
            ).convert_alpha()
            pg_frame = pg.transform.scale(
                pg_frame,
                (
                    pg_frame.get_width() * player_scaled,
                    pg_frame.get_height() * player_scaled,
                ),
            )
            frames.append(pg_frame)
            gif_image.seek(gif_image.tell() + 1)
    except EOFError:
        pass
    return frames


def get_enemies(path, x, y):
    frames = []
    spritesheet = pg.image.load(path)
    for i in range(12):
        frame = spritesheet.subsurface(pg.Rect(i * x, 0, x, y))
        frames.append(frame)
    return frames
