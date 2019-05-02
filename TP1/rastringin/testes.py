# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 18:31:08 2019

@author: Marcio Souza Filho
"""

from ga_rastrigin_partial_elitism_gray import run as run_gray
from ga_rastrigin_partial_elitism_gray import run as run_bin
import numpy as np
import statistics as st

# Esse teste consiste em rodar o ga utilizando com numero de variaveis de 1 a nvar, nruns vezes,
# utilizando o numero de avaliacoes relacionados ao fat_aval e o algoritmo especificado
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
    medias_val = []
    dps_val = []
    medias_ger = []
    dps_ger = []
    n_convergencias = []
    for var in range(1,nvar+1):
        valores.append([])
        geracoes.append([])
        conv = 0
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
            if valor < 1e-4:
                conv += 1
            
        media_val = st.mean(valores[var-1])
        dp_val = st.pstdev(valores[var-1],media_val)
        media_ger = st.mean(geracoes[var-1])
        dp_ger = st.pstdev(geracoes[var-1],media_ger)
        
        medias_val.append(media_val)
        dps_val.append(dp_val)
        medias_ger.append(media_ger)
        dps_ger.append(dp_ger)
        n_convergencias.append(conv)
    np.savez('teste_1_'+algoritmo+'_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes, valores=valores, geracoes=geracoes, medias_val=medias_val, dps_val=dps_val, medias_ger=medias_ger, dps_ger=dps_ger, n_convergencias=n_convergencias)

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
    medias_val = dados['medias_val']
    dps_val = dados['dps_val']
    medias_ger = dados['medias_ger']
    dps_ger = dados['dps_ger']
    n_convergencias = dados['n_convergencias']
    return valores, geracoes, medias_val, dps_val, medias_ger, dps_ger, n_convergencias

   
def teste_2(max_nvar, runs, fat_aval):
    nvar = max_nvar
    nruns = runs
    
    # Se fat_aval = 0, o numero de avaliacoes e 10000, caso contrario e 10000*nvar
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
        
    valores = []
    geracoes = []
    medias_val = []
    dps_val = []
    medias_ger = []
    dps_ger = []
    n_convergencias = []
    for elitism in range(4, 21):
        valores.append([])
        geracoes.append([])
        conv = 0
        if fat_aval == 0:
            fat_ger = 1
        else:
            fat_ger = nvar
        for i in range(0,nruns):
            valor, geracao = run_gray(max_nvar, fat_ger, elitism/20)
            valores[elitism-4].append(valor)
            geracoes[elitism-4].append(geracao)
            if valor < 8e-5:
                conv += 1
            
        media_val = st.mean(valores[elitism-4])
        dp_val = st.pstdev(valores[elitism-4],media_val)
        media_ger = st.mean(geracoes[elitism-4])
        dp_ger = st.pstdev(geracoes[elitism-4],media_ger)
        
        medias_val.append(media_val)
        dps_val.append(dp_val)
        medias_ger.append(media_ger)
        dps_ger.append(dp_ger)
        n_convergencias.append(conv)
    np.savez('teste_1_gray_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes+'elitismo_02-10', valores=valores, geracoes=geracoes, medias_val=medias_val, dps_val=dps_val, medias_ger=medias_ger, dps_ger=dps_ger, n_convergencias=n_convergencias)

# leitura do arquivo do teste 1 de gray
def leitura_teste_2(nvar, nruns, fat_aval):
    if fat_aval == 0:
        tipo_avaliacoes = '_avaliacoes_fixa'
    else:
        tipo_avaliacoes = '_avaliacoes_nvar'
    file = 'teste_1_gray_nvar_'+str(nvar)+'_nruns_'+str(nruns)+tipo_avaliacoes+'elitismo_02-10.npz'
    dados = np.load(file)
    valores = dados['valores']
    geracoes = dados['geracoes']
    medias_val = dados['medias_val']
    dps_val = dados['dps_val']
    medias_ger = dados['medias_ger']
    dps_ger = dados['dps_ger']
    n_convergencias = dados['n_convergencias']
    return valores, geracoes, medias_val, dps_val, medias_ger, dps_ger, n_convergencias

nvar = 10
nruns = 20
fat_aval = 1
algoritmo = 'bin'
valores, geracoes, medias_val, dps_val, medias_ger, dps_ger, n_convergencias = leitura_teste_1(nvar, nruns, fat_aval, algoritmo)
#valores, geracoes, medias_val, dps_val, medias_ger, dps_ger, n_convergencias = leitura_teste_2(nvar, nruns, fat_aval)


# teste elitismo gray avaliacoes fixas
#fat_aval = 0
#teste_2(nvar, nruns, fat_aval)
#print('Terminou teste gray com avaliacoes fixas')
#
## teste elitismo gray avaliacoes nvar
#fat_aval = 1
#teste_2(nvar, nruns, fat_aval)
#print('Terminou teste gray com avaliacoes nvar')
#
## teste gray avaliacoes fixas
#fat_aval = 0
#algoritmo = 'gray'
#teste_1(nvar, nruns, fat_aval, algoritmo)
#print('Terminou teste gray com avaliacoes fixas')
#
## teste bin avaliacoes fixas
#fat_aval = 0
#algoritmo = 'bin'
#teste_1(nvar, nruns, fat_aval, algoritmo)
#print('Terminou teste bin com avaliacoes fixas')
#
## teste gray avaliacoes variaveis
#fat_aval = 1
#algoritmo = 'gray'
#teste_1(nvar, nruns, fat_aval, algoritmo)
#print('Terminou teste gray com avaliacoes nvar')
#
## teste bin avaliacoes variaveis
#fat_aval = 1
#algoritmo = 'bin'
#teste_1(nvar, nruns, fat_aval, algoritmo)
#print('Terminou teste bin com avaliacoes nvar')