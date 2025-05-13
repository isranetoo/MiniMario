from PIL import Image, ImageDraw

# Caminho para o seu tileset
tileset_path = 'assets/images/tileset.png'
# Caminho para salvar a imagem com a grade
output_path = 'assets/images/tileset_com_grade.png'

# Tamanho do tile
tile_size = 16

# Abrir a imagem do tileset
image = Image.open(tileset_path)
draw = ImageDraw.Draw(image)

# Obter as dimensões da imagem
width, height = image.size

# Desenhar linhas verticais
for x in range(0, width, tile_size):
    draw.line([(x, 0), (x, height)], fill=(255, 0, 0, 255))

# Desenhar linhas horizontais
for y in range(0, height, tile_size):
    draw.line([(0, y), (width, y)], fill=(255, 0, 0, 255))

# Salvar a imagem com a grade
image.save(output_path)
