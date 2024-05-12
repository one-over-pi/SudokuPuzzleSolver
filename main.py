class SudokuSolver:
    def __init__(self):
        # Create sudoku to solve
        self.sudoku = self.create_sudoku()

        # Solve the sudoku puzzle
        self.solve_sudoku()
        
        # Print the solved sudoku in a line-by-line format (easier to read)
        for i in self.sudoku:
            print(i)

    def create_sudoku(self):
        # Pre-made sudoku puzzle
        return [
            [None, None,    5, None, None, None, None,    4, None],
            [None, None,    4, None, None,    3,    5, None,    8],
            [None,    6,    8, None, None,   4 ,    3, None,    1],
            [None, None, None,    6,    8, None, None,    3, None],
            [None, None,    2, None, None, None,    8, None, None],
            [None,    3, None, None,    2,    9, None, None, None],
            [   5, None,    7,    2, None, None,    1,    8, None],
            [   6, None,    9,    5, None, None,    4, None, None],
            [None,    8, None, None, None, None,    2, None, None]
        ]
    
    def clamp_index_to_row(self, index):
        # Converts the sudoku index into row index
        # A value from 0-8 representing each line of the 9x9 puzzle
        for i in range(9):
            if index < (9*(i+1)):
                return i
        
    def clamp_index_to_column(self, index):
        # Converts the sudoku index into column index
        # A value from 0-8 representing each column of the 9x9 puzzle
        return (index % 9)
    
    def return_row(self, index):
        # Return a row of the sudoku
        return self.sudoku[index]
    
    def return_column(self, index):
        # Return a column of the sudoku
        return [self.sudoku[i][index] for i in range(9)]
    
    def return_grid(self, row_index, column_index):
        # Return the 3x3 grid from the sudoku puzzle in the form of a 9x1 list

        # Converts row_index into left-most square of that 3x3 grid that the row_index is present in
        if row_index < 3:
            row_index = 0
        elif row_index < 6:
            row_index = 3
        else:
            row_index = 6

        # Converts column_index into top-most square of that 3x3 grid that the column_index is present in
        if column_index < 3:
            column_index = 0
        elif column_index < 6:
            column_index = 3
        else:
            column_index = 6

        # Populate grid with relevant values
        grid = []
        for i in range(3):
            for j in range(3):
                grid.append(self.sudoku[row_index + i][column_index + j])
        return grid
        

    def context_solve(self, index):
        # Use data from intersecting rows/columns and grids the line we are trying to solve is a part of
        # Looking at a particular index, we can check intersecting groups and what numbers they have, leading to a logical conclusion of what number has not been used
        row_index = self.clamp_index_to_row(index)
        column_index = self.clamp_index_to_column(index)

        row = self.return_row(row_index)
        column = self.return_column(column_index)
        grid = self.return_grid(row_index, column_index)

        # Save which number have occured in the row, column, and grid we are working on
        occurance = [False for _ in range(9)]
        for item in row + column + grid:
            if item != None:
                occurance[item - 1] = True
        if occurance.count(False) == 1:
            # Return the missing value
            return occurance.index(False) + 1
        else:
            # Otherwise return None
            return None
        
    def solve_sudoku(self):
        solved_tile = True
        iterations = 0
        while solved_tile:
            iterations += 1
            solved_tile = False
            for row in range(9):
                for column in range(9):
                    if self.sudoku[row][column] == None:
                        solution = self.context_solve((row*9)+column)
                        if solution != None:
                            self.sudoku[row][column] = solution
                            solved_tile = True
        print("Iterations to solve = " + str(iterations))
    
sudoku_solver = SudokuSolver()
