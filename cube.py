# -*- coding: utf-8 -*-

from random import randint, shuffle, sample, choice
import json

DIRECTIONS = {
    "rg": {"dr": +1, "dg": -1, "db": 0},
    "rb": {"dr": +1, "dg": 0, "db": -1},
    "gb": {"dr": 0, "dg": +1, "db": -1},
    "gr": {"dr": -1, "dg": +1, "db": 0},
    "br": {"dr": -1, "dg": 0, "db": +1},
    "bg": {"dr": 0, "dg": -1, "db": +1}
}
PLACEHOLDER = '-'


class Cube:
    def __init__(self, r, g, b):
        self.__coords = {'r': r, 'g': g, 'b': b}
        self.__letter = PLACEHOLDER
        self.__links = {}
        # print('New cube at', str(self))

    def __str__(self):
        return str({'coords': self.__coords, 'links': [(dir, cube.coords) for dir, cube in self.__links.items()]})
        # return str(self.r) + ',' + str(self.g) + ',' + str(self.b)

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
        return min(abs(self.__coords['r']), abs(self.__coords['g']), abs(self.__coords['b']))

    @property
    def abs_max(self):
        return max(abs(self.__coords['r']), abs(self.__coords['g']), abs(self.__coords['b']))

    @property
    def numlinks(self):
        return len(self.__links)

    @property
    def r(self):
        return self.__coords['r']

    @property
    def g(self):
        return self.__coords['g']

    @property
    def b(self):
        return self.__coords['b']

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
            r = self.coords['r'] + direction['dr']
            if abs(r) > radius:
                # print('|__ world is flat X',)
                continue
            g = self.coords['g'] + direction['dg']
            if abs(g) > radius:
                # print('|__ world is flat Y',)
                continue
            b = self.coords['b'] + direction['db']
            if abs(b) > radius:
                # print('|__ world is flat Z',)
                continue

            if (r, g, b) not in cubes:
                cubes.setdefault((r, g, b), Cube(r, g, b))

            next_cube = cubes[(r, g, b)]
            # print('linking', dir_label, 'with', (x, y, b))
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
            str(coord) + ': ' + self.cubes[coord].letter
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
            max_r = 2 * self.radius + 1 if direction['dr'] == 0 else abs(direction['dr'] * self.radius - cube.r) + 1
            max_g = 2 * self.radius + 1 if direction['dg'] == 0 else abs(direction['dg'] * self.radius - cube.g) + 1
            max_b = 2 * self.radius + 1 if direction['db'] == 0 else abs(direction['db'] * self.radius - cube.b) + 1
            maxlen = min(max_r, max_g, max_b)
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