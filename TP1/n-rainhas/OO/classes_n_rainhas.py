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
        self.prob_selecao = None
        
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
                    self.fitness += 1
        self.fitness /= 2
        self.fitness = 1/(self.fitness+1)
        

    
    # Imprime os atributos do individuo
    def print_individuo(self):
        print(str(self.genotipo)+', '+str(self.fitness))
        
    
class Populacao:
    # Initializer / Instance Attributes
    def __init__(self, tamanho_populacao, dimensao_individuo):
        self.tamanho_populacao = tamanho_populacao
        self.dimensao_individuo = dimensao_individuo
        self.individuos = []
        self.reta_prob = []

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
    
    def media_fitnesses(self):
        soma_fitnesses = 0
        for individuo in self.individuos:
            soma_fitnesses += individuo.fitness
        media_fitnesses = soma_fitnesses/self.tamanho_populacao
        return media_fitnesses
        
    def melhor_fitness(self):
        return self.individuos[self.tamanho_populacao-1].fitness
        
        
class Selecao:
    pass
    def __init__(self):
        return
    
    @staticmethod
    def calcula_SPF(populacao):
        soma_fitness = 0
        for individuo in populacao.individuos:
            soma_fitness += individuo.fitness
        for individuo in populacao.individuos:
            individuo.prob_selecao = individuo.fitness/soma_fitness
        
        
    @staticmethod    
    def gera_reta_prob(populacao):
        prob_atual = 0;
        i = 0;
        reta_prob = np.empty([populacao.tamanho_populacao, 2])
        for individuo in populacao.individuos:
            prob_atual += individuo.prob_selecao
            reta_prob[i] = [i,prob_atual]
            i += 1
        populacao.reta_prob = reta_prob
        
    @staticmethod
    def seleciona_pais_roleta(populacao):
        prob_pai1 = np.random.rand()
        prob_pai2 = np.random.rand()
        flag_pai1 = 0
        flag_pai2 = 0
        pais = []
        prob_atual = 0
        for i in range(0,populacao.tamanho_populacao):
            prob_atual = populacao.reta_prob[i][1]
            if prob_atual > prob_pai1 and flag_pai1 == 0:
                pais.append(populacao.individuos[i])
                flag_pai1 = 1
            if prob_atual > prob_pai2 and flag_pai2 == 0:
                pais.append(populacao.individuos[i])
                flag_pai2 = 1
            if flag_pai1 + flag_pai2 == 2:
                break
        return(pais)
        
    def seleciona_pais_torneio(populacao, participantes):
        if participantes > populacao.tamanho_populacao:
            participantes = populacao.tamanho_populacao
        index_pais = np.random.randint(low=0, high=populacao.tamanho_populacao, size=participantes)
        index_pais.sort()
        pais = []
        pais.append(populacao.individuos[index_pais[participantes-1]])
        pais.append(populacao.individuos[index_pais[participantes-2]])
        return(pais)
   
     
class Cruzamento:
    pass
    def __init__(self):
        return
        
    def cut_and_crossfill(pais):
        dimensao_individuo = pais[0].dimensao_individuo
        pos_corte = np.random.randint(low=1, high=dimensao_individuo-1)
        pai1 = pais[0].genotipo
        pai2 = pais[1].genotipo
        filho1 = pai1[0:pos_corte]
        filho2 = pai2[0:pos_corte]    
        for i in range(0, dimensao_individuo):
            if(not pai2[i] in filho1):
                filho1 = np.append(filho1, pai2[i])
            if(not pai1[i] in filho2):
                filho2 = np.append(filho2, pai1[i])
                
        filhos = []
        filhos.append(Individuo(dimensao_individuo))
        filhos[0].genotipo = filho1
        filhos.append(Individuo(dimensao_individuo))
        filhos[1].genotipo = filho2
        for individuo in filhos:
            individuo.calcula_fitness()
        return(filhos)
                
        
class Mutacao:
    pass
    def __init__(self):
        return
    
    @staticmethod
    def swap(individuo):
        pos_trocas = np.random.randint(low=0, high=individuo.dimensao_individuo, size=2)
        aux = individuo.genotipo[pos_trocas[0]]
        individuo.genotipo[pos_trocas[0]] = individuo.genotipo[pos_trocas[1]]
        individuo.genotipo[pos_trocas[1]] = aux