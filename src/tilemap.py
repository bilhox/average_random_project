import pygame
import json
import os
import pathlib

class Tilemap():

    def __init__(self):

        self.size = pygame.Vector2()
        self.n_size = pygame.Vector2()
        self.tile_size = pygame.Vector2()

        self.tileset = []

        self.tileset_path = ""
        self.tilemap_path = ""

        self.layers : dict[str, dict[tuple[int, int], int]] = {}
        self.object_layers : dict[str, list] = {}
    
    @staticmethod
    def load_tileset(path) -> list[pygame.Surface]:
        
        tile_list = []

        path_obj = pathlib.Path(path)

        with open(path_obj) as reader:
            json_obj = json.load(reader)

            tile_width, tile_height = json_obj["tilewidth"], json_obj["tileheight"]

            image = pygame.image.load(path_obj.parent.joinpath(json_obj["image"])).convert_alpha()

            for y in range(json_obj["imageheight"]//tile_height):
                for x in range(json_obj["columns"]):
                    
                    tile_list.append(image.subsurface(pygame.Rect([x*tile_width, y*tile_height], [tile_width, tile_height])))
        
        return tile_list

    def load(self, path : str) -> None:

        path_obj = pathlib.Path(path)

        with open(path_obj) as reader:

            json_obj = json.load(reader)

            self.n_size = pygame.Vector2(json_obj["width"], json_obj["height"])            
            self.tile_size = pygame.Vector2(json_obj["tilewidth"], json_obj["tileheight"])
            self.size = pygame.Vector2(self.n_size.x*self.tile_size.x, self.n_size.y*self.tile_size.y)

            self.tileset = []

            for tileset in json_obj['tilesets']:
                self.tileset.extend(self.load_tileset(path_obj.parent.joinpath(tileset["source"])))
            
            
            for layer in json_obj["layers"]:
                if layer["type"] == "tilelayer":
                    layer_data = layer["data"]
                    final_layer_data = {}
                    for y in range(layer["height"]):
                        for x in range(layer["width"]):
                            tile_value = layer_data[y*layer["width"] + x%layer["width"]]
                            if tile_value != 0:
                                final_layer_data[(x, y)] = tile_value
                    
                    self.layers[layer["name"]] = final_layer_data
                
                elif layer["type"] == "objectgroup":
                    objects = []
                    for obj in layer["objects"]:
                        rect = pygame.FRect(obj["x"], obj["y"], obj["width"], obj["height"])
                        objects.append(rect)
                    
                    self.object_layers[layer["name"]] = objects
                    

    def draw(self, dest : pygame.Surface, cam_pos : pygame.Vector2) -> None:

        for layer in self.layers.values():
            for coords, tile in layer.items():
                dest.blit(self.tileset[tile-1], pygame.Vector2(coords[0]*self.tile_size.x, coords[1]*self.tile_size.y) - pygame.Vector2(cam_pos))