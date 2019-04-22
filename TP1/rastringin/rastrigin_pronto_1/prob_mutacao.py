# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:18:42 2019

@author: Marcio Souza Filho
"""
import numpy as np
import matplotlib.pyplot as plt

n_bits = 32
n_variaveis = 10
n_geracoes = 200
prob_mutacao_min = n_bits*n_variaveis/10000 # quando tiver 5 constantes de tempo, sera mutado 1bit por individuo
prob_mutacao_max = 0.95
constante_tempo_mutacao = n_geracoes*90/(5*100) # e atingio 5 constantes de tempo em 70% do total de geracoes
y = []
for i in range(0,200):
    y.append(prob_mutacao_min + (prob_mutacao_max-prob_mutacao_min)*np.exp(-i/constante_tempo_mutacao))
plt.plot(y)
plt.show()