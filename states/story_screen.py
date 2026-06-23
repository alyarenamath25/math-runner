import pygame
import sys
from settings import *
from states.base_state import BaseState
from entities.player import Player
from ui.button import Button
from ui.popup import ExitPopup
from utils import draw_shadowed_text

STORY_PAGES = [
    {
        "lines": [
            "Di negeri yang penuh misteri,",
            "seorang penjelajah bernama Ryusui",
            "mengemban misi yang tak mudah...",
        ],
        "highlight": None,
    },
    {
        "lines": [
            "Ia harus menjelajahi wilayah baru",
            "dan mengumpulkan koin emas sebanyak",
            "mungkin untuk ditukar dengan pasokan",
            "ramuan sihir yang amat ia butuhkan.",
        ],
        "highlight": None,
    },
    {
        "lines": [
            "Namun di sepanjang jalannya,",
            "gerombolan monster menghadang...",
            "membekukan langkah Ryusui di tempat!",
        ],
        "highlight": None,
    },
    {
        "lines": [
            "Ryusui tak bertarung dengan pedang.",
            "Senjatanya adalah akal:",
            "jawab teka-teki matematika mereka,",
            "dan jalan pun terbuka kembali!",
        ],
        "highlight": None,
    },
    {
        "lines": [
            "Kumpulkan koin sebanyak mungkin.",
            "Kalahkan setiap monster yang menghadang.",
            "Seberapa jauh kamu bisa berlari",
            "sebelum waktu habis?",
        ],
        "highlight": "Petualangan dimulai sekarang!",
    },
]

STORY_BG_COLOR   = (15, 12, 30)       # Biru-tua pekat, nuansa malam
TEXT_COLOR       = (220, 210, 255)     # Lavender pucat
HIGHLIGHT_COLOR  = GOLDEN
DIM_OVERLAY      = (0, 0, 0, 160)


