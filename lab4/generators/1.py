import math
def square(n):
    for i in range(1, n + 1):
        yield i * i


res = square(10)
for n in res:
    print(n)