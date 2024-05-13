class SudokuSolver:
    def __init__(self):
        
        # Create sudoku to solve
        self.sudoku = self.create_sudoku()

        # Create a copy of self.sudoku_copy
        self.regenerate_sudoku_copy([])

        # Solve the sudoku puzzle
        self.solve_sudoku()
        
        # Print the unsolved sudoku in a line-by-line format (easier to read)
        for i in self.sudoku:
            print(i)
        
        print()

        # Do the same for the solved sudoku
        for i in self.sudoku_copy:
            print(i)

    def create_sudoku(self):
        
        # Pre-made sudoku puzzle
        return [
            [8, None, None, None, None, None, None, None, None],
            [None, None, 3, 6, None, None, None, None, None],
            [None, 7, None, None, 9, None, 2, None, None],
            [None, 5, None, None, None, 7, None, None, None],
            [None, None, None, None, 4, 5, 7, None, None],
            [None, None, None, 1, None, None, None, 3, None],
            [None, None, 1, None, None, None, None, 6, 8],
            [None, None, 8, 5, None, None, None, 1, None],
            [None, 9, None, None, None, None, 4, None, None]
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
        return self.sudoku_copy[index]
    
    def return_column(self, index):
        
        # Return a column of the sudoku
        return [self.sudoku_copy[i][index] for i in range(9)]
    
    def return_grid(self, row_index, column_index):
        
        # Return the 3x3 grid from the sudoku puzzle in the form of a 9x1 list

        # Converts row_index into left-most cell of that 3x3 grid that the row_index is present in
        if row_index < 3:
            row_index = 0
        elif row_index < 6:
            row_index = 3
        else:
            row_index = 6

        # Converts column_index into top-most cell of that 3x3 grid that the column_index is present in
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
                grid.append(self.sudoku_copy[row_index + i][column_index + j])
        
        # Return populated grid
        return grid
        

    def context_solve(self, index):
        
        # Use data from intersecting rows/columns and grids the line we are trying to solve
        # is a part of Looking at a particular index, we can check intersecting groups and
        # what numbers they have, leading to a logical conclusion of what number has not been used
        
        # Get row and column index
        row_index = self.clamp_index_to_row(index)
        column_index = self.clamp_index_to_column(index)

        # Get row, column, and grid cells
        row = self.return_row(row_index)
        column = self.return_column(column_index)
        grid = self.return_grid(row_index, column_index)

        # Save which numbers have occurred in the row, column, and grid we are working on
        occurrence = [False for _ in range(9)]
        for item in row + column + grid:
            if item != None:
                occurrence[item - 1] = True

        # If there is only one value that we didn't find, that must be the missing value for the cell we are trying to calculate
        if occurrence.count(False) == 1:
            # Return the missing value
            return occurrence.index(False) + 1
        else:
            # Otherwise return None
            return None
        
    def get_cell_with_potential_solutions(self, index):
        
        # If the index is not provided, find the best value to predict
        if index == None:
            # Find the cell with the most values populated on its respective row, column, and grid,
            # and return the list of values that the cell could be

            # Store the number of populated cells each cell is "correlated" with (the number of cells that are
            # in each cells respective row, column, and grid)
            correlated_values = [0 for _ in range(81)]
            
            # Loop through the rows and columns
            for row_index in range(9):
                for column_index in range(9):
                    
                    # Only do check if value is unpopulated
                    if self.sudoku_copy[row_index][column_index] == None:
                        
                        # Get the row, column, and grid cells
                        row = self.return_row(row_index)
                        column = self.return_column(column_index)
                        grid = self.return_grid(row_index, column_index)
                        
                        # Loop through the row, column, and grid cells and if it has a
                        # populated value increase the corresponding value in correlated_values
                        for cell in row + column + grid:
                            if cell != None:
                                correlated_values[(row_index * 9) + column_index] += 1
                    
                    # If the cell we are looking at is populated, assign the value -1 in correlated_values to this cell
                    else:
                        # (Populating with -1 will make the search for unpopulated cell easier as cells with no value will be always 0 or higher)
                        correlated_values[(row_index * 9) + column_index] = -1
            
            # Find the cell with the highest number of correlated values
            target_cell_index = correlated_values.index(max(correlated_values))
        
        # Otherwise use the provided index
        else:
            target_cell_index = index

        # Find potential values for that cell
        potential_values = [True for _ in range(9)]

        # Store the row, column, and grid of the target cell
        row = self.return_row(self.clamp_index_to_row(target_cell_index))
        column = self.return_column(self.clamp_index_to_column(target_cell_index))
        grid = self.return_grid(self.clamp_index_to_row(target_cell_index), self.clamp_index_to_column(target_cell_index))

        for cell in row + column + grid:
            if cell != None:
                potential_values[cell - 1] = False
        
        valid_solutions = []
        for i, value in enumerate(potential_values):
            if value == True:
                valid_solutions.append(i+1)

        return (target_cell_index, valid_solutions)

    def regenerate_sudoku_copy(self, guess_tree):
        # Make copy of sudoku puzzle
        self.sudoku_copy = [list(row) for row in self.sudoku]

        # For each guess in the guess_tree
        for guess in guess_tree:

            # Convert guess[0] (sudoku index) into row and column index
            row_index = self.clamp_index_to_row(guess[0])
            column_index = self.clamp_index_to_column(guess[0])

            # Change the corresponding value in the sudoku list
            self.sudoku_copy[row_index][column_index] = guess[1]

    def solve_sudoku(self):
        
        # Function that solves the sudoku by iteratively running through the cells and
        # attempting to solve them until the puzzle is solved or we are unable to solve
        # any cells after a complete iteration over the entire puzzle

        # Store the guessed values in a list ([(cell_index, guessed_value), (cell_index, guessed value)...])
        guess_tree = []

        # Store whether or not we have found a contradiction
        contradiction = False

        
        
        # Store the number of iterations we have to do in order to solve the puzzle
        iterations = 0

        # Store the number of guesses used
        guesses = 0

        # Store whether or not the puzzle is solved or not
        solved = False

        # Start main solving loop
        while solved == False:
            
            # Stores whether we have solved a cell or not (starts as true as the while loop
            # only runs if solved_cell == True)
            solved_cell = True

            while solved_cell:

                # Immediately set solved_cell to False
                solved_cell = False

                # Increase number of iterations by 1
                iterations += 1

                # Loop over each row and column
                for row in range(9):
                    for column in range(9):

                        # If the value our row and column index is currently selecting is unpopulated
                        if self.sudoku_copy[row][column] == None:

                            # Attempt to find the solution for that cell (function returns None if 
                            # no solution is found)
                            solution = self.context_solve((row*9)+column)

                            # If we found a solution
                            if solution != None:

                                # Update the cell in the sudoku puzzle with the solution
                                self.sudoku_copy[row][column] = solution

                                # Store that we have solved a cell (this means that this may have effected our
                                # ability to solve another cell, and therefore we need to loop over the puzzle
                                # again to be sure we can't solve it anymore)
                                solved_cell = True

            # Check if sudoku is solved
            solved = True
            
            # Loop through sudoku
            for row in self.sudoku_copy:
                for cell in row:

                    # If cell is unpopulated
                    if cell == None:

                        # Then sudoku is not solved
                        solved = False

            # If the sudoku is not solved
            if not(solved):
                guesses += 1

                # If the guess tree is empty
                if guess_tree == []:
                        
                        # Then make the first guess
                        index, possible_solutions = self.get_cell_with_potential_solutions(None)
                        guess_tree.append((index, possible_solutions[0]))
                        
                        # Regenerate the sudoku_copy according to the new guess_tree
                        self.regenerate_sudoku_copy(guess_tree)
                
                # If the guess tree is populated
                else:
                    
                    # Search for contradiction
                    
                    # Loop through puzzle
                    for i in range(9):
                        for j in range(9):

                            # If the value is unpopulated
                            if self.sudoku_copy[i][j] == None:

                                # Store the row, column, and grid
                                row = self.return_row(i)
                                column = self.return_column(j)
                                grid = self.return_grid(i, j)

                                # Store the occurrence of each number
                                occurrence = [False for _ in range(9)]

                                # Loop through all the populated values
                                for item in row + column + grid:

                                    # If the cell is not unpopulated
                                    if item != None:

                                        # Store the number of the cell occurring in occurrence
                                        occurrence[item - 1] = True

                                # If occurrence does not contain False and the value we are calculating for in unpopulated
                                if occurrence.count(False) == 0:

                                    # There must logically be a contradiction
                                    contradiction = True


                    # If we found a contradiction in the puzzle based on the guesses we have used so far
                    if contradiction:
                        
                        # Increment a value in the guess_tree and test again to see if there is a contradiction or whether we can solve
                        # the sudoku based off of those guesses / that guess alone

                        # Set contradiction to false so that the code can check again to see if the new value creates a contradiction
                        contradiction = False

                        # Store whether or not we have incremented a value in the guess_tree
                        incremented_guess_tree = False

                        # Store an index that is equal to the length of the guess_tree minus one
                        guess_tree_index = len(guess_tree) - 1

                        # While we haven't incremented a value in the guess tree
                        while incremented_guess_tree == False:

                            # If the index we are currently at is greater or equal to 0 (the first index of the guess tree list)
                            if guess_tree_index >= 0:
                                self.regenerate_sudoku_copy(guess_tree)
                                # Store the potential solutions of the guess tree index we are looking at
                                index, possible_solutions = self.get_cell_with_potential_solutions(guess_tree[guess_tree_index][0])
                                
                                # If the guess we currently have is less than the largest possible one in the possible_solutions
                                max_value = 0
                                for solution in possible_solutions:
                                    if solution > max_value:
                                        max_value = solution

                                if guess_tree[guess_tree_index][1] < max_value:

                                    # Use the next highest one
                                    for possible_solution in possible_solutions:
                                        if possible_solution > guess_tree[guess_tree_index][1]:
                                            guess_tree[guess_tree_index] = (guess_tree[guess_tree_index][0], possible_solution)
                                            break

                                    # Update the fact we have incremented a value on the guess_tree
                                    incremented_guess_tree = True
                                
                                # If the guess is the largest possible guess
                                else:

                                    # Then remove the guess we are working on and reduce the 
                                    guess_tree.remove(guess_tree[guess_tree_index])
                                    
                                    # Reduce the index we are using on the guess_tree (and repeat this whole loop again with lowered index)
                                    guess_tree_index -= 1
                            
                            # If index is less than zero
                            else:

                                # Print debug hint
                                print("Guess tree index below 0; code aborted")
                                
                                # Quit the program
                                quit()

                        # Once the loop has ended (therefore the guess_tree has been update)        
                        # Regenerate the sudoku_copy based off of the new guess tree
                        self.regenerate_sudoku_copy(guess_tree)
                    
                    # If the code did not encounter a contradiction; therefore the code must have not had enough filled in values to correctly populate the puzzle
                    else:

                        # Then find a potential solution as well as its index
                        index, possible_solutions = self.get_cell_with_potential_solutions(None)

                        # Update the guess_tree with said value
                        guess_tree.append((index, possible_solutions[0]))
                        
                        # Regenerate the sudoku_copy based off of the new guess_tree (Note: We need to write a function that doesn't destroy all
                        # the populated values in the sudoku_copy, as this destroys filled in values that we have calculated and this section of
                        # code does not ruin any of the data we have actually accumulated so far)
                        self.regenerate_sudoku_copy(guess_tree)


        # When solving loop has finished, print how many iterations and guesses it took to solve the puzzle
        print("Iterations to solve: " + str(iterations))
        print("Guesses to solve: " + str(guesses))
    
sudoku_solver = SudokuSolver()
