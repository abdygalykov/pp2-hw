def squares(a,b):
    for i in range(a, b + 1):
        yield i * i

x = int(input())
y = int(input())

res = squares(x,y)

for i in res:
    print(i)
