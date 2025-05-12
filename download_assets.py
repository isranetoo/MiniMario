import os
import requests
import io
import zipfile
from PIL import Image
import pygame

def download_assets():
    print("Baixando recursos para o Mini Mario...")
    
    # Cria diretórios se não existirem
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    
    # URLs para download de sprites e sons (placeholders)
    # Nota: Em um projeto real, deveria usar sprites e sons autorizados ou criar os próprios
    resources = {
        "player": "https://opengameart.org/sites/default/files/styles/medium/public/character_1.gif",
        "tiles": "https://opengameart.org/sites/default/files/styles/medium/public/tileset_1.png",
        "enemies": "https://opengameart.org/sites/default/files/styles/medium/public/enemies_1.png",
        "jump_sound": "https://opengameart.org/sites/default/files/jump_1.wav",
        "coin_sound": "https://opengameart.org/sites/default/files/coin_1.wav"
    }
    
    print("Como não temos acesso à internet para baixar recursos reais, vamos criar alguns sprites simples.")
    
    # Criar sprites simples
    # Jogador (retângulo vermelho)
    player_img = Image.new('RGBA', (32, 64), (255, 0, 0, 255))
    player_img.save('assets/images/player.png')
    
    # Chão (retângulo marrom)
    ground_img = Image.new('RGBA', (32, 32), (139, 69, 19, 255))
    ground_img.save('assets/images/ground.png')
    
    # Tijolo (retângulo marrom claro)
    brick_img = Image.new('RGBA', (32, 32), (207, 102, 0, 255))
    brick_img.save('assets/images/brick.png')
      # Bloco de interrogação (retângulo dourado)
    question_img = Image.new('RGBA', (32, 32), (255, 215, 0, 255))
    question_img.save('assets/images/question.png')
    
    # Inimigo (retângulo verde)
    enemy_img = Image.new('RGBA', (32, 32), (34, 139, 34, 255))
    enemy_img.save('assets/images/enemy.png')
    
    # Moeda (círculo amarelo)
    coin_img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    coin_draw = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for x in range(16):
        for y in range(16):
            # Desenha um círculo amarelo
            if (x-8)**2 + (y-8)**2 < 6**2:  # Raio 6
                coin_draw.putpixel((x, y), (255, 215, 0, 255))
    coin_img.paste(coin_draw, (0, 0), coin_draw)
    coin_img.save('assets/images/coin.png')
    
    # Cogumelo (círculo vermelho)
    mushroom_img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    mushroom_draw = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    for x in range(32):
        for y in range(32):
            # Desenha o topo vermelho
            if (x-16)**2 + (y-12)**2 < 12**2 and y < 16:  # Meio círculo superior
                mushroom_draw.putpixel((x, y), (255, 0, 0, 255))
            # Desenha o caule branco
            elif 12 <= x <= 20 and 16 <= y <= 28:
                mushroom_draw.putpixel((x, y), (255, 255, 255, 255))
    mushroom_img.paste(mushroom_draw, (0, 0), mushroom_draw)
    mushroom_img.save('assets/images/mushroom.png')
    question_img.save('assets/images/question.png')
    
    # Inimigo (retângulo verde)
    enemy_img = Image.new('RGBA', (32, 32), (34, 139, 34, 255))
    enemy_img.save('assets/images/enemy.png')
    
    print("Sprites básicos criados com sucesso!")
    print("Para um jogo completo, você deveria usar sprites e sons reais.")

if __name__ == "__main__":
    download_assets()
