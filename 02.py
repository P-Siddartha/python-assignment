#question 2
def matrix_multiplication(matrix_a, matrix_b):
    row_1 = len(matrix_a)
    col_1 = len(matrix_a[0])
    row_2 = len(matrix_b)
    col_2 = len(matrix_b[0])
    #checks if number of columns of first matrix is equal to the number of rows of the second matrix
    if col_1 != row_2:
        return "matrices cannot be multiplied"
    #size will be rows of first matrix x columns of second matrix
    result = []
    for i in range(row_1):
        row = [0] * col_2
        result.append(row)
    #matrix multiplication
    for i in range(row_1):
        for j in range(col_2):
            for k in range(col_1):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return result

mat_a = [
    [1, 2, 3],
    [4, 5, 6]
]

mat_b = [
    [7, 8],
    [9, 10],
    [11, 12]
]

product = matrix_multiplication(mat_a, mat_b)

print("Result:",product)
