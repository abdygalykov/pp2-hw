import re

def bool(text):
    x = re.findall("^a.*b$", text)
    if x:
        return True
    else:
        return False


a = "aasdasdasd"
print(bool(a))