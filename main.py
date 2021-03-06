#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

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

tiling = Tiling(17)
print(tiling)
