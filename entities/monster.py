import pygame
from utils import resource_path

class Monster:
    def __init__(self, x: int, y: int):
        raw_image = pygame.image.load(resource_path("assets/images/objects/monster.png")).convert_alpha()
        self.image = pygame.transform.smoothscale(raw_image, (70, 70))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        
        self.defeated = False
        self.passed = False  # Monster sudah berhasil dilompati

    def draw(self, screen: pygame.Surface):
        if not self.defeated:
            screen.blit(self.image, self.rect)
