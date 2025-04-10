import tkinter as tk
from tkinter import messagebox
import sqlite3

# Sample Questions and Answers
questions = [
    "What is the capital of France?",
    "Which language is used for web apps?",
    "Who developed Python?",
    "What does CPU stand for?",
    "Which one is a Python framework?"
]

options = [
    ["Paris", "London", "Berlin", "Madrid"],
    ["Python", "Java", "HTML", "All of the above"],
    ["Guido van Rossum", "Dennis Ritchie", "James Gosling", "Bjarne Stroustrup"],
    ["Central Processing Unit", "Computer Personal Unit", "Central Power Unit", "Control Processing Unit"],
    ["Django", "React", "Angular", "Laravel"]
]

answers = [0, 0, 0, 0, 0]  # 0-indexed correct answers

# Database setup
def init_db():
    conn = sqlite3.connect("quiz_scores.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Main Quiz Class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App with Database")
        self.root.geometry("500x400")

        self.q_no = 0
        self.score = 0
        self.username = tk.StringVar()
        self.selected_option = tk.IntVar()

        self.create_user_input()

    def create_user_input(self):
        """Initial screen for username entry."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter your name:", font=("Arial", 14)).pack(pady=20)
        tk.Entry(self.root, textvariable=self.username, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz, font=("Arial", 12)).pack(pady=20)

    def start_quiz(self):
        if self.username.get().strip() == "":
            messagebox.showwarning("Input Error", "Please enter your name.")
            return

        self.show_question()

    def show_question(self):
        """Displays the current question and options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.selected_option.set(-1)

        tk.Label(self.root, text=f"Q{self.q_no + 1}: {questions[self.q_no]}", font=("Arial", 14), wraplength=450, justify="left").pack(pady=20)

        self.radio_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.root, text=options[self.q_no][i], variable=self.selected_option, value=i, font=("Arial", 12))
            btn.pack(anchor="w", padx=20)
            self.radio_buttons.append(btn)

        tk.Button(self.root, text="Next", command=self.next_question, font=("Arial", 12)).pack(pady=20)

    def next_question(self):
        """Handles answer checking and moves to next question or result."""
        selected = self.selected_option.get()
        if selected == -1:
            messagebox.showwarning("Warning", "Please select an option.")
            return

        if selected == answers[self.q_no]:
            self.score += 1

        self.q_no += 1

        if self.q_no == len(questions):
            self.save_score()
            self.show_result()
        else:
            self.show_question()

    def save_score(self):
        """Saves the username and score to the database."""
        conn = sqlite3.connect("quiz_scores.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (self.username.get(), self.score))
        conn.commit()
        conn.close()

    def show_result(self):
        """Displays the final result."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Thanks for playing, {self.username.get()}!", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text=f"Your final score is: {self.score} out of {len(questions)}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Play Again", command=self.reset_quiz, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 12)).pack(pady=5)

    def reset_quiz(self):
        """Resets the quiz to play again."""
        self.q_no = 0
        self.score = 0
        self.username.set("")
        self.create_user_input()

# Main Execution
if __name__ == "__main__":
    init_db()  # Initialize database
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
