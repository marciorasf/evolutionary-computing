# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 18:31:08 2019

@author: Marcio Souza Filho
"""

from ga_rastrigin_partial_elitism_gray import run as run_gray
from ga_rastrigin_partial_elitism_gray import run as run_bin
import numpy as np

# Esse teste consiste em rodar o ga utilizando gray para um numero fixo de avaliacoes igual a 10e4
def teste_1_gray(max_nvar, runs, fat_aval):
    nvar = max_nvar
    nruns = runs
    
    # Se fat_aval = 0, o numero de avaliacoes e 10000, caso contrario e 10000*nvar
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
    valores = []
    geracoes = []
    for var in range(1,nvar+1):
        valores.append([])
        geracoes.append([])
        if fat_aval == 0:
            fat_ger = 1
        else:
            fat_ger = nvar
        for i in range(0,nruns):
            valor, geracao = run_gray(var, fat_ger)
            valores[var-1].append(valor)
            geracoes[var-1].append(geracao)
            print(str(valor)+', '+str(geracao))
    np.savez('teste_1_gray_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes, valores=valores, geracoes=geracoes)

# leitura do arquivo do teste 1 de gray
def leitura_teste_1_gray(nvar, nruns, fat_aval):
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
    file = 'teste_1_gray_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes+'.npz'
    dados = np.load(file)
    valores = dados['valores']
    geracoes = dados['geracoes']
    return valores, geracoes


# Esse teste consiste em rodar o ga utilizando binario
def teste_1_bin(max_nvar, runs, fat_aval):
    nvar = max_nvar
    nruns = runs
    
    # Se fat_aval = 0, o numero de avaliacoes e 10000, caso contrario e 10000*nvar
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
    valores = []
    geracoes = []
    for var in range(1,nvar+1):
        valores.append([])
        geracoes.append([])
        if fat_aval == 0:
            fat_ger = 1
        else:
            fat_ger = nvar
        for i in range(0,nruns):
            valor, geracao = run_bin(var, fat_ger)
            valores[var-1].append(valor)
            geracoes[var-1].append(geracao)
            print(str(valor)+', '+str(geracao))
    np.savez('teste_1_bin_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes, valores=valores, geracoes=geracoes)

# leitura do arquivo do teste 1 de gray
def leitura_teste_1_bin(nvar, nruns, fat_aval):
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
    file = 'teste_1_bin_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes+'.npz'
    dados = np.load(file)
    valores = dados['valores']
    geracoes = dados['geracoes']
    return valores, geracoes

# Esse teste consiste em rodar o ga utilizando binario
def teste_1(max_nvar, runs, fat_aval, algoritmo):
    nvar = max_nvar
    nruns = runs
    
    # Se fat_aval = 0, o numero de avaliacoes e 10000, caso contrario e 10000*nvar
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
        
    valores = []
    geracoes = []
    for var in range(1,nvar+1):
        valores.append([])
        geracoes.append([])
        if fat_aval == 0:
            fat_ger = 1
        else:
            fat_ger = nvar
        for i in range(0,nruns):
            if algoritmo == 'gray':
                valor, geracao = run_gray(var, fat_ger)
            else:
                valor, geracao = run_bin(var, fat_ger)
            valores[var-1].append(valor)
            geracoes[var-1].append(geracao)
    np.savez('teste_1_'+algoritmo+'_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes, valores=valores, geracoes=geracoes)

# leitura do arquivo do teste 1 de gray
def leitura_teste_1(nvar, nruns, fat_aval, algoritmo):
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
    file = 'teste_1_'+algoritmo+'_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes+'.npz'
    dados = np.load(file)
    valores = dados['valores']
    geracoes = dados['geracoes']
    return valores, geracoes    
   

nvar = 10
nruns = 20
fat_aval = 0
algoritmo = 'bin'
teste_1(nvar, nruns, fat_aval, algoritmo)
valores, geracoes = leitura_teste_1(nvar,nruns,fat_aval, algoritmo)
