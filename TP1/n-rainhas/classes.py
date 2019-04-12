# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 21:02:01 2019

@author: Marcio Souza Filho
"""
import numpy as np
import operator

class Individuo:
    # Initializer / Instance Attributes
    def __init__(self, dimensao_individuo):
        self.dimensao_individuo = dimensao_individuo
        self.genotipo = None
        self.fitness = None
        
    # Cria um individuo aleatorio
    def gera_genotipo_aleatorio(self):
        self.genotipo = np.random.permutation(self.dimensao_individuo)
    
    # Calcula a fitness do individuo    
    def calcula_fitness(self):
        self.fitness = 0
        for i in range(0,self.dimensao_individuo):
            self.fitness -= 1
            for j in range(0,self.dimensao_individuo):
                delta_x = abs(i-j)
                delta_y = abs(self.genotipo[i] - self.genotipo[j])
                if(delta_x == delta_y):
                    self.fitness += 1;
        self.fitness /= 2
        

    
    # Imprime os atributos do individuo
    def print_individuo(self):
        print('dimensao:' + str(self.dimensao_individuo) + ', genotipo:' + str(self.genotipo) + ', fitness:' + str(self.fitness))
        
    
class Populacao:
    # Initializer / Instance Attributes
    def __init__(self, tamanho_populacao, dimensao_individuo):
        self.tamanho_populacao = tamanho_populacao
        self.dimensao_individuo = dimensao_individuo
        self.individuos = []

    # Gera populacao aleatoria
    def gera_populacao_aleatoria(self):
        for i in range(0, self.tamanho_populacao):
            individuo = Individuo(self.dimensao_individuo)
            individuo.gera_genotipo_aleatorio()
            self.individuos.append(individuo)
            
    # Calcula fitness de todos individuos
    def calcula_fitnesses(self):
        for individuo in self.individuos:
            individuo.calcula_fitness()
            
    # Ordena a lista individuos pela ordem de fitness dos individuos
    def ordena_por_fitnesses(self):
        self.individuos.sort(key=operator.attrgetter('fitness'))
        
    # Imprime os dados da populacao na tela
    def print_populacao(self):
        for individuo in self.individuos:
            individuo.print_individuo()
        
        
class Selecao:
    pass
    def __init__(self):
        return
    
    @staticmethod
    def seleciona_pais(populacao):
        pais_escolhidos = np.random.randint(populacao.dimensao_individuo, size=2)
        print(pais_escolhidos)

        