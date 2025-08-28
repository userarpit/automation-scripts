import tkinter as tk
import random
from functools import partial

# ---------- Game Config ----------
HUMAN = 'X'
AI = 'O'
DIFFICULTIES = ["Easy", "Medium", "Hard"]

# ---------- Core Game Logic ----------
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]

def check_winner(board):
    """Return 'X' or 'O' if someone won, 'Draw' if full, or None if ongoing."""
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return "Draw"
    return None

def available_moves(board):
    return [i for i, v in enumerate(board) if not v]

def minimax(board, is_maximizing, alpha, beta):
    """
    Alpha-beta minimax for optimal play.
    Returns (score, move). AI maximizes, Human minimizes.
    Score convention: AI win=+1, Human win=-1, Draw=0
    """
    result = check_winner(board)
    if result == AI:    return (1, None)
    if result == HUMAN: return (-1, None)
    if result == "Draw":return (0, None)

    best_move = None
    if is_maximizing:
        best_score = -2  # less than min possible
        for m in available_moves(board):
            board[m] = AI
            score, _ = minimax(board, False, alpha, beta)
            board[m] = None
            if score > best_score:
                best_score, best_move = score, m
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = 2  # greater than max possible
        for m in available_moves(board):
            board[m] = HUMAN
            score, _ = minimax(board, True, alpha, beta)
            board[m] = None
            if score < best_score:
                best_score, best_move = score, m
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move

# ---------- UI App ----------
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe (You vs Computer)")
        self.root.resizable(False, False)

        self.board = [None] * 9
        self.buttons = []
        self.game_over = False
        self.human_score = 0
        self.ai_score = 0
        self.draws = 0
        self.current_player = HUMAN  # X starts by default

        # Top bar: difficulty + reset + score
        top = tk.Frame(root, padx=10, pady=10)
        top.grid(row=0, column=0, sticky="ew")

        tk.Label(top, text="Difficulty:").pack(side="left")
        self.difficulty_var = tk.StringVar(value="Hard")
        tk.OptionMenu(top, self.difficulty_var, *DIFFICULTIES).pack(side="left", padx=(5, 15))

        tk.Button(top, text="Reset Game", command=self.reset_board).pack(side="left")

        self.score_var = tk.StringVar()
        self.update_score_label()
        tk.Label(top, textvariable=self.score_var, font=("Arial", 11, "bold")).pack(side="right")

        # Status label
        self.status_var = tk.StringVar(value="Your turn (X)")
        tk.Label(root, textvariable=self.status_var, font=("Arial", 12), pady=5).grid(row=1, column=0)

        # Board grid
        board_frame = tk.Frame(root, padx=10, pady=10)
        board_frame.grid(row=2, column=0)

        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                width=6, height=3,
                font=("Arial", 20, "bold"),
                command=partial(self.handle_click, i)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Start with human turn (X)
        self.set_status()

    # ----- Helpers -----
    def update_score_label(self):
        self.score_var.set(f"Score  You (X): {self.human_score}   Computer (O): {self.ai_score}   Draws: {self.draws}")

    def set_status(self, msg=None):
        if msg:
            self.status_var.set(msg)
        elif self.game_over:
            result = check_winner(self.board)
            if result == HUMAN:
                self.status_var.set("You win! 🎉")
            elif result == AI:
                self.status_var.set("Computer wins! 🤖")
            else:
                self.status_var.set("It's a draw.")
        else:
            if self.current_player == HUMAN:
                self.status_var.set("Your turn (X)")
            else:
                self.status_var.set("Computer thinking… (O)")

    def end_game_if_over(self):
        result = check_winner(self.board)
        if result:
            self.game_over = True
            if result == HUMAN:
                self.human_score += 1
            elif result == AI:
                self.ai_score += 1
            else:
                self.draws += 1
            self.update_score_label()
            self.set_status()
            self.disable_all()
            return True
        return False

    def disable_all(self):
        for b in self.buttons:
            b.config(state="disabled")

    def enable_empty(self):
        for i, b in enumerate(self.buttons):
            if self.board[i] is None:
                b.config(state="normal")

    # ----- Actions -----
    def handle_click(self, idx):
        if self.game_over or self.board[idx] is not None or self.current_player != HUMAN:
            return
        self.make_move(idx, HUMAN)
        if self.end_game_if_over():
            return
        self.current_player = AI
        self.set_status()
        # Give a tiny delay so UI updates before AI moves
        self.root.after(250, self.computer_move)

    def make_move(self, idx, player):
        self.board[idx] = player
        self.buttons[idx].config(text=player, state="disabled")

    def computer_move(self):
        if self.game_over:
            return

        move = self.choose_ai_move()
        if move is not None:
            self.make_move(move, AI)

        if self.end_game_if_over():
            return

        self.current_player = HUMAN
        self.set_status()
        self.enable_empty()

    def choose_ai_move(self):
        difficulty = self.difficulty_var.get()

        moves = available_moves(self.board)
        if not moves:
            return None

        if difficulty == "Easy":
            # Random legal move
            return random.choice(moves)

        if difficulty == "Medium":
            # 60% best move, 40% random
            if random.random() < 0.6:
                _, best = minimax(self.board, True, -2, 2)
                return best if best is not None else random.choice(moves)
            else:
                return random.choice(moves)

        # Hard: pure minimax (optimal)
        _, best = minimax(self.board, True, -2, 2)
        return best if best is not None else random.choice(moves)

    def reset_board(self):
        self.board = [None] * 9
        self.game_over = False
        self.current_player = HUMAN  # Human starts each round; change here if you want alternation
        for b in self.buttons:
            b.config(text="", state="normal")
        self.set_status()

# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
