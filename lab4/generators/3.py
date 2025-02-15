def fun(n):
    for i in range(n):
        if i % 3 == 0 and i % 4 == 0:
            yield i


res = fun(100)
for x in res:
    print(x)