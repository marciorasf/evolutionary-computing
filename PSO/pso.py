import matplotlib.pyplot as plt
import numpy as np
import abc
import operator
from random import choice, sample

class ProblemaStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calcula_fitness(self, particula):
        """Required Method"""

    @abc.abstractmethod
    def inicializa_limites(self, limite_inferior, limite_superior, dimensao):
        """Required Method"""

    @abc.abstractmethod
    def set_melhor_solucao(self, populacao):
        """Required Method"""

class RastriginStrategy(ProblemaStrategyAbstract):
    # limites [-5.12, 5.12]
    # f(x*) 0, x* = 0
    def calcula_fitness(self, particula):
        particula.fitness = 10*particula.dimensao
        for i in range(particula.n_variaveis):
            particula.fitness += (np.power(particula.variaveis[i], 2) - 10*np.cos(2*particula.variaveis[i]*np.pi))

    def inicializa_limites(self, dimensao):
        lim_inferior = [-5.12]*n_variaveis
        lim_superior = [5.12]*n_variaveis
        return(lim_inferior, lim_superior)

    def set_melhor_solucao(self, populacao):
        populacao.melhor_solucao = populacao.solucao_menor_fitness()


class Problema:
    def __init__(self, problema_strategy):
        self.problema_strategy = problema_strategy

    def calcula_fitness(self, individuo):
        self.problema_strategy.calcula_fitness(individuo)

    def inicializa_limites(self, n_variaveis):
        return(self.problema_strategy.inicializa_limites(n_variaveis))

    def set_melhor_solucao(self, populacao):
        return(self.problema_strategy.set_melhor_solucao(populacao))


class Particula:
    def __init__(self, dimensao):
        self.dimensao = dimensao
        self.posicao = []
        self.fitness = None
        self.velocidade = []
        self.melhor_posicao = None
        self.melhor_fitness = None
        return

    def gera_particula_aleatoria(self, lim_inferior, lim_superior):
        for i in range(self.dimensao):
            self.posicao.append(np.random.uniform(lim_inferior[i], lim_superior[i]))

    def print(self):
        print(self.posicao)
   

class Enxame:
    def __init__(self):
        self.particulas = []
        self.melhor_posicao = None
        self.printmelhor_fitness = None
        return
    
    def gera_particulas_aleatorias(self, n_particulas, dimensao, lim_inferior, lim_superior):
        for _ in range(n_particulas):
            p = Particula(dimensao)
            p.gera_particula_aleatoria(lim_inferior, lim_superior)
            self.particulas.append(p)
        return

    def print(self):
        for particula in self.particulas:
            particula.print()
        return

def run_pso():
    dimensao = 2
    lim_inferior = [-2,-2]
    lim_superior = [2, 2]
    n_particulas = 4
    max_iteracoes = 10
    swarm = Enxame()
    swarm.gera_particulas_aleatorias(n_particulas, dimensao, lim_inferior, lim_superior)

    iteracoes = 0
    while iteracoes < max_iteracoes:
        iteracoes += 1
        print("aqui dentro")
    return

run_pso()