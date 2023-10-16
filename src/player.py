import pygame


class Player:

    def __init__(self):

        self.rect = pygame.FRect(0, 0, 16, 24)

        self.image = pygame.Surface(self.rect.size)
        self.image.fill([237, 225, 158])

        self.y_timer = 0
        self.jump_time_value = -0.6

        self.velocity = pygame.Vector2()
    
        self.speed = 150
        self.x_movement_stop_reduction = 0.3

        self.keys = {"left":False, "right":False}
        self.collision_side = {"left":False, "right":False, "top":False, "bottom":False}

        self.jumping = False

    def update(self, dt : float):

        self.velocity.y = 200*(self.y_timer+dt)**2 - 200*(self.y_timer)**2
        self.y_timer += dt

        if self.keys["left"]:
            self.velocity.x = -self.speed * dt
        elif self.keys["right"]:
            self.velocity.x = self.speed * dt
        else:
            self.velocity.x *= self.x_movement_stop_reduction
    
    def is_able_to_jump(self):
        return not self.jumping and (self.y_timer <= 0)


    def collided(self, colliders : list[pygame.FRect]) -> list[pygame.FRect]:

        collided = []

        for collider in colliders:
            if self.rect.colliderect(collider):
                collided.append(collider)

        return collided
    
    def collisions(self, colliders : list[pygame.FRect]):
        
        collision_side = {"left":False, "right":False, "top":False, "bottom":False}

        self.rect.x += self.velocity.x
        collided = self.collided(colliders)

        for collider in collided:
            if self.velocity.x < 0:
                self.rect.left = collider.right
                collision_side["left"] = True
            else:
                self.rect.right = collider.left
                collision_side["right"] = True
        
        self.rect.y += self.velocity.y
        collided = self.collided(colliders)

        for collider in collided:
            if self.velocity.y < 0:
                self.rect.top = collider.bottom
                collision_side["top"] = True
            else:
                self.rect.bottom = collider.top
                collision_side["bottom"] = True
        
        self.collision_side = collision_side
    
    def post_update(self):

        if self.collision_side["bottom"]:
            self.velocity.y = 0
            self.y_timer = 0
            self.jumping = False
        elif self.collision_side["top"]:
            self.velocity.y = 0
            self.y_timer = 0

    def draw(self, dest : pygame.Surface, cam_pos : pygame.Vector2):

        dest.blit(self.image, pygame.Vector2(self.rect.topleft) - pygame.Vector2(cam_pos))