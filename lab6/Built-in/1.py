from functools import reduce

def multiply_list(numbers):
    def multiply(x, y):
        return x * y
    
    return reduce(multiply, numbers)

nums = [2, 3, 4, 5]
print(multiply_list(nums)) 
