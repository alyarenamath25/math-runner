# ui/hud.py
import pygame
from settings import FONT_VCR, SCREEN_WIDTH, WHITE

class HUD:
    """HUD menggunakan font VCR OSD Mono."""
    # Setup font
    def __init__(self):
        self.font = pygame.font.Font(FONT_VCR, 36)

    # Render skor & waktu
    def draw(self, screen, score: int, timer_str: str):
        score_surf = self.font.render(f"SCORE: {score:05d}", True, WHITE)
        screen.blit(score_surf, (20, 20))
        
        timer_surf = self.font.render(timer_str, True, WHITE)
        
        align_x = SCREEN_WIDTH - timer_surf.get_width() - 170 
        screen.blit(timer_surf, (align_x, 20))