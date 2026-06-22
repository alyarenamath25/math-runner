import pygame
from settings import FONT_PIXEL, FONT_VCR, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLDEN, DARK_NAVY
from systems.math_engine import generate_question, check_answer
from ui.button import Button
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_VCR, FONT_PIXEL, DARK_NAVY, GOLDEN, WHITE

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
        # Overlay
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
        
        self.font_math = pygame.font.Font(FONT_VCR, 48)  # Teks soal normal
        self.font_story = pygame.font.Font(FONT_VCR, 24) # Teks khusus soal cerita (lebih kecil agar muat)
        self.font_btn = pygame.font.Font(FONT_VCR, 32)   # Pilihan jawaban
        self.font_lbl = pygame.font.Font(FONT_VCR, 28) # Label instruksi
        
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

    def new_question(self) -> dict:
        """Generate soal baru secara acak (bisa soal cerita) berdasarkan skor saat ini."""
        # Ambil skor pemain secara aman dari game_screen
        try:
            current_score = self.game.current_state.score
        except:
            current_score = 0

        teks_soal = ""
        jawaban_benar = 0
        is_story = False # Penanda apakah soal yang keluar berbentuk soal cerita

        # Soal acak berdasarkan skor
        if current_score < 50:
            if random.choice([True, False]):
                a, b = random.randint(1, 20), random.randint(1, 20)
                operasi = random.choice(['+', '-'])
                if operasi == '+':
                    jawaban_benar = a + b
                else:
                    if a < b: a, b = b, a
                    jawaban_benar = a - b
                teks_soal = f"{a} {operasi} {b} = ?"
            else:
                is_story = True
                a = random.randint(5, 15)
                b = random.randint(2, 6)
                cerita_mudah = [
                    (f"Ryusui punya {a} koin, lalu menemukan {b} koin lagi.\nBerapa total koin Ryusui?", a + b),
                    (f"Ryusui membawa {a} ramuan, tapi terjatuh {b} botol.\nBerapa sisa ramuan Ryusui?", max(0, a - b))
                ]
                teks_soal, jawaban_benar = random.choice(cerita_mudah)

        elif current_score < 150:
            if random.choice([True, False]):
                a, b = random.randint(2, 10), random.randint(2, 10)
                jawaban_benar = a * b
                teks_soal = f"{a} x {b} = ?"
            else:
                is_story = True
                a = random.randint(2, 5)
                b = random.randint(4, 10)
                cerita_sedang = [
                    (f"Ada {a} gerombolan monster, tiap gerombolan berisi\n{b} monster. Berapa total monster?", a * b),
                    (f"Ryusui membeli {a} kotak buah misterius.\nTiap kotak berisi {b} koin. Total koin?", a * b)
                ]
                teks_soal, jawaban_benar = random.choice(cerita_sedang)

        else:
            if random.choice([True, False]):
                a, b, c = random.randint(1, 10), random.randint(2, 5), random.randint(1, 10)
                jawaban_benar = a + (b * c)
                teks_soal = f"{a} + {b} x {c} = ?"
            else:
                is_story = True
                a = random.randint(20, 50)
                b = random.randint(2, 4)
                c = random.randint(5, 10)
                cerita_sulit = [
                    (f"Ryusui punya {a} poin. Dia kalah {b} kali dan\ntiap kalah minus {c} poin. Sisa poin?", a - (b * c)),
                    (f"Sebuah jebakan aktif setiap {b} detik sekali.\nJika aktif {c} kali ditambah {a} detik. Total?", (b * c) + a)
                ]
                teks_soal, jawaban_benar = random.choice(cerita_sulit)

        # Distractor
        choices_set = set()
        choices_set.add(jawaban_benar)
        while len(choices_set) < 4:
            salah = jawaban_benar + random.randint(-5, 5)
            if salah >= 0 and salah != jawaban_benar:
                choices_set.add(salah)
        
        choices_list = [str(x) for x in choices_set]
        random.shuffle(choices_list)

        self.question = {
            "question": teks_soal,
            "choices": choices_list,
            "answer": str(jawaban_benar),
            "is_story": is_story # Ditambahkan penanda tipe teks
        }
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
        
        # Teks Soal (Dipisah berdasarkan tipe Soal Cerita atau Matematika Biasa)
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
        self.font_score = pygame.font.Font(FONT_VCR, 36)
        self.font_btn = pygame.font.Font(FONT_PIXEL, 32)
        
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 191)) # 0.75 opacity
        
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.box_rect = pygame.Rect(cx - 310, cy - 180, 620, 360)
        self.btn_again = Button("assets/images/ui/btn_play_again.png", center=(cx - 150, cy + 110))
        self.btn_home = Button("assets/images/ui/btn_home.png", center=(cx + 150, cy + 110))

    def set_score(self, score: int):
        self.score = score

    def handle_event(self, event) -> str | None:
        """Return "play_again", "home", atau None."""
        if self.btn_again.is_clicked(event): 
            return "play_again"
        if self.btn_home.is_clicked(event): 
            return "home"
        return None

    def draw(self, screen):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        
        # Overlay
        screen.blit(self.overlay, (0, 0))
        
        # Kotak popup
        pygame.draw.rect(screen, DARK_NAVY, self.box_rect, border_radius=16)
        pygame.draw.rect(screen, GOLDEN, self.box_rect, 3, border_radius=16)
        
        # Teks "Times Up!"
        title = self.font_title.render("Time's Up!", True, GOLDEN)
        screen.blit(title, title.get_rect(centerx=cx, top=self.box_rect.y + 60))
        
        # Skor akhir
        score_text = self.font_score.render(f"Score: {self.score:05d}", True, WHITE)
        screen.blit(score_text, score_text.get_rect(centerx=cx, top=self.box_rect.y + 165))
        
        # Button
        self.btn_again.draw(screen)
        self.btn_home.draw(screen)
