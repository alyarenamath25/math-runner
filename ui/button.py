# ui/button.py
import pygame

class Button:
    """Tombol yang di-render dari gambar PNG (aset dari Figma)."""

    #Setup gambar dan skala
    def __init__(self, image_path: str, center: tuple, scale: float = 1.0):
        img = pygame.image.load(image_path).convert_alpha()
        if scale != 1.0:
            w = int(img.get_width() * scale)
            h = int(img.get_height() * scale)
            img = pygame.transform.scale(img, (w, h))
        self.image = img
        self.rect = img.get_rect(center=center)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    # Cek tabrakan kursor
    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos))

    # Ganti state gambar
    def swap_image(self, new_path: str):
        """Ganti gambar tombol (misal: toggle sound on/off)."""
        img = pygame.image.load(new_path).convert_alpha()
        self.image = pygame.transform.scale(img, self.rect.size)
