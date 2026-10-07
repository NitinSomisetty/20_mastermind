import random
from logic import feedback


class Mastermind:
    # Task 3: each difficulty changes the code length, symbols, and turn limit.
    DIFFICULTIES = {
        "easy": {"length": 4, "symbols": "123456", "turns": 10},
        "medium": {"length": 5, "symbols": "12345678", "turns": 12},
        "hard": {"length": 6, "symbols": "123456789", "turns": 15},
    }

    def __init__(self, difficulty="easy"):
        self.difficulty = self._resolve_difficulty(difficulty)
        self.code_length = self.DIFFICULTIES[self.difficulty]["length"]
        self.symbols = self.DIFFICULTIES[self.difficulty]["symbols"]
        self.code = [random.choice(self.symbols) for _ in range(self.code_length)]
        self.history = []
        self.turns = self.DIFFICULTIES[self.difficulty]["turns"]
        self.game_over = False
        self.won = False
        self.quit = False

    def _show_history(self):
        # Task 4: display only accepted guesses and their feedback.
        if not self.history:
            print("Guess history: none")
            return
        print("Guess history:")
        for index, (guess, exact, partial) in enumerate(self.history, start=1):
            print(f"  {index}. {guess} -> exact={exact}, partial={partial}")

    @classmethod
    def _resolve_difficulty(cls, difficulty):
        if difficulty is None:
            return "easy"
        key = str(difficulty).strip().lower()
        if key in cls.DIFFICULTIES:
            return key
        if key in {"1", "e", "easy"}:
            return "easy"
        if key in {"2", "m", "medium"}:
            return "medium"
        if key in {"3", "h", "hard"}:
            return "hard"
        raise ValueError(f"Unknown difficulty: {difficulty}")

    def select_difficulty(self):
        print("Difficulty choices: 1) Easy  2) Medium  3) Hard")
        while True:
            choice = input("Select difficulty > ").strip().lower()
            try:
                self.difficulty = self._resolve_difficulty(choice)
                self.code_length = self.DIFFICULTIES[self.difficulty]["length"]
                self.symbols = self.DIFFICULTIES[self.difficulty]["symbols"]
                self.code = [random.choice(self.symbols) for _ in range(self.code_length)]
                self.history = []
                self.turns = self.DIFFICULTIES[self.difficulty]["turns"]
                # Reset lifecycle state when a new difficulty is selected.
                self.game_over = False
                self.won = False
                self.quit = False
                return
            except ValueError:
                print("Choose 1, 2, 3, easy, medium, or hard.")

    def _print_rules(self):
        first, last = self.symbols[0], self.symbols[-1]
        print(
            f"Mastermind — enter {self.code_length} digits from {first} to {last}."
        )

    def run(self):
        self.select_difficulty()
        self._print_rules()
        self._show_history()
        while not self.game_over and self.turns > 0:
            raw = input(f"{self.turns} turns left > ").strip()
            if raw.lower() == "q":
                # Task 2: quitting ends the game without consuming a turn.
                self.game_over = True
                self.quit = True
                print("Game ended.")
                return

            first, last = self.symbols[0], self.symbols[-1]
            if len(raw) != self.code_length or any(ch not in self.symbols for ch in raw):
                # Task 4: reject malformed guesses before changing history or turns.
                print(f"Invalid guess. Enter exactly {self.code_length} digits from {first} to {last}.")
                self._show_history()
                continue

            guess = list(raw)
            exact, partial = feedback(self.code, guess)
            self.history.append((raw, exact, partial))
            self.turns -= 1
            print("Exact:", exact, " Partial:", partial)
            self._show_history()

            if exact == self.code_length:
                # Task 2: mark a win immediately, including on the final turn.
                self.won = True
                self.game_over = True
                print("Cracked the code!")
                return

            if self.turns == 0:
                # Task 2: reaching zero turns without a win is a loss.
                self.won = False
                self.game_over = True
                print("You ran out of turns!")
                print("The code was", "".join(self.code))
                return

        if self.game_over and not self.won and not self.quit:
            print("The code was", "".join(self.code))
