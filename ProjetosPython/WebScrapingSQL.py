import sqlite3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

# Verificar se o arquivo eventos.db existe e excluí-lo se necessário
db_file = 'eventos.db'
if os.path.exists(db_file):
    os.remove(db_file)
else:
    print(f"Arquivo {db_file} não encontrado.")

# Configurando as opções do Chrome
options = Options()
options.headless = True  

# Inicializando o driver do Chrome usando ChromeDriverManager e opções configuradas
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL da página que você deseja fazer scraping
url = 'https://www.niallhoran.com/#/tour'

# Fazendo a requisição GET
driver.get(url)

try:
    # Encontrando todos os elementos com as classes específicas usando Selenium
    date_elements = driver.find_elements("class name", "seated-event-date-cell")
    venue_name_elements = driver.find_elements("class name", "seated-event-venue-name")
    venue_location_elements = driver.find_elements("class name", "seated-event-venue-location")
    metadata_elements = driver.find_elements("class name", "seated-event-link-cell1")

    # Verificar se há elementos suficientes capturados
    if not date_elements or not venue_name_elements or not venue_location_elements:
        raise ValueError("Não foi possível encontrar elementos na página.")

    # Lista para armazenar os dados dos eventos
    eventos = []

    # Iterando sobre os elementos encontrados
    for i in range(len(date_elements)):
        # Extraindo os dados dos eventos
        data_evento = date_elements[i].text.strip()
        localizacao = venue_location_elements[i].text.strip()
        nome_evento = "The Show Live On Tour 2024"
        tipo = venue_name_elements[i].text.strip()

        # Capturando o link dos ingressos como metadado
        metadado = "Sem metadado disponível"
        if i < len(metadata_elements):
            link_element = metadata_elements[i].find_element("tag name", "a")
            metadado = link_element.get_attribute("href")

        # Adicionando os dados do evento à lista
        eventos.append((nome_evento, tipo, data_evento, localizacao, metadado))

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('eventos.db')
    cursor = conn.cursor()

    # Criando as tabelas no banco de dados (se ainda não existirem)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DadosEventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_evento INTEGER,
            data TEXT,
            localizacao TEXT,
            FOREIGN KEY (id_evento) REFERENCES Eventos (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Metadados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_evento INTEGER,
            metadado TEXT,
            FOREIGN KEY (id_evento) REFERENCES Eventos (id)
        )
    ''')

    # Inserindo os dados nas tabelas
    for evento in eventos:
        # Inserindo na tabela Eventos
        cursor.execute('INSERT INTO Eventos (nome, tipo) VALUES (?, ?)', (evento[0], evento[1]))
        evento_id = cursor.lastrowid

        # Inserindo na tabela DadosEventos
        cursor.execute('INSERT INTO DadosEventos (id_evento, data, localizacao) VALUES (?, ?, ?)', (evento_id, evento[2], evento[3]))

        # Inserindo na tabela Metadados
        cursor.execute('INSERT INTO Metadados (id_evento, metadado) VALUES (?, ?)', (evento_id, evento[4]))

    # Commit das alterações e fechamento da conexão
    conn.commit()

    # 1. Mostrar todos os eventos com suas datas, localização, e tipo de evento.
    print("1. Todos os eventos com suas datas, localização, e tipo de evento:")
    cursor.execute('''
        SELECT Eventos.id, Eventos.nome, Eventos.tipo, DadosEventos.data, DadosEventos.localizacao 
        FROM Eventos 
        JOIN DadosEventos ON Eventos.id = DadosEventos.id_evento
    ''')
    eventos = cursor.fetchall()
    for evento in eventos:
        print(evento)

    # 2. Mostrar os dados dos 2 eventos mais próximos de iniciar.
    print("\n2. Os dados dos 2 eventos mais próximos de iniciar:")
    cursor.execute('''
        SELECT Eventos.id, Eventos.nome, DadosEventos.data, DadosEventos.localizacao 
        FROM Eventos 
        JOIN DadosEventos ON Eventos.id = DadosEventos.id_evento 
        ORDER BY DadosEventos.data ASC 
        LIMIT 2
    ''')
    proximos_eventos = cursor.fetchall()
    for evento in proximos_eventos:
        print(evento)

    # 3. Mostrar os eventos que acontecem no Rio de Janeiro.
    print("\n3. Eventos que acontecem no Rio de Janeiro:")
    cursor.execute('''
        SELECT Eventos.id, Eventos.nome, DadosEventos.data, DadosEventos.localizacao 
        FROM Eventos 
        JOIN DadosEventos ON Eventos.id = DadosEventos.id_evento 
        WHERE DadosEventos.localizacao LIKE '%Rio de Janeiro%'
    ''')
    eventos_rio = cursor.fetchall()
    for evento in eventos_rio:
        print(evento)

    # 4. Mostrar todos os eventos que são ao ar livre.
    print("\n4. Todos os eventos que são ao ar livre:")
    cursor.execute('''
        SELECT Eventos.id, Eventos.nome, DadosEventos.data, DadosEventos.localizacao 
        FROM Eventos 
        JOIN DadosEventos ON Eventos.id = DadosEventos.id_evento 
        WHERE Eventos.tipo LIKE '%Amphitheater%' OR DadosEventos.localizacao LIKE '%Amphitheater%'
    ''')
    eventos_ao_ar_livre = cursor.fetchall()
    for evento in eventos_ao_ar_livre:
        print(evento)

    # 5. Mostrar todos os Metadados por evento.
    print("\n5. Todos os Metadados por evento:")
    cursor.execute('''
        SELECT Metadados.id, Metadados.id_evento, Metadados.metadado 
        FROM Metadados
    ''')
    metadados = cursor.fetchall()
    for metadado in metadados:
        print(metadado)

    # Fechamento da conexão
    conn.close()

except Exception as e:
    print(f"Erro ao processar os elementos: {e}")

finally:
    # Encerrando o driver
    driver.quit()
