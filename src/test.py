import pygame
import pygamevideo

a = pygame.FRect(50,20,100,100)


# video = pygamevideo.Video("./assets/WHAT_hd.mp4")
# print(video.get_size())
# screen = pygame.display.set_mode(video.get_size())

# video.play(True)

# clock = pygame.Clock()

# while True:

#     dt = clock.tick(video.fps) / 1000
#     video.draw_to(screen, [0,0])

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_p:
#                 pygame.display.toggle_fullscreen()
#             elif event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 exit()
    
    
#     pygame.display.set_caption(f"{round(clock.get_fps())}")
#     pygame.display.flip()