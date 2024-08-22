import sqlite3
import pandas as pd

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

# Função para executar consultas SQL
def executar_consulta_sql(consulta):
    conn = sqlite3.connect('database.db')
    try:
        df_resultado = pd.read_sql_query(consulta, conn)
        print(df_resultado)
    except Exception as e:
        print("Erro ao executar consulta:", e)
    conn.close()

# Consulta para listar a tabela de Funcionários
consulta_funcionarios = "SELECT * FROM funcionarios ORDER BY Funcionario_ID ASC;"
print("\nFuncionários:")
executar_consulta_sql(consulta_funcionarios)

# Consulta para listar a tabela de Cargos
consulta_cargos = "SELECT * FROM cargos ORDER BY Cargo_ID ASC;"
print("\nCargos:")
executar_consulta_sql(consulta_cargos)

# Consulta para listar a tabela de Departamentos
consulta_departamentos = "SELECT * FROM departamentos ORDER BY Departamento_ID ASC;"
print("\nDepartamentos:")
executar_consulta_sql(consulta_departamentos)

# Consulta para listar a tabela de Histórico de Salários
consulta_historico_salarios = "SELECT * FROM historico_salarios ORDER BY Historico_ID ASC;"
print("\nHistórico de Salários:")
executar_consulta_sql(consulta_historico_salarios)

# Consulta para listar a tabela de Dependentes
consulta_dependentes = "SELECT * FROM dependentes ORDER BY Dependente_ID ASC;"
print("\nDependentes:")
executar_consulta_sql(consulta_dependentes)


# Consulta para listar os funcionários com seus cargos, departamentos e dependentes
consulta_funcionarios_completos = """
SELECT 
    f.Nome AS Nome_Funcionario, 
    c.Descricao AS Cargo,
    d.Nome_Departamento AS Departamento, 
    dep.Nome AS Nome_Dependente
FROM 
    funcionarios f
JOIN 
    cargos c ON f.Cargo_ID = c.Cargo_ID
JOIN 
    departamentos d ON f.Departamento_ID = d.Departamento_ID
LEFT JOIN 
    dependentes dep ON f.Funcionario_ID = dep.Funcionario_ID
ORDER BY 
    f.Nome, c.Descricao, d.Nome_Departamento, dep.Nome;
"""
print("\nFuncionários com seus cargos, departamentos e dependentes:")
executar_consulta_sql(consulta_funcionarios_completos)



# Consulta para listar os funcionários que tiveram aumento salarial nos últimos 3 meses
consulta_aumento_salarial = """
SELECT f.Nome AS Nome_Funcionario
FROM funcionarios f
JOIN historico_salarios hs ON f.Funcionario_ID = hs.Funcionario_ID
WHERE hs.Data_Pagamento >= DATE('now', '-3 months')
GROUP BY f.Funcionario_ID
ORDER BY f.Funcionario_ID;
"""

print("\nFuncionários que tiveram aumento salarial nos últimos 3 meses:")
executar_consulta_sql(consulta_aumento_salarial)

# Consulta para listar a média de idade dos filhos dos funcionários por departamento
consulta_media_idade_filhos = """
SELECT d.Nome_Departamento AS Departamento, AVG(strftime('%Y', 'now') - strftime('%Y', dep.Data_Nascimento)) AS Media_Idade_Filhos
FROM dependentes dep
JOIN funcionarios f ON dep.Funcionario_ID = f.Funcionario_ID
JOIN departamentos d ON f.Departamento_ID = d.Departamento_ID
GROUP BY d.Nome_Departamento
ORDER BY Media_Idade_Filhos;
"""
print("\nMédia de idade dos filhos dos funcionários por departamento:")
executar_consulta_sql(consulta_media_idade_filhos)

# Consulta para listar qual estagiário possui filho
consulta_estagiario_com_filho = """
SELECT f.Nome AS Estagiario
FROM funcionarios f
JOIN cargos c ON f.Cargo_ID = c.Cargo_ID
WHERE c.Descricao = 'Estagiário de TI'
AND EXISTS (SELECT 1 FROM dependentes WHERE Funcionario_ID = f.Funcionario_ID)
"""
print("\nEstagiários que possuem filho:")
executar_consulta_sql(consulta_estagiario_com_filho)

