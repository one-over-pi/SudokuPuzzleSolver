# Sudoku Solver

This Python code is a simple Sudoku solver that utilizes a backtracking algorithm to find the solution. Sudoku is a popular puzzle game where the objective is to fill a 9x9 grid with digits so that each column, each row, and each of the nine 3x3 subgrids contain all of the digits from 1 to 9.

## License

This code is licensed under the MIT License. See the LICENSE file for details.

## Methodology

The solver follows these main steps:

Create Sudoku Puzzle: The initial puzzle is a 9x9 grid with some cells already filled.

Solve Sudoku Puzzle: It iteratively attempts to fill in each empty cell with a valid digit until the entire puzzle is solved. The solving process involves checking each cell's row, column, and 3x3 subgrid for available numbers and choosing the appropriate number that fits.

Print Solved Sudoku: Once solved, the Sudoku puzzle is printed in a readable format, displaying each row of the grid.

## Methods

create_sudoku(): Creates a pre-made Sudoku puzzle.

clamp_index_to_row(index): Converts the Sudoku index to a row index.

clamp_index_to_column(index): Converts the Sudoku index to a column index.

return_row(index): Returns a row of the Sudoku grid.

return_column(index): Returns a column of the Sudoku grid.

return_grid(row_index, column_index): Returns the 3x3 grid from the Sudoku puzzle as a 9x1 list.

get_cell_with_potential_solutions(): Identifies an empty cell in the Sudoku puzzle and determines the possible values that can be placed in that cell without violating Sudoku rules. It returns the index of the cell along with a list of valid candidate values.

regenerate_sudoku_copy(): Updates a copy of the Sudoku puzzle grid based on the provided guess tree, which tracks the sequence of guesses made during the solving process. It ensures that the solver explores different solution paths while maintaining the integrity of previous guesses and solution attempts.

context_solve(index): Uses data from intersecting rows/columns and grids to logically deduce the missing number for a given cell.

solve_sudoku(): Iteratively solves the Sudoku puzzle using backtracking.

## Note

This solver uses a simple backtracking algorithm and may not be optimized for solving all Sudoku puzzles efficiently. It's intended for educational purposes and as a starting point for further exploration into Sudoku-solving algorithms. If the algorithm is unable to solve any cells, the program will still print what it was able to solve.

## Future Features

1. I will introduce the capability to randomly generate Sudoku puzzles with varying preset difficulties. There will be an option to select the desired level of challenge, ranging from easy to hard.
2. I will implement a more robust/elegant algorithm compared to the current one, using more of the sudoku meta rather than a trial and error approach.
