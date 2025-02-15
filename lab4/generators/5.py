def reverse_nums(n):
    for i in range(n, 0, -1):
        yield i

res = reverse_nums(100)

for x in res:
    print(x)