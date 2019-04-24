# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:20:08 2019

@author: Marcio Souza Filho
"""

import numpy as np
import operator
import matplotlib.pyplot as plt

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
    
    @staticmethod
    def bin_2_gray(vetor_bin):
        vetor_gray = []
        vetor_gray.append(vetor_bin[0])
        for i in range(1, len(vetor_bin)):
            vetor_gray.append(vetor_bin[i-1]^vetor_bin[i])
        return(vetor_gray)
        
    @staticmethod    
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
        self.var_real = []
        self.var_bin = []
        self.prob_selecao = None
        self.rastrigin_valor = None
        return
        
    # Cria um individuo aleatorio
    def gera_individuo_aleatorio(self):
        for i in range(0,self.n_variaveis):
            self.var_real.insert(i, np.random.uniform(self.lim_inferior, self.lim_superior))
            self.var_bin.insert(i, Codificacao.codifica(self.var_real[i], self.lim_inferior, self.lim_superior, self.bits_individuo))
        return    
    
    # Calcula as variaveis reais a partir das variaveis em binario
    def calcula_var_real(self):
        var_real = []
        for i in range(0, self.n_variaveis):
            var_real.append(Codificacao.decodifica(self.var_bin[i], self.lim_inferior, self.lim_superior, self.bits_individuo))
        self.var_real = var_real
        return
            
    # Calcula a funcao rastrigin para as variaveis do individuo    
    def calcula_rastrigin(self):
        self.rastrigin_valor = 10*self.n_variaveis
        for i in range(0, self.n_variaveis):
            self.rastrigin_valor += (np.power(self.var_real[i], 2) - 10*np.cos(2*self.var_real[i]*np.pi))
        self.rastrigin_valor = self.rastrigin_valor
        return
    
    # Imprime os atributos do individuo
    def print_individuo(self):
        print(str(self.var_real)+', '+str(self.rastrigin_valor))
        return

class Populacao:
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
            individuo.calcula_rastrigin()
            self.individuos.append(individuo)
        return
            
    # Calcula fitness de todos individuos
    def calcula_rastrigin(self):
        for individuo in self.individuos:
            individuo.calcula_rastrigin()
        return
        
     # Calcula fitness de todos individuos
    def calcula_var_real(self):
        for individuo in self.individuos:
            individuo.calcula_var_real()
        return
    
    # Ordena a lista individuos pela ordem do valor da rastrigin dos individuos
    def ordena_por_rastrigin(self):
        self.individuos.sort(key=operator.attrgetter('rastrigin_valor'), reverse=True)
        return
        
    # Imprime os dados da populacao na tela
    def print_populacao(self):
        for individuo in self.individuos:
            individuo.print_individuo()
        return
        
    # retorna o melhor individuo desde que a populacao esteja ordenada
    def melhor_individuo(self):
        return self.individuos[self.tamanho_populacao-1]
    
class Selecao:
    pass
    def __init__(self):
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
        
    @staticmethod    
    def seleciona_pais_torneio(populacao, participantes):
        if participantes > populacao.tamanho_populacao:
            participantes = populacao.tamanho_populacao
        index_pais1 = np.random.randint(low=0, high=populacao.tamanho_populacao, size=participantes)
        index_pais2 = np.random.randint(low=0, high=populacao.tamanho_populacao, size=participantes)
        index_pais1.sort()
        index_pais2.sort()
        pais = []
        pais.append(populacao.individuos[index_pais1[participantes-1]])
        pais.append(populacao.individuos[index_pais2[participantes-1]])
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
            pai1 = pais[0].var_bin[i]
            pai2 = pais[1].var_bin[i]
            filho1 = pai1[0:pos_corte]
            filho1[pos_corte:bits_individuo] = pai2[pos_corte:bits_individuo]
            filho2 = pai2[0:pos_corte]    
            filho2[pos_corte:bits_individuo] = pai1[pos_corte:bits_individuo]
            filhos[0].var_bin.append(filho1)
            filhos[1].var_bin.append(filho2)
            
        for individuo in filhos:
            individuo.calcula_var_real()
            individuo.calcula_rastrigin()
        return(filhos)
    
class Mutacao:
    pass
    def __init__(self):
        return
        
    @staticmethod
    def bit_flip(individuo, prob_mutacao):
        for var in range(0,individuo.n_variaveis):
            var_bin = individuo.var_bin[var]
            for i in range(0, individuo.bits_individuo):
                if prob_mutacao > np.random.uniform(0, 1):
                    if var_bin[i] == 0:
                        var_bin[i] = 1
                    else:
                        var_bin[i] = 0
            individuo.var_bin[var] = var_bin
        return    


n_bits = 16
n_variaveis = 4
n_geracoes = 200
limite_inferior = -5.12
limite_superior = 5.12
tam_pop = 100
inclinacao_reta = 2

participantes_torneio = 2
prob_mutacao = 0.03
prob_cruzamento = 0.9
prob_torneio = 0.5

populacao = Populacao(tam_pop)
populacao.gera_populacao_aleatoria(n_bits, n_variaveis, limite_inferior, limite_superior)
populacao.ordena_por_rastrigin()

for ger in range(0,n_geracoes):
    print('geracao '+str(ger))
    populacao_nova = Populacao(tam_pop)

    Selecao.calcula_probs_ranking(populacao,inclinacao_reta)
    Selecao.gera_reta_prob(populacao)
    
    for i in range(0, int(tam_pop/2)):
        # Selecao dos pais
        if prob_torneio > np.random.uniform(0,1):
            pais = Selecao.seleciona_pais_torneio(populacao, participantes_torneio)
        else:
            pais = Selecao.seleciona_pais_roleta(populacao)
        
        # Cruzamento dos pais escolhidos
        if prob_cruzamento > np.random.uniform(0,1):
            filhos = Cruzamento.crossover_1_ponto(pais)
        else:
            # Necessario fazer isso para instanciar novos objetos
            filhos = [Individuo(n_bits, n_variaveis, limite_inferior, limite_superior),Individuo(n_bits, n_variaveis, limite_inferior, limite_superior)]
            filhos[0].var_bin = pais[0].var_bin
            filhos[1].var_bin = pais[1].var_bin
            
        # Mutacao dos filhos
        # A prob de mutacao e utilizada dentro do metodo bit_flip
        for individuo in filhos:
            Mutacao.bit_flip(individuo, prob_mutacao)
        
        for individuo in filhos:
            populacao_nova.individuos.append(individuo)
    
    populacao_nova.calcula_var_real()
    populacao_nova.calcula_rastrigin()
    populacao_nova.ordena_por_rastrigin()
    melhor_pop_nova = populacao_nova.melhor_individuo()
    melhor_pop_antiga = populacao.melhor_individuo()
    if melhor_pop_antiga.rastrigin_valor < melhor_pop_nova.rastrigin_valor:
        populacao_nova.individuos[0] = melhor_pop_antiga
        populacao_nova.ordena_por_rastrigin()
    populacao = populacao_nova
melhor = populacao.melhor_individuo()
melhor.print_individuo()