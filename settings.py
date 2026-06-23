SCREEN_WIDTH = 1280 
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Math Runner"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLDEN = (245, 166, 35) # Warna tombol START
DARK_NAVY = ( 26, 26, 46) # Warna kotak popup
SHADOW_WARM = ( 73, 37, 0) # Shadow judul
OVERLAY = ( 0, 0, 0, 180) # Overlay popup

FONT_PIXEL = "assets/fonts/PixelifySans-Regular.ttf" # Judul & tombol Home Screen
FONT_VCR = "assets/fonts/vcr_osd_mono.ttf" # Skor, Timer, Soal Matematika

INITIAL_TIME = 60 # detik
TIME_BONUS = 3 # detik (bonus jawaban benar)
SCORE_COIN = 10
SCORE_MONSTER = 25

SPAWN_MIN_DIST = 100 # px jarak minimum antar objek
SPAWN_MAX_DIST = 300 # px jarak maksimum
PLAYER_SPEED = 4 # px per frame (kecepatan scroll)

GROUND_Y_RYUSUI = int(SCREEN_HEIGHT * 0.865)
GROUND_Y_OBJECT = int(SCREEN_HEIGHT * 0.85)

STATE_HOME = "home"
STATE_STORY = "story"
STATE_GAME = "game"

SPAWN_POOL = ["coin", "coin", "coin", "monster", "monster"]
