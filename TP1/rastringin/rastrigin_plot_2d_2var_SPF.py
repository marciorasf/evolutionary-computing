# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:20:08 2019

@author: Marcio Souza Filho
"""

import numpy as np
import operator
import matplotlib.pyplot as plt

class Rastrigin():

    def __get_error_surface_volume(self, *X, **kwargs):
        A = kwargs.get('A', 10)
        return A + sum([(np.square(x) - A * np.cos(2 * np.pi * x)) for x in X])


    def evaluate(self, position):
        A = 10
        return A + np.sum([(np.square(x) - A * np.cos(2 * np.pi * x)) for x in position])

    
    def get_surface(self, resolution=200, bound=5.12):
        
        X = np.linspace(-bound, bound, resolution)    
        Y = np.linspace(-bound, bound, resolution)  
        
        X, Y = np.meshgrid(X, Y)
        Z = self.__get_error_surface_volume(X, Y, A=10)
        return np.stack((X, Y, Z))

# A way of plotting each step of the optimisation process.
def plot(surface, positions, best_fitness, best_position, iteration):
    plt.cla()
    
    # Plot the feature / error surface.
    plt.pcolormesh(surface[0], surface[1], surface[2])

    # Plot all of the genepool.
    x, y = zip(*positions)
    plt.scatter(x, y, 1, 'k', edgecolors='face')
    
    # Plot the best gene.
    plt.scatter(best_position[0], best_position[1], 20, 'w', edgecolors='face')

    # Add the title to the plot.
    title = "iteration {}, fitness {}".format(iteration, best_fitness)
    plt.title(title)

# Classe com as funcoes para transformar binario <-> real
class Codificacao:
    pass
    def __init__(self):
        return
    
    # Retorna a representacao binaria de um valor real utilizando n_bits entre os limites passados como parametro
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

    # Retorna um numero real equivalente ao numero binario passado
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
    
    # Converte um numero em codigo binario padrao para codigo de gray
    @staticmethod
    def bin_2_gray(vetor_bin):
        vetor_gray = []
        vetor_gray.append(vetor_bin[0])
        for i in range(1, len(vetor_bin)):
            vetor_gray.append(vetor_bin[i-1]^vetor_bin[i])
        return(vetor_gray)
        
    # Converte um numero representado em codigo de gray para binario
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
        self.fitness = None
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
    
    # Calcula as variaveis binarias a partir das variaveis reais
    def calcula_var_bin(self):
        var_bin = []
        for i in range(0, self.n_variaveis):
            var_bin.append(Codificacao.codifica(self.var_real[i], self.lim_inferior, self.lim_superior, self.bits_individuo))
        self.var_bin = var_bin
        return
            
    # Calcula a funcao rastrigin para as variaveis do individuo    
    def calcula_rastrigin_fitness(self):
        self.rastrigin_valor = 10*self.n_variaveis
        for i in range(0, self.n_variaveis):
            self.rastrigin_valor += (np.power(self.var_real[i], 2) - 10*np.cos(2*self.var_real[i]*np.pi))
        self.rastrigin_valor = self.rastrigin_valor
        self.fitness = 1/self.rastrigin_valor+0.000001
        return
    
    # Imprime os atributos do individuo
    def print_individuo(self):
        print(str(self.rastrigin_valor)+', '+str(self.fitness)+', '+str(self.var_real))
        return


class Populacao:
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.individuos = []
        self.reta_prob = []
        return 
    
    # Gera uma populacao aleatoria
    def gera_populacao_aleatoria(self, bits_individuo, n_variaveis, lim_inferior, lim_superior):
        for i in range(0, self.tamanho_populacao):
            individuo = Individuo(bits_individuo, n_variaveis, lim_inferior, lim_superior)
            individuo.gera_individuo_aleatorio()
            individuo.calcula_rastrigin_fitness()
            self.individuos.append(individuo)
        return
            
    # Calcula fitness de todos individuos da populacao
    def calcula_rastrigin_fitness(self):
        for individuo in self.individuos:
            individuo.calcula_rastrigin_fitness()
        return
        
    # Calcula fitness de todos individuos da populacao
    def calcula_var_real(self):
        for individuo in self.individuos:
            individuo.calcula_var_real()
        return
    
    # Dado que o individuo possui as variaveis reais, calcula as representacoes binarias das variaveis
    def calcula_var_bin(self):
        for individuo in self.individuos:
            individuo.calcula_var_bin()
        return
    
    # Ordena a lista individuos pela ordem do valor da rastrigin dos individuos, ordem decrescente
    def ordena_por_fitness(self):
        self.individuos.sort(key=operator.attrgetter('fitness'))
        return
    
    # Ordena a lista individuos pela ordem do valor da rastrigin dos individuos, ordem decrescente
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
    def calcula_probs_SPF(populacao):
        soma_fitnesses = 0
        for individuo in populacao.individuos:
            soma_fitnesses += individuo.fitness
        for individuo in populacao.individuos:
            individuo.prob_selecao = individuo.fitness/soma_fitnesses
    
    # Calcula as probabilidades de selecao para cada individuo da populacao baseado no rankeamento
    # E necessario que a populacao esteja ordenada
    @staticmethod
    def calcula_probs_ranking(populacao, inclinacao_reta):
        s = inclinacao_reta
        tam = populacao.tamanho_populacao
        i = 0
        for individuo in populacao.individuos:
            individuo.prob_selecao = (2-s)/tam + (2*(i)*(s-1))/(tam*(tam-1))
            i += 1
        
    # Gera a reta de probabilidade utilizada pela roleta
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
        
    # Seleciona 2 pais uutilizando o metodo da roleta
    # Requer que a reta_prob tenha sido gerada
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
        
    # Seleciona dois pais utilizando torneio
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
        
    # Crossover binario utilizando um ponto de corte aleatorio
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
            individuo.calcula_rastrigin_fitness()
        return(filhos)
    
    # Crossover binario uniforme
    # A cada bit do filho, e' gerado um numero aleatorio para decidir se o bit sera do pai1 ou pai2
    def crossover_uniforme(pais):
        bits_individuo = pais[0].bits_individuo
        n_variaveis = pais[0].n_variaveis
        lim_inferior = pais[0].lim_inferior
        lim_superior = pais[0].lim_superior
        filhos = [Individuo(bits_individuo, n_variaveis, lim_inferior, lim_superior), Individuo(bits_individuo, n_variaveis, lim_inferior, lim_superior)]
        for i in range(0,n_variaveis):
            pai1 = pais[0].var_bin[i]
            pai2 = pais[1].var_bin[i]
            filho1 = []
            filho2 = []
            for j in range(0,bits_individuo):
                if np.random.uniform(0,1) > 0.5:
                    filho1.append(pai1[j])
                    filho2.append(pai2[j])
                else:
                    filho2.append(pai1[j])
                    filho1.append(pai2[j])
                    
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
        
    # Mutacao binaria bit flip
    # A mutacao e' feita para cada bit
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
    
def run():
    n_bits = 16
    # So pode ter 2 variaveis para que seja possivel o plot
    n_variaveis = 2
    n_geracoes = 40
    lim_inf = -5.12
    lim_sup = 5.12
    tam_pop = 100
    prob_mutacao = 2/n_bits
    participantes_torneio = 2
    prob_cruzamento = 1
    prob_torneio = 0.5
    passo_mut = int(n_geracoes*0.1)
    if passo_mut < 1:
        passo_mut = 1
    elitismo = 0.8
    if elitismo > 1:
        elitismo = 1
    tam_elite = int(tam_pop*elitismo)
    
    function = Rastrigin()
    surface = function.get_surface()

    populacao = Populacao(tam_pop)
    populacao.gera_populacao_aleatoria(n_bits, n_variaveis, lim_inf, lim_sup)
    populacao.ordena_por_fitness()
    
    for ger in range(0,n_geracoes):
        Selecao.calcula_probs_SPF(populacao)
        Selecao.gera_reta_prob(populacao)
        populacao_filhos = Populacao(tam_pop)
        if ger%passo_mut == 0:
            prob_mutacao = prob_mutacao*0.85
            
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
                filhos = [Individuo(n_bits, n_variaveis, lim_inf, lim_sup),Individuo(n_bits, n_variaveis, lim_inf, lim_sup)]
                filhos[0].var_bin = pais[0].var_bin
                filhos[1].var_bin = pais[1].var_bin
            for individuo in filhos:
                populacao_filhos.individuos.append(individuo)

        # Mutacao dos filhos
        # A prob de mutacao e utilizada dentro do metodo bit_flip
        for individuo in populacao_filhos.individuos:
            Mutacao.bit_flip(individuo, prob_mutacao)
            individuo.calcula_var_real()
            individuo.calcula_rastrigin_fitness()
        
        populacao_filhos.ordena_por_rastrigin()
        populacao.ordena_por_rastrigin()
        
        f_add = 1
        p_add = 1
        for k in range(0, tam_elite):
            if populacao.individuos[tam_pop-p_add].rastrigin_valor < populacao_filhos.individuos[tam_pop-f_add].rastrigin_valor:
                p_add += 1
            else:
                populacao.individuos.append(populacao_filhos.individuos[tam_pop-f_add])
                f_add += 1
        f_add -= 1
        
        populacao.ordena_por_rastrigin()
        
        del populacao.individuos[0:tam_pop-tam_elite+f_add]
        
        indexes_non_elite = np.arange(tam_elite, tam_pop)
        np.random.shuffle(indexes_non_elite)
        indexes_non_elite = indexes_non_elite[0:tam_pop-tam_elite]
        
        for k in range(0, tam_pop-tam_elite):
            populacao.individuos.append(populacao_filhos.individuos[indexes_non_elite[k]])
           
        populacao.ordena_por_rastrigin()
        
        # Get the gene pool and the fitnesses.
        positions = []
        fitnesses = []
        for individuo in populacao.individuos:
            positions.append(individuo.var_real)
            fitnesses.append(individuo.rastrigin_valor)
        
        # Get the best gene
        melhor_individuo = populacao.melhor_individuo()
        best_position = melhor_individuo.var_real
        best_fitness = melhor_individuo.rastrigin_valor
    
        # Plot the optimsation
        plot(surface, positions, best_fitness, best_position, ger)
        if ger % 1 == 0:
            plt.show()
            
    melhor = populacao.melhor_individuo()
    melhor.print_individuo()
    print('geracoes = '+str(ger))
    return(melhor.rastrigin_valor)

run()
