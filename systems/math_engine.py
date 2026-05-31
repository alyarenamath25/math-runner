import random

# Generate soal acak
def generate_question() -> dict:
    """
    Hasilkan satu soal matematika dengan 4 pilihan ganda.
    Return: {"question": str, "answer": int, "choices": list[str]}
    """
    op = random.choice(["+", "-", "x", "/"])
    
    if op == "+":
        a, b = random.randint(1, 50), random.randint(1, 50)
        ans = a + b
    elif op == "-":
        a = random.randint(10, 99)
        b = random.randint(1, a)
        ans = a - b
    elif op == "x":
        a, b = random.randint(2, 12), random.randint(2, 12)
        ans = a * b
    else: 
        b = random.randint(2, 10)
        ans = random.randint(1, 12)
        a = ans * b  # Memastikan hasil bagi selalu bulat sempurna
        
    op_display = {"x": "x", "/": ":"}
    question_text = f"{a} {op_display.get(op, op)} {b} = ?"
    
    # Generate jawaban yang salah
    wrong_answers = set()
    possible_noises = [-5, -3, -2, -1, 1, 2, 3, 5]
    
    while len(wrong_answers) < 3:
        noise = random.choice(possible_noises)
        candidate = ans + noise
        if candidate > 0 and candidate != ans:
            wrong_answers.add(candidate)
        
    choices = [str(ans)] + [str(w) for w in list(wrong_answers)[:3]]
    random.shuffle(choices)
    
    return {"question": question_text, "answer": ans, "choices": choices}

# Cek jawaban
def check_answer(question: dict, player_answer: str) -> bool:
    """Return True jika jawaban benar."""
    return str(question["answer"]) == player_answer.strip()