from collections import Counter


def feedback(code, guess):
    exact = 0
    code_remaining = []
    guess_remaining = []

    # Task 1: resolve exact matches first so each code position is used once.
    for code_symbol, guess_symbol in zip(code, guess):
        if code_symbol == guess_symbol:
            exact += 1
        else:
            code_remaining.append(code_symbol)
            guess_remaining.append(guess_symbol)

    # Task 1: count only the available unmatched occurrences for partial matches.
    code_counts = Counter(code_remaining)
    guess_counts = Counter(guess_remaining)
    partial = sum(min(code_counts[symbol], guess_counts[symbol]) for symbol in code_counts)
    return exact, partial
