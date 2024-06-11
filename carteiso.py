import pygame
import sys

# Dimensions des tuiles et de la carte
TILE_WIDTH = 64
TILE_HEIGHT = 32
MAP_WIDTH = 10
MAP_HEIGHT = 10

# Couleurs
BACKGROUND_COLOR = (0, 0, 0)
TILE_COLOR = (100, 100, 255)
HIGHLIGHT_COLOR = (255, 0, 0)

# Initialisation de la carte
def init_map():
    return [[0 for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]

# Dessine une tuile isométrique
def draw_isometric_tile(screen, x, y, tile_width, tile_height, offset_x, offset_y):
    screen_x = (x - y) * (tile_width // 2) + offset_x
    screen_y = (x + y) * (tile_height // 2) + offset_y
    points = [
        (screen_x, screen_y),
        (screen_x + tile_width // 2, screen_y + tile_height // 2),
        (screen_x, screen_y + tile_height),
        (screen_x - tile_width // 2, screen_y + tile_height // 2)
    ]
    pygame.draw.polygon(screen, TILE_COLOR, points)

# Met en évidence une tuile
def highlight_tile(screen, x, y, tile_width, tile_height, offset_x, offset_y):
    screen_x = (x - y) * (tile_width // 2) + offset_x
    screen_y = (x + y) * (tile_height // 2) + offset_y
    points = [
        (screen_x, screen_y),
        (screen_x + tile_width // 2, screen_y + tile_height // 2),
        (screen_x, screen_y + tile_height),
        (screen_x - tile_width // 2, screen_y + tile_height // 2)
    ]
    pygame.draw.polygon(screen, HIGHLIGHT_COLOR, points, 2)

# Calcule les coordonnées de la tuile à partir des coordonnées de l'écran
def get_tile_coordinates(screen_x, screen_y, offset_x, offset_y):
    screen_x -= offset_x
    screen_y -= offset_y
    tile_x = (screen_x // (TILE_WIDTH // 2) + screen_y // (TILE_HEIGHT // 2)) // 2
    tile_y = (screen_y // (TILE_HEIGHT // 2) - (screen_x // (TILE_WIDTH // 2))) // 2
    return tile_x, tile_y

# Fonction principale
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Carte Isométrique')
    
    map = init_map()
    
    offset_x = 400
    offset_y = 100
    selected_tile_x = -1
    selected_tile_y = -1

    dragging = False
    prev_mouse_x, prev_mouse_y = 0, 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    tile_x, tile_y = get_tile_coordinates(mouse_x, mouse_y, offset_x, offset_y)
                    if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                        selected_tile_x, selected_tile_y = tile_x, tile_y
                    dragging = True
                    prev_mouse_x, prev_mouse_y = mouse_x, mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - prev_mouse_x
                    dy = mouse_y - prev_mouse_y
                    offset_x += dx
                    offset_y += dy
                    prev_mouse_x, prev_mouse_y = mouse_x, mouse_y
        
        screen.fill(BACKGROUND_COLOR)
        
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                draw_isometric_tile(screen, x, y, TILE_WIDTH, TILE_HEIGHT, offset_x, offset_y)
        
        if 0 <= selected_tile_x < MAP_WIDTH and 0 <= selected_tile_y < MAP_HEIGHT:
            highlight_tile(screen, selected_tile_x, selected_tile_y, TILE_WIDTH, TILE_HEIGHT, offset_x, offset_y)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
