#question 1
def countvandc(word):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    vowels = "aeiouAEIOU"
    v_count = 0
    c_count = 0

    for char in word:
        if char in alphabet:  #checks if the character is an alphabet
            if char in vowels:
                v_count = v_count + 1 #increases vowel count
            else:
                c_count = c_count + 1 #increase character count

    return v_count, c_count

word_input = input("Enter a string")

vowels, consonants = countvandc(word_input)

print("Number of Vowels:", vowels)
print("Number of Consonants:", consonants)