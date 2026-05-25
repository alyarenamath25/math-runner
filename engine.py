import random

class GameEngine:
    def __init__(self):
        self.player_hp = 100
        self.monster_hp = 50
        self.player_level = 1
        self.score = 0
        self.difficulty_modifier = 1.0
        self.current_monster_max_hp = 50

    def generate_question(self, strategy):
        max_val = int(10 * self.player_level * self.difficulty_modifier)
        a = random.randint(1, max_val)
        b = random.randint(1, max_val)
        
        effective_level = self.player_level
        if strategy == "defend":
            effective_level = max(1, effective_level - 1)
        elif strategy == "special":
            effective_level += 1

        if effective_level == 1:
            operator = random.choice(["+", "-"])
            if operator == "-": a, b = max(a, b), min(a, b)
            question = f"{a} {operator} {b}"
            correct_answer = a + b if operator == "+" else a - b
        elif effective_level == 2:
            b = random.randint(2, 10)
            operator = random.choice(["*", "//"])
            if operator == "//": a = b * random.randint(1, 10)
            question = f"{a} {operator} {b}"
            correct_answer = a * b if operator == "*" else a // b
        else:
            c = random.randint(1, 5)
            b = random.randint(1, 5)
            question = f"({a} * {b}) + {c}^2"
            correct_answer = (a * b) + c**2
            
        return question, correct_answer

    def update_difficulty(self, is_correct):
        if is_correct:
            self.difficulty_modifier += 0.05
        else:
            self.difficulty_modifier = max(0.5, self.difficulty_modifier - 0.1)

    def execute_strategy(self, strategy, is_correct):
        if not is_correct:
            damage_taken = int(15 * self.difficulty_modifier)
            self.player_hp -= damage_taken
            return 0, damage_taken, "SALAH! Monster menyerangmu!"

        base_dmg = 10 * self.player_level
        if strategy == "attack":
            self.monster_hp -= base_dmg
            return base_dmg, 0, "BENAR! Serangan langsung berhasil!"
        elif strategy == "defend":
            dmg = int(base_dmg * 0.5)
            self.monster_hp -= dmg
            return dmg, 0, "BENAR! Strategi aman, damage minimal."
        elif strategy == "special":
            dmg = base_dmg * 2
            self.monster_hp -= dmg
            return dmg, 0, "BENAR! CRITICAL DAMAGE!"
        elif strategy == "run":
            if random.random() > 0.4:
                return "RUN_SUCCESS", 0, "Berhasil kabur mencari celah!"
            else:
                damage_taken = int(5 * self.difficulty_modifier)
                self.player_hp -= damage_taken
                return "RUN_FAIL", damage_taken, "Gagal kabur! Monster menyerang!"

    def spawn_new_monster(self):
        self.score += 100
        self.player_level += 1
        self.current_monster_max_hp = int(50 * (1.2 ** self.player_level))
        self.monster_hp = self.current_monster_max_hp