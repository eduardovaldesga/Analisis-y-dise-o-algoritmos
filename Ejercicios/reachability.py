# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:15:20 2017

@author: Eduardo
"""


def reach(inicio,fin,textfile):
    'determina si un nodo fin es alcanzable desde inicio'
    d = dict()
    with open(textfile, "r") as archivo:
        for linea in archivo:
            x, y = (linea.strip()).split()
            n = d.get(x, {x}) | d.get(y, {y})
            if inicio in n and fin in n:
                return True
            for cuate in n:
                d[cuate] = n
    return False