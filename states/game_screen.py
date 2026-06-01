# states/game_screen.py
import pygame
from settings import *
from states.base_state import BaseState
from entities.player import Player
from systems.spawner import Spawner
from systems.timer import GameTimer
from ui.hud import HUD
from ui.popup import MathPopup, TimesUpPopup, ExitPopup
from ui.button import Button

class GameScreen(BaseState):
    def enter(self, data=None):
        # Background
        bg_raw = pygame.image.load("assets/images/backgrounds/game_bg.png")
        self.bg = pygame.transform.scale(bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.bg_x = 0
        
        # Entitas & sistem
        self.player = Player("assets/images/sprites/ryusui_run.png", frame_count=1, frame_w=144, frame_h=144, bottomleft=(150, GROUND_Y_RYUSUI))
        self.timer = GameTimer(INITIAL_TIME)
        self.spawner = Spawner()
        self.score = 0
        self.hud = HUD()
        
        # State popup
        self.math_popup = MathPopup(self.game)
        self.timesup_popup = TimesUpPopup(self.game)
        self.exit_popup = ExitPopup(self.game)

        self.btn_pause = Button("assets/images/ui/btn_pause.png", center=(SCREEN_WIDTH - 120, 40), scale=0.7)
        self.btn_exit = Button("assets/images/ui/btn_exit.png", center=(SCREEN_WIDTH - 50, 40), scale=0.7)

        self._full_reset()
        self.game.audio.play_bgm("assets/sounds/bgm_game.ogg")

    # Logika event in- game
    def handle_event(self, event):
        if self.active_popup == "math":
            result = self.math_popup.handle_event(event)
            if result == "correct":
                self.score += SCORE_MONSTER
                self.timer.add_time(TIME_BONUS)

                if self.current_monster is not None:
                    self.current_monster.defeated = True

                self.player.blocked = False
                self.active_popup = None
                self.game.audio.play_sfx("assets/sounds/sfx_correct.ogg")
                
            elif result == "wrong":
                self.score = max(0, self.score - 5) 
                self.hud.trigger_flash() 
                
                # Soal yang sama muncul ulang, Ryusui tetap stuck
                self.game.audio.play_sfx("assets/sounds/sfx_wrong.ogg")
            return
            
        if self.active_popup == "times_up":
            result = self.timesup_popup.handle_event(event)
            if result == "play_again":
                self._full_reset()
            elif result == "home":
                self.game.change_state(STATE_HOME)
            return

        if self.active_popup == "exit":
            result = self.exit_popup.handle_event(event)
            if result == "yes":
                self.game.change_state(STATE_HOME) # Keluar ke menu utama jika Yes
            elif result == "no":
                self.active_popup = None # Tutup popup dan kembali ke game jika No
            return

        if self.active_popup is None:
            if self.btn_pause.is_clicked(event):
                self.is_paused = not self.is_paused

                # Ganti gambar berdasarkan status
                if self.is_paused:
                    self.btn_pause.swap_image("assets/images/ui/btn_play_again.png")
                else:
                    self.btn_pause.swap_image("assets/images/ui/btn_pause.png")
                return 

            # Tombol Exit
            if self.btn_exit.is_clicked(event):
                self.active_popup = "exit" 
                return

    # Main update loop in-game
    def update(self, dt):
        self.hud.update(dt)

        # Logika timer game
        if not self.is_paused and self.active_popup not in ["times_up", "exit"]:
            if self.timer.update(dt):
                self.timesup_popup.set_score(self.score)
                self.active_popup = "times_up"
                return

        # 2. UPDATE RUNNER/GAMEPLAY (hanya jalan jika tidak ada popup dan tidak diklik pause)
        if self.active_popup is None and not self.is_paused:
            self.bg_x -= PLAYER_SPEED
            if self.bg_x <= -SCREEN_WIDTH: 
                self.bg_x = 0
            
            self.spawner.update(PLAYER_SPEED)
            self.player.update(dt) 
            
            self._check_collisions()
            self.spawner.cleanup()

    # Deteksi tabrakan
    def _check_collisions(self):
        from entities.coin import Coin
        from entities.monster import Monster
        
        for obj in self.spawner.objects:
            # 1. Jika secara kotak tidak bersentuhan sama sekali, abaikan.
            if not self.player.rect.colliderect(obj.rect):
                continue
                
            # 2. Logika untuk Koin
            if isinstance(obj, Coin) and not obj.collected:
                obj.collected = True
                self.score += SCORE_COIN
                self.game.audio.play_sfx("assets/sounds/sfx_coin.ogg")
                
            # 3. Logika untuk Monster
            elif isinstance(obj, Monster):
                # Jika monster sudah berhasil dilewati sebelumnya, abaikan tabrakan baru
                if getattr(obj, 'passed', False) or obj.defeated:
                    continue

                # obj.rect.top adalah koordinat ujung kepala paling atas si monster.
                # cek: Apakah posisi kaki bawah Ryusui (self.player.rect.bottom) 
                # masih berada DI ATAS kepala monster? 
                # beri toleransi amblas sedikit (10-15 piksel) agar terasa adil secara visual.
                if self.player.rect.bottom <= obj.rect.top + 12:
                    # Ryusui sedang berada di udara di atas monster (Baik saat naik maupun turun)
                    obj.passed = True 
                    continue 

                # jika menabrak tubuh monster
                obj.defeated = True 
                self.player.blocked = True
                self.current_monster = obj
                q = self.math_popup.new_question()
                self.active_popup = "math"

    # Reset sesi
    def _full_reset(self):
        """Reset lengkap untuk Play Again atau kembali ke Home."""
        self.is_paused = False
        
        self.score = 0
        self.player.blocked = False
        self.player.rect.bottomleft = (150, GROUND_Y_RYUSUI)
        self.player.frame_idx = 0
        self.timer.reset(INITIAL_TIME)
        self.spawner = Spawner()
        self.active_popup = None
        self.current_monster = None
        self.bg_x = 0

        if hasattr(self, 'btn_pause'):
            self.btn_pause.swap_image("assets/images/ui/btn_pause.png")

    # Render layer in-game
    def draw(self, screen):
        # 1. Background (looping tile)
        screen.blit(self.bg, (self.bg_x, 0))
        screen.blit(self.bg, (self.bg_x + SCREEN_WIDTH, 0))
        
        # 2. Spawned objects (koin & monster)
        self.spawner.draw(screen)
        
        # 3. Player (Ryusui)
        self.player.draw(screen)
        
        # 4. HUD (skor & timer selalu di atas)
        self.hud.draw(screen, self.score, self.timer.get_display())
        
        # 5. Tombol pause & exit
        self.btn_pause.draw(screen)
        self.btn_exit.draw(screen)

        # 6. Popup aktif, timer terus jalan
        if self.active_popup == "math":
            self.math_popup.draw(screen)
        elif self.active_popup == "times_up":
            self.timesup_popup.draw(screen)
        elif self.active_popup == "exit":
            self.exit_popup.draw(screen)

    def exit(self):
        self.game.audio.stop_bgm()
