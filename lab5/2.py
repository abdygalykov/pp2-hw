import re

def bool(text):
    x = re.findall("ab{2,3}", text)
    if x:
        return True
    else:
        return False
    
a = "ab"
print(bool(a))