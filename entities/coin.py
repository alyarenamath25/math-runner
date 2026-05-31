# entities/coin.py
import pygame
from utils import resource_path

class Coin:
    # Setup gambar & hitbox
    def __init__(self, x: int, y: int):
        raw_image = pygame.image.load(resource_path("assets/images/objects/coin.png")).convert_alpha()
        self.image = pygame.transform.scale(raw_image, (64, 64))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.collected = False

    # Logika draw
    def draw(self, screen: pygame.Surface):
        if not self.collected:
            screen.blit(self.image, self.rect)