# vowel = ['a', 'e', 'i', 'o', 'u']
# data = []
# response = str(input("Enter your desired word\n>> ")).split()
# for i in response:
#     data.append(i)
#     print(data)

def split_input_into_alphabets(input_string):
    # Split the input string into words
    words = input_string.split()

    # Initialize an empty list to store alphabets
    alphabet_list = []

    # Iterate over each word
    for x in words:
        # Split the word into individual alphabets
        alphabets = list(x)
        # Append the alphabets to the list
        alphabet_list.extend(alphabets)

    return alphabet_list

# Get input from the user
user_input = input("Enter a sentence: ")

# Call the function and print the result
result = split_input_into_alphabets(user_input)
print("Alphabets in the input:", result)
