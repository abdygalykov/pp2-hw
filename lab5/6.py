import re

def sub(text):
    x = re.sub("[,. ]", ":", text)

    return x

a = "asd,asd.asdasda        asdasd, aasdasdad..."
print(sub(a))