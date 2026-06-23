import pygame
from settings import FONT_VCR, SCREEN_WIDTH, WHITE

class HUD:
    """HUD menggunakan font VCR OSD Mono dengan efek kedip merah saat salah."""
    def __init__(self):
        self.font = pygame.font.Font(FONT_VCR, 36)
        
        # Efek kedip merah
        self.flash_timer = 0.0
        self.flash_duration = 0.5 # Durasi kedip merah (0.5 detik)

    def trigger_flash(self):
        """Memicu efek kedip merah saat jawaban salah."""
        self.flash_timer = self.flash_duration

    def update(self, dt: float):
        """Mengurangi durasi timer kedip setiap frame."""
        if self.flash_timer > 0:
            self.flash_timer -= dt

    def draw(self, screen, score: int, timer_str: str):
        # Warna Skor (Bergantian Merah dan Putih saat flash_timer aktif)
        if self.flash_timer > 0:
            if int(self.flash_timer * 10) % 2 == 0:
                score_color = (255, 0, 0)      # Merah murni saat kedip
            else:
                score_color = (255, 120, 120)  # Merah muda cerah agar terlihat berkedip
        else:
            score_color = WHITE                # Kembali ke warna normal (Putih)

        # Skor
        score_surf = self.font.render(f"SCORE: {score:05d}", True, score_color)
        screen.blit(score_surf, (20, 20))
        
        # Timer (tetap putih seperti asli)
        timer_surf = self.font.render(timer_str, True, WHITE)
        align_x = SCREEN_WIDTH - timer_surf.get_width() - 170 
        screen.blit(timer_surf, (align_x, 20))
