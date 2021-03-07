#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from random import shuffle

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from cube import Tiling

MINWORDS, MAXTRY, WORDLENGTH, RADIUS, RETRY_COUNT = 10, 100, 6, 6, 1000

BOOKLET_PAGES = 2
PDF_GRID_CENTER = 21 / 2 * cm
PDF_FONT_SIZE = 16 * 16 / RADIUS
PDF_LEFT = (21 - (RADIUS - 0.5) * PDF_FONT_SIZE / 16) / 2 * cm
PDF_TOP = 29.7 * cm - PDF_LEFT

PLACEHOLDER = '-'
DIRECTIONS = ((0,-1,1), (1,-1,0), (1,0,-1), (0,1,-1), (-1,1,0), (-1,0,1))
E_WORD_TOO_LONG = 'Nii pikk sõna ei mahu ära'

WORDPOOL_INGREDIENTS = [
    {'size': 22, 're': '[KPTGBD][AEIOUÕÜÄÖ][KPTGBD][AEIOUÕÜÄÖ][KPTGBD]'},
    {'size': 22, 're': '[AEIOUÕÜÄÖ][KPTGBD][AEIOUÕÜÄÖ][AEIOUÕÜÄÖ]'}
]
RADIUS = 2
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

tiling = Tiling(RADIUS)
print(tiling)
words = new_words()
for word in words:
    tiling.engrave(word)

tiles = tiling.tiles
print(tiles)
# print(tiling.words)
