import pygame
import sys, os

def draw_shadowed_text(surface, font, text, color, shadow_color, pos, shadow_offset=(4, 4)):
    """Render teks dengan drop shadow."""
    shadow_pos = (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1])
    surface.blit(font.render(text, True, shadow_color), shadow_pos)
    surface.blit(font.render(text, True, color), pos)

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)