import pygame
from settings import FONT_PIXEL, FONT_VCR, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLDEN, DARK_NAVY
from systems.math_engine import generate_question
from ui.button import Button
import random

class ExitPopup:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font(FONT_PIXEL, 36)
        self.font_btn = pygame.font.Font(FONT_PIXEL, 32)
        
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 178))
        
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.box_rect = pygame.Rect(cx - 300, cy - 140, 600, 280)
        self.rect_yes = pygame.Rect(cx - 220, cy + 60, 200, 70)
        self.rect_no = pygame.Rect(cx + 20, cy + 60, 200, 70)
    
    def handle_event(self, event) -> str | None:
        """Return "yes", "no", atau None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_yes.collidepoint(event.pos): 
                return "yes"
            if self.rect_no.collidepoint(event.pos): 
                return "no"
        return None

    def draw(self, screen):
        # Overlay gelap
        screen.blit(self.overlay, (0, 0))
        
        # Kotak popup fill + border golden
        pygame.draw.rect(screen, DARK_NAVY, self.box_rect, border_radius=16)
        pygame.draw.rect(screen, GOLDEN, self.box_rect, 3, border_radius=16)
        
        # Teks pertanyaan
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        q = self.font_title.render("Are you sure exit the game?", True, WHITE)
        screen.blit(q, q.get_rect(centerx=cx, centery=cy - 20))
        
        # Button
        pygame.draw.rect(screen, GOLDEN, self.rect_yes, border_radius=8)
        yes_text = self.font_btn.render("YES", True, WHITE)
        screen.blit(yes_text, yes_text.get_rect(center=self.rect_yes.center))
        
        # Tombol NO
        pygame.draw.rect(screen, (100, 80, 40), self.rect_no, border_radius=8)
        no_text = self.font_btn.render("NO", True, WHITE)
        screen.blit(no_text, no_text.get_rect(center=self.rect_no.center))


class MathPopup:
    def __init__(self, game):
        self.game = game
        self.question = None
        
        self.font_math = pygame.font.Font(FONT_VCR, 48)
        self.font_story = pygame.font.Font(FONT_VCR, 24)
        self.font_btn = pygame.font.Font(FONT_VCR, 32)
        self.font_lbl = pygame.font.Font(FONT_VCR, 28)
        
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 191))
        
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.box_rect = pygame.Rect(cx - 350, cy - 210, 700, 420)
        
        self.choice_rects = []
        for row in range(2):
            for col in range(2):
                rx = self.box_rect.x + 80 + (col * 280)
                ry = self.box_rect.y + 230 + (row * 90)
                self.choice_rects.append(pygame.Rect(rx, ry, 240, 70))

    def new_question(self, current_score: int) -> dict:
        """Meminta soal baru dari math_engine berdasarkan skor pemain."""
        
        self.question = generate_question(current_score)
        return self.question

    def handle_event(self, event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.question:
            for index, rect in enumerate(self.choice_rects):
                if rect.collidepoint(event.pos):
                    if self.question["choices"][index] == self.question["answer"]: 
                        return "correct"
                    return "wrong"
        return None

    def draw(self, screen):
        if self.question is None: return
        
        # Overlay
        screen.blit(self.overlay, (0, 0))
        
        # Kotak popup
        pygame.draw.rect(screen, DARK_NAVY, self.box_rect, border_radius=16)
        pygame.draw.rect(screen, GOLDEN, self.box_rect, 3, border_radius=16)
        
        # Teks Soal
        cx = self.box_rect.centerx
        if self.question.get("is_story", False):
            lines = self.question["question"].split('\n')
            for idx, line in enumerate(lines):
                q_surf = self.font_story.render(line, True, WHITE)
                screen.blit(q_surf, q_surf.get_rect(centerx=cx, top=self.box_rect.y + 65 + (idx * 30)))
        else:
            q_surf = self.font_math.render(self.question["question"], True, WHITE)
            screen.blit(q_surf, q_surf.get_rect(centerx=cx, top=self.box_rect.y + 80))
        
        # Label instruksi
        hint = self.font_lbl.render("Pilih jawaban yang benar:", True, GOLDEN)
        screen.blit(hint, hint.get_rect(centerx=cx, top=self.box_rect.y + 165))
        
        # Tombol pilihan jawaban
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.choice_rects):
            bg_color = (255, 180, 40) if rect.collidepoint(mouse_pos) else GOLDEN
            
            pygame.draw.rect(screen, bg_color, rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
            
            choice_surf = self.font_btn.render(self.question["choices"][i], True, WHITE)
            screen.blit(choice_surf, choice_surf.get_rect(center=rect.center))            

class TimesUpPopup:
    def __init__(self, game):
        self.game = game
        self.score = 0
        
        self.font_title = pygame.font.Font(FONT_PIXEL, 64)
        self.font_score = pygame.font.Font(FONT_VCR, 28)
        self.font_btn = pygame.font.Font(FONT_PIXEL, 32)
        
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 191)) 
        
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.box_rect = pygame.Rect(cx - 310, cy - 205, 620, 410)
        self.btn_again = Button("assets/images/ui/btn_play_again.png", center=(cx - 150, cy + 140))
        self.btn_home = Button("assets/images/ui/btn_home.png", center=(cx + 150, cy + 140))

        try:
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(base_dir)
            self.potion_path = os.path.join(root_dir, "assets", "images", "ui", "ramuan.png")
            
            print(f"Python mencari ramuan.png di: {self.potion_path}")
            
            if os.path.exists(self.potion_path):
                print("STATUS: File ditemukan!")
                raw_potion = pygame.image.load(self.potion_path).convert_alpha()
                self.potion_img = pygame.transform.scale(raw_potion, (96, 96))
            else:
                print("STATUS: File TIDAK ADA di folder tersebut! Cek foldermu lagi.")
                self.potion_img = None
                
        except Exception as e:
            print(f" Gagal load karena: {e}")
            self.potion_img = None

    def set_score(self, score: int):
        self.score = score

    def handle_event(self, event) -> str | None:
        if self.btn_again.is_clicked(event): 
            return "play_again"
        if self.btn_home.is_clicked(event): 
            return "home"
        return None

    def draw(self, screen):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        
        screen.blit(self.overlay, (0, 0))
        
        pygame.draw.rect(screen, DARK_NAVY, self.box_rect, border_radius=16)
        pygame.draw.rect(screen, GOLDEN, self.box_rect, 3, border_radius=16)
        
        title = self.font_title.render("Misi Selesai!", True, GOLDEN)
        screen.blit(title, title.get_rect(centerx=cx, top=self.box_rect.y + 25))
        
        # Gambar ramuan berhasil di-load
        if self.potion_img:
            potion_rect = self.potion_img.get_rect(centerx=cx, top=self.box_rect.y + 115)
            screen.blit(self.potion_img, potion_rect)
        
        jumlah_ramuan = self.score // 50
        ramuan_text = self.font_score.render("Ryusui telah berhasil", True, WHITE)
        mengumpulkan_text = self.font_score.render(f"mengumpulkan {jumlah_ramuan} ramuan", True, WHITE)
        
        screen.blit(ramuan_text, ramuan_text.get_rect(centerx=cx, top=self.box_rect.y + 215))
        screen.blit(mengumpulkan_text, mengumpulkan_text.get_rect(centerx=cx, top=self.box_rect.y + 250))
        
        self.btn_again.draw(screen)
        self.btn_home.draw(screen)
