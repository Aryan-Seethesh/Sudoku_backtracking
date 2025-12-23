class SudokuSolver:
    def __init__(self, board):
        """
        board: 9x9 list of lists of integers (0-9). 0 means empty.
        """
        # Create a deep copy to avoid modifying the original list directly until we want to
        self.board = [row[:] for row in board]
        
    @staticmethod
    def is_valid_placement(board, row, col, num):
        """
        Check if placing num at board[row][col] is valid.
        board: 9x9 list of lists
        """
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
                
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
                
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
                    
        return True

    def is_valid(self, row, col, num):
        """
        Check if placing num at board[row][col] is valid.
        """
        return self.is_valid_placement(self.board, row, col, num)

    def solve_generator(self):
        """
        Generator function using backtracking to solve the Sudoku.
        Yields (row, col, num, type)
            type: 'try' (placing a number), 'revert' (backtracking/clearing), 'solved'
        """
        empty = self.find_empty()
        if not empty:
            yield (None, None, None, 'solved')
            return True

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                # Yield the placement action
                yield (row, col, num, 'try')

                # Recursively try to solve
                if (yield from self.solve_generator()):
                    return True

                # If we get here, it means the recursive path failed
                self.board[row][col] = 0
                # Yield the backtrack/revert action
                yield (row, col, 0, 'revert')

        return False

    def find_empty(self):
        """Finds an empty cell (represented by 0). Returns (row, col) or None."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
