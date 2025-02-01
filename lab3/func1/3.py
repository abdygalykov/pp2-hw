def solve(numheads, numlegs):
    count = 0
    count = numlegs - 2 * numheads
    count = count / 2

    return count, numheads - count


print(solve(35, 94))