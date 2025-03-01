import time
import math

num = 25100
delay = 2123  # in milliseconds

time.sleep(delay / 1000)  # Convert milliseconds to seconds
result = math.sqrt(num)

print(f"Square root of {num} after {delay} milliseconds is {result}")
