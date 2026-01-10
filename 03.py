#question 3
def common_elements(list1, list2):
    count = 0
    checked_numbers = [] #helps avoid repetition of numbers
    for num in list1:
        if num in list2:
            if num not in checked_numbers: #if statement only works if the num wasn't already checked
                count = count + 1
                checked_numbers.append(num)
    return count

list1= []
size1 = int(input("Enter list1 size:"))
for i in range(size1): #user input for list 1
    n = int(input("Enter a numer:"))
    list1.append(n)

list2 = []
size2 = int(input("Enter list2 size:"))
for i in range(size2): #user input for list 2
    n = int(input("Enter a numer:"))
    list2.append(n)

common_count = common_elements(list1, list2)

print("The number of common elements are:", common_count)