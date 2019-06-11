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

class RastriginStrategy(ProblemStrategyAbstract):
    # limites [-5.12, 5.12]
    # f(x*) 0, x* = 0
    def calculate_fitness(self, particle):
        fitness = 10*particle.dimension
        for i in range(particle.dimension):
            fitness += np.power(particle.position[i], 2) - 10*np.cos(2*particle.position[i]*np.pi)
        return fitness

    def initialize_limits(self, dimension):
        inf_limit = [-5.12]*dimension
        sup_limit = [5.12]*dimension
        return(inf_limit, sup_limit)

class Problem:
    def __init__(self, problem_strategy):
        self.problem_strategy = problem_strategy

    def calculate_fitness(self, particle):
        return self.problem_strategy.calculate_fitness(particle)

    def initialize_limits(self, dimension):
        return(self.problem_strategy.initialize_limits(dimension))

# TODO maybe include a index attribute on particle
class Particle:
    def __init__(self, dimension):
        self.dimension = dimension
        self.position = None
        self.velocity = None
        self.fitness = None
        self.best_position = None
        self.best_fitness = None
        return

    def generate_random_particle(self, inf_limit, sup_limit):
        self.best_position = self.position = np.random.uniform(low=inf_limit, high=sup_limit, size=self.dimension)
        self.velocity = np.zeros(self.dimension)
        self.best_fitness = 9999

    def print(self):
        print("position: " + str(self.position) + "\nvelocity: " + str(self.velocity)+"\nfitness: "+str(self.fitness))
   
class Swarm:
    def __init__(self):
        self.particles = []
        return
    
    def generate_random_swarm(self, n_particles, dimension, inf_limit, sup_limit):
        for _ in range(n_particles):
            p = Particle(dimension)
            p.generate_random_particle(inf_limit, sup_limit)
            self.particles.append(p)
        return

    def print(self):
        for particle in self.particles:
            particle.print()
        return

class PSO:
    def __init__(self, **kwargs):
        self.C1 = kwargs.get('C1')
        self.C2 = kwargs.get('C2')
        self.W = kwargs.get('W')
        self.X = kwargs.get('X')
        self.neighborhood_size = kwargs.get('neighborhood_size')
        return

    def get_neighborhood_best_position(self, swarm, particle_index):
        neighborhood = circular_slice(swarm.particles, int(particle_index-self.neighborhood_size), int(particle_index+self.neighborhood_size))
        best_particle = min(neighborhood, key=get_best_fitness)
        return best_particle.position

    def update_particle(self, particle, neighborhood_best_position, inf_limit, sup_limit, problem):
        self.update_velocity(particle, neighborhood_best_position)
        self.update_position(particle, inf_limit, sup_limit)
        self.update_fitness(particle, problem)
        self.update_best_position(particle)

    def update_velocity(self, particle, neighborhood_best_position):
        new_velocity = self.calculate_inertia_component(particle)
        new_velocity = np.add(self.calculate_cognitive_component(particle), new_velocity)
        new_velocity = np.add(self.calculate_social_component(particle, neighborhood_best_position), new_velocity)
        particle.velocity = self.X*new_velocity
    
    def calculate_inertia_component(self, particle):
        inertia_component = self.W*particle.velocity
        return inertia_component

    def calculate_cognitive_component(self, particle):
        cognitive_component = np.subtract(particle.best_position, particle.position)
        r1 = calculate_r(low=0, high=1, size=particle.dimension, r_type='random_array')
        cognitive_component = (self.C1*r1)*(cognitive_component)
        return cognitive_component

    def calculate_social_component(self, particle, neighborhood_best_position):
        r2 = calculate_r(low=0, high=1, size=particle.dimension, r_type='random_array')
        social_component = (self.C2*r2)*(np.subtract(neighborhood_best_position, particle.position))
        return social_component

    def update_position(self, particle, inf_limit, sup_limit):
        particle.position = np.add(particle.position, particle.velocity)
        for index in range(particle.dimension):
            if particle.position[index] < inf_limit[index]:
                particle.position[index] = 2*inf_limit[index] - particle.position[index]
            elif particle.position[index] > sup_limit[index]:
                particle.position[index] = 2*sup_limit[index] - particle.position[index]

    def update_fitness(self, particle, problem):
        particle.fitness = problem.calculate_fitness(particle)

    def update_best_position(self, particle):
        if particle.best_fitness > particle.fitness:
            particle.best_fitness = particle.fitness
            particle.best_position = particle.position

def get_best_fitness(particle):
    return particle.best_fitness

# type can be 'random_array' or 'random_scalar'
def calculate_r(**kwargs):
    low = kwargs.get('low')
    high = kwargs.get('high')
    size = kwargs.get('size')
    r_type = kwargs.get('r_type')
    if r_type == 'random_scalar':
        return np.random.uniform(low=low, high=high, size=1)
    else:
        return np.random.uniform(low=low, high=high, size=size)

def circular_slice(input_list, start_index, stop_index):
    indexes = np.linspace(start_index, stop_index, stop_index-start_index+1).astype(int)
    indexes = indexes%len(input_list)
    return [input_list[index] for index in indexes]

def run_pso():
    pso = PSO(C1=1.5, C2=1.5, W=0.6, X=1, neighborhood_size=2)
    problem = RastriginStrategy()
    dimension = 6
    inf_limit, sup_limit = problem.initialize_limits(dimension);

    n_particles = 50
    max_iterations = 200*dimension

    swarm = Swarm()
    swarm.generate_random_swarm(n_particles, dimension, inf_limit, sup_limit)

    for particle in swarm.particles:
        particle.fitness = problem.calculate_fitness(particle)

    for iteration in range(max_iterations):
        for particle_index in range(len(swarm.particles)):
            pso.update_particle(swarm.particles[particle_index], pso.get_neighborhood_best_position(swarm, particle_index), inf_limit, sup_limit, problem)
    
    best_particle = min(swarm.particles, key=get_best_fitness)
    best_particle.print()
    
run_pso()