class StoryScreen(BaseState):
    def enter(self, data=None):
        # ── Background ──────────────────────────────────────────────
        try:
            bg_raw = pygame.image.load("assets/images/backgrounds/homescreen_bg.png")
            self.bg = pygame.transform.scale(bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        except Exception:
            self.bg = None

        # Overlay gelap di atas BG biar teks terbaca
        self.dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.dim.fill(DIM_OVERLAY)

        # ── Sprite Ryusui (idle / frame pertama) ────────────────────
        self.player = Player(
            "assets/images/sprites/ryusui_run.png",
            frame_count=1,
            frame_w=144,
            frame_h=144,
            bottomleft=(-200, GROUND_Y_RYUSUI),   # mulai di luar layar kiri
        )
        # Kita hanya perlu gambar diam, matikan gerak
        self.player.speed = 0

        # ── Animasi slide-in karakter ────────────────────────────────
        self.char_target_x  = int(SCREEN_WIDTH * 0.15)   # posisi akhir karakter
        self.char_current_x = -200
        self.char_slide_done = False

        # ── State halaman cerita ─────────────────────────────────────
        self.page_index    = 0
        self.total_pages   = len(STORY_PAGES)

        # Efek ketik (typewriter) per halaman
        self.typed_chars   = 0.0
        self.type_speed    = 40.0          # karakter per detik
        self._build_full_text()

        # ── Font ─────────────────────────────────────────────────────
        self.font_body      = pygame.font.Font(FONT_VCR,   28)
        self.font_highlight = pygame.font.Font(FONT_PIXEL, 34)
        self.font_nav       = pygame.font.Font(FONT_PIXEL, 26)
        self.font_hint      = pygame.font.Font(FONT_VCR,   20)

        # ── Kotak teks ───────────────────────────────────────────────
        box_w, box_h = 680, 260
        box_x = SCREEN_WIDTH // 2 - box_w // 2 + 60   # sedikit ke kanan dari tengah
        box_y = int(SCREEN_HEIGHT * 0.30)
        self.text_box = pygame.Rect(box_x, box_y, box_w, box_h)

        # ── Tombol SKIP (lewati cerita → langsung game) ─────────────
        # Dirender sebagai rect teks, tidak butuh aset gambar
        self.skip_rect = pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 60, 130, 40)

        # ── Tombol EXIT (pojok kanan atas, ikon silang) ───────────────
        self.btn_exit = Button(
            "assets/images/ui/btn_exit.png",
            center=(SCREEN_WIDTH - 50, 40),
            scale=0.75,
        )

        # ── Popup konfirmasi exit ─────────────────────────────────────
        self.exit_popup  = ExitPopup(self.game)
        self.show_exit   = False

        # ── Tombol NEXT / MULAI ──────────────────────────────────────
        self.next_rect  = pygame.Rect(
            self.text_box.right - 200,
            self.text_box.bottom + 20,
            180, 52,
        )

        # ── Indikator halaman (dot) ──────────────────────────────────
        self.dot_y = self.next_rect.centery

        self.game.audio.play_bgm("assets/sounds/bgm_home.ogg")

        self._ready = False
    # ─────────────────────────────────────────────────────────────────
    #  Helper
    # ─────────────────────────────────────────────────────────────────
    def _build_full_text(self):
        """Gabungkan semua baris halaman aktif menjadi string tunggal untuk efek ketik."""
        page   = STORY_PAGES[self.page_index]
        joined = " ".join(page["lines"])
        if page["highlight"]:
            joined += "  " + page["highlight"]
        self.full_text   = joined
        self.typed_chars = 0.0

    def _advance_page(self):
        if self.page_index < self.total_pages - 1:
            self.page_index += 1
            self._build_full_text()
        else:
            self._start_game()

    def _start_game(self):
        self.game.audio.stop_bgm()
        self.game.change_state(STATE_GAME)

    # ─────────────────────────────────────────────────────────────────
    #  BaseState interface
    # ─────────────────────────────────────────────────────────────────
    def handle_event(self, event):

        if not self._ready:
            return
        
        # ── Popup exit diprioritaskan ─────────────────────────────────
        if self.show_exit:
            result = self.exit_popup.handle_event(event)
            
            if result == "yes":
                pygame.quit()
                sys.exit()
            elif result == "no":
                self.show_exit = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Tombol EXIT (silang) → munculkan konfirmasi
            if self.btn_exit.is_clicked(event):
                self.show_exit = True
                return

            # Tombol SKIP → langsung mulai game
            if self.skip_rect.collidepoint(event.pos):
                self._start_game()
                return

            # Klik area NEXT / MULAI — kalau efek ketik belum selesai, selesaikan dulu
            if self.next_rect.collidepoint(event.pos):
                if self.typed_chars < len(self.full_text):
                    self.typed_chars = float(len(self.full_text))
                else:
                    self._advance_page()
                return

            # Klik di mana saja = percepat teks kalau belum selesai
            if self.typed_chars < len(self.full_text):
                self.typed_chars = float(len(self.full_text))

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_RIGHT):
                if self.typed_chars < len(self.full_text):
                    self.typed_chars = float(len(self.full_text))
                else:
                    self._advance_page()
            if event.key == pygame.K_ESCAPE:
                self._start_game()

    def update(self, dt):
        
        self._ready = True
        
        # Slide-in karakter dari kiri
        if not self.char_slide_done:
            self.char_current_x += int(600 * dt)
            if self.char_current_x >= self.char_target_x:
                self.char_current_x  = self.char_target_x
                self.char_slide_done = True
        self.player.rect.x = self.char_current_x

        # Efek ketik
        if self.typed_chars < len(self.full_text):
            self.typed_chars += self.type_speed * dt

    def draw(self, screen):
        # ── BG ───────────────────────────────────────────────────────
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill(STORY_BG_COLOR)
        screen.blit(self.dim, (0, 0))

        # ── Karakter Ryusui ──────────────────────────────────────────
        screen.blit(self.player.image, self.player.rect)

        # ── Kotak teks (glassmorphism ringan) ────────────────────────
        box_surf = pygame.Surface((self.text_box.width, self.text_box.height), pygame.SRCALPHA)
        box_surf.fill((26, 26, 46, 200))
        screen.blit(box_surf, self.text_box.topleft)
        pygame.draw.rect(screen, GOLDEN, self.text_box, 2, border_radius=14)

        # ── Teks dengan efek ketik ────────────────────────────────────
        page          = STORY_PAGES[self.page_index]
        visible_chars = int(self.typed_chars)

        # Render baris-baris biasa
        chars_so_far = 0
        line_y       = self.text_box.y + 28
        line_spacing = 38

        for line in page["lines"]:
            if chars_so_far >= visible_chars:
                break
            shown   = line[: max(0, visible_chars - chars_so_far)]
            surf    = self.font_body.render(shown, True, TEXT_COLOR)
            screen.blit(surf, (self.text_box.x + 28, line_y))
            chars_so_far += len(line) + 1   # +1 untuk spasi gabungan
            line_y       += line_spacing

        # Teks highlight (baris terakhir halaman terakhir)
        if page["highlight"]:
            offset     = sum(len(l) + 1 for l in page["lines"]) + 2
            hl_visible = max(0, visible_chars - offset)
            if hl_visible > 0:
                shown_hl = page["highlight"][:hl_visible]
                hl_surf  = self.font_highlight.render(shown_hl, True, HIGHLIGHT_COLOR)
                screen.blit(hl_surf, hl_surf.get_rect(
                    centerx=self.text_box.centerx,
                    top=line_y + 8,
                ))

        # ── Tombol NEXT / MULAI ───────────────────────────────────────
        is_last   = (self.page_index == self.total_pages - 1)
        btn_label = "MULAI!" if is_last else "LANJUT"
        mx, my    = pygame.mouse.get_pos()
        btn_hover = self.next_rect.collidepoint(mx, my)
        btn_color = (255, 190, 50) if btn_hover else GOLDEN

        pygame.draw.rect(screen, btn_color, self.next_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE,     self.next_rect, 2, border_radius=10)
        lbl = self.font_nav.render(btn_label, True, DARK_NAVY)
        screen.blit(lbl, lbl.get_rect(center=self.next_rect.center))

        # ── Dot indikator halaman ─────────────────────────────────────
        dot_r    = 6
        dot_gap  = 18
        total_w  = (self.total_pages - 1) * dot_gap
        start_x  = self.text_box.x + (self.text_box.width - total_w) // 2
        for i in range(self.total_pages):
            cx = start_x + i * dot_gap
            cy = self.dot_y
            color = GOLDEN if i == self.page_index else (80, 70, 40)
            pygame.draw.circle(screen, color, (cx, cy), dot_r if i == self.page_index else dot_r - 2)

        # ── Hint keyboard ─────────────────────────────────────────────
        hint = self.font_hint.render("SPACE / ENTER untuk lanjut  •  ESC untuk skip", True, (120, 110, 80))
        screen.blit(hint, hint.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 16))

        # ── Tombol SKIP (kiri dari EXIT) ─────────────────────────────
        mx, my     = pygame.mouse.get_pos()
        skip_hover = self.skip_rect.collidepoint(mx, my)
        skip_bg    = (255, 190, 50) if skip_hover else (60, 45, 10)
        pygame.draw.rect(screen, skip_bg,  self.skip_rect, border_radius=8)
        pygame.draw.rect(screen, GOLDEN,   self.skip_rect, 2, border_radius=8)
        skip_lbl = self.font_hint.render("SKIP", True, WHITE)
        screen.blit(skip_lbl, skip_lbl.get_rect(center=self.skip_rect.center))

        # ── Tombol EXIT (ikon silang, pojok kanan atas) ───────────────
        self.btn_exit.draw(screen)

        # ── Popup konfirmasi exit ─────────────────────────────────────
        if self.show_exit:
            self.exit_popup.draw(screen)

    def exit(self):
        self.game.audio.stop_bgm()