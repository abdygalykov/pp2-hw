def is_palindrome(s):
    return s == s[::-1]

word = "madam"
print(is_palindrome(word))  # Output: True
