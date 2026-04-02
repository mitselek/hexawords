#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from random import shuffle
from math import sqrt, floor

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from cube import Tiling

GRID_RADIUS = 8
GRID_FILL_RATIO = 0.8
GRID_MAX_EMPTY_LETTERS = 12

BOOKLET_PAGES = 12
BOOKLET_TITLE = 'segadik'

PDF_GRID_CENTER = 21 / 2 * cm
PDF_HEX_SIDE_LEN = 4.3 / GRID_RADIUS * cm
PDF_MARGIN = 1 * cm
PDF_FONT_SIZE = 150 / GRID_RADIUS
PDF_TOP = 29.7 * cm
PDF_LEFT = PDF_GRID_CENTER - sqrt(3) * GRID_RADIUS * PDF_HEX_SIDE_LEN
PDF_HINT_FONT_SIZE_RATIO = 0.7
PDF_PRINT_COORDS = False

DIRECTIONS = ((0, -1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1))

WORDPOOL_INGREDIENTS = [
    {'size': 1000, 're': '.\{4,7\}'},
    {'size': 100, 're': '.\{7,9\}'},
    # {'size': 10000, 're': '[ÕÜÄÖ]'},
]

MIN_WORD_LENGTH = min(4, GRID_RADIUS + 1)
MAX_WORD_LENGTH = 2 * GRID_RADIUS + 1
FIRST_WORD_LENGTH = 2 * GRID_RADIUS


def read_words(re, cnt):
    shell_str = "cat et/4.txt | grep '^.\{" + str(MIN_WORD_LENGTH) + "," + str(MAX_WORD_LENGTH) + "\}$' | grep '" + \
                re + "' | sort -R | head -" + str(cnt)
    stream = os.popen(shell_str)
    word_chain = ''
    for word in stream.readlines():
        word_chain += word
    return  [(word.rstrip("\n"), word.rstrip("\n")) for word in word_chain.rstrip("\n").split('\n')]


def new_words():
    words = []
    for wp in WORDPOOL_INGREDIENTS:
        words.extend(read_words(wp['re'], wp['size']))
    shuffle(words)
    return words


def cartesian(hex):
    r, g, b = hex
    x = sqrt(3) * (b / 2 + r) * PDF_HEX_SIDE_LEN + PDF_GRID_CENTER
    y = PDF_TOP - PDF_GRID_CENTER - PDF_MARGIN - 3 / 2 * b * PDF_HEX_SIDE_LEN
    return (x, y)


canvas = Canvas('booklet_' + BOOKLET_TITLE + '.pdf', pagesize=A4)

solutions = {}
for page_nr in range(BOOKLET_PAGES):
    canvas.setFont("Times-Roman", 12)
    canvas.drawString(1 * cm, PDF_TOP - 1 * cm,
                      'Micheleki sõnaheksadix, 2021   ' + str(page_nr + 1) + '/' + str(BOOKLET_PAGES))

    print('Page', page_nr + 1, 'fill ratio:', end='')
    while True:
        tiling = Tiling(GRID_RADIUS)
        words = new_words()
        # print('All words:', [word[0] for word in words])
        canvas.setFont("Courier", 12)
        stat_line_nr = 0
        last_stat = 0
        for ix, word in enumerate(words):
            if word[0] == '':
                continue
            tiling.engrave(word)
            if tiling.fill_ratio > last_stat:
                last_stat = tiling.fill_ratio
                stat_line_nr += 1
                if PDF_PRINT_COORDS:
                    canvas.drawString(1 * cm, PDF_TOP - 3 * cm - stat_line_nr * 0.5 * cm,
                                      (str(floor(ix / len(words) * 100))).rjust(2) + ': ' + str(
                                          floor(tiling.fill_ratio * 100)).ljust(2) + ' ' + word[0])
                # else:
                #     print(
                #         str(floor(ix / len(words) * 100)).rjust(2) + ': ' +
                #         str(floor(tiling.fill_ratio * 100)).ljust(2) + ' ' + word[0])

        print(' ', str(floor(tiling.fill_ratio * 100)) + '%', end='')
        if tiling.fill_ratio > GRID_FILL_RATIO and len(tiling.empty_cubes) <= GRID_MAX_EMPTY_LETTERS:
            break
    print('.')

    solution = tiling.empty_cubes
    word = '*'.rjust(len(solution), '*')
    if len(solution) >= 4:
        word = read_words('^.\{' + str(len(solution)) + '\}$', 1)[0][0]

    solutions[page_nr + 1] = word
    for c in tiling.empty_cubes:
        tiling.cubes[c].engrave('rg', word[0])
        word = word[1:]

    for (coordinates, letter) in tiling.tiles.items():
        cart = cartesian(coordinates)
        x, y = cart
        if PDF_PRINT_COORDS:
            if letter == '-':
                canvas.setFont("Courier", PDF_FONT_SIZE / 6)
                canvas.drawString(x, y, ','.join([str(c) for c in coordinates]))
            else:
                canvas.setFont("Courier", PDF_FONT_SIZE / 6)
                canvas.drawString(x, y - PDF_FONT_SIZE / 6, ','.join([str(c) for c in coordinates]))
        canvas.setFont("Courier", PDF_FONT_SIZE)
        canvas.drawString(x, y, letter.upper())

    canvas.setFont("Courier", PDF_FONT_SIZE * PDF_HINT_FONT_SIZE_RATIO)
    first_line_y = 8 * cm
    max_letters_on_line = (GRID_RADIUS * 1.2 * 4 + 1) / PDF_HINT_FONT_SIZE_RATIO
    letters_on_line = 0
    line_nr = 0
    words_on_line = ''

    lines = []
    line = ''
    # lines.append(line)
    for (word, hint) in sorted(tiling.words, key=lambda tup: tup[0]):
        if len(line) == 0:
            line += word
        elif len(line) + 2 + len(word) > max_letters_on_line:
            lines.append(line)
            line = word
            line_nr += 1
        else:
            line += '  ' + word
    lines.append(line)

    # canvas.setFont("Courier", 12)
    line_height = 6 / GRID_RADIUS
    for ix, line in enumerate(lines):
        # print(ix, line)
        canvas.drawString(PDF_LEFT, first_line_y - ix * line_height * cm, line)

    canvas.showPage()  # saves a page to PDF and gets ready for a new one

for nr in solutions:
    canvas.drawString(PDF_LEFT, (29 - nr * line_height) * cm, str(nr) + ': ' + solutions[nr])

canvas.save()
