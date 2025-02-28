import re
text = input("Enter a camel case string: ")
print(re.split(r'(?=[A-Z])', text)[1:])