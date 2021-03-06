#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from cube import Tiling

MINWORDS, MAXTRY, WORDLENGTH, RADIUS, RETRY_COUNT = 10, 100, 6, 6, 1000

BOOKLET_PAGES = 2
PDF_FONT_SIZE = 16 * 16 / RADIUS
PDF_LEFT = (21 - (RADIUS - 0.5) * PDF_FONT_SIZE / 16) / 2 * cm
PDF_TOP = 29.7 * cm - PDF_LEFT

PLACEHOLDER = '_'
DIRECTIONS = ((0,-1,1), (1,-1,0), (1,0,-1), (0,1,-1), (-1,1,0), (-1,0,1))
E_WORD_TOO_LONG = 'Nii pikk sõna ei mahu ära'

WORDPOOL_INGREDIENTS = [
    { 'size': 100, 're': '[KPTGBD][AEIOUÕÜÄÖ][KPTGBD][AEIOUÕÜÄÖ][KPTGBD]' }
]
RADIUS = 3
MIN_WORD_LENGTH = min(4, RADIUS + 1)
MAX_WORD_LENGTH = 2 * RADIUS + 1
FIRST_WORD_LENGTH = 2 * RADIUS


def new_words():
    words = ''
    for wp in WORDPOOL_INGREDIENTS:
        shell_str = "cat et/4.txt | grep '^.\{" + str(MIN_WORD_LENGTH) + "," + str(MAX_WORD_LENGTH) + "\}$' | grep '" + wp['re'] + "' | sort -R | head -" + str(wp['size'])
        print(shell_str)
        stream = os.popen(shell_str)
        for word in stream.readlines():
            print(word)
            words += word
        words = [(word, word) for word in words.rstrip("\n").split('\n')]
        print(words)
tiling = Tiling(2)
tiling.engrave('bars')
print(tiling)
new_words()
