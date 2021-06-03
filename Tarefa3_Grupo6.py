# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:18:25 2021

@author: jujub_000
"""

# Turma:33D
# Professor:JOISA
# Nome completo:Juliana Rezende Coutinho
# Matrícula PUC-Rio:1810391
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_rows",100)

dFilmes=pd.read_excel("Grupo6_excel.xlsx",index_col=1, header=0)

print(dFilmes)

#Para melhorar a visualizaçÃo do Data Frame eliminaremos a coluna que contém a sinopse do filme e a numeração
print('\n DFilmes sem timeline e Column 1')
dFilmes.drop(["timeline","Column1"],axis=1,inplace=True)
print(dFilmes)

print("\n-----------------------------------------------------")

#Substituição de valores
print('\n1 DFilmes com colunas e index renomeadas em português')
dFilmes.rename(columns={"year":"Ano","runtime":"Duração","genre": "Gênero","rating":"Avaliação","metascore":"Nota","votes":"Votos","gross":"Faturamento"},inplace=True)
dFilmes.index.name = 'Nome'
print(dFilmes)

print("\n-----------------------------------------------------")

print('\n - Preenchendo valores distintos na Nota e Faturamento \
      Em nota com a sua media e em Faturamento com o valor mais frequente')
media = int(dFilmes.Nota.mean())
dFilmes.fillna({'Nota':media,'Faturamento':dFilmes.Faturamento.mode().loc[0]}, inplace=True)
print(dFilmes)

print("\n-----------------------------------------------------")

#PERGUNTAS

print('\n1- Criação de categorias dos filmes de acordo com a duração: \
      de 0 até média de duração (inclusive) - Abaixo da média \
      a partir da média até 150 (inclusive) - Regular \
      acima de 150 - Muito Longo ')

dmed=dFilmes.Duração.mean()
srFxTempoFilmes=pd.cut(dFilmes.Duração,bins=[0,dmed,150,dFilmes.Duração.max()],labels=["Abaixo da média","Regular","Muito Longo"])
print(srFxTempoFilmes)

print("\n-----------------------------------------------------")

print('\n2- Apresente a tabela de frequencia dos filmes de acordo com a duração')
TabFreqTempo=srFxTempoFilmes.value_counts()
print(TabFreqTempo)

print("\n-----------------------------------------------------")

print('\n3- Apresente a tabela de Frequencia Percentual (RELATIVA) graficamente')
TabFreqTempo.plot.pie(title='Tab Freq Percentual Grafica', figsize=(6,6), autopct='%.1f')
plt.show()

print("\n-----------------------------------------------------")

print('\n4- Apresente a tabela de Frequencia Percentual (RELATIVA) NUMERICAMENTE')
tfp = TabFreqTempo / dFilmes.shape[0] * 100
print(tfp)

print("\n-----------------------------------------------------")

print('n5- Por Nota, dos filmes de apenas DRAMA, a quantidade,o max, min e idxmax de Avaliações ')
dfDrama=dFilmes.loc[dFilmes.Gênero=="Drama"]
# print(dfDrama)
agDrama = dfDrama.groupby('Nota')
# print(agDrama)
dfResposta = agDrama.Avaliação.agg(['count','max','min','idxmax'])
print(dfResposta)

print("\n-----------------------------------------------------")

print('n6 - Por Gênero dos filmes de avaliação maior ou igual a 90, apresente: \
quantidade de filmes, tempo médio de duração, melhor avaliação e seu nome.')
dfMelhores=dFilmes.loc[dFilmes.Avaliação>=90]
# print(dfMelhores)
agGenero = dfMelhores.groupby('Gênero')
medDur = agGenero.Duração.agg(['count','mean'])
medDur.rename(columns={'count':'Quant', 'mean':'TempoMedio'},inplace=True)
medAva = agGenero.Avaliação.agg(['max','idxmax'])
medAva.rename(columns={'max':'Nota_max', 'idxmax':'Nome_max'},inplace=True)
dfResp = pd.concat([medDur,medAva],axis=1)
print(dfResp)

#-------
#Usar em perguntas
print('\n3- Nome do(s) filme(s) de maior duração')
dfMaiorTempo=dFilmes.loc[dFilmes.Duração==dFilmes.Duração.max()]
print('Nome:', list(dfMaiorTempo.index),"- Tempo de duração:",dfMaiorTempo.Duração.max(),"min")


