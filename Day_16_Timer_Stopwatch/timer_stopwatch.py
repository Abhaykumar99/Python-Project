# Countdown Timer & Stopwatch ⏱️
# Concepts: time module, real-time output (\r), loops, datetime formatting

import time
import os


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║    ⏱️   TIMER  &  STOPWATCH   ⏱️       ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Countdown Timer                 │")
    print("  │   2  ➜  Stopwatch                       │")
    print("  │   3  ➜  Multi-Lap Stopwatch             │")
    print("  │   4  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def format_time(seconds):
    """Convert seconds → HH:MM:SS string."""
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_ms(seconds):
    """Convert seconds → MM:SS.mm string."""
    m  = int(seconds) // 60
    s  = int(seconds) % 60
    ms = int((seconds - int(seconds)) * 100)
    return f"{m:02d}:{s:02d}.{ms:02d}"


def get_duration():
    """Ask user for timer duration in HH MM SS format."""
    print("\n  Enter duration (press Enter to skip a field):")
    while True:
        try:
            h = input("    Hours   : ").strip()
            m = input("    Minutes : ").strip()
            s = input("    Seconds : ").strip()
            h = int(h) if h else 0
            m = int(m) if m else 0
            s = int(s) if s else 0
            total = h * 3600 + m * 60 + s
            if total <= 0:
                print("  ⚠️  Total time must be greater than 0.")
                continue
            return total
        except ValueError:
            print("  ⚠️  Enter whole numbers only.")


def countdown_timer():
    total = get_duration()
    label = format_time(total)
    print(f"\n  Starting countdown from {label}")
    print("  Press Ctrl+C to stop.\n")

    try:
        remaining = total
        while remaining >= 0:
            bar_done    = int(((total - remaining) / total) * 30)
            bar_left    = 30 - bar_done
            bar         = "[" + "#" * bar_done + "-" * bar_left + "]"
            time_str    = format_time(remaining)

            if remaining <= 10 and remaining > 0:
                urgency = " ⚠️  HURRY!"
            elif remaining == 0:
                urgency = ""
            else:
                urgency = ""

            print(f"\r  {bar}  {time_str}{urgency}   ", end="", flush=True)

            if remaining == 0:
                break
            time.sleep(1)
            remaining -= 1

        print("\n")
        print("  ╔════════════════════════════════════════╗")
        print("  ║       ⏰  TIME IS UP!  ⏰               ║")
        print("  ╚════════════════════════════════════════╝")
        # Beep 3 times using bell character
        for _ in range(3):
            print("\a", end="", flush=True)
            time.sleep(0.4)
        print()

    except KeyboardInterrupt:
        remaining_str = format_time(remaining)
        print(f"\n\n  ⛔  Timer stopped. Remaining: {remaining_str}\n")


def stopwatch():
    print("\n  Stopwatch started!")
    print("  Press Enter to STOP.\n")
    input("  Press Enter to START...")

    start = time.perf_counter()
    print("  Running...  (Press Enter to stop)\n")

    try:
        input()  # wait for Enter
    except KeyboardInterrupt:
        pass

    elapsed = time.perf_counter() - start
    print(f"\n  ✅  Elapsed Time : {format_ms(elapsed)}")
    print(f"      ({elapsed:.4f} seconds total)\n")


def multi_lap_stopwatch():
    print("\n  Multi-Lap Stopwatch")
    print("  Press Enter to START, then Enter to LAP/STOP, Ctrl+C to cancel.\n")
    input("  Press Enter to START...")

    start     = time.perf_counter()
    lap_start = start
    laps      = []

    print("  Running! Press Enter for each lap, then one more time to stop.\n")

    lap_num = 1
    while True:
        try:
            input()
        except KeyboardInterrupt:
            break

        now      = time.perf_counter()
        lap_time = now - lap_start
        total    = now - start
        laps.append((lap_num, lap_time, total))
        print(f"  Lap {lap_num:>2}  |  Lap: {format_ms(lap_time)}  |  Total: {format_ms(total)}")

        stop = input("  [Enter] = Next Lap  |  [s] = Stop: ").strip().lower()
        if stop == "s":
            break

        lap_start = now
        lap_num  += 1

    # Summary
    if laps:
        print(f"\n  ── Lap Summary ──────────────────────────")
        print(f"  {'Lap':<6}  {'Lap Time':<14}  {'Total Time'}")
        print(f"  {'─'*6}  {'─'*14}  {'─'*12}")
        for num, lap, total in laps:
            print(f"  {num:<6}  {format_ms(lap):<14}  {format_ms(total)}")

        lap_times = [l[1] for l in laps]
        print(f"\n  Fastest lap : Lap {min(range(len(lap_times)), key=lambda i: lap_times[i]) + 1}  ({format_ms(min(lap_times))})")
        print(f"  Slowest lap : Lap {max(range(len(lap_times)), key=lambda i: lap_times[i]) + 1}  ({format_ms(max(lap_times))})")
    print()


def main():
    show_banner()
    while True:
        show_menu()
        choice = input("\n  👉  Select (1-4): ").strip()

        if choice == "1":
            countdown_timer()
        elif choice == "2":
            stopwatch()
        elif choice == "3":
            multi_lap_stopwatch()
        elif choice == "4":
            print("\n  ════════════════════════════════════════")
            print("  ⏱️  Time well spent! Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Select 1 to 4.\n")


if __name__ == "__main__":
    main()
