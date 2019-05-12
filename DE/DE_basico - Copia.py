# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:43:54 2019

@author: Marcio Souza Filho

!!!!!! A funcao que executa o algoritmo genetico esta no final do codigo com nome GA
"""
import matplotlib.pyplot as plt
import numpy as np
import operator
from random import choice, sample


class Individuo:
    def __init__(self, n_variaveis):
        self.variaveis = []  # Variaveis do individuo
        self.n_variaveis = n_variaveis
        self.fitness = None
        return

    def gera_individuo_aleatorio(self, lim_inferior, lim_superior):
        for i in range(self.n_variaveis):
            self.variaveis.append(np.random.uniform(lim_inferior[i], lim_superior[i]))
        return

    def calcula_fitness(self):
        self.fitness = 10*self.n_variaveis
        for i in range(0, self.n_variaveis):
            self.fitness += (np.power(self.variaveis[i], 2) - 10*np.cos(2 * self.variaveis[i] * np.pi))
        return

    def print(self):
        print(str(self.variaveis)+', '+str(self.fitness))
        return


class Populacao:
    def __init__(self):
        self.individuos = []
        self.reta_prob = []
        return

    def gera_populacao_aleatoria(self, n_variaveis, tam_pop, lim_inferior, lim_superior):
        for _ in range(tam_pop):
            individuo = Individuo(n_variaveis)
            individuo.gera_individuo_aleatorio(lim_inferior, lim_superior)
            self.individuos.append(individuo)
        return

    def calcula_fitness(self):
        for individuo in self.individuos:
            individuo.calcula_fitness()

    # Ordena a populacao pelo fitness em ordem crescente
    def ordena(self):
        self.individuos.sort(key=operator.attrgetter('fitness'), reverse=False)
        return
    
    def menor_fitness(self):
        return self.individuos[0].fitness

    def maior_fitness(self):
        return self.individuos[-1].fitness

    def print(self):
        for individuo in self.individuos:
            individuo.print()
        return


class DE:
    @staticmethod
    def seleciona_individuos(populacao):
        individuos = sample(populacao.individuos, 3)
        return individuos

    @staticmethod
    def mutacao(individuos, fator_escala):
        n_variaveis = len(individuos[0].variaveis)
        novo_individuo = Individuo(n_variaveis)
        n_var = len(individuos[0].variaveis)
        for i in range(n_var):
            x = individuos[0].variaveis[i] + fator_escala * (individuos[1].variaveis[i]-individuos[2].variaveis[i])
            novo_individuo.variaveis.append(x)
        return novo_individuo

    # Confere se as solucoes mutantes estao saindo dos limites, caso estejam reflete
    @staticmethod
    def reflexao_limites(mutante, limite_inferior, limite_superior):
        variaveis = mutante.variaveis
        for i in range (mutante.n_variaveis):
            if variaveis[i] < limite_inferior[i]:
                variaveis[i] = limite_inferior[i] - (variaveis[i] - limite_inferior[i])
            elif variaveis[i] > limite_superior[i]:
                variaveis[i] = limite_superior[i] - (variaveis[i] - limite_superior[i])
        return

    @staticmethod    
    def recombinacao(sol_original, sol_mutante, prob_mutante):
        n_variaveis = sol_original.n_variaveis
        delta = np.random.randint(low=0, high=n_variaveis)
        for i in range(n_variaveis):
            if not(prob_mutante > np.random.rand() or i == delta) :
                sol_mutante.variaveis[i] = sol_original.variaveis[i]
        return

    @staticmethod
    def selecao_sobreviventes(pop_original, pop_mutante, tam_pop):
        for ind in range(tam_pop):
            if pop_original.individuos[ind].fitness > pop_mutante.individuos[ind].fitness:
                pop_original.individuos[ind] = pop_mutante.individuos[ind]

def run_DE():
    n_variaveis = 10
    tam_pop = 50
    max_iteracoes = 200*n_variaveis

    # Os limites devem ter mesma dimensao que os vetores solucao
    lim_inferior = [-5.12]*n_variaveis
    lim_superior = [5.12]*n_variaveis

    if len(lim_inferior) != len(lim_superior):
        print('lim_inferior e lim_superior tem dimensoes diferentes')
        return
    elif len(lim_inferior) != n_variaveis:
        print('dimensao dos limites e diferente da dimensao das variaveis')
        return

    precisao = 1e-12

    fator_escala = 0.4
    prob_mutante = 0.5

    # Inicializa populacao
    populacao = Populacao()
    populacao.gera_populacao_aleatoria(n_variaveis, tam_pop, lim_inferior, lim_superior)
    populacao.calcula_fitness()

    populacao_mutante = Populacao()
    melhor_fitness = populacao.individuos[0].fitness
    iteracao = 0
    while (iteracao < max_iteracoes) and (melhor_fitness > precisao):
        iteracao += 1
        for ind in range(tam_pop):
            selecionados = DE.seleciona_individuos(populacao)
            mutante = DE.mutacao(selecionados, fator_escala)
            DE.reflexao_limites(mutante,lim_inferior,lim_superior)
            DE.recombinacao(populacao.individuos[ind], mutante,  prob_mutante)
            mutante.calcula_fitness()
            populacao_mutante.individuos.append(mutante)
        DE.selecao_sobreviventes(populacao, populacao_mutante, tam_pop)
        populacao_mutante.individuos.clear()
        populacao.ordena()
        melhor_fitness_iteracao = populacao.menor_fitness()
        if melhor_fitness_iteracao < melhor_fitness:
            melhor_fitness = melhor_fitness_iteracao

    print('melhor solucao = ' + str(melhor_fitness) + 'em ' + str(iteracao) +' iteracoes')
    return

run_DE()