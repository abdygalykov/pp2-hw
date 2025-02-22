import re

def bool(text):
    x = re.findall("ab*", text)
    if x:
        return True
    else:
        return False

a = "a"
print(bool(a))