# entities/player.py
import pygame
from utils import resource_path

class Player:
    # Setup karakter
    def __init__(self, image_path: str, frame_count: int, frame_w: int, frame_h: int, bottomleft: tuple):
        self.frame_count = frame_count
        
        sheet = pygame.image.load(resource_path(image_path)).convert_alpha()
        self.run_frames = []

        for i in range(frame_count):
            rect_potong = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            self.run_frames.append(sheet.subsurface(rect_potong))
            
        self.frame_idx = 0.0
        self.animation_speed = 10.0 # Diubah ke frame per detik agar pas dengan dt
        self.image = self.run_frames[0]
        
        # Menggunakan self.rect sebagai posisi aktual yang bisa bergerak fleksibel
        self.rect = self.image.get_rect(bottomleft=bottomleft)
        
        # Batas bawah tanah (ground) berdasarkan posisi awal saat spawn
        self.ground_y = self.rect.bottom 
        
        # Variabel Pergerakan & Fisika
        self.speed = 250         # Kecepatan maju/mundur (pixel per detik)
        self.gravity = 1200      # Kekuatan gravitasi menarik ke bawah
        self.jump_speed = -550   # Kecepatan awal loncat (minus artinya ke atas)
        self.velocity_y = 0      # Kecepatan vertikal saat ini
        self.is_grounded = True  # Penanda apakah kaki menempel di tanah
        
        self.blocked = False
        self.facing_right = True # Untuk membalik sprite saat mundur

    # Animasi & Pergerakan Fisika
    def update(self, dt: float):
        # 1. LOGIKA INPUT (MAJU / MUNDUR / LOMPAT)
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
                # Jika diam, balikkan ke frame awal (idle)
                self.frame_idx = 0.0
        else:
            self.frame_idx = 0.0

        # 2. LOGIKA FISIKA LOMPAT & GRAVITASI
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded and not self.blocked:
            self.velocity_y = self.jump_speed
            self.is_grounded = False

        # Terapkan gravitasi sepanjang waktu
        self.velocity_y += self.gravity * dt
        self.rect.y += self.velocity_y * dt

        # Cek Batas Tanah (Agar tidak amblas menembus tanah)
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.is_grounded = True

        # 3. UPDATE SPRITE IMAGE
        current_frame = self.run_frames[int(self.frame_idx)]
        
        # Balik gambar secara horizontal jika player sedang bergerak ke kiri
        if self.facing_right:
            self.image = current_frame
        else:
            self.image = pygame.transform.flip(current_frame, True, False)

    def _animate(self, dt: float):
        """Fungsi pembantu untuk menjalankan loop animasi run."""
        self.frame_idx += self.animation_speed * dt
        if self.frame_idx >= self.frame_count:
            self.frame_idx = 0.0

    # Render frame
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
