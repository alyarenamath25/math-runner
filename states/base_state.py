from abc import ABC, abstractmethod
import pygame

class BaseState(ABC):
    def __init__(self, game):
        self.game = game # referensi ke Game utama
    
    def enter(self, data: dict | None = None):
        """Dipanggil sekali saat state diaktifkan."""
        pass

    def exit(self):
        """Dipanggil saat state ditinggalkan (cleanup)."""
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
