# Hangman Game 🪓
# Concepts: Strings, Sets, Lists, Loops, Functions, ASCII Art

import random


WORDS = {
    "Animals":     ["elephant", "giraffe", "dolphin", "penguin", "cheetah", "kangaroo", "crocodile", "butterfly"],
    "Countries":   ["brazil", "germany", "australia", "argentina", "thailand", "portugal", "indonesia", "switzerland"],
    "Python":      ["function", "variable", "iterator", "dictionary", "exception", "inheritance", "recursion", "decorator"],
    "Sports":      ["basketball", "volleyball", "swimming", "badminton", "gymnastics", "wrestling", "archery", "cricket"],
}

HANGMAN_STAGES = [
    # 0 wrong
    """
         ┌──────┐
         │      │
                │
                │
                │
                │
       ══════════""",
    # 1 wrong
    """
         ┌──────┐
         │      │
         O      │
                │
                │
                │
       ══════════""",
    # 2 wrong
    """
         ┌──────┐
         │      │
         O      │
         │      │
                │
                │
       ══════════""",
    # 3 wrong
    """
         ┌──────┐
         │      │
         O      │
        /│      │
                │
                │
       ══════════""",
    # 4 wrong
    """
         ┌──────┐
         │      │
         O      │
        /│\\     │
                │
                │
       ══════════""",
    # 5 wrong
    """
         ┌──────┐
         │      │
         O      │
        /│\\     │
        /       │
                │
       ══════════""",
    # 6 wrong — dead
    """
         ┌──────┐
         │      │
         O      │
        /│\\     │
        / \\     │
                │
       ══════════""",
]

MAX_WRONG = len(HANGMAN_STAGES) - 1


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║          🪓  HANGMAN GAME  🪓           ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def choose_category():
    categories = list(WORDS.keys())
    print("  ┌────────────────────────────────────────┐")
    print("  │         Choose a Category:              │")
    print("  ├────────────────────────────────────────┤")
    for i, cat in enumerate(categories, 1):
        print(f"  │   {i}  ➜  {cat:<34}│")
    print(f"  │   {len(categories)+1}  ➜  {'Random (surprise me!)':<34}│")
    print("  └────────────────────────────────────────┘")

    while True:
        try:
            choice = int(input("\n  👉  Select category: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            elif choice == len(categories) + 1:
                return random.choice(categories)
            else:
                print(f"  ⚠️  Enter 1 to {len(categories)+1}.")
        except ValueError:
            print("  ⚠️  Enter a valid number.")


def display_state(word, guessed, wrong_letters, wrong_count):
    print(HANGMAN_STAGES[wrong_count])
    print()

    # Show word with blanks
    display = "  "
    for ch in word:
        display += f" {ch.upper()} " if ch in guessed else " _ "
    print(display)
    print()

    # Wrong letters
    if wrong_letters:
        wrong_str = "  ".join(sorted(wrong_letters))
        print(f"  ❌  Wrong ({wrong_count}/{MAX_WRONG}): {wrong_str}")
    else:
        print(f"  ✅  No wrong guesses yet! ({MAX_WRONG} lives)")
    print()


def get_guess(guessed):
    while True:
        guess = input("  👉  Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("  ⚠️  Enter a single letter only.")
        elif guess in guessed:
            print(f"  ℹ️  You already guessed '{guess.upper()}'. Try another.")
        else:
            return guess


def play_game():
    category = choose_category()
    word = random.choice(WORDS[category]).lower()
    guessed = set()
    wrong_letters = set()
    wrong_count = 0

    print(f"\n  🎯  Category: {category}  |  Word has {len(word)} letters\n")

    while True:
        display_state(word, guessed, wrong_letters, wrong_count)

        # Check win
        if all(ch in guessed for ch in word):
            print(f"  🎉🎉  YOU WIN!  The word was: {word.upper()}")
            remaining_lives = MAX_WRONG - wrong_count
            print(f"  🏆  You had {remaining_lives} life/lives remaining!\n")
            return True

        # Check loss
        if wrong_count >= MAX_WRONG:
            print(f"  💀  GAME OVER!  The word was: {word.upper()}\n")
            return False

        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in word:
            occurrences = word.count(guess)
            print(f"\n  ✅  '{guess.upper()}' is in the word! ({occurrences}x)\n")
        else:
            wrong_letters.add(guess.upper())
            wrong_count += 1
            lives_left = MAX_WRONG - wrong_count
            if lives_left == 1:
                print(f"\n  ⚠️  '{guess.upper()}' is NOT in the word! Last life remaining!\n")
            elif lives_left == 0:
                print(f"\n  💀  '{guess.upper()}' is NOT in the word!\n")
            else:
                print(f"\n  ❌  '{guess.upper()}' is NOT in the word! {lives_left} lives left.\n")


def main():
    show_banner()
    wins = 0
    games = 0

    while True:
        result = play_game()
        games += 1
        if result:
            wins += 1

        print(f"  📊  Record: {wins}W / {games - wins}L  out of {games} game(s)")
        print()
        again = input("  [Enter] ➜ Play Again  |  [q] ➜ Quit\n  👉  ").strip().lower()
        if again == "q":
            print(f"\n  ════════════════════════════════════════")
            print(f"  👋  Goodbye! Won {wins}/{games} games. Keep it up!")
            print(f"  ════════════════════════════════════════\n")
            break
        print()


if __name__ == "__main__":
    main()
