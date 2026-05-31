import pygame

class AudioManager:
    """Kelola BGM dan SFX dengan dukungan toggle mute."""
    def __init__(self):
        self.enabled = True
        self._sfx_cache: dict = {}

    # Kontrol BGM
    def play_bgm(self, path: str, volume: float = 0.5):
        if not self.enabled: 
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1) # -1 berarti loop selamanya

    def stop_bgm(self):
        pygame.mixer.music.stop()

    # Kontrol SFX
    def play_sfx(self, path: str, volume: float = 0.7):
        if not self.enabled: 
            return
            
        if path not in self._sfx_cache:
            self._sfx_cache[path] = pygame.mixer.Sound(path)
            
        sfx = self._sfx_cache[path]
        sfx.set_volume(volume)
        sfx.play()

    # Toggle mute
    def toggle(self):
        """Toggle mute/unmute seluruh audio (tombol Sound)."""
        self.enabled = not self.enabled
        if self.enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()