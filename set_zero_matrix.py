class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        row0_has_zero = None
        col0_has_zero = None

        # check if first row has a zero
        for j in range(len(matrix[0])):
            if matrix[0][j] == 0:
                row0_has_zero = True

        # check if first col has a zero
        for i in range(len(matrix)):
            if matrix[i][0] == 0:
                col0_has_zero = True

        for i in range(1,len(matrix)):
            for j in range(1,len(matrix[0])):
                if matrix[i][j] == 0:
                    matrix[0][j] = matrix[i][0] = 0

        for i in range(1,len(matrix)):
            for j in range(1,len(matrix[0])):
                if matrix[0][j] == 0 or matrix[i][0] == 0:
                    matrix[i][j] = 0

        if row0_has_zero:
            for j in range(len(matrix[0])):
                matrix[0][j] = 0

        if col0_has_zero:
            for i in range(len(matrix)):
                matrix[i][0] = 0


