# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 21:02:01 2019

@author: Marcio Souza Filho
"""
import numpy as np
import math
import operator

class Codificacao:
    pass
    def __init__(self):
        return
    
    @staticmethod
    def codifica(valor_real, lim_inferior, lim_superior, n_bits):
        if valor_real < lim_inferior:
            valor_real = lim_inferior
        elif valor_real > lim_superior:
            valor_real = lim_superior
            
        delta_x = (lim_superior - lim_inferior)/(2**n_bits-1)
        valor_2_bin = round((valor_real-lim_inferior)/delta_x)
        lixo, valor_bin = str(bin(valor_2_bin)).split('b')
        vetor_bin = [0]*n_bits
        
        tam_valor_bin = len(valor_bin)
        for i in range(0, tam_valor_bin):
            vetor_bin[n_bits-1-i] = int(valor_bin[tam_valor_bin-1-i])
        return vetor_bin

    @staticmethod
    def decodifica(vetor_bin, lim_inferior, lim_superior, n_bits):
        delta_x = (lim_superior - lim_inferior)/(2**n_bits-1)
        valor_real = 0
        for i in range(0,n_bits):
            valor_real += vetor_bin[i] * (2**(n_bits-1-i))
        valor_real = lim_inferior + delta_x*valor_real
        
        if valor_real < lim_inferior:
            valor_real = lim_inferior
        elif valor_real > lim_superior:
            valor_real = lim_superior
        
        return(valor_real)
    
    def bin_2_gray(vetor_bin):
        vetor_gray = []
        vetor_gray.append(vetor_bin[0])
        for i in range(1, len(vetor_bin)):
            vetor_gray.append(vetor_bin[i-1]^vetor_bin[i])
        return(vetor_gray)
        
    def gray_2_bin(vetor_gray):
        vetor_bin = []
        vetor_bin.append(vetor_gray[0])
        for i in range(1, len(vetor_gray)):
            vetor_bin.append(vetor_bin[i-1]^vetor_gray[i])
        return(vetor_bin)
    
class Individuo:
    def __init__(self, bits_individuo, n_variaveis, lim_inferior, lim_superior):
        self.bits_individuo = bits_individuo
        self.n_variaveis = n_variaveis
        self.lim_inferior = lim_inferior
        self.lim_superior = lim_superior
        self.fenotipo = []
        self.genotipo = []
        self.fitness = None
        self.prob_selecao = None
        self.rastrigin_valor = None
        return
        
    # Cria um individuo aleatorio
    def gera_individuo_aleatorio(self):
        for i in range(0,self.n_variaveis):
            self.fenotipo.insert(i, np.random.uniform(self.lim_inferior, self.lim_superior))
            self.genotipo.insert(i, Codificacao.codifica(self.fenotipo[i], self.lim_inferior, self.lim_superior, self.bits_individuo))
        return    
    
    def calcula_fenotipo(self):
        fenotipo = []
        for i in range(0, self.n_variaveis):
            fenotipo.append(Codificacao.decodifica(self.genotipo[i], self.lim_inferior, self.lim_superior, self.bits_individuo))
        self.fenotipo = fenotipo
        return
            
    # Calcula a fitness do individuo    
    def calcula_fitness(self):
        self.fitness = 10*self.n_variaveis
        for i in range(0, self.n_variaveis):
            self.fitness += (np.power(self.fenotipo[i], 2) - 10*np.cos(2*self.fenotipo[i]*math.pi))
        self.rastrigin_valor = self.fitness
        self.fitness = 1/(self.fitness + 1)
        return
    
    # Imprime os atributos do individuo
    def print_individuo(self):
        print(str(self.fenotipo)+', '+str(len(self.genotipo))+', '+str(self.rastrigin_valor))
        return
        
    
class Populacao:
    # Initializer / Instance Attributes
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.individuos = []
        self.reta_prob = []
        return 
    
    # Gera populacao aleatoria
    def gera_populacao_aleatoria(self, bits_individuo, n_variaveis, lim_inferior, lim_superior):
        for i in range(0, self.tamanho_populacao):
            individuo = Individuo(bits_individuo, n_variaveis, lim_inferior, lim_superior)
            individuo.gera_individuo_aleatorio()
            individuo.calcula_fitness()
            self.individuos.append(individuo)
        return
            
    # Calcula fitness de todos individuos
    def calcula_fitnesses(self):
        for individuo in self.individuos:
            individuo.calcula_fitness()
        return
        
    # Ordena a lista individuos pela ordem de fitness dos individuos
    def ordena_por_fitnesses(self):
        self.individuos.sort(key=operator.attrgetter('fitness'))
        return
        
    # Imprime os dados da populacao na tela
    def print_populacao(self):
        for individuo in self.individuos:
            individuo.print_individuo()
        return
    
    def fitnesses_media(self):
        soma_fitnesses = 0
        for individuo in self.individuos:
            soma_fitnesses += individuo.fitness
        media_fitnesses = soma_fitnesses/self.tamanho_populacao
        return media_fitnesses
        
    def fitness_melhor_individuo(self):
        return self.individuos[self.tamanho_populacao-1].fitness
        
        
class Selecao:
    pass
    def __init__(self):
        return
    
    @staticmethod
    def calcula_probs_SPF(populacao):
        soma_fitness = 0
        for individuo in populacao.individuos:
            soma_fitness += individuo.fitness
        for individuo in populacao.individuos:
            individuo.prob_selecao = individuo.fitness/soma_fitness
        return
    
    @staticmethod
    def calcula_probs_ranking(populacao, inclinacao_reta):
        s = inclinacao_reta
        tam = populacao.tamanho_populacao
        i = 0
        for individuo in populacao.individuos:
            individuo.prob_selecao = (2-s)/tam + (2*(i)*(s-1))/(tam*(tam-1))
            i += 1
        
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
        return
        
    @staticmethod
    def seleciona_pais_roleta(populacao):
        prob_pai1 = np.random.uniform(0,1)
        prob_pai2 = np.random.uniform(0,1)
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
        
    def crossover_1_ponto(pais):
        bits_individuo = pais[0].bits_individuo
        n_variaveis = pais[0].n_variaveis
        lim_inferior = pais[0].lim_inferior
        lim_superior = pais[0].lim_superior
        filhos = [Individuo(bits_individuo, n_variaveis, lim_inferior, lim_superior), Individuo(bits_individuo, n_variaveis, lim_inferior, lim_superior)]
        for i in range(0,n_variaveis):
            pos_corte = np.random.randint(low=1, high=bits_individuo-1)
            pai1 = pais[0].genotipo[i]
            pai2 = pais[1].genotipo[i]
            
            filho1 = pai1[0:pos_corte]
            filho1[pos_corte:bits_individuo] = pai2[pos_corte:bits_individuo]
            filho2 = pai2[0:pos_corte]    
            filho2[pos_corte:bits_individuo] = pai1[pos_corte:bits_individuo]
            
            filhos[0].genotipo.append(filho1)
            filhos[1].genotipo.append(filho2)
        
        for individuo in filhos:
            individuo.calcula_fenotipo()
            individuo.calcula_fitness()
        return(filhos)
                
        
class Mutacao:
    pass
    def __init__(self):
        return
        
    @staticmethod
    def bit_flip(individuo, prob_mutacao):
        for var in range(0,individuo.n_variaveis):
            genotipo = individuo.genotipo[var]
            for i in range(0, individuo.bits_individuo):
                if prob_mutacao > np.random.uniform(0, 1):
                    if genotipo[i] == 0:
                        genotipo[i] = 1
                    else:
                        genotipo[i] = 0
            individuo.genotipo[var] = genotipo
        return