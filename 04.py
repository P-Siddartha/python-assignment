#question 4
def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    #create a matrix with inverted dimensions
    transposed_matrix = []
    for i in range(cols):
        new_row = [0] * rows
        transposed_matrix.append(new_row)

    #swaps the rows and columns
    for i in range(rows):
        for j in range(cols):
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix

original_matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

transposed = transpose_matrix(original_matrix)

print("Original Matrix:")
for row in original_matrix:
    print(row)

print("\nTransposed Matrix:")
for row in transposed:
    print(row)