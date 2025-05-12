import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # Configurações da câmera
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        
        # Limites da câmera (para um nível maior)
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        self.camera_rect = pygame.Rect(self.camera_borders['left'], 
                                     self.camera_borders['top'], 
                                     SCREEN_WIDTH - self.camera_borders['left'] - self.camera_borders['right'],
                                     SCREEN_HEIGHT - self.camera_borders['top'] - self.camera_borders['bottom'])
    
    def center_target_camera(self, target):
        # Centraliza a câmera no alvo (jogador)
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height
    
    def box_target_camera(self, target):
        # Câmera de caixa que segue o jogador suavemente
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom
            
        # Calcula o offset da câmera
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']
    
    def custom_draw(self, player):
        # Atualiza a posição da câmera
        self.center_target_camera(player)  # Ou use box_target_camera para uma câmera mais suave
        
        # Desenha todos os sprites com o offset da câmera
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
