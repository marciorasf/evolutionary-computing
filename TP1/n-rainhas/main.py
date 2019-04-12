# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:43:54 2019

@author: Marcio Souza Filho
"""

from classes import Populacao, Selecao

dimensao_populacao = 10
dimensao_individuo = 10
populacao = Populacao(dimensao_populacao, dimensao_individuo)
populacao.gera_populacao_aleatoria()
populacao.calcula_fitnesses()
populacao.print_populacao()
Selecao.seleciona_pais(populacao)