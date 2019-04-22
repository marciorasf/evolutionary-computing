# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:25:44 2019

@author: Marcio Souza Filho
"""

from GA_n_rainhas import GA_n_rainhas

n_amostras = 100
amostras = []
for i  in range(0, n_amostras):
    amostras.append(GA_n_rainhas())
total = sum(amostras)
media = total/n_amostras
print(media)
