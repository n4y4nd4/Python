# -*- coding: utf-8 -*-
"""nayanda_robers_DR4_TP1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j0L8GjEqzemDawPIFo8DhdyoyhPqTBPu

Faça um programa em Python utilizando SETs, que encontre e apresente na tela os valores máximo e mínimo de um conjunto de valores pré-definido.
Exemplo:

Set_A : {17, 56, 23, 8, 10, 45}
Max: 56
Min: 8
"""

set_A = {17, 56, 23, 8, 10, 45}
max_valor = max(set_A)
min_valor = min(set_A)
print(f"Max: {max_valor}\nMin: {min_valor} ")

"""Faça uma função que utilize SETs (conjuntos em Python) e verifique se duas listas fornecidas possuem, pelo menos, um elemento em comum. Caso tenha pelo menos um, apresente todos os elementos em comum. Execute para os seguintes pares de listas:

a = [1, 2, 3, 4, 5]
b = [5, 6, 7, 8, 9]
--------------------
c =[1, 2, 3, 4, 5]
d =[6, 7, 8, 9]
"""

def elementos_comuns(lista1, lista2):

    elementos_em_comum = set(lista1).intersection(lista2)

    if elementos_em_comum:
        print("elementos em comum:", elementos_em_comum)
    else:
        print("não há elementos em comum")


a = [1, 2, 3, 4, 5]
b = [5, 6, 7, 8, 9]
print("listas a e b:")
elementos_comuns(a, b)

print("--------------------")

c = [1, 2, 3, 4, 5]
d = [6, 7, 8, 9]
print("listas c e d:")
elementos_comuns(c, d)

"""Remova os elementos 10, 20 e 30 do conjunto formado pelos elementos 10, 20, 30, 40, 50, 70, 80, utilizando um método único."""

conjunto = {10, 20, 30, 40, 50, 70, 80}
remover = {10,20,30}
conjunto.difference_update(remover)

print(f"Conjunto: {conjunto}")

"""Utilize as estruturas de dados fornecidas com a questão para responder às seguintes perguntas:
Mamíferos e pássaros possuem elementos em comum?
Animais e mamíferos compartilham elementos?
mamiferos = ['squirrel','dog','cat','cow', 'tiger', 'elephant']
animais = {'chicken': 'white',
           'sparrow': 'grey',
           'eagle': 'brown and white',
           'albatross': 'grey and white',
           'crow': 'black',
           'elephant': 'grey',
           'dog': 'rust',
           'cow': 'black and white',
           'tiger': 'orange and black',
           'cat': 'grey',
           'squirrel': 'black'}
passaros = {'crow','sparrow','eagle','chicken', 'albatross'}
"""

mamiferos = ['squirrel', 'dog', 'cat', 'cow', 'tiger', 'elephant']
animais = {'chicken': 'white',
           'sparrow': 'grey',
           'eagle': 'brown and white',
           'albatross': 'grey and white',
           'crow': 'black',
           'elephant': 'grey',
           'dog': 'rust',
           'cow': 'black and white',
           'tiger': 'orange and black',
           'cat': 'grey',
           'squirrel': 'black'}
passaros = {'crow', 'sparrow', 'eagle', 'chicken', 'albatross'}

comum_mamiferos_passaros = set(mamiferos).intersection(passaros)

if comum_mamiferos_passaros:
    print("Mamíferos e pássaros possuem elementos em comum:", comum_mamiferos_passaros)
else:
    print("Mamíferos e pássaros não possuem elementos em comum.")


comum_animais_mamiferos = set(animais).intersection(mamiferos)

if comum_animais_mamiferos:
    print("Animais e mamíferos compartilham elementos:", comum_animais_mamiferos)
else:
    print("Animais e mamíferos não compartilham elementos.")