import matplotlib.pyplot as plt
import numpy as np
import abc
import operator
from random import choice, sample

class ProblemStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate_fitness(self, particle):
        """Required Method"""

    @abc.abstractmethod
    def initialize_limits(self, inf_limit, sup_limit, dimension):
        """Required Method"""

    @abc.abstractmethod
    def set_best_solution(self, swarm):
        """Required Method"""

class RastriginStrategy(ProblemStrategyAbstract):
    # limites [-5.12, 5.12]
    # f(x*) 0, x* = 0
    def calculate_fitness(self, particle):
        particle.fitness = 10*particle.dimension
        for i in range(particle.dimension):
            particle.fitness += (np.power(particle.variaveis[i], 2) - 10*np.cos(2*particle.variaveis[i]*np.pi))

    def initialize_limits(self, dimension):
        inf_limit = [-5.12]*dimension
        sup_limit = [5.12]*dimension
        return(inf_limit, sup_limit)

    def set_best_solution(self, swarm):
        swarm.melhor_solucao = swarm.solucao_menor_fitness()


class Problem:
    def __init__(self, problem_strategy):
        self.problem_strategy = problem_strategy

    def calculate_fitness(self, particle):
        self.problem_strategy.calculate_fitness(particle)

    def initialize_limits(self, dimension):
        return(self.problem_strategy.initialize_limits(dimension))

    def set_best_solution(self, swarm):
        return(self.problem_strategy.set_best_solution(swarm))


class Particle:
    def __init__(self, dimension):
        self.dimension = dimension
        self.position = []
        self.velocity = []
        self.fitness = None
        self.best_position = None
        self.best_fitness = None
        return

    def generate_random_particle(self, inf_limit, sup_limit):
        for i in range(self.dimension):
            self.position.append(np.random.uniform(inf_limit[i],sup_limit[i]))
            self.velocity.append(0)

    def print(self):
        print(self.position)
   

class Swarm:
    def __init__(self):
        self.particulas = []
        self.best_position = None
        self.best_fitness = None
        return
    
    def gera_particulas_aleatorias(self, n_particles, dimension, inf_limit, sup_limit):
        for _ in range(n_particles):
            p = Particle(dimension)
            p.generate_random_particle(inf_limit, sup_limit)
            self.particulas.append(p)
        return

    def print(self):
        for particle in self.particulas:
            particle.print()
        return

class PSO:
    def __init__(self):
        self.pso = None

    def calculate_social_component(self, swarm, particle):
        social_component = swarm.best_position - particle.position
        return social_component

    def calculate_velocities(self, swarm, pso):
        velocities = []
        for particle in swarm:
            new_velocity = particle.velocity + (particle.best_position - particle.position) + (pso.calculate_social_component(swarm, particle))
            velocities.append(new_velocity)
        return velocities

def run_pso():
    pso = PSO()
    dimension = 2
    inf_limit, sup_limit = [2, 2]
    n_particles = 4
    max_iterations = 10
    swarm = Swarm()
    swarm.gera_particulas_aleatorias(n_particles, dimension, inf_limit, sup_limit)

    velocities = []
    velocities = pso.calculate_velocities(swarm, pso)
    print(velocities)

    iterations = 0
    while iterations < max_iterations:
        iterations += 1
        swarm.print()
        print("aqui dentro")
    return

run_pso()