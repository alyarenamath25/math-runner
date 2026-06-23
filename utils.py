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
def bubble_sort_choices(array: list) -> list:
    """
    Materi: Sorting (Bubble Sort)
    Mengurutkan pilihan jawaban dari angka terkecil ke terbesar.
    """
    n = len(array)
    # Konversi ke integer untuk proses sorting
    arr_int = [int(x) for x in array]
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr_int[j] > arr_int[j + 1]:
                # Tukar posisi angka integer dan string-nya sekaligus
                arr_int[j], arr_int[j + 1] = arr_int[j + 1], arr_int[j]
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

def linear_search_index(array: list, target: str) -> int:
    """
    Materi: Searching (Linear Search)
    Mencari indeks posisi kunci jawaban di dalam daftar pilihan.
    """
    for i in range(len(array)):
        if array[i] == target:
            return i 
    return -1
