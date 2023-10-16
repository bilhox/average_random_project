import pygame

from player import Player
from tilemap import Tilemap

SCREEN_SIZE = pygame.Vector2(960, 540)


def main():
    screen = pygame.display.set_mode(SCREEN_SIZE, vsync=1)
    display = pygame.Surface(SCREEN_SIZE/2)
    clock = pygame.Clock()

    game_map = Tilemap()
    game_map.load("./assets/maps/map_0.tmj")

    player = Player()
    player.rect.topleft = pygame.Vector2(64, 64)

    camera = pygame.FRect([0,0], SCREEN_SIZE/2)

    running = True
        
    while running:
        
        dt = clock.tick() / 1000

        player.update(dt)
        player.collisions(game_map.object_layers["colliders"])
        player.post_update()

        camera.x += (player.rect.centerx - camera.centerx)*0.1
        camera.y += (player.rect.centery - camera.centery)*0.1

        camera.x = pygame.math.clamp(camera.x, 0, game_map.size.x - camera.width)
        camera.y = pygame.math.clamp(camera.y, 0, game_map.size.y - camera.height)

        display.fill(0x000000)

        player.draw(display, camera.topleft)

        game_map.draw(display, camera.topleft)
        
        screen.blit(pygame.transform.scale_by(display, 2), [0,0])
        pygame.display.set_caption(f"{round(clock.get_fps(), 2)}")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.keys["right"] = True
                elif event.key == pygame.K_LEFT:
                    player.keys["left"] = True
                elif event.key == pygame.K_UP and player.is_able_to_jump():
                    player.jumping = True
                    player.y_timer = player.jump_time_value
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.keys["right"] = False
                elif event.key == pygame.K_LEFT:
                    player.keys["left"] = False

    pygame.quit()

if __name__ == "__main__":
    main()
                

# back in a short time