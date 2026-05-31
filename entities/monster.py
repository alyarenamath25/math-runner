# entities/monster.py
import pygame
from utils import resource_path

class Monster:
    # Setup gambar & hitbox
    def __init__(self, x: int, y: int):
        raw_image = pygame.image.load(resource_path("assets/images/objects/monster.png")).convert_alpha()
        self.image = pygame.transform.scale(raw_image, (96, 96))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.defeated = False

    # Logika draw
    def draw(self, screen: pygame.Surface):
        if not self.defeated:
            screen.blit(self.image, self.rect)