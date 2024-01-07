from csv import reader
from os import walk

import pygame


def import_csv_layout(file):
    """Загрузить слой карты (.csv)"""
    map = []
    with open(file, 'r') as layer:
        layout = reader(layer, delimiter=',')
        for row in layout:
            map.append(row)
        return map


def import_folder(file):
    textures_list = []
    for data in walk(file):
        _, __, images_list = data
        for image in images_list:
            image_file = file + '/' + image
            texture = pygame.image.load(image_file).convert_alpha()
            textures_list.append(texture)
    return textures_list



