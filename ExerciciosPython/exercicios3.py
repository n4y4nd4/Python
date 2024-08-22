# -*- coding: utf-8 -*-
"""Tp3pyhton.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1r5xY2Bgqt7Kak7W4Ht5MPNTaLLurUFLB

Faça um programa que permita ao usuário digitar o seu nome e em seguida mostre o nome do usuário de trás para frente utilizando somente letras maiúsculas.
"""

nome = input("Digite seu nome: ").upper()

nome_invertido = nome[::-1]
print(nome_invertido)
         #ou
nome_invertido2 = ''.join(reversed(nome))
print(nome_invertido2)

"""Faça um programa que solicite a data de nascimento (dd/mm/aaaa) do usuário e imprima a data com o nome do mês por extenso. Não utilize nenhuma biblioteca específica para conversão de datas."""

data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ")
dia, mes, ano = data_nascimento.split("/")
mes_extenso = {1:'janeiro', 2 :'fevereiro', 3:'março', 4:'abril', 5:'maio', 6:'junho', 7:'julho', 8:'agosto', 9:'setembro', 10:'outubro', 11:'novembro', 12:'dezembro'}
print(f"Data de nascimento: {dia} de {mes_extenso[int(mes)]} de {ano}")

"""Faça um programa que peça duas strings para o usuário e informe o conteúdo delas, seguido do seu comprimento e se são iguais ou diferentes no conteúdo."""

string1 = input("Entre com uma string: ")
string2 = input("Entre com outra string: ")

print(f"Conteúdo primeira string: '{string1}', Comprimento primeira string: {len(string1)}")
print(f"Conteúdo segunda string: '{string2}', Comprimento segunda string: {len(string2)}")
if string1 == string2:
  print("São iguais no conteúdo")
else:
  print("São diferentes em conteúdo")

"""Dado uma string com uma frase informada pelo usuário (incluindo espaços em branco), conte e apresente:
Quantos espaços em branco existem na frase;
Quantas vezes aparecem as vogais ‘a, e, i, o, u’.
"""

string = input("Digite uma string: ")

count_espacos = 0
count_vogais = 0

for char in string:
    if char.isspace():
        count_espacos += 1
    elif char.lower() in 'aeiouáéíóúãõâêîôû':
        count_vogais += 1

print(f"Existem {count_espacos} espaços em branco.")
print(f"Existem {count_vogais} vogais.")