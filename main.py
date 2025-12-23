import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSlider, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QTimer, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QFont, QPalette, QColor
from solver import SudokuSolver

class SudokuCell(QLineEdit):
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setFixedSize(50, 50)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Arial", 20))
        self.setMaxLength(1)
        
        # Validator: Allow only digits 1-9
        regex = QRegularExpression("[1-9]")
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)
        
        
        # Styles
        self.base_style = """
            QLineEdit {
                border: 1px solid #ccc;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """
        self.setStyleSheet(self.base_style)

    def set_value(self, value):
        self.setText(str(value) if value != 0 else "")

    def get_value(self):
        text = self.text()
        return int(text) if text else 0

    def set_solving_style(self):
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                background-color: #f1c40f; /* Yellow focus */
                color: black;
            }
        """)

    def set_solved_style(self):
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                background-color: #2ecc71; /* Green success */
                color: white;
            }
        """)

    def set_backtrack_style(self):
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                background-color: #e74c3c; /* Red revert */
                color: white;
            }
        """)
        
    def reset_style(self):
        self.setStyleSheet(self.base_style)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver - Backtracking Visualization")
        self.setGeometry(100, 100, 600, 700)
        
        # Initialize
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.solver = None
        self.solve_generator = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_step)
        self.solving = False
        self.dark_mode = False
        self.step_counter = 0

        # UI Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Title
        title_label = QLabel("Sudoku Solver")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        main_layout.addWidget(title_label)

        # ------------------- Grid -------------------
        grid_container = QFrame()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setSpacing(0)
        
        for r in range(9):
            for c in range(9):
                cell = SudokuCell(r, c)
                self.cells[r][c] = cell
                cell.textEdited.connect(lambda text, row=r, col=c: self.validate_input(row, col, text))
                grid_layout.addWidget(cell, r, c)
                
                # Visual separation for 3x3 blocks
                # We can do this by adjusting margins or qss, 
                # but simplest QGridLayout spacing tricks are trickier.
                # Let's add thick borders via QSS to specific cells?
                # A simpler way is to just let the user see the grid.
                
                # Add heavy border to 3x3 blocks edges
                style = "QLineEdit { border: 1px solid #ccc; background-color: white; color: black; }"
                
                top = "1px" if r % 3 != 0 else "2px"
                left = "1px" if c % 3 != 0 else "2px"
                # bottom = "2px" if (r + 1) % 3 == 0 else "1px" # standard QLineEdit has implicit borders
                
                # Let's just trust basic grid first
        
        main_layout.addWidget(grid_container, alignment=Qt.AlignCenter)
        
        # ------------------- Controls -------------------
        controls_layout = QHBoxLayout()
        
        self.solve_btn = QPushButton("Solve")
        self.solve_btn.clicked.connect(self.start_solving)
        style_btn = """
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 10px 20px; 
                font-size: 16px; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """
        self.solve_btn.setStyleSheet(style_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_board)
        self.clear_btn.setStyleSheet(style_btn.replace("#3498db", "#e67e22").replace("#2980b9", "#d35400"))

        controls_layout.addWidget(self.solve_btn)
        controls_layout.addWidget(self.clear_btn)
        main_layout.addLayout(controls_layout)
        
        # Speed Slider
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50) # default
        self.speed_slider.valueChanged.connect(self.update_speed)
        
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.speed_slider)
        main_layout.addLayout(slider_layout)

        # Theme Toggle
        theme_layout = QHBoxLayout()
        self.theme_btn = QPushButton("Toggle Dark Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_btn)
        main_layout.addLayout(theme_layout)

        # Status & Step Counter
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Apply initial theme
        self.apply_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow { background-color: #2c3e50; }
                QLabel { color: #ecf0f1; }
                QFrame { background-color: #34495e; }
            """)
            self.theme_btn.setText("Switch to Light Mode")
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #ecf0f1; }
                QLabel { color: #2c3e50; }
                QFrame { background-color: white; }
            """)
            self.theme_btn.setText("Switch to Dark Mode")


    def get_board(self):
        board = []
        for r in range(9):
            row_vals = []
            for c in range(9):
                row_vals.append(self.cells[r][c].get_value())
            board.append(row_vals)
        return board

    def start_solving(self):
        if self.solving:
            return

        board = self.get_board()
        self.solver = SudokuSolver(board)
        self.solve_generator = self.solver.solve_generator()
        self.solving = True
        self.step_counter = 0
        self.status_label.setText("Solving...")
        self.solve_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        
        # Initial speed setup
        self.update_speed()
        self.timer.start()

    def update_speed(self):
        # 1 -> slowest (e.g. 500ms), 100 -> fastest (e.g. 1ms)
        # Invert logic: val 1 => 500ms, val 100 => 0ms ???
        # Better: Max speed = 1ms, Min speed = 200ms
        val = self.speed_slider.value()
        interval = max(1, 200 - val * 2) 
        self.timer.setInterval(interval)

    def update_step(self):
        try:
            step = next(self.solve_generator)
            self.step_counter += 1
            self.status_label.setText(f"Steps: {self.step_counter}")
            
            # Step unpacking: (row, col, num, type)
            row, col, num, type_ = step
            
            if type_ == 'solved':
                self.finish_solving(success=True)
                return
            
            # Update GUI
            cell = self.cells[row][col]
            if type_ == 'try':
                cell.set_value(num)
                cell.set_solving_style()
            elif type_ == 'revert':
                cell.set_value(0)
                cell.set_backtrack_style()

        except StopIteration:
            self.finish_solving(success=False)

    def validate_input(self, row, col, text):
        if not text:
            return

        try:
            num = int(text)
        except ValueError:
            return

        # Construct current board state
        # We need to act as if the current cell is empty to check validity of NEW number
        current_board = self.get_board()
        # The get_value() call inside get_board might return the new value if we are not careful.
        # However, textEdited triggers *after* the text is updated. 
        # So get_board() will contain 'num' at [row][col]. 
        # We must temporarily set it to 0 for validation purposes.
        current_board[row][col] = 0
        
        if not SudokuSolver.is_valid_placement(current_board, row, col, num):
            QMessageBox.warning(self, "Invalid Move", 
                                f"Placing {num} here violates Sudoku rules.\nPlease try a different number.")
            self.cells[row][col].set_value(0)


    def finish_solving(self, success):
        self.timer.stop()
        self.solving = False
        self.solve_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        
        if success:
            self.status_label.setText(f"Solved in {self.step_counter} steps!")
            QMessageBox.information(self, "Success", "Sudoku Solved!")
            # Reset styles to base or success
        else:
            self.status_label.setText("No Solution Found")
            QMessageBox.warning(self, "Failure", "No solution exists for this board.")

    def clear_board(self):
        self.timer.stop()
        self.solving = False
        for r in range(9):
            for c in range(9):
                self.cells[r][c].set_value(0)
                self.cells[r][c].reset_style()
        self.status_label.setText("Ready")
        self.step_counter = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
