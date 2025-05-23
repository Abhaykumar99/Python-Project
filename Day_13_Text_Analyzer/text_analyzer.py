# Word Counter & Text Analyzer 📊
# Concepts: String methods, Collections (Counter), File I/O, RegEx, Statistics

import re
import os
from collections import Counter


STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "was", "are", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "shall", "can",
    "not", "no", "nor", "so", "yet", "both", "either", "this", "that",
    "it", "its", "as", "if", "then", "than", "i", "we", "you", "he",
    "she", "they", "my", "your", "his", "her", "our", "their", "me",
    "him", "us", "them", "what", "which", "who", "whom", "how", "when",
    "where", "why", "all", "each", "every", "s", "t", "just", "about",
}


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║   📊  WORD COUNTER & TEXT ANALYZER 📊  ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Analyze Typed Text              │")
    print("  │   2  ➜  Analyze a .txt File             │")
    print("  │   3  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def get_text_from_input():
    print("\n  📝  Type or paste your text below.")
    print("  (Type 'END' on a new line when done)\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def get_text_from_file():
    path = input("\n  📂  Enter file path (.txt): ").strip().strip('"')
    if not os.path.exists(path):
        print(f"  ❌  File not found: {path}\n")
        return None
    if not path.lower().endswith(".txt"):
        print("  ⚠️  Only .txt files are supported.\n")
        return None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_words(text):
    """Return all words (lowercase, letters only)."""
    return re.findall(r"[a-zA-Z]+", text.lower())


def extract_sentences(text):
    """Split on . ! ? as sentence boundaries."""
    sentences = re.split(r"[.!?]+", text)
    return [s.strip() for s in sentences if s.strip()]


def analyze(text):
    words      = extract_words(text)
    sentences  = extract_sentences(text)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    total_words      = len(words)
    unique_words     = len(set(words))
    total_chars      = len(text)
    total_chars_nsp  = len(text.replace(" ", "").replace("\n", ""))
    total_sentences  = len(sentences)
    total_paragraphs = max(len(paragraphs), 1)

    avg_word_len = (sum(len(w) for w in words) / total_words) if total_words else 0
    avg_sent_len = (total_words / total_sentences) if total_sentences else 0

    # Reading time: ~200 words/min average
    read_minutes = total_words / 200
    read_seconds = read_minutes * 60

    # Keyword freq — exclude stop words
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    top_words = Counter(words).most_common(10)
    top_keywords = Counter(keywords).most_common(10)

    return {
        "total_words":      total_words,
        "unique_words":     unique_words,
        "total_chars":      total_chars,
        "total_chars_nsp":  total_chars_nsp,
        "total_sentences":  total_sentences,
        "total_paragraphs": total_paragraphs,
        "avg_word_len":     avg_word_len,
        "avg_sent_len":     avg_sent_len,
        "read_minutes":     read_minutes,
        "read_seconds":     read_seconds,
        "top_words":        top_words,
        "top_keywords":     top_keywords,
    }


def display_results(stats):
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║            📊 ANALYSIS RESULTS         ║")
    print("  ╚════════════════════════════════════════╝")

    print()
    print("  ── General Stats ────────────────────────")
    print(f"  📝  Total Words        : {stats['total_words']:,}")
    print(f"  🔤  Unique Words       : {stats['unique_words']:,}")
    print(f"  🔡  Total Characters   : {stats['total_chars']:,}  (with spaces)")
    print(f"  🔡  Total Characters   : {stats['total_chars_nsp']:,}  (no spaces)")
    print(f"  📄  Sentences          : {stats['total_sentences']:,}")
    print(f"  📃  Paragraphs         : {stats['total_paragraphs']:,}")

    print()
    print("  ── Readability ──────────────────────────")
    print(f"  📏  Avg Word Length    : {stats['avg_word_len']:.1f} characters")
    print(f"  📐  Avg Sentence Length: {stats['avg_sent_len']:.1f} words")
    if stats['read_seconds'] < 60:
        read_str = f"{stats['read_seconds']:.0f} seconds"
    else:
        read_str = f"{stats['read_minutes']:.1f} min ({stats['read_seconds']:.0f}s)"
    print(f"  ⏱️  Est. Reading Time  : {read_str}  (~200 wpm)")

    print()
    print("  ── Top 10 Words ─────────────────────────")
    _print_freq_chart(stats["top_words"])

    print()
    print("  ── Top 10 Keywords (stop words removed) ─")
    _print_freq_chart(stats["top_keywords"])
    print()


def _print_freq_chart(word_freq):
    if not word_freq:
        print("  📭  No words found.")
        return
    max_count = word_freq[0][1]
    for word, count in word_freq:
        bar_len = int((count / max_count) * 20)
        bar = "#" * bar_len
        print(f"  {word:<18}  {count:>4}  {bar}")


def main():
    show_banner()

    while True:
        show_menu()
        choice = input("\n  👉  Select (1-3): ").strip()

        if choice == "1":
            text = get_text_from_input()
            if not text.strip():
                print("  ⚠️  No text entered.\n")
                continue
            stats = analyze(text)
            display_results(stats)

        elif choice == "2":
            text = get_text_from_file()
            if text is None:
                continue
            if not text.strip():
                print("  ⚠️  File is empty.\n")
                continue
            stats = analyze(text)
            display_results(stats)

        elif choice == "3":
            print("\n  ════════════════════════════════════════")
            print("  📊  Thanks for using Text Analyzer! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Select 1 to 3.\n")


if __name__ == "__main__":
    main()
