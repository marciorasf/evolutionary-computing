# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:43:54 2019

@author: Marcio Souza Filho
"""

from classes_n_rainhas import Populacao, Selecao, Cruzamento, Mutacao
#import matplotlib.pyplot as plt
import numpy as np

def GA_n_rainhas():
    tamanho_populacao = 100
    dimensao_individuo = 8
    fitness_ideal = 1
    numero_geracoes = 100000
    prob_mutacao = 0.6
    prob_cruzamento = 0.8
    prob_torneio = 0.5
    
    
    populacao = Populacao(tamanho_populacao, dimensao_individuo)
    populacao.gera_populacao_aleatoria()
    populacao.calcula_fitnesses()
    populacao.ordena_por_fitnesses()
    
    melhores_fitnesses = []
    melhores_fitnesses.append(populacao.melhor_fitness()) 
    
    #medias_fitnesses = []
    #medias_fitnesses.append(populacao.media_fitnesses())
    
    geracao = 0
    geracoes_estagnadas = 0
    while geracao < numero_geracoes and melhores_fitnesses[geracao] < fitness_ideal:
        geracao += 1
        if prob_torneio > np.random.uniform(0,1):
            pais = Selecao.seleciona_pais_torneio(populacao, 10)
        else:
            Selecao.calcula_SPF(populacao)
            Selecao.gera_reta_prob(populacao)
            pais = Selecao.seleciona_pais_roleta(populacao)
        
        if (prob_cruzamento > np.random.rand()):
            filhos = Cruzamento.cut_and_crossfill(pais)
            for individuo in filhos:
                if(prob_mutacao > np.random.rand()):
                    Mutacao.swap(individuo)
        else:
            filhos = pais
            for individuo in filhos:
                Mutacao.swap(individuo)
                
        populacao.individuos[0] = filhos[0]
        populacao.individuos[1] = filhos[1]
        
        populacao.ordena_por_fitnesses()
        
        melhores_fitnesses.append(populacao.melhor_fitness())
    #    medias_fitnesses.append(populacao.media_fitnesses())
        
        if melhores_fitnesses[geracao] == melhores_fitnesses[geracao-1]:
            geracoes_estagnadas += 1
        else:
            geracoes_estagnadas = 0
            prob_mutacao = 0.6
            prob_cruzamento = 0.8
        if geracoes_estagnadas >= 10:
            prob_mutacao = 1
            prob_cruzamento = 0.9
        
    #plt.plot(medias_fitnesses)
    #plt.show()
    #plt.plot(melhores_fitnesses)
    #plt.show()
    return(geracao+1)