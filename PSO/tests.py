import pso
import numpy as np

def generate_particle_test():
    dimension = 4
    inf_limit = []
    sup_limit = []
    for i in range(1, dimension+1):
        inf_limit.append(-i)
        sup_limit.append(i)

    particle = pso.Particle(dimension)
    particle.generate_random_particle(inf_limit, sup_limit)
    particle.print()

def generate_swarm_test():
    dimension = 4
    n_particles = 3
    inf_limit = []
    sup_limit = []
    for i in range(1, dimension+1):
        inf_limit.append(-i)
        sup_limit.append(i)

    swarm = pso.Swarm()
    swarm.generate_random_swarm(n_particles, dimension, inf_limit, sup_limit)
    swarm.print()

def pso_tests():
    dimension = 4
    n_particles = 3
    inf_limit = []
    sup_limit = []
    problem = pso.Problem(pso.RastriginStrategy())
    for i in range(1, dimension+1):
        inf_limit.append(-i)
        sup_limit.append(i)

    swarm = pso.Swarm()
    swarm.generate_random_swarm(n_particles, dimension, inf_limit, sup_limit)
    for particle in swarm.particles:
        particle.position = np.random.uniform(low=0, high=1, size=particle.dimension)
        particle.velocity = np.random.uniform(low=0, high=1, size=particle.dimension)
        particle.fitness = problem.calculate_fitness(particle)
    pso_object = pso.PSO(1,1,0.5,1,2)
    print(pso_object.calculate_inertia_component(swarm.particles[0]))
    print(pso_object.calculate_memory_component(swarm.particles[0]))
    print(pso_object.calculate_cooperation_component(swarm.particles[0], pso_object.get_neighborhood_best_position(swarm,0)))
    pso_object.update_velocity(swarm.particles[0], pso_object.get_neighborhood_best_position(swarm,0))
    swarm.particles[0].print()

pso_tests()