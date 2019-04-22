# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 02:46:48 2019

@author: Marcio Souza Filho
"""

from GA_rastrigin import GA_rastrigin

nvar = 10
ncal = 10000
iteracoes = 100
#for i in range(0,10):
#    print('lancamento '+str(i)+' ----------------------------------------')
#    individuo,valor = GA_rastrigin(ncal,nvar)
#    print(valor)
resultados_individuos = []
resultados_valores = []
for i in range(0,nvar):
    resultados_individuos_n = []
    resultados_valores_n = []
    for j in range(0,iteracoes):
        print('-------------------------------------------------------------------')
        print('variaveis = ' + str(i+1) + ', teste = ' + str(j))
        resultado_iteracao = GA_rastrigin(ncal,i+1)
        resultados_individuos_n.append(resultado_iteracao[0])
        resultados_valores_n.append(resultado_iteracao[1])
#        print(resultado_iteracao[0])
        print(resultado_iteracao[1])
    resultados_individuos.append(resultados_individuos_n)
    resultados_valores.append(resultados_valores_n)