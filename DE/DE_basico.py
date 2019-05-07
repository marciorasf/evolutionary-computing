# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:43:54 2019

@author: Marcio Souza Filho

!!!!!! A funcao que executa o algoritmo genetico esta no final do codigo com nome GA
"""
import matplotlib.pyplot as plt
import numpy as np
import operator
from random import choice

class Individuo:
    def __init__(self):
        self.variaveis = [] #Variaveis do individuo
        self.fitness = None
        self.prob_selecao = None
        return
        
    # Cria um individuo aleatorio
    def gera_individuo_aleatorio(self, n_variaveis, lim_inferior, lim_superior):
        for i in range(n_variaveis):
            self.variaveis = np.random.uniform(lim_inferior, lim_superior)
        return
    
    # Calcula a fitness do individuo    
    def calcula_fitness(self):
        self.fitness = 0
        return        
    
    # Imprime os atributos do individuo. Usada apenas para testes
    def print_individuo(self):
        print(str(self.variaveis)+', '+str(self.fitness))
        
    
class Populacao:
    def __init__(self):
        self.individuos = []
        self.reta_prob = []

    # Gera populacao aleatoria
    def gera_populacao_aleatoria(self, n_variaveis, tam_pop, lim_inferior, lim_superior):
        for _ in range(tam_pop):
            individuo = Individuo()
            individuo.gera_individuo_aleatorio(n_variaveis, lim_inferior, lim_superior)
            self.individuos.append(individuo)
            
    # Calcula fitness de todos individuos
    def calcula_fitnesses(self):
        for individuo in self.individuos:
            individuo.calcula_fitness()
            
    # Ordena a lista individuos pela ordem de fitness dos individuos. Do pior para o melhor
    def ordena_por_fitnesses(self):
        self.individuos.sort(key=operator.attrgetter('fitness'))
        
    # Imprime os dados da populacao na tela. Usado apenas para testes
    def print_populacao(self):
        for individuo in self.individuos:
            individuo.print_individuo()
    
    # Retorna a media dos fitnesses da populacao
    def media_fitnesses(self):
        soma_fitnesses = 0
        for individuo in self.individuos:
            soma_fitnesses += individuo.fitness
        media_fitnesses = soma_fitnesses/len(self.individuos)
        return media_fitnesses
        
    # Retorna o melhor fitness da populacao. Precisa estar ordenada
    def melhor_fitness(self):
        return self.individuos[-1].fitness
        
class DE:
    @staticmethod
    def seleciona_individuos(populacao):
        individuos = sample(populacao.individuos, 3)
      

n_variaveis = 2
tam_pop = 50
n_geracoes = 100
lim_inferior = -1
lim_superior = 1

populacao = Populacao()
populacao.gera_populacao_aleatoria(n_variaveis, tam_pop, lim_inferior, lim_superior)
