def count_case(s):
    upper_count = sum(1 for char in s if char.isupper())
    lower_count = sum(1 for char in s if char.islower())
    return upper_count, lower_count

text = "Hello World"
upper, lower = count_case(text)
print("Uppercase letters:", upper)  # Output: 2
print("Lowercase letters:", lower)  # Output: 8
