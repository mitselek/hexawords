#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from random import shuffle
from math import sqrt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from cube import Tiling

MINWORDS, MAXTRY, RADIUS, RETRY_COUNT = 10, 100, 5, 1000

BOOKLET_PAGES = 3
BOOKLET_TITLE = 'segadik'
PDF_GRID_CENTER = 21 / 2 * cm
PDF_HEX_SIDE_LEN = 4.3 / RADIUS * cm
PDF_MARGIN = 1 * cm
PDF_FONT_SIZE = 150 / RADIUS
PDF_TOP = 29.7 * cm
PDF_LEFT = PDF_GRID_CENTER - sqrt(3) * RADIUS * PDF_HEX_SIDE_LEN

DIRECTIONS = ((0,-1,1), (1,-1,0), (1,0,-1), (0,1,-1), (-1,1,0), (-1,0,1))

WORDPOOL_INGREDIENTS = [
    {'size': 22000, 're': '[ÕÜÄÖ]'},
]

MIN_WORD_LENGTH = min(4, RADIUS + 1)
MAX_WORD_LENGTH = 2 * RADIUS + 1
FIRST_WORD_LENGTH = 2 * RADIUS


def new_words():
    words = []
    for wp in WORDPOOL_INGREDIENTS:
        shell_str = "cat et/4.txt | grep '^.\{" + str(MIN_WORD_LENGTH) + "," + str(MAX_WORD_LENGTH) + "\}$' | grep '" + wp['re'] + "' | sort -R | head -" + str(wp['size'])
        print(shell_str)
        stream = os.popen(shell_str)
        wordchain = ''
        for word in stream.readlines():
            wordchain += word
        words.extend([(word.rstrip("\n"), word.rstrip("\n")) for word in wordchain.rstrip("\n").split('\n')])
    shuffle(words)
    return words

def cartesian(hex):
    r, g, b = hex
    x = sqrt(3) * (b / 2 + r) * PDF_HEX_SIDE_LEN + PDF_GRID_CENTER
    y = PDF_TOP - PDF_GRID_CENTER - PDF_MARGIN - 3 / 2 * b * PDF_HEX_SIDE_LEN
    return (x, y)


canvas = Canvas('booklet_' + BOOKLET_TITLE + '.pdf', pagesize=A4)

for pagenr in range(BOOKLET_PAGES   ):
    tiling = Tiling(RADIUS)
    words = new_words()
    for word in words:
        tiling.engrave(word)

    tiles = tiling.tiles
    canvas.setFont("Times-Roman", 12)
    canvas.drawString(1 * cm, PDF_TOP - 1 * cm, 'Micheleki sõnaheksadix, 2021   ' + str(pagenr) + '/' + str(BOOKLET_PAGES))

    canvas.setFont("Courier", PDF_FONT_SIZE)
    for (coords, letter) in tiles.items():
        cart = cartesian(coords)
        x, y = cart
        canvas.drawString(x, y, letter.upper())
        # print(coords, letter, cart)

    canvas.setFont("Courier", PDF_FONT_SIZE / 1.2)
    first_line_y = 8 * cm
    max_letters_on_line = (RADIUS * 4 + 1) * 1.2
    letters_on_line = 0
    line_nr = 0
    words_on_line = ''

    lines = []
    line = ''
    # lines.append(line)
    for (word, hint) in tiling.words:
        print(word)
        if len(line) == 0:
            line += word
        elif len(line) + 2 + len(word) > max_letters_on_line:
            lines.append(line)
            line = word
            line_nr += 1
        else:
            line += '  ' + word
    lines.append(line)

    for ix, line in enumerate(lines):
        print(ix, line)
        canvas.drawString(PDF_LEFT, first_line_y - ix/1.2 * cm, line)

    canvas.showPage() # saves a page to PDF and gets ready for a new one

canvas.save()
