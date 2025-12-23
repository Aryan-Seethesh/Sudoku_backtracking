🧩 Sudoku Solver with Backtracking Visualization

A Python-based desktop application that solves any valid 9×9 Sudoku puzzle using the Backtracking algorithm, with step-by-step visualisation to demonstrate how the algorithm works.

📌 Features

Solves any valid 9×9 Sudoku using recursive backtracking

Step-by-step visual animation of the solving process

Interactive GUI built with PySide6 (Qt)

Input validation to prevent invalid Sudoku entries

Adjustable solving speed for better visualization

Clean and modular code structure

🧠 Algorithm Used

The solver uses the Backtracking algorithm, which:

Finds an empty cell

Tries valid numbers (1–9)

Recursively proceeds if valid

Backtracks when a dead-end is reached

This approach guarantees a solution for any valid Sudoku.

⚙️ Tech Stack

Language: Python

GUI Framework: PySide6 (Qt)

Core Concepts:

Recursion

Backtracking

Constraint checking

Timers for animation

🚀 Performance

Solves typical valid 9×9 Sudoku puzzles in under one second

Visualization speed can be adjusted for learning purposes

📂 Project Structure
.
├── main.py        # Application entry point & GUI logic
├── solver.py      # Backtracking Sudoku solver logic
├── requirements.txt

▶️ How to Run

Install dependencies:

pip install -r requirements.txt


Run the application:

python main.py

🎯 Learning Outcomes

Practical implementation of backtracking and recursion

Understanding how algorithms behave step-by-step

Building interactive desktop applications with Qt

Writing clean, modular, and readable Python code

📌 Future Improvements

Support for different grid sizes (e.g., 4×4, 16×16)

Option to generate Sudoku puzzles

Performance optimizations for visualization
