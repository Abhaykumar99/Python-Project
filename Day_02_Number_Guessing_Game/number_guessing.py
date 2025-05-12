# Number Guessing Game 🎯

import random


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║     🎯 NUMBER GUESSING GAME 🎯        ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def choose_difficulty():
    print("  ┌────────────────────────────────────────┐")
    print("  │       Select Difficulty Level:          │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Easy     (1-50,   10 chances)  │")
    print("  │   2  ➜  Medium   (1-100,   7 chances)  │")
    print("  │   3  ➜  Hard     (1-500,   9 chances)  │")
    print("  │   4  ➜  Extreme  (1-1000, 10 chances)  │")
    print("  └────────────────────────────────────────┘")

    levels = {
        "1": ("Easy", 50, 10),
        "2": ("Medium", 100, 7),
        "3": ("Hard", 500, 9),
        "4": ("Extreme", 1000, 10),
    }

    while True:
        choice = input("\n  👉 Select level (1-4): ").strip()
        if choice in levels:
            return levels[choice]
        print("  ⚠️  Please select 1 to 4!")


def play_game():
    level_name, max_num, max_chances = choose_difficulty()

    secret = random.randint(1, max_num)
    print(f"\n  ✨ {level_name} Mode Selected!")
    print(f"  🔢 I've picked a number between 1 and {max_num}.")
    print(f"  🎯 You have {max_chances} chances. Start guessing!\n")

    attempts = 0

    while attempts < max_chances:
        remaining = max_chances - attempts
        print(f"  ⏳ Chances remaining: {remaining}")

        while True:
            try:
                guess = int(input("  👉 Your guess: "))
                if guess < 1 or guess > max_num:
                    print(f"  ⚠️  Guess between 1 and {max_num}!\n")
                    continue
                break
            except ValueError:
                print("  ⚠️  Please enter a valid number!\n")

        attempts += 1

        if guess == secret:
            print(f"\n  🎉🎉🎉 CORRECT! The number was: {secret}")
            print(f"  🏆 You guessed it in {attempts} attempt(s)!")

            if attempts == 1:
                print("  🔥 INCREDIBLE! First try!")
            elif attempts <= max_chances // 3:
                print("  ⭐ AMAZING! Very quick!")
            elif attempts <= max_chances // 2:
                print("  👏 GREAT JOB! Well played!")
            else:
                print("  ✅ WELL DONE! You got it!")

            return True, attempts

        elif guess < secret:
            diff = secret - guess
            if diff > max_num // 2:
                print("  📈 Way too LOW! Go much higher!\n")
            elif diff > max_num // 5:
                print("  📈 Too low! Go higher.\n")
            else:
                print("  📈 Slightly low! You're very close!\n")
        else:
            diff = guess - secret
            if diff > max_num // 2:
                print("  📉 Way too HIGH! Go much lower!\n")
            elif diff > max_num // 5:
                print("  📉 Too high! Go lower.\n")
            else:
                print("  📉 Slightly high! You're very close!\n")

    print(f"\n  😢 Game Over! You ran out of chances.")
    print(f"  🔑 The correct answer was: {secret}")
    return False, attempts


def main():
    show_banner()

    total_games = 0
    wins = 0

    while True:
        won, attempts = play_game()
        total_games += 1
        if won:
            wins += 1

        print(f"\n  📊 Score: {wins}/{total_games} games won")

        print("\n  [Enter] ➜ Play Again  |  [q] ➜ Exit")
        again = input("  👉 ").strip().lower()
        if again == "q":
            print(f"\n  ════════════════════════════════════════")
            print(f"  👋 Goodbye! Played {total_games} game(s), won {wins}.")
            print(f"  ════════════════════════════════════════\n")
            break

        print()


if __name__ == "__main__":
    main()
