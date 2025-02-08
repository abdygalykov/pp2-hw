def is_palindrome(word):
    word = word.replace(" ", "").lower()
    return word == word[::-1]

phrase = input("Enter a phrase: ")
if is_palindrome(phrase):
    print("This is a palindrome.")
else:
    print("This is not a palindrome.")