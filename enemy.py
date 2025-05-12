import pygame
import os
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, obstacle_sprites, speed=2):
        super().__init__(groups)
        
        # Configuração da imagem do inimigo
        try:
            self.image = pygame.image.load('assets/images/enemy.png').convert_alpha()
        except:
            # Fallback para superfície colorida se a imagem não puder ser carregada
            self.image = pygame.Surface((size, size))
            self.image.fill((34, 139, 34))  # Verde
        
        # Configuração da posição
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # Hitbox um pouco menor na altura
        
        # Movimento
        self.direction = pygame.math.Vector2(-1, 0)  # Começa movendo para a esquerda
        self.speed = speed
        self.gravity = GRAVITY
        
        # Grupos para colisão
        self.obstacle_sprites = obstacle_sprites
    
    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.hitbox.centerx = self.rect.centerx
        self.check_collisions()
        # Sincroniza rect e hitbox após colisão horizontal
        self.rect.centerx = self.hitbox.centerx

        # Aplica gravidade
        self.rect.y += self.direction.y
        self.hitbox.centery = self.rect.centery
        self.apply_gravity()
        # Sincroniza rect e hitbox após colisão vertical
        self.rect.centery = self.hitbox.centery
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
        # Verifica colisões verticais
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:  # Caindo
                    self.hitbox.bottom = sprite.hitbox.top
                    self.rect.bottom = self.hitbox.bottom
                    self.direction.y = 0
    
    def check_collisions(self):
        # Verifica colisões horizontais
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                # Inverte a direção se colidir com obstáculo
                self.direction.x *= -1
                break
    
    def update(self):
        self.move()
