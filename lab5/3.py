import re

def bool(text):
    x = re.findall("[a-z]_", text)
    if x:
        return True
    else:
        return False
    
a = "asdada_sdasd"

print(bool(a))