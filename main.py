import pygame
import sys
from settings import *
from player import Player
from level import Level

class Game:
    def __init__(self):
        # Inicializa o pygame e seus subsistemas
        pygame.init()
        pygame.font.init()  # Inicializa o sistema de fontes
        
        # Configurações da janela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mini Mario")
        self.clock = pygame.time.Clock()
        
        # Carrega o nível
        self.level = Level()

        # Carregar backgrounds
        self.bg0 = pygame.image.load('assets/images/background_0.png').convert()
        self.bg1 = pygame.image.load('assets/images/background_1.png').convert_alpha()
        self.bg2 = pygame.image.load('assets/images/background_2.png').convert_alpha()
        
    def draw_background(self):
        # Offset da câmera baseado no jogador
        offset_x = int(self.level.player.rect.centerx - SCREEN_WIDTH // 2)
        # Paralaxe: camadas mais distantes movem menos
        bg0_scaled = pygame.transform.scale(self.bg0, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg1_scaled = pygame.transform.scale(self.bg1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg2_scaled = pygame.transform.scale(self.bg2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg0_scaled, (0, 0))
        self.screen.blit(bg1_scaled, (0, 0))
        self.screen.blit(bg2_scaled, (0, 0))
        
    def run(self):
        # Loop principal do jogo
        while True:
            # Verifica eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Atualiza o jogo
            self.level.update()

            # Preenche a tela com a cor de fundo antes de desenhar o background
            self.screen.fill(BACKGROUND_COLOR)
            # Renderiza o background
            self.draw_background()
            # Renderiza o jogo
            self.level.draw(self.screen)
            # Atualiza a tela
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
