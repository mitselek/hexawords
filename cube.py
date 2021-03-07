# -*- coding: utf-8 -*-

from random import randint, shuffle, sample, choice
import json

DIRECTIONS = {
    "xy": {"dx": +1, "dy": -1, "dz": 0},
    "xz": {"dx": +1, "dy": 0, "dz": -1},
    "yz": {"dx": 0, "dy": +1, "dz": -1},
    "yx": {"dx": -1, "dy": +1, "dz": 0},
    "zx": {"dx": -1, "dy": 0, "dz": +1},
    "zy": {"dx": 0, "dy": -1, "dz": +1}
}


class Cube:
    def __init__(self, x, y, z):
        self.__coords = {'x': x, 'y': y, 'z': z}
        self.__letter = ''
        self.__links = {}
        # print('New cube at', str(self))

    def __str__(self):
        return str({'coords': self.__coords, 'links': [(dir, cube.coords) for dir, cube in self.__links.items()]})
        # return str(self.x) + ',' + str(self.y) + ',' + str(self.z)

    @property
    def coords(self):
        return self.__coords

    @property
    def letter(self):
        return self.__letter

    @property
    def links(self):
        return self.__links

    @property
    def abs_min(self):
        return min(abs(self.__coords['x']), abs(self.__coords['y']), abs(self.__coords['z']))

    @property
    def abs_max(self):
        return max(abs(self.__coords['x']), abs(self.__coords['y']), abs(self.__coords['z']))

    @property
    def numlinks(self):
        return len(self.__links)

    @property
    def x(self):
        return self.__coords['x']

    @property
    def y(self):
        return self.__coords['y']

    @property
    def z(self):
        return self.__coords['z']

    def max_word_length(self, radius):
        return (radius + 1) + self.abs_max - self.abs_min  #

    def engrave(self, dir, word):
        # print('engraving', word, 'to', dir, self)
        self.__letter = word[0]
        if len(word) > 1:
            return self.links[dir].engrave(dir, word[1:])
        return True

    def link(self, dir_label, other_cube):
        self.links.setdefault(dir_label, other_cube)

    def grow(self, cubes, radius):
        # print('growing', self, 'minmax', self.abs_min, self.abs_max)
        for dir_label, direction in DIRECTIONS.items():
            # print('testing', dir_label, 'in my links')
            if dir_label in self.links.keys():
                # print('already linked', 'to', dir_label)
                continue
            # print('heading at', dir_label)
            x = self.coords['x'] + direction['dx']
            if abs(x) > radius:
                # print('|__ world is flat X',)
                continue
            y = self.coords['y'] + direction['dy']
            if abs(y) > radius:
                # print('|__ world is flat Y',)
                continue
            z = self.coords['z'] + direction['dz']
            if abs(z) > radius:
                # print('|__ world is flat Z',)
                continue

            if (x, y, z) not in cubes:
                cubes.setdefault((x, y, z), Cube(x, y, z))

            next_cube = cubes[(x, y, z)]
            # print('linking', dir_label, 'with', (x, y, z))
            self.link(dir_label=dir_label, other_cube=next_cube)
            cntr_dir_label = dir_label[1] + dir_label[0]
            next_cube.link(dir_label=cntr_dir_label, other_cube=self)

            if next_cube.numlinks == 1:
                next_cube.grow(cubes, radius)

        return


class Tiling:
    def __init__(self, radius):
        self.radius = radius
        self.cubes = {}
        centerCube = self.cubes.setdefault((0, 0, 0), Cube(0, 0, 0))
        centerCube.grow(self.cubes, self.radius)
        self.words = []

    def __str__(self):
        coords = [
            (
                coord,
                self.cubes[coord].letter,
                # [
                #     link
                #     for link in self.cubes[coord].links.keys()
                # ]
            )
            for coord in self.cubes
        ]
        return json.dumps(coords)

    @property
    def tiles(self):
        return {
            coord: self.cubes[coord].letter
            for coord in self.cubes
        }

    def max_word_length(self, cube, direction=None):
        if direction:
            # print(cube, direction)
            max_x = 2 * self.radius + 1 if direction['dx'] == 0 else abs(direction['dx'] * self.radius - cube.x) + 1
            max_y = 2 * self.radius + 1 if direction['dy'] == 0 else abs(direction['dy'] * self.radius - cube.y) + 1
            max_z = 2 * self.radius + 1 if direction['dz'] == 0 else abs(direction['dz'] * self.radius - cube.z) + 1
            maxlen = min(max_x, max_y, max_z)
            # print('maxlen', maxlen)
            return maxlen
        else:
            return (self.radius + 1) + cube.abs_max - cube.abs_min  #

    def engrave(self, word, hint=None):
        cubes = list(self.cubes.values())
        shuffle(cubes)
        for cube in cubes:
            # print('\nTry', cube)
            if self.max_word_length(cube) < len(word):
                continue
            directions = list(DIRECTIONS.items())
            shuffle(directions)
            for dir_label, direction in directions:
                # print(dir_label)
                max_word_length = self.max_word_length(cube, direction)
                if max_word_length < len(word[0]):
                    continue
                if cube.engrave(dir_label, word[0]):
                    print('Engraved', word[0], 'to', cube.coords, '->', dir_label)
                    self.store(word)
                return

    def store(self, word):
        self.words.append(word)