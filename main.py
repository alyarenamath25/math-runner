import pygame
import sys
import random
from engine import GameEngine

# ==============================================================================
# 1. INISIALISASI & KONFIGURASI AWAL
# ==============================================================================
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Arena - Pygame Edition")

# --- PALET WARNA TEMA HUTAN ---
BLACK       = (12, 24, 16)      
FOREST_DARK = (20, 43, 29)      
MOSS_GREEN  = (59, 122, 87)     
LEAF_LIGHT  = (130, 199, 142)   
WOOD_BROWN  = (101, 67, 33)     
EARTH_LIGHT = (160, 120, 85)    
ORCHID_RED  = (214, 40, 40)     
GOLD_SUN    = (247, 127, 0)     
WHITE       = (240, 244, 241)   
GRAY        = (90, 110, 95)     

font_style = pygame.font.match_font('consolas', 'arial')
FONT_TITLE = pygame.font.Font(font_style, 28)
FONT_TEXT  = pygame.font.Font(font_style, 20)

engine = GameEngine()

# State System & Animasi
current_scene = "CHOOSE_STRATEGY" 
current_question = ""
correct_answer = None
player_input_text = ""
log_message = ""
selected_strategy = ""

screen_shake_intensity = 0
floating_damage_text = ""
floating_damage_color = ORCHID_RED 
floating_y_offset = 0
floating_alpha = 255

# Variasi Animasi Baru (Efek Flash & Klik)
flash_screen_duration = 0
player_flash_bar = 0
monster_flash_bar = 0
active_click_btn = None
click_timer = 0

visual_player_hp = engine.player_hp
visual_monster_hp = engine.monster_hp

# Layout Tombol Strategi dengan Ikon Karakter Baru
buttons = {
    "attack":  {"rect": pygame.Rect(50, 480, 150, 60),  "base_color": (184, 61, 39),  "hover_color": (224, 81, 59),   "text": "🪓 Attack"}, 
    "defend":  {"rect": pygame.Rect(230, 480, 150, 60), "base_color": (52, 110, 83),  "hover_color": (72, 140, 108),  "text": "🛡️ Defend"}, 
    "special": {"rect": pygame.Rect(410, 480, 150, 60), "base_color": (214, 157, 56), "hover_color": (244, 187, 86),  "text": "❓ Special"},
    "run":     {"rect": pygame.Rect(590, 480, 150, 60), "base_color": (133, 102, 72), "hover_color": (163, 132, 102), "text": "🏃 Run"}     
}

# ==============================================================================
# SISTEM PARTIKEL
# ==============================================================================
class Particle:
    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y
        self.p_type = p_type
        self.lifetime = random.randint(20, 40)
        self.alpha = 255
        
        if p_type == "leaf":
            self.vx = random.uniform(-4, 4)
            self.vy = random.uniform(-6, -1)
            self.size = random.randint(4, 8)
            self.color = random.choice([LEAF_LIGHT, MOSS_GREEN, (46, 97, 69)])
            self.gravity = 0.2
        elif p_type == "magic":
            self.vx = random.uniform(-5, 5)
            self.vy = random.uniform(-5, 5)
            self.size = random.randint(3, 6)
            self.color = random.choice([GOLD_SUN, (255, 214, 10), (255, 166, 0)])
            self.gravity = -0.05

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        self.alpha = max(0, int((self.lifetime / 40) * 255))

    def draw(self, surface):
        if self.alpha <= 0:
            return
        p_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(p_surface, (*self.color, self.alpha), (self.size, self.size), self.size)
        surface.blit(p_surface, (int(self.x - self.size), int(self.y - self.size)))

particles = []

def spawn_particles(x, y, p_type, count=30):
    for _ in range(count):
        particles.append(Particle(x, y, p_type))

