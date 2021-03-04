# -*- coding: utf-8 -*-
DIRECTIONS = {
    "xy": {"dx": +1, "dy": -1, "dz":  0},
    "xz": {"dx": +1, "dy":  0, "dz": -1},
    "yz": {"dx":  0, "dy": +1, "dz": -1},
    "yx": {"dx": -1, "dy": +1, "dz":  0},
    "zx": {"dx": -1, "dy":  0, "dz": +1},
    "zy": {"dx":  0, "dy": -1, "dz": +1}
}

class Cube:
    def __init__(self, x: int, y: int, z: int):
        self.coords = {'x': x, 'y': y, 'z': z}
        self.letter = ''
        self.links = {}

    def link_with(self, dir_label, other_cube):
        self.links.setdefault(dir_label, other_cube)
        cntr_dir_label = dir_label[1] + dir_label[0]
        other_cube.links.setdefault(cntr_dir_label, self)

    def set(self, letter):
        self.letter = letter

    def get(self):
        return self.letter

    def __str__(self):
        return str(self.coords.x) + ',' + str(self.coords.y) + ',' + str(self.coords.z) + ': ' + self.letter

    def grow(self, cubes, radius):
        for dir_label, direction in DIRECTIONS.items():
            print(self.coords, radius, dir_label, direction)
            x = self.coords['x'] + direction['dx']
            y = self.coords['y'] + direction['dy']
            z = self.coords['z'] + direction['dz']
            next_cube: Cube = cubes.setdefault(x, {}).setdefault(y, {}).setdefault(z, Cube(x, y, z))
            clean_new_cube = True if len(next_cube.links) == 0 else False
            self.link_with(dir_label=dir_label, other_cube=next_cube)
            if clean_new_cube and radius >= 1:
                next_cube.grow(cubes, radius - 1)


class Tiling:
    def __init__(self, radius):
        self.radius = radius
        self.cubes = {}
        centerCube = self.cubes.setdefault(0, {}).setdefault(0, {}).setdefault(0, Cube(0, 0, 0))
        centerCube.grow(self.cubes, self.radius)
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