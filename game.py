import random
from logic import feedback


class Mastermind:
    def __init__(self):
        self.code = [str(random.randint(1, 6)) for _ in range(4)]
        self.history = []
        self.turns = 10
        self.game_over = False
        self.won = False
        self.quit = False

    def run(self):
        print("Mastermind — enter four digits from 1 to 6.")
        while not self.game_over and self.turns > 0:
            raw = input(f"{self.turns} turns left > ").strip()
            if raw.lower() == "q":
                self.game_over = True
                self.quit = True
                print("Game ended.")
                return
            if len(raw) != 4 or any(ch not in "123456" for ch in raw):
                print("Enter exactly four digits from 1 to 6.")
                continue

            guess = list(raw)
            exact, partial = feedback(self.code, guess)
            self.history.append((raw, exact, partial))
            self.turns -= 1
            print("Exact:", exact, " Partial:", partial)

            if exact == 4:
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
