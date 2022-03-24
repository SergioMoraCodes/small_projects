from csv import reader
from os import walk
import pygame

def import_csv_file(path):
    terrain_map=[]
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = [] #list of the images converted into surfaces
    for _,__,img_files in walk(path): #walk returns dirpath, dirnames, filenames
        for img in img_files: # for each file in the path
            full_path = path + "/" + img
            image_surf = pygame.image.load(full_path).convert_alpha() #load the image with pygame and convert it
            surface_list.append(image_surf)
    return surface_list #list full of the images in that folder