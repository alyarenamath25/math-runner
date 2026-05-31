# entities/player.py
import pygame
from utils import resource_path

class Player:
    # Setup karakter
    def __init__(self, image_path: str, frame_count: int, frame_w: int, frame_h: int, bottomleft: tuple):
        self.frame_count = frame_count
        self.bottomleft_pos = bottomleft 
        
        sheet = pygame.image.load(resource_path(image_path)).convert_alpha()
        self.run_frames = []

        for i in range(frame_count):
            rect_potong = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            self.run_frames.append(sheet.subsurface(rect_potong))
            
        self.frame_idx = 0.0
        self.animation_speed = 0.25
        self.image = self.run_frames[0]
        self.rect = self.image.get_rect(bottomleft=self.bottomleft_pos)
        self.blocked = False

    # Animasi loop
    def update(self):
        if not self.blocked:
            self.frame_idx += self.animation_speed
            if self.frame_idx >= self.frame_count:
                self.frame_idx = 0.0
        else:
            self.frame_idx = 0.0
            
        self.image = self.run_frames[int(self.frame_idx)]
        self.rect = self.image.get_rect(bottomleft=self.bottomleft_pos)

    # Render frame
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)