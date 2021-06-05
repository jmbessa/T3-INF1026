# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:52:16 2021

@author: Carolina
"""
# Turma:33D
# Professor: Joisa Oliveira
# Nome completo: Carolina de Moura Costa Gomes Zehuri
# Matrícula PUC-Rio: 1920965
# Grupo 6

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_rows",100)

dFilmes=pd.read_excel("Grupo6.xlsx",index_col=1, header=0)

print(dFilmes)

print("\n-----------------------------------------------------")

#PERGUNTAS
print('\n 1- Melhorando o dFilmes:')
print('\n a) Para melhor visualização, eliminar a coluna sinopse e column1')
dFilmes.drop(["timeline","Column1"],axis=1,inplace=True)

print('\n b) Dfilmes com colunas e index renomeadas em português')
dFilmes.rename(columns={"year":"Ano","runtime":"Duração","genre": "Gênero","rating":"Avaliação","metascore":"Nota","votes":"Votos","gross":"Faturamento"},inplace=True)
dFilmes.index.name = 'Nome'

print('\n c) Preeencher os valares distintos na Nota e Faturamento:')
print('\n    Em nota com a sua média')
print('\n    Em faturamento com o valor mais frequente')
media = int(dFilmes.Nota.mean())
dFilmes.fillna({'Nota':media,'Faturamento':dFilmes.Faturamento.mode().loc[0]}, inplace=True)

print('\n d) Na coluna Votos, trocar a virgula por ponto')
dFilmes.Votos = dFilmes.Votos.str.replace(',', '.')

print('\n e) Exiba o dFilmes com as alterações feitas')
print(dFilmes)

print('\n f) Mostre uma sumarização geral de dFilmes')
print(dFilmes.describe())


print("\n-----------------------------------------------------")

print('\n 2- Criação de categorias dos filmes de acordo com a duração:')
print('\n de 0 até média de duração (inclusive) - Abaixo da média')
print('\n a partir da média até 150 (inclusive) - Regular')
print('\n acima de 150 - Muito Longo ')

print('\n a) Exiba as categorias')
dmed=dFilmes.Duração.mean()
srFxTempoFilmes=pd.cut(dFilmes.Duração,bins=[0,dmed,150,dFilmes.Duração.max()],labels=["Abaixo da média","Regular","Muito Longo"])
print(srFxTempoFilmes)
# dFilmes['CAT'] = srFxTempoFilmes

print('\n b) Apresente a tabela de frequencia dos filmes de acordo com a duração')
TabFreqTempo=srFxTempoFilmes.value_counts()
print(TabFreqTempo)

print('\n c) Apresente a tabela de Frequencia Percentual (RELATIVA) graficamente')
TabFreqTempo.plot.pie(title='Tab Freq Percentual Grafica', figsize=(6,6), autopct='%.1f')
plt.show()

print('\n d) Apresente a tabela de Frequencia Percentual (RELATIVA) NUMERICAMENTE')
tfp = TabFreqTempo / dFilmes.shape[0] * 100
print(tfp)

print('\n d) Apresente a tabela de Frequencia Percentual (RELATIVA) NUMERICAMENTE')
tfp = TabFreqTempo / dFilmes.shape[0] * 100
print(tfp)

print("\n-----------------------------------------------------")

print('n 3- Por Nota, dos filmes de apenas DRAMA, a quantidade de filmes,o max, min e idxmax de Avaliações ')
dfDrama=dFilmes.loc[dFilmes.Gênero=="Drama"]
# print(dfDrama)
agDrama = dfDrama.groupby('Nota')
# print(agDrama)
dfResposta = agDrama.Avaliação.agg(['count','max','min','idxmax'])
print(dfResposta)

print("\n-----------------------------------------------------")

print('n 4 -Tendo como base os filmes com avalição maior ou igual a 90 (dfMelhores), responda:')

print('\n a) Exiba o nome dos filmes')
dfMelhores=dFilmes.loc[dFilmes.Avaliação>=90]
print(list(dfMelhores.index))

print('\n b) Por genero dos filmes, apresente a quantidade de filmes, tempo médio de duração e nome da melhor avaliação') 
agGenero = dfMelhores.groupby('Gênero')
medDur = agGenero.Duração.agg(['count','mean'])
medDur.rename(columns={'count':'Quant', 'mean':'TempoMedio'},inplace=True)
medAva = agGenero.Avaliação.agg(['idxmax'])
medAva.rename(columns={'idxmax':'Nome_max'},inplace=True)
dfResp = pd.concat([medDur,medAva],axis=1)
print(dfResp)

print('\n c) Crie um dataframe (dfNum) com os valores referentes a avaliação, nota e votos de dfMelhores')
dfNum = pd.concat([dfMelhores.Avaliação,dfMelhores.Nota,dfMelhores.Votos],axis=1)
print(dfNum)

print('\n d) Exiba a tabela de frequencia resultante do cruzamento de avaliação e votos de dfNum')
TabFreqAvaVotos = pd.crosstab(dfNum.Avaliação, dfNum.Votos)
print(TabFreqAvaVotos)

print('\n e) Adicione ao dataframe criado anteriormente (dfNum) os valores referentes a Gênero e Ano de dfMelhores e exiba a tabela de frequencia resultando do cruzamento de Gênero e Ano')
dfNum['Gênero'] = dfMelhores.Gênero
dfNum['Ano'] = dfMelhores.Ano
TabFreqGenAno = pd.crosstab(dfNum.Gênero, dfNum.Ano, margins = True)
print(TabFreqGenAno)

print("\n-----------------------------------------------------")

print('n 5 -Tendo como base os filmes de comédia e faroeste, responda:')
print('\n a) Crie um dataframe (dFilmesSelec) com os filmes de comédia, faroeste e dfMelhores.')
dFaroeste=dFilmes.loc[dFilmes.Gênero=="Western"]

dfComedia = dFilmes.loc[dFilmes.Gênero=="Comedy"]

dFilmesSelec = pd.concat([dFaroeste,dfComedia,dfMelhores],join='inner')
print(dFilmesSelec)

print('\n b) Gráfico de dispersão de Avaliação X Gênero do dFilmesSelec')
dFilmesSelec.plot.scatter(x='Avaliação',y='Gênero')
plt.show()

print('n 6 - Criação de tabelas')

