import pygame
import os
from settings import *

class Tile(pygame.sprite.Sprite):
    # Mapeamento de tipos para coordenadas do tileset (coluna, linha)
    TILE_SIZE = 16  # Cada tile tem 16x16 pixels

    TILESET_MAP = {
        'ground': (0, 9),        # chão escuro com grama
        'plataforma': (2, 6),    # galho/plataforma
        'folha': (3, 2),         # folhas penduradas
        'pedra': (1, 2),         # pedra roxa
        'arbusto': (0, 8),       # moita/matinho
        # Tiles maiores serão tratados separadamente
    }

    def __init__(self, pos, size, groups, sprite_type='ground', tileset_coords=None, collidable=True):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.collidable = collidable

        # Caminho do tileset
        tileset_path = os.path.join('assets', 'images', 'tileset.png')
        tileset = pygame.image.load(tileset_path).convert_alpha()

        if sprite_type == 'arvore_grande':
            # Árvore grande (personalizada)
            self.image = pygame.Surface((112, 144), pygame.SRCALPHA)
            self.image.blit(tileset, (0, 0), pygame.Rect(144, 0, 112, 144))  # ajustar se necessário
        elif sprite_type == 'arvore_pequena':
            # Árvore pequena (à esquerda do tileset)
            self.image = pygame.Surface((64, 80), pygame.SRCALPHA)
            self.image.blit(tileset, (0, 0), pygame.Rect(0, 0, 64, 80))
        else:
            # Tile normal de 16x16
            if tileset_coords is None and sprite_type in self.TILESET_MAP:
                tileset_coords = self.TILESET_MAP[sprite_type]

            if tileset_coords is not None:
                tile_x, tile_y = tileset_coords
                tile_rect = pygame.Rect(tile_x * self.TILE_SIZE, tile_y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                self.image = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE), pygame.SRCALPHA)
                self.image.blit(tileset, (0, 0), tile_rect)

                # Redimensiona se necessário
                if size != self.TILE_SIZE:
                    self.image = pygame.transform.scale(self.image, (size, size))
            else:
                # Fallback visual
                self.image = pygame.Surface((size, size))
                self.image.fill((255, 0, 255))  # rosa para indicar erro visual

        # Configuração da posição
        self.rect = self.image.get_rect(topleft=pos)
        # O matinho (arbusto) não tem colisão
        if self.sprite_type == 'arbusto':
            self.hitbox = pygame.Rect(0, 0, 0, 0)
        elif self.collidable:
            self.hitbox = self.rect.inflate(0, 0)
        else:
            self.hitbox = pygame.Rect(0, 0, 0, 0)  # Sem colisão

def criar_chao_com_arbusto(pos, size, groups):
    """Cria um tile de chão e um tile de arbusto (matinho) em cima do chão."""
    Tile(pos, size, groups, sprite_type='ground')
    # Arbusto em cima do chão
    x, y = pos
    Tile((x, y - size), size, groups, sprite_type='arbusto', collidable=False)
