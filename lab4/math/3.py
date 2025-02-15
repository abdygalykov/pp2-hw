import math
NumOfSides= int(input())
LenghtOfSide = int(input())

Perimeter = NumOfSides * LenghtOfSide

apothem = LenghtOfSide / (2 * math.tan(math.pi/NumOfSides))

print(Perimeter * apothem * 1/2)