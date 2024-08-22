import sqlite3
import pandas as pd
import json

# Função para importar CSV para SQL
def importar_csv_para_sql(nome_tabela, arquivo_csv):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Remover a tabela se já existir
    cursor.execute(f"DROP TABLE IF EXISTS {nome_tabela};")

    # Importar os dados do CSV para a tabela
    df = pd.read_csv(arquivo_csv)
    df.to_sql(nome_tabela, conn, if_exists='replace', index=False)

    conn.close()

# Importar dados para cada tabela
importar_csv_para_sql("funcionarios", "Funcionarios.csv")
importar_csv_para_sql("cargos", "Cargos.csv")
importar_csv_para_sql("departamentos", "Departamentos.csv")
importar_csv_para_sql("historico_salarios", "Historico_Salarios.csv")
importar_csv_para_sql("dependentes", "Dependentes.csv")
importar_csv_para_sql("projetos_desenvolvidos", "Projetos_Desenvolvidos.csv")
importar_csv_para_sql("recursos_projeto", "Recursos_Projeto.csv")

# Função para executar consultas SQL
def executar_consulta_sql(consulta):
    conn = sqlite3.connect('database.db')
    try:
        df_resultado = pd.read_sql_query(consulta, conn)
        print(df_resultado)
    except Exception as e:
        print("Erro ao executar consulta:", e)
    conn.close()

# 1. Trazer a média dos salários (atual) dos funcionários responsáveis por projetos concluídos, agrupados por departamento.
media_salario = """
SELECT d.Nome_Departamento, AVG(f.Salario) AS Media_Salarial
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_Responsavel = f.Funcionario_ID
JOIN Departamentos d ON f.Departamento_ID = d.Departamento_ID
WHERE p.Status = 'Concluído'
GROUP BY d.Nome_Departamento;
"""
print("\nMédia dos salários dos funcionários responsáveis por projetos concluídos, agrupados por departamento:")
executar_consulta_sql(media_salario)

# 2. Identificar os três recursos materiais mais usados nos projetos, listando a descrição do recurso e a quantidade total usada.
recursos_materiais = """
SELECT Descricao_Recurso AS Descricao, SUM(Quantidade_Utilizada) AS Quantidade_Total
FROM Recursos_Projeto
WHERE Tipo_Recurso = 'Material'
GROUP BY Descricao
ORDER BY Quantidade_Total DESC
LIMIT 3;
"""
print("\nTrês recursos materiais mais usados nos projetos:")
executar_consulta_sql(recursos_materiais)

# 3. Calcular o custo total dos projetos por departamento, considerando apenas os projetos 'Concluídos'.
custo_total_projetos = """
SELECT d.Nome_Departamento, SUM(p.Custo_Projeto) AS Custo_Total
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_Responsavel = f.Funcionario_ID
JOIN Departamentos d ON f.Departamento_ID = d.Departamento_ID
WHERE p.Status = 'Concluído'
GROUP BY d.Nome_Departamento;
"""
print("\nCusto total dos projetos por departamento, considerando apenas os projetos 'Concluídos':")
executar_consulta_sql(custo_total_projetos)

# 4. Listar todos os projetos com seus respectivos nomes, custo, data de início, data de conclusão e o nome do funcionário responsável, que estejam 'Em Execução'.
listar_projetos = """
SELECT p.Nome_Projeto, p.Custo_Projeto AS Custo, p.Data_Inicio, p.Data_Conclusao, f.Nome AS Funcionario_Responsavel
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_Responsavel = f.Funcionario_ID
WHERE p.Status = 'Em Execução';
"""
print("\nProjetos 'Em Execução' com detalhes:")
executar_consulta_sql(listar_projetos)

# 5. Identificar o projeto com o maior número de dependentes envolvidos, considerando que os dependentes são associados aos funcionários que estão gerenciando os projetos.
identificar_projeto = """
SELECT p.Nome_Projeto, COUNT(d.Dependente_ID) AS Numero_Dependentes
FROM Projetos_Desenvolvidos p
JOIN Dependentes d ON p.Funcionario_Responsavel = d.Funcionario_ID
GROUP BY p.Nome_Projeto
ORDER BY Numero_Dependentes DESC
LIMIT 1;
"""
print("\nProjeto com o maior número de dependentes envolvidos:")
executar_consulta_sql(identificar_projeto)


# Função para executar consulta SQL e converter o resultado em JSON
def consulta_para_json(consulta, nome_arquivo_json):
    conn = sqlite3.connect('database.db')
    df_resultado = pd.read_sql_query(consulta, conn)
    conn.close()

    # Convertendo DataFrame para JSON
    json_resultado = df_resultado.to_json(orient="records", date_format="iso")

    # Salvando JSON em arquivo
    with open(nome_arquivo_json, 'w') as arquivo_json:
        arquivo_json.write(json_resultado)

    print(f"Dados exportados para {nome_arquivo_json}")

# Consultas SQL
media_salario = """
SELECT d.Nome_Departamento, AVG(f.Salario) AS Media_Salarial
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_Responsavel = f.Funcionario_ID
JOIN Departamentos d ON f.Departamento_ID = d.Departamento_ID
WHERE p.Status = 'Concluído'
GROUP BY d.Nome_Departamento;
"""

recursos_materiais = """
SELECT Descricao_Recurso, SUM(Quantidade_Utilizada) AS Quantidade_Total
FROM Recursos_Projeto
WHERE Tipo_Recurso = 'Material'
GROUP BY Descricao_Recurso
ORDER BY Quantidade_Total DESC
LIMIT 3;
"""

custo_total_projetos = """
SELECT d.Nome_Departamento, SUM(p.Custo_Projeto) AS Custo_Total
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_Responsavel = f.Funcionario_ID
JOIN Departamentos d ON f.Departamento_ID = d.Departamento_ID
WHERE p.Status = 'Concluído'
GROUP BY d.Nome_Departamento;
"""

# Executando consultas e exportando resultados para JSON
consulta_para_json(media_salario, 'media_salario.json')
consulta_para_json(recursos_materiais, 'recursos_materiais.json')
consulta_para_json(custo_total_projetos, 'custo_total_projetos.json')