import re

s = "some_awesome_var"

def camel(text):
    x = re.sub("[_]", "", text.title())

    return x

print(camel(s))