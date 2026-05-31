import random
import pygame
from settings import SPAWN_MIN_DIST, SPAWN_MAX_DIST, SPAWN_POOL, SCREEN_WIDTH, GROUND_Y_OBJECT

class Spawner:
    # Jarak spawn
    def __init__(self):
        self.objects = []
        self.next_spawn_dist = random.randint(SPAWN_MIN_DIST, SPAWN_MAX_DIST)
        self.distance_since_last = 0

    # Gerakan spawn
    def update(self, speed: int):
        # Geser seluruh objek ke arah kiri
        for obj in self.objects:
            obj.rect.x -= speed

        # Akumulasi jarak tempuh pergeseran
        self.distance_since_last += speed
        
        # Penciptaan objek baru jika jarak sudah terpenuhi
        if self.distance_since_last >= self.next_spawn_dist:
            self._spawn_object()
            self.distance_since_last = 0
            self.next_spawn_dist = random.randint(SPAWN_MIN_DIST, SPAWN_MAX_DIST)

    # Factory objek
    def _spawn_object(self):
        from entities.coin import Coin
        from entities.monster import Monster
        
        obj_type = random.choice(SPAWN_POOL)
        spawn_x = SCREEN_WIDTH + 50
        spawn_y = GROUND_Y_OBJECT
        
        if obj_type == "coin":
            self.objects.append(Coin(spawn_x, spawn_y))
        else:
            self.objects.append(Monster(spawn_x, spawn_y))

    # Pembersihan memori
    def cleanup(self):
        """Buang objek yang sudah melewati batas kiri layar (X < 0) dari memori."""
        self.objects = [obj for obj in self.objects if obj.rect.right > 0]

    def draw(self, screen: pygame.Surface):
        for obj in self.objects:
            obj.draw(screen)