def filter_prime(nums):
    for x in nums:
        check = True
        if x <= 1:
            check = False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0:
                check = False
        if check == True :
            return x 


nums = [1,2 , 4, 7, 9, 3, 11]

print(filter_prime(nums))