# -*- coding: utf-8 -*-

class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.letter = ''
    
    def set(self, letter):
        self.letter = letter
    
    def get(self):
        return self.letter

    def __str__(self):
        return str(self.x) + ':' + str(self.y) + ',' + str(self.z) + ': ' + self.letter

class Tiling:
    def __init__(self, radius):
        self.radius = radius
        self.cubes = {}
        for x in range(-self.radius, self.radius + 1):
            for y in range(-self.radius, self.radius + 1):
                z = -x - y
                if abs(z) > self.radius:
                    continue
                self.cubes.setdefault(x, {}).setdefault(y, {}).setdefault(z, Cube(x, y, z).get())
        print(self.cubes)

# -2  0  2
# -2  1  1
# -2  2  0

# -1 -1  2
# -1  0  1
# -1  1  0
# -1  2 -1

#  0 -2  2
#  0 -1  1
#  0  0  0
#  0  1 -1
#  0  2 -2

#  1 -2  1
#  1 -1  0
#  1  0 -1
#  1  1 -2

#  2 -2  0
#  2 -1 -1
#  2  0 -2