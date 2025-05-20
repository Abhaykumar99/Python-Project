# Tic-Tac-Toe 🎮
# Concepts: 2D Lists, Nested Loops, Functions, Game Logic, Win Detection

import random


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║        🎮  TIC - TAC - TOE  🎮         ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  2 Players (Human vs Human)     │")
    print("  │   2  ➜  vs Computer (Easy)             │")
    print("  │   3  ➜  vs Computer (Hard / AI)        │")
    print("  │   4  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def new_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board):
    print()
    print("        1   2   3")
    print("      ┌───┬───┬───┐")
    for i, row in enumerate(board):
        cells = " │ ".join(
            f"\033[92m{c}\033[0m" if c == "X" else (f"\033[93m{c}\033[0m" if c == "O" else c)
            for c in row
        )
        print(f"   {i+1}  │ {cells} │")
        if i < 2:
            print("      ├───┼───┼───┤")
    print("      └───┴───┴───┘")
    print()


def check_winner(board, mark):
    # Rows & columns
    for i in range(3):
        if all(board[i][j] == mark for j in range(3)):
            return True
        if all(board[j][i] == mark for j in range(3)):
            return True
    # Diagonals
    if all(board[i][i] == mark for i in range(3)):
        return True
    if all(board[i][2 - i] == mark for i in range(3)):
        return True
    return False


def is_full(board):
    return all(board[r][c] != " " for r in range(3) for c in range(3))


def get_empty(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]


def human_move(board, mark, name):
    while True:
        try:
            raw = input(f"  👉  {name} ({mark}) — Enter row col (e.g. 1 2): ").strip()
            parts = raw.split()
            if len(parts) != 2:
                raise ValueError
            r, c = int(parts[0]) - 1, int(parts[1]) - 1
            if not (0 <= r <= 2 and 0 <= c <= 2):
                print("  ⚠️  Row and column must be 1, 2, or 3.")
                continue
            if board[r][c] != " ":
                print("  ⚠️  That cell is already taken!")
                continue
            board[r][c] = mark
            return
        except ValueError:
            print("  ⚠️  Enter two numbers separated by space, e.g. '2 3'.")


def computer_move_easy(board, mark):
    """Random available cell."""
    r, c = random.choice(get_empty(board))
    board[r][c] = mark
    print(f"  🤖  Computer plays: row {r+1}, col {c+1}")


def minimax(board, is_maximizing, ai_mark, human_mark):
    if check_winner(board, ai_mark):
        return 1
    if check_winner(board, human_mark):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best = -10
        for r, c in get_empty(board):
            board[r][c] = ai_mark
            best = max(best, minimax(board, False, ai_mark, human_mark))
            board[r][c] = " "
        return best
    else:
        best = 10
        for r, c in get_empty(board):
            board[r][c] = human_mark
            best = min(best, minimax(board, True, ai_mark, human_mark))
            board[r][c] = " "
        return best


def computer_move_hard(board, ai_mark, human_mark):
    """Minimax — unbeatable AI."""
    best_score = -10
    best_move = None
    for r, c in get_empty(board):
        board[r][c] = ai_mark
        score = minimax(board, False, ai_mark, human_mark)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            best_move = (r, c)
    if best_move:
        r, c = best_move
        board[r][c] = ai_mark
        print(f"  🤖  Computer plays: row {r+1}, col {c+1}")


def play_game(mode):
    board = new_board()
    marks   = ["X", "O"]
    current = 0

    if mode == "1":
        names = {
            "X": input("  🧑  Enter Player 1 name (X): ").strip() or "Player 1",
            "O": input("  🧑  Enter Player 2 name (O): ").strip() or "Player 2",
        }
        ai_plays = None
    else:
        p_name = input("  🧑  Enter your name: ").strip() or "Player"
        names  = {"X": p_name, "O": "🤖 Computer"}
        ai_plays = "O"      # computer is always O

    print()
    print("  ── HOW TO PLAY: Enter row and column (1-3) ─")
    print("  ── Example: '2 3' = row 2, column 3 ────────")

    while True:
        print_board(board)
        mark = marks[current]
        name = names[mark]

        if ai_plays == mark:
            if mode == "2":
                computer_move_easy(board, mark)
            else:
                computer_move_hard(board, mark, "X")
        else:
            human_move(board, mark, name)

        if check_winner(board, mark):
            print_board(board)
            print(f"  🎉  {name} ({mark}) WINS! Congratulations!\n")
            return mark

        if is_full(board):
            print_board(board)
            print("  🤝  It's a DRAW! Well played both!\n")
            return "draw"

        current = 1 - current


def main():
    show_banner()
    score = {"X": 0, "O": 0, "draw": 0}

    while True:
        show_menu()
        mode = input("\n  👉  Select an option (1-4): ").strip()

        if mode in ("1", "2", "3"):
            result = play_game(mode)
            score[result] += 1

            print(f"  📊  Score  ➜  X: {score['X']}  |  O: {score['O']}  |  Draws: {score['draw']}")
            print()
            again = input("  [Enter] ➜ Play Again  |  [q] ➜ Main Menu\n  👉  ").strip().lower()
            if again != "q":
                continue
        elif mode == "4":
            print("\n  ════════════════════════════════════════")
            print("  🎮  Thanks for playing! Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Please select 1 to 4.\n")


if __name__ == "__main__":
    main()
