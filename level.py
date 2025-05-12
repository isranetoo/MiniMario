import pygame
from settings import *
from player import Player
from tile import Tile
from enemy import Enemy
from items import Coin, Mushroom
from camera import CameraGroup

class Level:
    def __init__(self):
        # Configurações da tela
        self.display_surface = pygame.display.get_surface()
        
        # Grupos de sprites com câmera
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()
        
        # Configuração do jogador
        self.player = None
        
        # Pontuação do jogo
        self.score = 0
        
        # Configuração do nível
        self.create_level()

    def create_level(self):
        # Formato do nível
        level_layout = [
            '                            ',
            '                            ',
            '                            ',
            '                            ',
            '                            ',
            '                            ',
            '                            ',
            '         ?   ?  B           ',
            '       C C C     C C        ',
            '     E         M            ',
            '               C  E         ',
            'GGGGGGGGGGGGGGGGGGGGGGGGGGGG',
            'GGGGGGGGGGGGGGGGGGGGGGGGGGGG'
        ]
        
        # Criar o nível a partir do layout
        for row_index, row in enumerate(level_layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if cell == 'G':  # Bloco de chão
                    Tile((x, y), TILE_SIZE, [self.visible_sprites, self.obstacle_sprites], 'ground')
                elif cell == 'B':  # Bloco de tijolo
                    Tile((x, y), TILE_SIZE, [self.visible_sprites, self.obstacle_sprites], 'brick')
                elif cell == '?':  # Bloco de interrogação
                    Tile((x, y), TILE_SIZE, [self.visible_sprites, self.obstacle_sprites], 'question')
                elif cell == 'E':  # Inimigo
                    Enemy((x, y), TILE_SIZE, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites)
                elif cell == 'C':  # Moeda
                    Coin((x, y), TILE_SIZE, [self.visible_sprites, self.coin_sprites])
                elif cell == 'M':  # Cogumelo
                    Mushroom((x, y), TILE_SIZE, [self.visible_sprites, self.powerup_sprites], self.obstacle_sprites)
                elif cell == 'P':  # Jogador
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
        
        # Se o jogador não foi definido no layout, coloque-o em uma posição padrão
        if not self.player:
            self.player = Player((TILE_SIZE * 5, TILE_SIZE * 10), [self.visible_sprites], self.obstacle_sprites)

    def check_enemy_collisions(self):
        # Verifica colisões do jogador com inimigos
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        for enemy in enemy_hits:
            if self.player.rect.bottom < enemy.rect.centery and self.player.direction.y > 0:
                # Jogador pulou em cima do inimigo
                enemy.kill()
                self.player.direction.y = self.player.jump_force / 2  # Mini pulo ao derrotar inimigo
                self.score += 100  # Pontos por derrotar inimigo
            else:
                # Jogador colidiu com o inimigo (aqui você pode implementar perda de vida)
                pass

    def check_coin_collisions(self):
        # Verifica colisões do jogador com moedas
        coin_hits = pygame.sprite.spritecollide(self.player, self.coin_sprites, True)
        for coin in coin_hits:
            # Adiciona pontos por coletar moeda
            self.score += 10
            # Aqui você poderia adicionar um som ou efeito visual

    def check_powerup_collisions(self):
        # Verifica colisões do jogador com power-ups
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerup_sprites, True)
        for powerup in powerup_hits:
            # Implementa o efeito do power-up (aqui só adicionamos pontos)
            self.score += 50
            # Em um jogo mais completo, você poderia adicionar crescimento, vidas extras, etc.

    def update(self):
        # Atualiza o jogador
        self.player.update()
        
        # Atualiza os inimigos
        self.enemy_sprites.update()
        
        # Atualiza as moedas (para animação)
        self.coin_sprites.update()
        
        # Atualiza os power-ups
        self.powerup_sprites.update()
        
        # Verifica colisões
        self.check_enemy_collisions()
        self.check_coin_collisions()
        self.check_powerup_collisions()

    def draw(self, screen):
        # Desenha todos os sprites usando a câmera
        self.visible_sprites.custom_draw(self.player)
        
        # Desenha a pontuação
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
