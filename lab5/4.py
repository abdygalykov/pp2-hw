import re

def bool(text):
    x = re.search("^[A-Z]{1}[a-z]", text)
    if x:
        return True
    else:
        return False
    
a = "Axczcx"
print(bool(a))