# Consulta para listar o funcionário que teve o salário médio mais alto
def funcionario_com_maior_salario_medio():
    conn = sqlite3.connect('database.db')
    query = """
    SELECT f.Funcionario_ID, f.Nome AS Nome_Funcionario, AVG(hs.Salario) AS Salario_Medio
    FROM funcionarios f
    JOIN historico_salarios hs ON f.Funcionario_ID = hs.Funcionario_ID
    GROUP BY f.Funcionario_ID, f.Nome
    ORDER BY Salario_Medio DESC
    LIMIT 1;
    """
    try:
        df_resultado = pd.read_sql_query(query, conn)
        print("\nFuncionário com maior salário médio:")
        print(df_resultado)
    except Exception as e:
        print("Erro ao executar consulta:", e)
    conn.close()

funcionario_com_maior_salario_medio()

# Consulta para listar o analista que é pai de 2 (duas) meninas
def analista_com_duas_filhas():
    conn = sqlite3.connect('database.db')
    query = """
    SELECT f.Funcionario_ID, f.Nome AS Nome_Funcionario
    FROM funcionarios f
    JOIN cargos c ON f.Cargo_ID = c.Cargo_ID
    JOIN dependentes d ON f.Funcionario_ID = d.Funcionario_ID
    WHERE c.Nivel = 'Analista' AND d.Sexo = 'F'
    GROUP BY f.Funcionario_ID, f.Nome
    HAVING COUNT(*) >= 2;
    """
    try:
        df_resultado = pd.read_sql_query(query, conn)
        print("\nAnalista que é pai de duas meninas:")
        print(df_resultado)
    except Exception as e:
        print("Erro ao executar consulta:", e)
    conn.close()

analista_com_duas_filhas()

# Consulta para listar o analista que tem o salário mais alto, e que ganhe entre 5000 e 9000
def analista_com_salario_alto():
    conn = sqlite3.connect('database.db')
    query = """
    SELECT f.Funcionario_ID, f.Nome AS Nome_Funcionario, hs.Salario
    FROM funcionarios f
    JOIN cargos c ON f.Cargo_ID = c.Cargo_ID
    JOIN historico_salarios hs ON f.Funcionario_ID = hs.Funcionario_ID
    WHERE c.Nivel = 'Analista' AND hs.Salario BETWEEN 5000 AND 9000
    ORDER BY hs.Salario DESC
    LIMIT 1;
    """
    try:
        df_resultado = pd.read_sql_query(query, conn)
        print("\nAnalista com salário mais alto entre 5000 e 9000:")
        print(df_resultado)
    except Exception as e:
        print("Erro ao executar consulta:", e)
    conn.close()

analista_com_salario_alto()

# Consulta para listar o departamento com o maior número de dependentes
def departamento_com_mais_dependentes():
    conn = sqlite3.connect('database.db')
    query = """
    SELECT dp.Nome_Departamento AS Departamento, COUNT(*) AS Numero_Dependentes
    FROM dependentes d
    JOIN funcionarios f ON d.Funcionario_ID = f.Funcionario_ID
    JOIN departamentos dp ON f.Departamento_ID = dp.Departamento_ID
    GROUP BY dp.Nome_Departamento
    ORDER BY Numero_Dependentes DESC
    LIMIT 1;
    """
    try:
        df_resultado = pd.read_sql_query(query, conn)
        print("\nDepartamento com o maior número de dependentes:")
        print(df_resultado)
    except Exception as e:
        print("Erro ao executar consulta:", e)
    conn.close()

departamento_com_mais_dependentes()


# Consulta para listar a média de salário por departamento em ordem decrescente
def media_salario_por_departamento():
    conn = sqlite3.connect('database.db')
    query = """
    SELECT d.Nome_Departamento AS Departamento, AVG(hs.Salario) AS Media_Salario
    FROM historico_salarios hs
    JOIN funcionarios f ON hs.Funcionario_ID = f.Funcionario_ID
    JOIN departamentos d ON f.Departamento_ID = d.Departamento_ID
    GROUP BY d.Departamento_ID
    ORDER BY Media_Salario DESC;
    """
    try:
        df_resultado = pd.read_sql_query(query, conn)
        print("\nMédia de salário por departamento em ordem decrescente:")
        print(df_resultado)
    except Exception as e:
        print("Erro ao executar consulta:", e)
    conn.close()

media_salario_por_departamento()
