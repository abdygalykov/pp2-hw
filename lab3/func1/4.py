def filter_prime(nums):
    for x in nums:
        for i in range(2, int(x**0.5) + 1):
            if n % i != 0:
                return x
                break


nums = [1, 4, 7, 9, 3, 11]

print(filter_prime(nums))