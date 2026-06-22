import pygame, sys
from settings import *
from states.home_screen import HomeScreen
from states.game_screen import GameScreen
from systems.audio_manager import AudioManager

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.audio = AudioManager()

        self.current_state = None
        self.states = {
            STATE_HOME: HomeScreen(self),
            STATE_GAME: GameScreen(self),
        }
        self.change_state(STATE_HOME)

    # Transisi layar
    def change_state(self, state_id: str, data: dict | None = None):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[state_id]
        self.current_state.enter(data)

    # Main game loop
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0 # delta-time dalam detik

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.current_state:
                    self.current_state.handle_event(event)

            if self.current_state:
                self.current_state.update(dt)
                self.current_state.draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
