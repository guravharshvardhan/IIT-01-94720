import math_utils

# Circle
r = float(input("Enter radius of circle: "))
print("\n Area of circle =", math_utils.area_circle(r))

# Rectangle
l = float(input("Enter rectangle length: "))
w = float(input("Enter rectangle width: "))
print("\n Area of rectangle =", math_utils.area_rectangle(l, w))

# Triangle
b = float(input("Enter base of triangle: "))
h = float(input("Enter height of triangle: "))
print("\n Area of triangle =", math_utils.area_triangle(b, h))

#square
s=float(input("enter side of square"))
print("\n Area of square=",math_utils.area_square(h))
