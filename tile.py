import pygame
import os
from settings import *

class Tile(pygame.sprite.Sprite):
    # Mapeamento de tipos para coordenadas do tileset (coluna, linha)
    TILESET_MAP = {
        'ground': (0, 7),        # Exemplo: ajuste conforme seu tileset
        'plataforma': (2, 6),   # Exemplo: ajuste conforme seu tileset
        'folha': (4, 2),        # Exemplo: ajuste conforme seu tileset
        'arvore': (0, 0),       # Exemplo: ajuste conforme seu tileset
        # Adicione mais tipos conforme necessário
    }

    def __init__(self, pos, size, groups, sprite_type='ground', tileset_coords=None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        
        # Se não passar tileset_coords, tenta pegar do mapeamento
        if tileset_coords is None and sprite_type in self.TILESET_MAP:
            tileset_coords = self.TILESET_MAP[sprite_type]

        # Novo: carregar tileset e recortar tile específico
        if tileset_coords is not None:
            tileset = pygame.image.load('assets/images/tileset.png').convert_alpha()
            tile_x, tile_y = tileset_coords
            tileset_width, tileset_height = tileset.get_size()
            # Verificação de limites para evitar erro de subsurface
            if (tile_x + 1) * size > tileset_width or (tile_y + 1) * size > tileset_height:
                print(f"[Tile] ERRO: Tile ({tile_x}, {tile_y}) de tamanho {size} está fora do tileset ({tileset_width}x{tileset_height})!")
                self.image = pygame.Surface((size, size))
                self.image.fill((255, 0, 0))  # Tile vermelho para indicar erro
            else:
                tile_rect = pygame.Rect(tile_x * size, tile_y * size, size, size)
                self.image = tileset.subsurface(tile_rect)
        else:
            # Configuração da imagem do bloco
            try:
                if sprite_type == 'ground':
                    self.image = pygame.image.load('assets/images/ground.png').convert_alpha()
                elif sprite_type == 'brick':
                    self.image = pygame.image.load('assets/images/brick.png').convert_alpha()
                elif sprite_type == 'question':
                    self.image = pygame.image.load('assets/images/question.png').convert_alpha()
            except:
                # Fallback para superfícies coloridas se as imagens não puderem ser carregadas
                self.image = pygame.Surface((size, size))
                if sprite_type == 'ground':
                    self.image.fill(BROWN)
                elif sprite_type == 'brick':
                    self.image.fill((207, 102, 0))  # Marrom mais claro
                elif sprite_type == 'question':
                    self.image.fill((255, 215, 0))  # Dourado
        
        # Configuração da posição
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)  # Mesma hitbox que o rect
