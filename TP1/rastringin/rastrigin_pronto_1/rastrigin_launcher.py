# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 02:46:48 2019

@author: Marcio Souza Filho
"""

from GA_rastrigin import GA_rastrigin

nvar = 10
ncal = 10000
#for i in range(0,10):
#    print('lancamento '+str(i)+' ----------------------------------------')
#    individuo,valor = GA_rastrigin(ncal,nvar)
#    print(valor)
resultados = []
for i in range(0,10):
    resultados_n = []
    for j in range(0,1000):
        print('variaveis = ' + str(i+1) + ', teste = ' + str(j))
        resultados_n.append(GA_rastrigin(ncal,i+1))
    resultados.append(resultados_n)