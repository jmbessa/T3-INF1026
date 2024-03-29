# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:52:16 2021
@author: Carolina
"""
###############################################################################
# Turma:33D
# Professor: Joisa Oliveira
# Nome completo: 
# Matrícula PUC-Rio: 
# Grupo 6
# Componentes do grupo: 
    # Carolina de Moura Costa Gomes Zehuri
    # João Marcello Bessa Rodrigues
    # Juliana Rezende Coutinho
###############################################################################

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_rows",100)

dFilmes=pd.read_excel("Grupo6.xlsx",index_col=1, header=0)

print(dFilmes)

print("\n-----------------------------------------------------")

print('\n 1- Melhorando o dFilmes:')
print('\n a) Para melhor visualização, eliminar a coluna sinopse e column1')
dFilmes.drop(["timeline","Column1"],axis=1,inplace=True)

print('\n b) Dfilmes com colunas e index renomeadas em português')
dFilmes.rename(columns={"year":"Ano","runtime":"Duração","genre": "Gênero","rating":"Avaliação","metascore":"Nota","votes":"Votos","gross":"Faturamento"},inplace=True)
dFilmes.index.name = 'Nome'

print('\n c) Preencher os valores distintos na Nota e Faturamento:')
print('\n    Em nota com a sua média')
print('\n    Em faturamento com o valor mais frequente')
media = int(dFilmes.Nota.mean())
dFilmes.fillna({'Nota':media,'Faturamento':dFilmes.Faturamento.mode().loc[0]}, inplace=True)

print('\n d) Na coluna Votos, trocar a vírgula por ponto')
dFilmes.Votos = dFilmes.Votos.str.replace(',', '.')

print('\n e) Exiba o dFilmes com as alterações feitas')
print(dFilmes)

print('\n f) Mostre uma sumarização geral de dFilmes por média')
print(dFilmes.mean(axis = 0))

print("\n-----------------------------------------------------")

print('\n 2- Criação de categorias dos filmes de acordo com a duração:')
print('\n de 0 até média de duração (inclusive) - Abaixo da média')
print('\n a partir da média até 150 (inclusive) - Regular')
print('\n acima de 150 - Muito Longo ')

print('\n a) Inclua a coluna Categoria com a respectiva categoria dos filmes')
dmed=dFilmes.Duração.mean()
srFxTempoFilmes=pd.cut(dFilmes.Duração,bins=[0,dmed,150,dFilmes.Duração.max()],labels=["Abaixo da média","Regular","Muito Longo"])
dFilmes['Categoria'] = srFxTempoFilmes
print(dFilmes)

print('\n b) Apresente a tabela de frequência dos filmes de acordo com a duração')
TabFreqTempo=srFxTempoFilmes.value_counts()
print(TabFreqTempo)

print('\n c) Apresente a tabela de Frequêcia Percentual (RELATIVA) graficamente')
TabFreqTempo.plot.pie(title='Tab Freq Percentual Grafica', figsize=(6,6), autopct='%.1f')
plt.show()

print('\n d) Apresente a tabela de Frequencia Percentual (RELATIVA) numericamente')
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

print('\n b) Por gênero dos filmes, apresente a quantidade de filmes, tempo médio de duração e nome da melhor avaliação') 
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

print('\n e) Adicione ao dataframe criado anteriormente (dfNum) os valores referentes a Gênero e Ano de dfMelhores e exiba a tabela de frequência resultante do cruzamento de Gênero e Ano')
dfNum['Gênero'] = dfMelhores.Gênero
dfNum['Ano'] = dfMelhores.Ano
TabFreqGenAno = pd.crosstab(dfNum.Gênero, dfNum.Ano, margins = True)
print(TabFreqGenAno)

print('\n f) Tabela de frequencia Gênero X Ano,Faturamento')
TabFreqGenAnoFat = pd.crosstab(index= dfMelhores.Gênero, columns=[dfMelhores.Ano, dfMelhores.Faturamento])
print(TabFreqGenAnoFat)

print('\n g) Duração média por gênero X Avaliação,Nota')
dFilmesCross = pd.crosstab(index= dfMelhores.Gênero, columns=[dfMelhores.Avaliação,dfMelhores.Nota],
                  values= dfMelhores.Duração, aggfunc='mean')
dFilmesCross.fillna('-',inplace=True)
print(dFilmesCross)


print("\n-----------------------------------------------------")

print('n 5 -Tendo como base os filmes de comédia (Comedy) e faroeste (Western), responda:')
print('\n a) Crie um dataframe (dFilmesSelec) com os filmes de comédia, faroeste e dfMelhores.')
dFaroeste=dFilmes.loc[dFilmes.Gênero=="Western"]
dfComedia = dFilmes.loc[dFilmes.Gênero=="Comedy"]
dFilmesSelec = pd.concat([dFaroeste,dfComedia,dfMelhores],join='inner')
print(dFilmesSelec)

print('\n b) Gráfico de dispersão de Avaliação X Gênero do dFilmesSelec')
dFilmesSelec.plot.scatter(x='Avaliação',y='Gênero')
plt.show()

print('\n c) Nota e Avaliação máxima por Gênero/Categoria, utilizando dFilmesSelec')
agGenCAT= dFilmesSelec.groupby(['Gênero','Categoria'])
dfGenCAT = agGenCAT[['Avaliação','Nota']].agg(['max'])
dfGenCAT.fillna('-',inplace=True)
print(dfGenCAT)

