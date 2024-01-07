import pygame


def cut_sprite(image, columns, rows, width, height):
    """Нарезать картинку на отдельные кадры"""
    frame_list = []
    for i in range(rows):
        for j in range(columns):
            frame_pos = (width * j + (5 * j), height * i + (10 * i))
            frame_list.append(image.subsurface(pygame.Rect(frame_pos[0], frame_pos[1], width, height)))
    return frame_list

# расстояние спрайтов на картинке - 5 пикселей, между рядами 10
