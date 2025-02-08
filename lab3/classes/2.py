"""
Define a class named Shape and its subclass Square. 
The Square class has an init function which takes a length as argument. 
Both classes have a area function which can print the area of the shape where Shape's area is 0 by default.
"""
class Shape:
    def init(self):
        pass

    def area(self):
        return 0

class Square(Shape):
    def init(self, length):
        super().init()
        self.length = length

    def area(self):
        return self.length * self.length

shape = Shape()
print(shape.area())

square = Square(8)
print(square.area())