# Quiz Game 🧠
# Concepts: Lists of Dicts, Loops, Conditionals, Functions, Score Tracking

import random


QUESTIONS = [
    # Python
    {"q": "What is the output of type([])?",              "options": ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"],  "ans": "A", "cat": "Python"},
    {"q": "Which keyword defines a function in Python?",  "options": ["func", "def", "define", "fun"],                                            "ans": "B", "cat": "Python"},
    {"q": "What does len('hello') return?",               "options": ["4", "5", "6", "None"],                                                     "ans": "B", "cat": "Python"},
    {"q": "Which of these is a mutable data type?",       "options": ["tuple", "string", "list", "int"],                                          "ans": "C", "cat": "Python"},
    {"q": "How do you start a comment in Python?",        "options": ["//", "/*", "#", "--"],                                                     "ans": "C", "cat": "Python"},
    {"q": "What is the result of 2 ** 3 in Python?",     "options": ["6", "8", "9", "5"],                                                        "ans": "B", "cat": "Python"},

    # Science
    {"q": "What planet is closest to the Sun?",           "options": ["Venus", "Earth", "Mercury", "Mars"],         "ans": "C", "cat": "Science"},
    {"q": "What gas do plants absorb from the air?",      "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "ans": "B", "cat": "Science"},
    {"q": "How many bones are in the adult human body?",  "options": ["196", "206", "216", "186"],                   "ans": "B", "cat": "Science"},
    {"q": "What is the chemical symbol for Gold?",        "options": ["Go", "Gd", "Au", "Ag"],                      "ans": "C", "cat": "Science"},
    {"q": "Which planet is known as the Red Planet?",     "options": ["Jupiter", "Saturn", "Venus", "Mars"],        "ans": "D", "cat": "Science"},

    # General Knowledge
    {"q": "How many continents are there on Earth?",      "options": ["5", "6", "7", "8"],                          "ans": "C", "cat": "General"},
    {"q": "What is the capital of Japan?",                "options": ["Beijing", "Seoul", "Bangkok", "Tokyo"],      "ans": "D", "cat": "General"},
    {"q": "How many days are in a leap year?",            "options": ["364", "365", "366", "367"],                  "ans": "C", "cat": "General"},
    {"q": "Which ocean is the largest?",                  "options": ["Atlantic", "Indian", "Arctic", "Pacific"],   "ans": "D", "cat": "General"},

    # Math
    {"q": "What is the square root of 144?",              "options": ["11", "12", "13", "14"],                      "ans": "B", "cat": "Math"},
    {"q": "What is 15% of 200?",                          "options": ["25", "30", "35", "40"],                      "ans": "B", "cat": "Math"},
    {"q": "How many sides does a hexagon have?",          "options": ["5", "6", "7", "8"],                          "ans": "B", "cat": "Math"},
    {"q": "What is the value of Pi (approx.)?",           "options": ["3.14", "3.41", "3.12", "3.16"],             "ans": "A", "cat": "Math"},
    {"q": "What is 7 × 8?",                               "options": ["54", "56", "58", "52"],                     "ans": "B", "cat": "Math"},
]


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║          🧠  QUIZ GAME  🧠              ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Quick Quiz  (5 random Qs)      │")
    print("  │   2  ➜  Full Quiz   (all 20 Qs)        │")
    print("  │   3  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def ask_question(index, total, question):
    cats = {"Python": "🐍", "Science": "🔬", "General": "🌍", "Math": "➕"}
    cat_icon = cats.get(question["cat"], "❓")

    print(f"  ─────────────────────────────────────────")
    print(f"  Q{index}/{total}  {cat_icon} [{question['cat']}]")
    print(f"  {question['q']}")
    print()

    labels = ["A", "B", "C", "D"]
    for label, option in zip(labels, question["options"]):
        print(f"    {label})  {option}")
    print()

    while True:
        answer = input("  👉  Your answer (A/B/C/D): ").strip().upper()
        if answer in labels:
            return answer
        print("  ⚠️  Enter A, B, C, or D only.")


def run_quiz(questions):
    score = 0
    results = []

    for i, q in enumerate(questions, start=1):
        answer = ask_question(i, len(questions), q)
        correct = answer == q["ans"]

        if correct:
            score += 1
            print(f"\n  ✅  Correct!\n")
        else:
            correct_text = q["options"][ord(q["ans"]) - ord("A")]
            print(f"\n  ❌  Wrong! Correct answer: {q['ans']}) {correct_text}\n")

        results.append({"q": q["q"], "your": answer, "correct": q["ans"], "ok": correct})

    return score, results


def show_results(score, total, results):
    pct = (score / total) * 100

    print()
    print("  ════════════════════════════════════════")
    print(f"  📊  QUIZ COMPLETE!")
    print("  ════════════════════════════════════════")
    print(f"  🏆  Score : {score}/{total}  ({pct:.0f}%)")

    if pct == 100:
        grade = "🌟 PERFECT!  Flawless!"
    elif pct >= 80:
        grade = "🥇 Excellent! Great job!"
    elif pct >= 60:
        grade = "🥈 Good! Keep it up!"
    elif pct >= 40:
        grade = "🥉 Fair. Keep practicing!"
    else:
        grade = "📚 Keep studying. You'll improve!"

    print(f"  🎯  Grade : {grade}")
    print()

    wrong = [r for r in results if not r["ok"]]
    if wrong:
        print(f"  ── Review ({len(wrong)} wrong answer(s)) ──────────")
        for r in wrong:
            print(f"  ✏️  {r['q'][:50]}...")
            print(f"     You: {r['your']}  |  Correct: {r['correct']}")
        print()

    print("  ════════════════════════════════════════\n")


def main():
    show_banner()

    while True:
        show_menu()
        choice = input("\n  👉  Select an option (1-3): ").strip()

        if choice == "1":
            selected = random.sample(QUESTIONS, 5)
            print()
            score, results = run_quiz(selected)
            show_results(score, 5, results)

        elif choice == "2":
            pool = QUESTIONS.copy()
            random.shuffle(pool)
            print()
            score, results = run_quiz(pool)
            show_results(score, len(pool), results)

        elif choice == "3":
            print("\n  👋  Thanks for playing! Keep learning! 🧠\n")
            break

        else:
            print("\n  ⚠️  Invalid option! Please select 1 to 3.\n")


if __name__ == "__main__":
    main()
