import random

'''Generates and returns a unique layout (9x9) of numbers from 1 to 9 
with no duplicate numbers in each row, column and 3x3 boxes.'''
class LayoutGenerator:

    '''Checks if the new number matches other numbers in the col.'''
    def __checkInCol(self, num, sudoku, n):
        if len(sudoku) > 0:
            for s in sudoku:
                if num == s[n]:  # if num is not unique
                    return True
        return False


    '''Checks if the new number matches other numbers in the row.'''
    def __checkInRow(self, num, raw):
        if len(raw) > 0:
            if num in raw:  # if num is not unique
                return True
        return False


    '''Checks if the new number matches other numbers in the 3x3 box.'''
    def __checkInBox(self, num, sudoku, n):
        if len(sudoku) == 0 or len(sudoku) == 3 or len(sudoku) == 6:
            return False
        # get numbers in sudoku to check
        numbersInBox = []
        # left box
        if n < 3:
            r1 = 0
            r2 = 3
        # middle box
        elif 2 < n < 6:
            r1 = 3
            r2 = 6
        # right box
        elif n > 5:
            r1 = 6
            r2 = 9
        # Upper three boxes
        if 0 < len(sudoku) < 3:
            for s in sudoku:
                for i in range(r1, r2):
                    numbersInBox.append(s[i])
        # num in 5-th line
        if len(sudoku) == 4:
            for i in range(r1, r2):
                numbersInBox.append(sudoku[3][i])
        # num in 6-th line
        elif len(sudoku) == 5:
            for i in range(r1, r2):
                numbersInBox.append(sudoku[3][i])
                numbersInBox.append(sudoku[4][i])
        # num in 8-th line
        elif len(sudoku) == 7:
            for i in range(r1, r2):
                numbersInBox.append(sudoku[6][i])
        # num in 9-th line
        elif len(sudoku) == 8:
            for i in range(r1, r2):
                numbersInBox.append(sudoku[6][i])
                numbersInBox.append(sudoku[7][i])
        if num in numbersInBox:
            return True

    '''Generates a row.'''
    def __getRow(self, sudoku):
        # when a match is found
        isNotValid = True
        attempts = 0
        while isNotValid:
            attempts += 1
            # if no variants
            if attempts == 6:
                return False
            isNotValid = False
            row = []
            for n in range(9):  # n is index of column
                numList = random.sample(range(1, 10), 9)
                num = numList.pop(0)
                # if there is a match with another number in a row, column or 3x3 box
                while self.__checkInRow(num, row) or self.__checkInCol(num, sudoku, n) or self.__checkInBox(num, sudoku, n):
                    # if whole row is incorrect (no of 1-9 numbers is fit)
                    if len(numList) == 0:
                        isNotValid = True
                        break
                    num = numList.pop(0)
                    if isNotValid:
                        break
                if isNotValid:
                    row = []
                    break
                row.append(num)
        return row

    '''Main method of a class. Generates and returns layout.'''
    def generateLayout(self):
        sudoku = []
        for i in range(9):  # i - raw
            raw = self.__getRow(sudoku)
            if not raw:
                return False
            sudoku.append(raw)
        return sudoku
