import pygame
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        
        # Animação Idle e Run
        self.idle_frames = []
        self.run_frames = []
        try:
            idle_sheet = pygame.image.load('assets/images/IDLE.png').convert_alpha()
            frame_width = idle_sheet.get_width() // 10
            frame_height = idle_sheet.get_height()
            for i in range(10):
                frame = idle_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                self.idle_frames.append(frame)
            run_sheet = pygame.image.load('assets/images/RUN.png').convert_alpha()
            run_frame_width = run_sheet.get_width() // 16
            run_frame_height = run_sheet.get_height()
            for i in range(16):
                frame = run_sheet.subsurface(pygame.Rect(i * run_frame_width, 0, run_frame_width, run_frame_height))
                self.run_frames.append(frame)
            self.image = self.idle_frames[0]
        except:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
            self.image.fill(RED)
            self.idle_frames = [self.image]
            self.run_frames = [self.image]
        
        # Configuração da posição
        self.rect = self.image.get_rect(topleft=pos)
        # Ajusta a hitbox para ser menor e mais próxima dos pés do personagem
        self.hitbox = self.rect.inflate(-8, -16)
        self.hitbox.bottom = self.rect.bottom
        
        # Movimento
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.jump_force = PLAYER_JUMP_FORCE
        self.jump_count = 0
        self.max_jumps = 1  # Pulo duplo mais tarde
        
        # Status
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.state = 'idle'
        
        # Grupos de sprites para colisão
        self.obstacle_sprites = obstacle_sprites
        
        # Animação
        self.animation_index = 0
        self.animation_speed = 0.15
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        # Pulo
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.jump()
    
    def jump(self):
        self.direction.y = self.jump_force
        self.jump_count += 1
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def horizontal_movement(self):
        self.rect.x += self.direction.x * self.speed
        self.hitbox.centerx = self.rect.centerx
        self.check_horizontal_collisions()
        # Sincroniza rect e hitbox após colisão
        self.rect.centerx = self.hitbox.centerx
    
    def vertical_movement(self):
        self.apply_gravity()
        self.hitbox.centery = self.rect.centery
        self.check_vertical_collisions()
        # Sincroniza rect e hitbox após colisão
        self.rect.centery = self.hitbox.centery
    
    def check_horizontal_collisions(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0:  # Movendo para a direita
                    self.hitbox.right = sprite.hitbox.left
                    self.rect.right = self.hitbox.right
                    self.on_right = True
                elif self.direction.x < 0:  # Movendo para a esquerda
                    self.hitbox.left = sprite.hitbox.right
                    self.rect.left = self.hitbox.left
                    self.on_left = True
        
        if self.on_right and (self.direction.x <= 0 or not self.check_for_collision_right()):
            self.on_right = False
        
        if self.on_left and (self.direction.x >= 0 or not self.check_for_collision_left()):
            self.on_left = False
    
    def check_vertical_collisions(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:  # Movendo para baixo
                    self.hitbox.bottom = sprite.hitbox.top
                    self.rect.bottom = self.hitbox.bottom
                    self.direction.y = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.direction.y < 0:  # Movendo para cima
                    self.hitbox.top = sprite.hitbox.bottom
                    self.rect.top = self.hitbox.top
                    self.direction.y = 0
                    self.on_ceiling = True
        
        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False
    
    def check_for_collision_right(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(pygame.Rect(self.hitbox.right, self.hitbox.top, 1, self.hitbox.height)):
                return True
        return False
    
    def check_for_collision_left(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(pygame.Rect(self.hitbox.left - 1, self.hitbox.top, 1, self.hitbox.height)):
                return True
        return False
    
    def animate(self):
        # Decide qual animação usar
        if self.direction.x != 0:
            frames = self.run_frames
        else:
            frames = self.idle_frames
        self.animation_index += self.animation_speed
        if self.animation_index >= len(frames):
            self.animation_index = 0
        frame = frames[int(self.animation_index)]
        if not self.facing_right:
            self.image = pygame.transform.flip(frame, True, False)
        else:
            self.image = frame
    
    def update(self):
        self.input()
        self.horizontal_movement()
        self.vertical_movement()
        self.animate()
