from collections import Counter


def feedback(code, guess):
    exact = 0
    code_remaining = []
    guess_remaining = []

    for code_symbol, guess_symbol in zip(code, guess):
        if code_symbol == guess_symbol:
            exact += 1
        else:
            code_remaining.append(code_symbol)
            guess_remaining.append(guess_symbol)

    code_counts = Counter(code_remaining)
    guess_counts = Counter(guess_remaining)
    partial = sum(min(code_counts[symbol], guess_counts[symbol]) for symbol in code_counts)
    return exact, partial
