# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:43:54 2019

@author: Marcio Souza Filho

!!!!!! A funcao que executa o algoritmo genetico esta no final do codigo com nome GA
"""
import matplotlib.pyplot as plt
import numpy as np
import operator

class Individuo:
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
        
    
    # Imprime os atributos do individuo. Usada apenas para testes
    def print_individuo(self):
        print(str(self.genotipo)+', '+str(self.fitness))
        
    
class Populacao:
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
            
    # Ordena a lista individuos pela ordem de fitness dos individuos. Do pior para o melhor
    def ordena_por_fitnesses(self):
        self.individuos.sort(key=operator.attrgetter('fitness'))
        
    # Imprime os dados da populacao na tela. Usado apenas para testes
    def print_populacao(self):
        for individuo in self.individuos:
            individuo.print_individuo()
    
    # Retorna a media dos fitnesses da populacao
    def media_fitnesses(self):
        soma_fitnesses = 0
        for individuo in self.individuos:
            soma_fitnesses += individuo.fitness
        media_fitnesses = soma_fitnesses/self.tamanho_populacao
        return media_fitnesses
        
    # Retorna o melhor fitness da populacao
    def melhor_fitness(self):
        return self.individuos[self.tamanho_populacao-1].fitness
        
        
class Selecao:
    pass
    def __init__(self):
        return
    
    # Calcula as probabilidades de selecao, usando operador SPF
    @staticmethod
    def calcula_SPF(populacao):
        soma_fitness = 0
        for individuo in populacao.individuos:
            soma_fitness += individuo.fitness
        for individuo in populacao.individuos:
            individuo.prob_selecao = individuo.fitness/soma_fitness
        
    # Gera segmento de reta utilizado pela roleta a partir das probabilidades de selecao
    # Acabou nao sendo utilizada    
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
        
    # Seleciona os pais utilizando o metodo da roleta.
    # Acabou nao sendo utilizada      
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
        
    # Seleciona os pais via um torneio entre um numero passsado como parametro de participantes
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
        
    # Cruzamento cut and crossfill
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
    
    # Operador de mutacao Swap
    @staticmethod
    def swap(individuo):
        pos_trocas = np.random.randint(low=0, high=individuo.dimensao_individuo, size=2)
        aux = individuo.genotipo[pos_trocas[0]]
        individuo.genotipo[pos_trocas[0]] = individuo.genotipo[pos_trocas[1]]
        individuo.genotipo[pos_trocas[1]] = aux


# Essa e a funcao que executa o GA-Rainhas
def GA():
    # Inicializa hiper-parametros
    tamanho_populacao = 50
    dimensao_individuo = 8
    fitness_ideal = 1
    numero_geracoes = 4975
    prob_mutacao = 0.6
    prob_cruzamento = 0.8
    
    # Gera a populacao inicial
    populacao = Populacao(tamanho_populacao, dimensao_individuo)
    populacao.gera_populacao_aleatoria()
    populacao.calcula_fitnesses()
    populacao.ordena_por_fitnesses()
    
    # Essas listas guardaram as informacoes dos fitness para cada geracao
    melhores_fitnesses = []
    melhores_fitnesses.append(populacao.melhor_fitness()) 
    
    medias_fitnesses = []
    medias_fitnesses.append(populacao.media_fitnesses())
    
    geracao = 0
    geracoes_estagnadas = 0
    # Condicao de parada e` encontrar uma solucao valida ou atingir o numero de geracoes maximo
    while geracao < numero_geracoes and melhores_fitnesses[geracao] < fitness_ideal:
        geracao += 1
        
        # Seleciona os pais via torneio
        pais = Selecao.seleciona_pais_torneio(populacao, 5)
        
        # Cruzamento dos pais escolhidos, sujeito a uma probabilidade
        if (prob_cruzamento > np.random.rand()):
            filhos = Cruzamento.cut_and_crossfill(pais)
        else:
            # Caso nao haja cruzamento
            # Necessario fazer isso para instanciar novos objetos 
            filhos = [Individuo(dimensao_individuo), Individuo(dimensao_individuo)]
            for indice in range(0,2):
                filhos[indice].genotipo = pais[indice].genotipo
        
        # Aplica mutacao nos filhos, sujeita a uma probabilidade
        for individuo in filhos:
            if prob_mutacao > np.random.uniform(0,1):
                Mutacao.swap(individuo)
            individuo.calcula_fitness()
            
        # Substitui os filhos gerados pelos piores pais
        # Esses sao os piores pais pois a populacao esta ordenada
        populacao.individuos[0] = filhos[0]
        populacao.individuos[1] = filhos[1]
        
        # Reordena populacao
        populacao.ordena_por_fitnesses()
        
        # Salva valores importantes nas listas
        melhores_fitnesses.append(populacao.melhor_fitness())
        medias_fitnesses.append(populacao.media_fitnesses())
        
        # Verifica se a melhor solucao esta estagnada
        if melhores_fitnesses[geracao] == melhores_fitnesses[geracao-1]:
            geracoes_estagnadas += 1
        else:
            geracoes_estagnadas = 0
            prob_mutacao = 0.6
        # Caso a melhor solucao esteja estagnada ha mais de 10 geracoes a probabilidade de mutacao e mudada para 1.0        
        if geracoes_estagnadas >= 10:
            prob_mutacao = 1
            
            
    populacao.ordena_por_fitnesses()
   
    
#    Plot dos resultados
#    Traduz os fitness para numero de conflitos entre rainhas     
#    for i in range(0, len(medias_fitnesses)):
#        medias_fitnesses[i] = (1-medias_fitnesses[i])/medias_fitnesses[i]
#        
#    for i in range(0, len(melhores_fitnesses)):
#        melhores_fitnesses[i] = (1-melhores_fitnesses[i])/melhores_fitnesses[i]
    
#    Plots do resultado
#    plt.xlabel('Gerações')
#    plt.ylabel('Conflitos entre rainhas')
#    plt.title('Média das soluções')
#    plt.plot(medias_fitnesses)
#    plt.show()
#    
#    plt.title('Melhor solução')
#    plt.xlabel('Gerações')
#    plt.ylabel('Conflitos entre rainhas')
#    plt.plot(melhores_fitnesses)
#    plt.show()
    
#    Retorna a quantidade de geracoes
#    return(geracao+1)
            
#    Retorna a solucao encontrada
#   return(populacao.individuos[tamanho_populacao-1].genotipo)
    return
