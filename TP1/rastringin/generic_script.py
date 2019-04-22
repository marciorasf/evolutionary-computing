# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 20:42:14 2019

@author: Marcio Souza Filho
"""

def obtem_valores(resultados):
    valores = []
    for i  in range(0,len(resultados)):
        valores_n = []
        for j in range(0, len(resultados[i])):
            valores_n.append(resultados[i][j][1])
        valores.append(valores_n)
    return valores
    
def medias(valores):
    medias = []
    for i in range(0,len(valores)):
        medias.append(sum(valores[i])/len(valores[i]))
    print(medias)