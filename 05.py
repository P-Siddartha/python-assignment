import random
#generates the numbers and finds the necessary answers
def calculations():
    #generates the numbers
    numbers = []
    for i in range(100):
        rand_num = random.randint(100, 150)
        numbers.append(rand_num)

    #mean
    total_sum = 0
    for num in numbers:
        total_sum = total_sum + num
    mean_val = total_sum / len(numbers)

    #median
    numbers.sort()
    n = len(numbers)
    mid1 = numbers[n // 2 - 1]
    mid2 = numbers[n // 2]
    median_val = (mid1 + mid2) / 2

    #mode
    frequency = {}
    for num in numbers:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    max_count = 0
    mode_val = numbers[0]

    for num in frequency:
        if frequency[num] > max_count:
            max_count = frequency[num]
            mode_val = num

    return numbers, mean_val, median_val, mode_val

num_list, mean, median, mode = calculations()

print("First 10 generated numbers:", num_list[:10])
print("Mean:", mean)
print("Median:", median)
print("Mode:", mode)