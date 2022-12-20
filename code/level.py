import pygame
from numpy.random import randint
from settings import *
from tile import Tile
from support import import_csv_layout, import_folder
from player import Player


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {

            "boundary": import_csv_layout("map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("map/map_Grass.csv"),
            "object": import_csv_layout("map/map_Objects.csv")

        }

        graphics = {
            'grass' : import_folder("graphics/grass"),
            'object': import_folder("graphics/objects")
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x, y = col_index * TILESIZE, row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), (self.obstacle_sprites), 'invisible')
                        if style == 'grass':
                            Tile((x,y), (self.visible_sprites, self.obstacle_sprites), 'grass', graphics['grass'][randint(3)] )
                        if style == 'object':
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'object',graphics['object'][int(col)])
                    else:
                        pass

        self.player = Player((2000, 1430), (self.visible_sprites), self.obstacle_sprites)
    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))


    def custom_draw(self, player):

        # getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor with offset w/ to player
        offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, offset_pos)

        # drawing all sprites w/ to player
        # usually the order of draw is based on when the sprite is created (in the level map above)
        # we need to sort by Y-Position
        # for this use sorted(sprites, key= lambda sprite: sprite.rect.centery) -> Y position of each sprite)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):

            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
