import random
from logic import feedback


class Mastermind:
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
        while not self.game_over and self.turns > 0:
            raw = input(f"{self.turns} turns left > ").strip()
            if raw.lower() == "q":
                self.game_over = True
                self.quit = True
                print("Game ended.")
                return

            first, last = self.symbols[0], self.symbols[-1]
            if len(raw) != self.code_length or any(ch not in self.symbols for ch in raw):
                print(f"Enter exactly {self.code_length} digits from {first} to {last}.")
                continue

            guess = list(raw)
            exact, partial = feedback(self.code, guess)
            self.history.append((raw, exact, partial))
            self.turns -= 1
            print("Exact:", exact, " Partial:", partial)

            if exact == self.code_length:
                self.won = True
                self.game_over = True
                print("Cracked the code!")
                return

            if self.turns == 0:
                self.won = False
                self.game_over = True
                print("You ran out of turns!")
                print("The code was", "".join(self.code))
                return

        if self.game_over and not self.won and not self.quit:
            print("The code was", "".join(self.code))
