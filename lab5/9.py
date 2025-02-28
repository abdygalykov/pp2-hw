import re
text = input("Enter a camel case string: ")
print(re.sub(r'([A-Z])', r' \1', text).strip())