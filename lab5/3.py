import re

def bool(text):
    x = re.findall("[a-z]_[a-z]", text)
    if x:
        return True
    else:
        return False
    
a = "asdada_Asdasd"

print(bool(a))