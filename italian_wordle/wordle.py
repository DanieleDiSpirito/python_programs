import random
import tkinter as tk
from tkinter import messagebox
import os


class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle - Italian Edition")
        self.root.resizable(False, False)
        self.COLOR_CORRECT = "#6aaa64"  # green
        self.COLOR_PRESENT = "#c9b458"  # yellow
        self.COLOR_ABSENT  = "#787c7e"   # gray
        self.COLOR_EMPTY   = "#1a1a1a"    # black
        self.COLOR_BORDER  = "#3a3a3c"   # dark gray
        self.words = set()
        self.word = ''
        self.attempts = []
        self.attempt_colors = []
        self.current_attempt = ""
        self.attempt_number = 0
        self.game_over = False
        self.won = False
        self.font = "8514oem"
        self.load_word()
        self.create_gui()
        
    def load_word(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'five_char_words.italian.txt')
        with open(file_path) as file_:
            lines = file_.readlines()
            self.word = random.choice(lines).strip().upper()
            self.words = set([line.strip().upper() for line in lines])
    
    def word_exists(self, word):
        return word.upper() in self.words
    
    def get_colors(self, attempt):
        colors = [self.COLOR_ABSENT] * 5
        word_chars = list(self.word)
        for i in range(5):
            if attempt[i] == word_chars[i]:
                colors[i] = self.COLOR_CORRECT
                word_chars[i] = None
        for i in range(5):
            if colors[i] == self.COLOR_ABSENT and attempt[i] in word_chars:
                colors[i] = self.COLOR_PRESENT
                word_chars[word_chars.index(attempt[i])] = None
        return colors
    
    def create_gui(self):
        main_frame = tk.Frame(self.root, bg="#121213")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        title = tk.Label(main_frame, text="WORDLE", font=(self.font, 28, "bold"), 
                        fg="white", bg="#121213")
        title.pack(pady=(10, 20))
        self.board_frame = tk.Frame(main_frame, bg="#121213")
        self.board_frame.pack(pady=10)
        self.tiles = []
        for row in range(6):
            row_tiles = []
            for col in range(5):
                tile = tk.Label(self.board_frame, text="", font=(self.font, 24, "bold"),
                              width=4, height=2, bg=self.COLOR_EMPTY, fg="white",
                              relief=tk.SOLID, borderwidth=2, bd=2)
                tile.grid(row=row, column=col, padx=2, pady=2)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)
        input_frame = tk.Frame(main_frame, bg="#121213")
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Inserisci la parola:", font=self.font,
                fg="white", bg="#121213").pack(anchor=tk.W)
        self.input_var = tk.StringVar()
        self.input_var.trace("w", self.on_input_change)
        input_entry = tk.Entry(input_frame, textvariable=self.input_var, 
                              font=(self.font, 16), width=5, 
                              bg="#3a3a3c", fg="white", justify=tk.CENTER)
        input_entry.pack(pady=10)
        input_entry.focus()
        button_frame = tk.Frame(main_frame, bg="#121213")
        button_frame.pack(pady=0)
        submit_btn = tk.Button(button_frame, text="Invia", command=self.submit_guess,
                              font=(self.font, 12), bg="#6aaa64", fg="white", padx=20)
        submit_btn.pack(side=tk.LEFT, padx=5)
        reset_btn = tk.Button(button_frame, text="Nuova Partita", command=self.reset_game,
                             font=(self.font, 12), bg="#3a3a3c", fg="white", padx=20)
        reset_btn.pack(side=tk.LEFT, padx=5)
        self.status_label = tk.Label(main_frame, text="", font=(self.font, 12),
                                     fg="white", bg="#121213")
        self.status_label.pack(pady=10)
    
    def on_input_change(self, *args):
        value = self.input_var.get().upper()
        value = ''.join(c for c in value if c.isalpha())[:5]
        if value != self.input_var.get():
            self.input_var.set(value)
    
    def submit_guess(self):
        if self.game_over:
            return
        attempt = self.input_var.get().upper()
        if len(attempt) != 5:
            messagebox.showerror("Errore", "La parola deve avere 5 lettere!")
            return
        if not self.word_exists(attempt):
            messagebox.showerror("Errore", "La parola non esiste nel dizionario!")
            return
        self.attempts.append(attempt)
        colors = self.get_colors(attempt)
        self.attempt_colors.append(colors)
        self.update_board()
        if attempt == self.word:
            self.game_over = True
            self.won = True
            self.status_label.config(text="Congratulazioni! Hai indovinato!", fg="#6aaa64")
            messagebox.showinfo("Vittoria!", f"Hai indovinato la parola: {self.word}\nTentativi: {len(self.attempts)}")
            return
        self.attempt_number += 1
        if self.attempt_number >= 6:
            self.game_over = True
            self.status_label.config(text=f"Hai perso! La parola era: {self.word}", fg="#ff6b6b")
            messagebox.showinfo("Sconfitta", f"La parola era: {self.word}")
            return
        remaining = 6 - self.attempt_number
        self.status_label.config(text=f"Tentativi rimasti: {remaining}", fg="white")
        self.input_var.set("")
    
    def update_board(self):
        for row_idx, (attempt, colors) in enumerate(zip(self.attempts, self.attempt_colors)):
            for col_idx, (letter, color) in enumerate(zip(attempt, colors)):
                tile = self.tiles[row_idx][col_idx]
                tile.config(text=letter.upper(), bg=color)
    
    def reset_game(self):
        self.word = ''
        self.attempts = []
        self.attempt_colors = []
        self.current_attempt = ""
        self.attempt_number = 0
        self.game_over = False
        self.won = False 
        self.load_word()
        for row in self.tiles:
            for tile in row:
                tile.config(text="", bg=self.COLOR_EMPTY)
        self.input_var.set("")
        self.status_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()




