import math

thickness = 100
angle = 5.71

angle_rad = math.radians(angle)

#surf_thickness = 100
#
surf_thickness = thickness/math.cos(angle_rad)
#
print(surf_thickness)

# thickness = surf_thickness*math.sin(angle_rad)
#
# print(thickness)