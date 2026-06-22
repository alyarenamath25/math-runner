import pygame
from utils import resource_path

class Player:
    # Karakter
    def __init__(self, image_path: str, frame_count: int, frame_w: int, frame_h: int, bottomleft: tuple):
        self.frame_count = frame_count
        
        sheet = pygame.image.load(resource_path(image_path)).convert_alpha()
        self.run_frames = []

        for i in range(frame_count):
            rect_potong = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            self.run_frames.append(sheet.subsurface(rect_potong))
            
        self.frame_idx = 0.0
        self.animation_speed = 10.0 
        self.image = self.run_frames[0]
        
        # Posisi aktual yang bisa bergerak fleksibel
        self.rect = self.image.get_rect(bottomleft=bottomleft)
        
        # Batas bawah tanah berdasarkan posisi awal saat spawn
        self.ground_y = self.rect.bottom 
        
        # Pergerakan
        self.speed = 250         # Kecepatan maju/mundur (pixel per detik)
        self.gravity = 1200      # Kekuatan gravitasi
        self.jump_speed = -550   # Kecepatan awal lompat (minus artinya ke atas)
        self.velocity_y = 0      # Kecepatan vertikal saat ini
        self.is_grounded = True  # Penanda apakah kaki menempel di tanah
        
        self.blocked = False
        self.facing_right = True

    # Animasi & Pergerakan
    def update(self, dt: float):
        # Maju/Mundur
        if not self.blocked:
            keys = pygame.key.get_pressed()
            
            # Maju (Kanan)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.speed * dt
                self.facing_right = True
                self._animate(dt)
            # Mundur (Kiri)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= self.speed * dt
                self.facing_right = False
                self._animate(dt)
            else:
                # Jika diam, balikkan ke frame awal
                self.frame_idx = 0.0
        else:
            self.frame_idx = 0.0

        # Lompat & Gravitasi
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded and not self.blocked:
            self.velocity_y = self.jump_speed
            self.is_grounded = False

        self.velocity_y += self.gravity * dt
        self.rect.y += self.velocity_y * dt

        # Batas Tanah agar tidak amblas
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.is_grounded = True

        current_frame = self.run_frames[int(self.frame_idx)]
        
        # Balik gambar horizontal jika player bergerak ke kiri
        if self.facing_right:
            self.image = current_frame
        else:
            self.image = pygame.transform.flip(current_frame, True, False)

    def _animate(self, dt: float):
        """Fungsi pembantu untuk menjalankan loop animasi run."""
        self.frame_idx += self.animation_speed * dt
        if self.frame_idx >= self.frame_count:
            self.frame_idx = 0.0

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
