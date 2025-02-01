def filter_prime(nums):
    b = []
    for x in nums:
        check = True
        if x <= 1:
            check = False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0:
                check = False
                break
        if check:
            b.append(x)
    return b

a = [1,2,3,4,5,6,7,8,9]

print(filter_prime(a))