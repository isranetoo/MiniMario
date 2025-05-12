import pygame
import os
import math  # Adicionado para funções matemáticas
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        
        # Configuração da imagem da moeda
        try:
            self.image = pygame.image.load('assets/images/coin.png').convert_alpha()
        except:
            # Fallback para círculo amarelo
            self.image = pygame.Surface((size // 2, size // 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 215, 0), (size // 4, size // 4), size // 4)
        
        # Configuração da posição
        self.rect = self.image.get_rect(center=(pos[0] + size // 2, pos[1] + size // 2))
        self.hitbox = self.rect.inflate(0, 0)
        
        # Animação
        self.float_y = pos[1]
        self.amplitude = 3
        self.speed = 0.1
        self.time = 0
    
    def update(self):
        # Animação simples de flutuação
        self.time += self.speed
        self.rect.y = self.float_y + self.amplitude * pygame.math.Vector2(0, 1).normalize().y * math.sin(self.time)

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, obstacle_sprites):
        super().__init__(groups)
        
        # Configuração da imagem do cogumelo
        try:
            self.image = pygame.image.load('assets/images/mushroom.png').convert_alpha()
        except:
            # Fallback para círculo vermelho
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (size // 2, size // 2), size // 2)
        
        # Configuração da posição
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        
        # Movimento
        self.direction = pygame.math.Vector2(1, 0)  # Começa movendo para a direita
        self.speed = 2
        self.gravity = GRAVITY
        
        # Grupos para colisão
        self.obstacle_sprites = obstacle_sprites
    
    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.hitbox.centerx = self.rect.centerx
        self.check_collisions()
        
        # Aplica gravidade
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.hitbox.centery = self.rect.centery
        self.check_vertical_collisions()
    
    def check_collisions(self):
        # Verifica colisões horizontais
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                # Inverte a direção se colidir com obstáculo
                if self.direction.x > 0:  # Movendo para a direita
                    self.hitbox.right = sprite.hitbox.left
                    self.rect.right = self.hitbox.right
                elif self.direction.x < 0:  # Movendo para a esquerda
                    self.hitbox.left = sprite.hitbox.right
                    self.rect.left = self.hitbox.left
                self.direction.x *= -1
                break
    
    def check_vertical_collisions(self):
        # Verifica colisões verticais
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:  # Caindo
                    self.hitbox.bottom = sprite.hitbox.top
                    self.rect.bottom = self.hitbox.bottom
                    self.direction.y = 0
    
    def update(self):
        self.move()
