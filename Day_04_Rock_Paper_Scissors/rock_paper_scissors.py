# Rock, Paper, Scissors ✊✋✌️
# Concepts: Random, Conditionals, Loops, Functions, Score Tracking

import random


CHOICES = {
    "1": ("Rock",     "✊"),
    "2": ("Paper",    "✋"),
    "3": ("Scissors", "✌️"),
}

WINS_AGAINST = {
    "Rock":     "Scissors",
    "Paper":    "Rock",
    "Scissors": "Paper",
}


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║   ✊✋✌️  ROCK · PAPER · SCISSORS  ✌️✋✊  ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_choice_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │   1  ➜  Rock     ✊                     │")
    print("  │   2  ➜  Paper    ✋                     │")
    print("  │   3  ➜  Scissors ✌️                     │")
    print("  │   0  ➜  Quit                           │")
    print("  └────────────────────────────────────────┘")


def get_player_choice():
    while True:
        choice = input("\n  👉  Your choice (0-3): ").strip()
        if choice == "0":
            return None
        if choice in CHOICES:
            return CHOICES[choice]
        print("  ⚠️  Please enter 1, 2, 3, or 0 to quit.")


def get_computer_choice():
    key = random.choice(list(CHOICES.keys()))
    return CHOICES[key]


def determine_winner(player, computer):
    p_name, _ = player
    c_name, _ = computer
    if p_name == c_name:
        return "tie"
    elif WINS_AGAINST[p_name] == c_name:
        return "player"
    else:
        return "computer"


def play_round(score):
    show_choice_menu()
    player = get_player_choice()

    if player is None:
        return False   # signal to quit

    computer = get_computer_choice()
    p_name, p_emoji = player
    c_name, c_emoji = computer

    print()
    print(f"  🧑  You   : {p_emoji}  {p_name}")
    print(f"  🤖  CPU   : {c_emoji}  {c_name}")
    print()

    result = determine_winner(player, computer)

    if result == "tie":
        print("  🤝  It's a TIE!")
        score["ties"] += 1
    elif result == "player":
        print(f"  🎉  YOU WIN!  {p_name} beats {c_name}!")
        score["player"] += 1
    else:
        print(f"  😢  CPU WINS!  {c_name} beats {p_name}!")
        score["computer"] += 1

    print()
    print(f"  📊  Score  ➜  You: {score['player']}  |  CPU: {score['computer']}  |  Ties: {score['ties']}")
    print()
    return True


def show_final_score(score):
    total = score["player"] + score["computer"] + score["ties"]
    print()
    print("  ════════════════════════════════════════")
    print(f"  🏁  FINAL SCORE  (after {total} round(s))")
    print("  ════════════════════════════════════════")
    print(f"  🧑  You : {score['player']}")
    print(f"  🤖  CPU : {score['computer']}")
    print(f"  🤝  Ties: {score['ties']}")
    print()

    if score["player"] > score["computer"]:
        print("  🏆  Overall Winner: YOU! Well played!")
    elif score["computer"] > score["player"]:
        print("  🤖  Overall Winner: CPU! Better luck next time.")
    else:
        print("  🤝  Overall Result: It's ALL square!")

    print("  ════════════════════════════════════════")
    print("  👋  Thanks for playing!\n")


def main():
    show_banner()
    score = {"player": 0, "computer": 0, "ties": 0}

    while True:
        running = play_round(score)
        if not running:
            show_final_score(score)
            break

        again = input("  [Enter] ➜ Next Round  |  [q] ➜ Quit\n  👉  ").strip().lower()
        if again == "q":
            show_final_score(score)
            break
        print()


if __name__ == "__main__":
    main()
