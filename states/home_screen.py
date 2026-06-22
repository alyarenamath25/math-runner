import pygame, sys
from settings import *
from states.base_state import BaseState
from ui.button import Button
from ui.popup import ExitPopup
from utils import draw_shadowed_text

class HomeScreen(BaseState):
    def enter(self, data=None):
        # Background
        bg_raw = pygame.image.load("assets/images/backgrounds/homescreen_bg.png")
        self.bg = pygame.transform.scale(bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.font_title = pygame.font.Font(FONT_PIXEL, 96)
        
        # Posisi judul
        cx = SCREEN_WIDTH // 2
        self.btn_start = Button("assets/images/ui/btn_start.png", center=(cx, int(SCREEN_HEIGHT * 0.6)))
        self.btn_sound = Button("assets/images/ui/btn_sound_on.png", center=(int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.85)))
        self.btn_exit = Button("assets/images/ui/btn_exit.png", center=(int(SCREEN_WIDTH * 0.75), int(SCREEN_HEIGHT * 0.85)))

        self.exit_popup = ExitPopup(self.game)
        self.show_exit = False
        self.game.audio.play_bgm("assets/sounds/bgm_home.ogg")

    def handle_event(self, event):
        if self.show_exit:
            result = self.exit_popup.handle_event(event)
            if result == "yes":
                pygame.quit()
                sys.exit()
            elif result == "no":
                self.show_exit = False
            return

        if self.btn_start.is_clicked(event):
            self.game.change_state(STATE_GAME)

        if self.btn_sound.is_clicked(event):
            self.game.audio.toggle()
            icon_status = "on" if self.game.audio.enabled else "off"
            self.btn_sound.swap_image(f"assets/images/ui/btn_sound_{icon_status}.png")

        if self.btn_exit.is_clicked(event):
            self.show_exit = True

    def update(self, dt): 
        pass

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        
        cx = SCREEN_WIDTH // 2
        pos_math = self.font_title.render("MATH", True, WHITE).get_rect(centerx=cx, centery=int(SCREEN_HEIGHT * 0.2))
        pos_runner = self.font_title.render("RUNNER", True, WHITE).get_rect(centerx=cx, centery=int(SCREEN_HEIGHT * 0.35))
        
        draw_shadowed_text(screen, self.font_title, "MATH", WHITE, SHADOW_WARM, pos_math.topleft, (8, 8))
        draw_shadowed_text(screen, self.font_title, "RUNNER", WHITE, SHADOW_WARM, pos_runner.topleft, (8, 8))

        self.btn_start.draw(screen)
        self.btn_sound.draw(screen)
        self.btn_exit.draw(screen)
        
        if self.show_exit:
            self.exit_popup.draw(screen)

    def exit(self):
        self.game.audio.stop_bgm()
