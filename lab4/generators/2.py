def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

x = int(input())
res = evens(x)
for i in res:
    print(i)