import random
from utils import bubble_sort_choices

def _hitung_faktorial(n: int) -> int:
    """Fungsi Rekursif untuk menghitung faktorial."""
    if n <= 1:
        return 1
    return n * _hitung_faktorial(n - 1)

def generate_question(current_score: int) -> dict:
    """
    Hasilkan satu soal matematika berjenjang berdasarkan skor.
    """
    teks_soal = ""
    jawaban_benar = 0
    is_story = False

    # Level 1: Mudah (Skor < 50)
    if current_score < 50:
        if random.choice([True, False]):
            a, b = random.randint(1, 20), random.randint(1, 20)
            operasi = random.choice(['+', '-'])
            if operasi == '+':
                jawaban_benar = a + b
            else:
                if a < b: a, b = b, a
                jawaban_benar = a - b
            teks_soal = f"{a} {operasi} {b} = ?"
        else:
            is_story = True
            a = random.randint(5, 15)
            b = random.randint(2, 6)
            cerita_mudah = [
                (f"Ryusui punya {a} koin, lalu menemukan {b} koin lagi.\nBerapa total koin Ryusui?", a + b),
                (f"Ryusui membawa {a} ramuan, tapi terjatuh {b} botol.\nBerapa sisa ramuan Ryusui?", max(0, a - b))
            ]
            teks_soal, jawaban_benar = random.choice(cerita_mudah)

    # Level 2: Sedang (Skor 50 - 149)
    elif current_score < 150:
        if random.choice([True, False]):
            a, b = random.randint(2, 10), random.randint(2, 10)
            jawaban_benar = a * b
            teks_soal = f"{a} x {b} = ?"
        else:
            is_story = True
            a = random.randint(2, 5)
            b = random.randint(4, 10)
            cerita_sedang = [
                (f"Ada {a} gerombolan monster, tiap gerombolan berisi\n{b} monster. Berapa total monster?", a * b),
                (f"Ryusui membeli {a} kotak buah misterius.\nTiap kotak berisi {b} koin. Total koin?", a * b)
            ]
            teks_soal, jawaban_benar = random.choice(cerita_sedang)

    # Level 3: Sulit (Skor >= 150)
    else:
        tipe_soal = random.choice(["kombinasi", "cerita", "faktorial"])
        
        if tipe_soal == "kombinasi":
            a, b, c = random.randint(1, 10), random.randint(2, 5), random.randint(1, 10)
            jawaban_benar = a + (b * c)
            teks_soal = f"{a} + {b} x {c} = ?"
            
        elif tipe_soal == "cerita":
            is_story = True
            a = random.randint(20, 50)
            b = random.randint(2, 4)
            c = random.randint(5, 10)
            cerita_sulit = [
                (f"Ryusui punya {a} poin. Dia kalah {b} kali dan\ntiap kalah minus {c} poin. Sisa poin?", a - (b * c)),
                (f"Sebuah jebakan aktif setiap {b} detik sekali.\nJika aktif {c} kali ditambah {a} detik. Total?", (b * c) + a)
            ]
            teks_soal, jawaban_benar = random.choice(cerita_sulit)
            
        else: # Faktorial
            is_story = False
            a = random.randint(3, 5) # Batasi 5! agar tidak over (120)
            jawaban_benar = _hitung_faktorial(a) 
            teks_soal = f"{a}! = ?"

    # Opsi jawaban salah
    choices_set = set()
    choices_set.add(jawaban_benar)
    while len(choices_set) < 4:
        salah = jawaban_benar + random.randint(-5, 5)
        if salah >= 0 and salah != jawaban_benar:
            choices_set.add(salah)
            
    # Sorting
    choices_list = [str(x) for x in choices_set]
    choices_list = bubble_sort_choices(choices_list)
    
    return {
        "question": teks_soal,
        "choices": choices_list,
        "answer": str(jawaban_benar),
        "is_story": is_story 
    }