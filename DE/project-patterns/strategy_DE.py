import abc  # Python's built-in abstract class library
import numpy as np


class FitnessStrategyAbstract(object):
    """You do not need to know about metaclasses.
    Just know that this is how you define abstract
    classes in Python."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calcula_fitness(self):
        """Required Method"""

class SomaStrategy(FitnessStrategyAbstract):
    def calcula_fitness(self, ind):
        ind.fitness = 0
        for i in range(0, ind.n_variaveis):
            ind.fitness += ind.variaveis[i]

class MultiplicaStrategy(FitnessStrategyAbstract):
    def calcula_fitness(self, ind):
        ind.fitness = 1
        for i in range(0, ind.n_variaveis):
            ind.fitness *= ind.variaveis[i]

class Times10Strategy(FitnessStrategyAbstract):
    def calcula_fitness(self, ind):
        ind.fitness = 0
        for i in range(0, ind.n_variaveis):
            ind.fitness += 10*ind.variaveis[i]


class Individuo:
    def __init__(self, n_variaveis):
        self.variaveis = []  # Variaveis do individuo
        self.n_variaveis = n_variaveis
        self.fitness = None

    def gera_individuo_aleatorio(self, lim_inferior, lim_superior):
        for i in range(self.n_variaveis):
            self.variaveis.append(np.random.uniform(lim_inferior[i], lim_superior[i]))

    def print(self):
        print(str(self.variaveis)+', '+str(self.fitness))


class Fitness:
    def __init__(self, fitness_strategy):
        self.fitness_strategy = fitness_strategy

    def calcula_fitness(self, individuo):
        self.fitness_strategy.calcula_fitness(individuo)


soma = SomaStrategy()   
multiplica = MultiplicaStrategy()
times = Times10Strategy()

fit_soma = Fitness(soma)
fit_multiplica = Fitness(multiplica)
fit_times = Fitness(times)

ind = Individuo(2)
ind.variaveis = [2,5]
ind.print()
fit_soma.calcula_fitness(ind)
ind.print()
fit_multiplica.calcula_fitness(ind)
ind.print()
fit_times.calcula_fitness(ind)
ind.print()