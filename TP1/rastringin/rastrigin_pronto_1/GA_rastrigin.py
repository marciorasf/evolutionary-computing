# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 02:30:47 2019

@author: Marcio Souza Filho
"""


from classes_rastrigin import Populacao, Selecao, Cruzamento, Mutacao, Individuo
import matplotlib.pyplot as plt
import numpy as np

def GA_rastrigin(ncal, nvar):
    lim_inferior = -5.12
    lim_superior = 5.12
    n_bits = 32
    n_variaveis = nvar
    tam_pop = 50
    n_geracoes = round((ncal-tam_pop)/tam_pop)
    prob_mutacao_min = n_bits*n_variaveis/10000 # quando tiver 5 constantes de tempo, sera mutado 1bit por individuo
    prob_mutacao_max = 0.95
    prob_cruzamento_min = 0.4
    prob_cruzamento_max = 0.9
    prob_torneio = 0.5
    constante_tempo_mutacao = n_geracoes*90/(5*100) # e atingio 5 constantes de tempo em 70% do total de geracoes
    
    populacao = Populacao(tam_pop)
    populacao.gera_populacao_aleatoria(n_bits, n_variaveis, lim_inferior, lim_superior)
    populacao.ordena_por_fitnesses()
    
    melhor_resultado = [populacao.individuos[tam_pop-1].fenotipo, populacao.individuos[tam_pop-1].rastrigin_valor]
#    medias_fitnesses = []
    minimos_valores_rastrigin = []
    
#    medias_fitnesses.append(populacao.fitnesses_media())
    minimos_valores_rastrigin.append(populacao.individuos[tam_pop-1].rastrigin_valor)
    
    ger = 0
    while ger < n_geracoes:
        prob_mutacao = prob_mutacao_min + (prob_mutacao_max-prob_mutacao_min)*np.exp(-ger/constante_tempo_mutacao)
        prob_cruzamento = prob_cruzamento_min + (prob_cruzamento_max-prob_cruzamento_min)*ger/n_geracoes
        ger += 1
        Selecao.calcula_probs_SPF(populacao)
        Selecao.gera_reta_prob(populacao)
        populacao_nova = Populacao(tam_pop)
        for i in range(0, int(tam_pop/2)-1):
            if prob_torneio > np.random.uniform(0 ,1):
               pais = Selecao.seleciona_pais_torneio(populacao,10)
            else:
                pais = Selecao.seleciona_pais_roleta(populacao)
            if prob_cruzamento > np.random.uniform(0 ,1):
                filhos = Cruzamento.crossover_1_ponto(pais)
            else:
                filhos = []
                for j in range(0,2):
                    filhos.append(Individuo(pais[0].bits_individuo, pais[0].n_variaveis, pais[0].lim_inferior, pais[0].lim_superior))
                    filhos[j].genotipo = pais[j].genotipo
            for individuo in filhos:
                Mutacao.bit_flip(individuo, prob_mutacao)
                individuo.calcula_fenotipo()
                individuo.calcula_fitness()
                
            for individuo in filhos:
                populacao_nova.individuos.append(individuo)
        
        populacao_nova.individuos.append(populacao.individuos[tam_pop-1])
        populacao_nova.individuos.append(populacao.individuos[tam_pop-2])
#        populacao_nova.individuos.append(populacao.individuos[tam_pop-3])
#        populacao_nova.individuos.append(populacao.individuos[tam_pop-4])
        populacao = populacao_nova
        populacao.ordena_por_fitnesses()
        
#        medias_fitnesses.append(populacao.fitnesses_media())
        minimos_valores_rastrigin.append(populacao.individuos[tam_pop-1].rastrigin_valor)
        if populacao.individuos[tam_pop-1].rastrigin_valor < melhor_resultado[1]:
            melhor_resultado = [populacao.individuos[tam_pop-1].fenotipo, populacao.individuos[tam_pop-1].rastrigin_valor]
    
#    plt.plot(medias_fitnesses)
#    plt.show()
#    plt.plot(minimos_valores_rastrigin)
#    plt.show()
    return(melhor_resultado)