def draw_text(surface, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# ==============================================================================
# 2. FUNGSI DRAW_UI
# ==============================================================================
def draw_ui():
    global screen_shake_intensity, active_click_btn
    
    mouse_pos = pygame.mouse.get_pos()
    
    offset_x = random.randint(-screen_shake_intensity, screen_shake_intensity) if screen_shake_intensity > 0 else 0
    offset_y = random.randint(-screen_shake_intensity, screen_shake_intensity) if screen_shake_intensity > 0 else 0

    game_surface = pygame.Surface((WIDTH, HEIGHT))
    game_surface.fill(BLACK) 
    
    # Hiasan latar belakang hutan
    pygame.draw.circle(game_surface, (15, 32, 22), (0, 40), 120)
    pygame.draw.circle(game_surface, (18, 38, 26), (180, 20), 140)
    pygame.draw.circle(game_surface, (15, 32, 22), (400, -10), 100)
    pygame.draw.circle(game_surface, (18, 38, 26), (620, 20), 130)
    pygame.draw.circle(game_surface, (15, 32, 22), (800, 40), 120)
    pygame.draw.rect(game_surface, FOREST_DARK, (0, 440, WIDTH, 160))
    pygame.draw.line(game_surface, MOSS_GREEN, (0, 442), (WIDTH, 442), 3)

    # Header panel status
    header_panel = pygame.Surface((WIDTH, 80), pygame.SRCALPHA)
    header_panel.fill((20, 43, 29, 200)) 
    game_surface.blit(header_panel, (0, 0))
    
    # HP Player
    pygame.draw.rect(game_surface, BLACK, (30, 40, 200, 16), border_radius=4) 
    p_color = WHITE if player_flash_bar > 0 else LEAF_LIGHT
    pygame.draw.rect(game_surface, p_color, (30, 40, int(max(0, visual_player_hp) * 2), 16), border_radius=4) 
    draw_text(game_surface, f"🌿 PLAYER HP: {engine.player_hp}/100", FONT_TEXT, LEAF_LIGHT, 30, 15)
    
    # HP Monster
    monster_bar_width = int((max(0, visual_monster_hp) / engine.current_monster_max_hp) * 200) if engine.current_monster_max_hp > 0 else 0
    pygame.draw.rect(game_surface, BLACK, (550, 40, 200, 16), border_radius=4)
    m_color = WHITE if monster_flash_bar > 0 else ORCHID_RED
    pygame.draw.rect(game_surface, m_color, (550, 40, monster_bar_width, 16), border_radius=4)
    draw_text(game_surface, f"🐾 MONSTER HP: {max(0, engine.monster_hp)}", FONT_TEXT, ORCHID_RED, 550, 15)
    
    draw_text(game_surface, f"Venture Level: {engine.player_level}", FONT_TEXT, EARTH_LIGHT, 340, 15)
    draw_text(game_surface, f"Score: {engine.score}", FONT_TEXT, GOLD_SUN, 370, 45)
    
    pygame.draw.line(game_surface, WOOD_BROWN, (0, 80), (WIDTH, 80), 3)
    pygame.draw.line(game_surface, WOOD_BROWN, (0, 440), (WIDTH, 440), 3)

    if log_message:
        draw_text(game_surface, log_message, FONT_TEXT, GOLD_SUN, WIDTH // 2, 110, center=True)

    for particle in particles:
        particle.draw(game_surface)

    # Logika Konten Adegan
    if current_scene == "CHOOSE_STRATEGY":
        panel_tengah = pygame.Surface((600, 120), pygame.SRCALPHA)
        panel_tengah.fill((20, 43, 29, 150))
        game_surface.blit(panel_tengah, (100, 170))
        pygame.draw.rect(game_surface, WOOD_BROWN, (100, 170, 600, 120), width=2, border_radius=5)
        draw_text(game_surface, "PILIH STRATEGI UNTUK MENEMBUS HUTAN:", FONT_TITLE, WHITE, WIDTH // 2, 230, center=True)
        
        # Render Tombol Menu Utama
        for btn_name, btn_data in buttons.items():
            rect = btn_data["rect"].copy()
            is_hover = rect.collidepoint(mouse_pos)
            current_color = btn_data["hover_color"] if is_hover else btn_data["base_color"]
            
            if active_click_btn == btn_name:
                rect.y += 4
                pygame.draw.rect(game_surface, current_color, rect, border_radius=8)
            else:
                pygame.draw.rect(game_surface, BLACK, (rect.x + 2, rect.y + 4, rect.width, rect.height), border_radius=8)
                pygame.draw.rect(game_surface, current_color, rect, border_radius=8)
                
            if is_hover and active_click_btn != btn_name:
                pygame.draw.rect(game_surface, WHITE, rect, width=2, border_radius=8)
                
            draw_text(game_surface, btn_data["text"], FONT_TEXT, BLACK, rect.centerx, rect.centery, center=True)
            
    elif current_scene == "ANSWERING":
        panel_tengah = pygame.Surface((600, 240), pygame.SRCALPHA)
        panel_tengah.fill((20, 43, 29, 180))
        game_surface.blit(panel_tengah, (100, 140))
        pygame.draw.rect(game_surface, MOSS_GREEN, (100, 140, 600, 240), width=2, border_radius=8)

        draw_text(game_surface, f"Taktik: {selected_strategy.upper()}", FONT_TEXT, GRAY, WIDTH // 2, 170, center=True)
        draw_text(game_surface, f"Pecahkan Kode Alam:  {current_question} = ?", FONT_TITLE, WHITE, WIDTH // 2, 220, center=True)
        
        input_box = pygame.Rect(275, 270, 250, 45)
        pygame.draw.rect(game_surface, WHITE, input_box, border_radius=5)
        pygame.draw.rect(game_surface, WOOD_BROWN, input_box, width=2, border_radius=5)
        draw_text(game_surface, player_input_text + "|", FONT_TITLE, BLACK, input_box.centerx, input_box.centery, center=True)
        draw_text(game_surface, "Ketik jawaban lalu tekan [ENTER]", FONT_TEXT, GRAY, WIDTH // 2, 350, center=True)
        
    elif current_scene == "SHOW_RESULT":
        draw_text(game_surface, "Tekan [SPACEBAR] untuk melanjutkan perjalanan...", FONT_TEXT, WHITE, WIDTH // 2, 280, center=True)
        
    elif current_scene == "GAME_OVER":
        draw_text(game_surface, "TERJEBAK DI HUTAN ABADI", FONT_TITLE, ORCHID_RED, WIDTH // 2, 220, center=True)
        draw_text(game_surface, f"Kamu gugur di Level {engine.player_level} dengan Skor {engine.score}", FONT_TEXT, WHITE, WIDTH // 2, 280, center=True)

    if floating_damage_text:
        f_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        f_text = FONT_TITLE.render(floating_damage_text, True, (*floating_damage_color, floating_alpha))
        f_surface.blit(f_text, (0, 0))
        text_x = 100 if "Monster menyerangmu" in log_message or "Gagal kabur" in log_message else 650
        game_surface.blit(f_surface, (text_x, 150 + floating_y_offset))

    screen.fill(BLACK)
    screen.blit(game_surface, (offset_x, offset_y))
    
    if flash_screen_duration > 0:
        flash_surf = pygame.Surface((WIDTH, HEIGHT))
        f_color = (200, 30, 30) if "Monster menyerangmu" in log_message else (240, 240, 240)
        flash_surf.fill(f_color)
        flash_surf.set_alpha(120)
        screen.blit(flash_surf, (0, 0))

    pygame.display.flip()


# ==============================================================================
# 3. GAME LOOP UTAMA
# ==============================================================================
clock = pygame.time.Clock()

while True:
    clock.tick(30) 
    
    if screen_shake_intensity > 0:
        screen_shake_intensity -= 1
    if flash_screen_duration > 0:
        flash_screen_duration -= 1
    if player_flash_bar > 0:
        player_flash_bar -= 1
    if monster_flash_bar > 0:
        monster_flash_bar -= 1

    if active_click_btn:
        click_timer -= 1
        if click_timer <= 0:
            active_click_btn = None
            current_scene = "ANSWERING"

    if floating_damage_text:
        floating_y_offset -= 2  
        floating_alpha = max(0, floating_alpha - 8)
        if floating_alpha <= 0:
            floating_damage_text = ""

    for particle in particles[:]:
        particle.update()
        if particle.lifetime <= 0:
            particles.remove(particle)

    visual_player_hp += (engine.player_hp - visual_player_hp) * 0.1
    visual_monster_hp += (engine.monster_hp - visual_monster_hp) * 0.1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if current_scene == "CHOOSE_STRATEGY" and not active_click_btn:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for btn_name, btn_data in buttons.items():
                    if btn_data["rect"].collidepoint(mouse_pos):
                        selected_strategy = btn_name
                        active_click_btn = btn_name
                        click_timer = 4 
                        current_question, correct_answer = engine.generate_question(selected_strategy)
                        player_input_text = ""
                        break
                        
        elif current_scene == "ANSWERING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    if player_input_text != "":
                        try:
                            ans_int = int(player_input_text)
                            is_correct = (ans_int == correct_answer)
                            
                            dmg_dealt, dmg_taken, log_msg = engine.execute_strategy(selected_strategy, is_correct)
                            engine.update_difficulty(is_correct)
                            log_message = log_msg
                            
                            floating_y_offset = 0
                            floating_alpha = 255
                            monster_x, monster_y = 650, 180
                            
                            # --- KALKULASI EFEK VISUAL BERDASARKAN JAWABAN ---
                            if is_correct:
                                if dmg_dealt != "RUN_SUCCESS" and dmg_dealt != "RUN_FAIL":
                                    monster_flash_bar = 6 
                                    floating_damage_text = f"-{dmg_dealt} HP"
                                    floating_damage_color = GOLD_SUN if selected_strategy == "special" else ORCHID_RED
                                    
                                    if selected_strategy == "attack":
                                        spawn_particles(monster_x, monster_y, "leaf", count=35)
                                    elif selected_strategy == "special":
                                        spawn_particles(monster_x, monster_y, "magic", count=50)
                            else:
                                screen_shake_intensity = 18 
                                flash_screen_duration = 3  
                                player_flash_bar = 8       
                                floating_damage_text = f"-{dmg_taken} HP"
                                floating_damage_color = ORCHID_RED 

                            # --- PENENTU SCENE & MEKANIK RECOVERY NYAWA ---
                            if engine.player_hp <= 0:
                                current_scene = "GAME_OVER"
                            else:
                                if engine.monster_hp <= 0:
                                    # FITUR BARU: Menambah darah player saat monster tumbang
                                    engine.player_hp = min(100, engine.player_hp + 20)
                                    
                                    floating_damage_text = "+20 HP"
                                    floating_damage_color = (59, 122, 87) 
                                    floating_y_offset = 0
                                    floating_alpha = 255
                                    
                                    spawn_particles(130, 50, "magic", count=40)
                                    log_message = "Monster kalah! Kamu dapat bonus +20 HP!"
                                    engine.spawn_new_monster()
                                elif dmg_dealt == "RUN_SUCCESS":
                                    engine.spawn_new_monster()
                                    
                                current_scene = "SHOW_RESULT"

                        except ValueError:
                            log_message = "Masukkan angka bulat saja!"
                            player_input_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    player_input_text = player_input_text[:-1]
                elif event.unicode.isdigit() or (event.unicode == '-' and len(player_input_text) == 0):
                    player_input_text += event.unicode
                    
        elif current_scene == "SHOW_RESULT":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                log_message = ""
                current_scene = "CHOOSE_STRATEGY"
                
        elif current_scene == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    engine = GameEngine()
                    log_message = ""
                    particles.clear()
                    current_scene = "CHOOSE_STRATEGY"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
    draw_ui()