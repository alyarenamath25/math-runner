# settings.py

# Layar 
SCREEN_WIDTH = 1280 # Sesuai canvas Figma
SCREEN_HEIGHT = 720 # Sesuai canvas Figma
FPS = 60
TITLE = "Math Runner"

# Palet Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLDEN = (245, 166, 35) # Warna tombol START
DARK_NAVY = ( 26, 26, 46) # Warna kotak popup
SHADOW_WARM = ( 73, 37, 0) # Shadow judu
OVERLAY = ( 0, 0, 0, 180) # Overlay popup

# Font
FONT_PIXEL = "assets/fonts/PixelifySans-Regular.ttf" # Judul & tombol Home Screen
FONT_VCR = "assets/fonts/vcr_osd_mono.ttf" # Skor, Timer, Soal Matematika

# Timer & Skor
INITIAL_TIME = 60 # detik
TIME_BONUS = 3 # detik bonus jawaban benar
SCORE_COIN = 50
SCORE_MONSTER = 100

# Spawn
SPAWN_MIN_DIST = 100 # px jarak minimum antar objek
SPAWN_MAX_DIST = 300 # px jarak maksimum
PLAYER_SPEED = 4 # px per frame (kecepatan scroll)

# Posisi Objek
GROUND_Y_RYUSUI = int(SCREEN_HEIGHT * 0.865)
GROUND_Y_OBJECT = int(SCREEN_HEIGHT * 0.85)

# Identifikasi State
STATE_HOME = "home"
STATE_GAME = "game"

# Peluang spawn
SPAWN_POOL = ["coin", "coin", "coin", "monster", "monster"]