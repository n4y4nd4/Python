CREATE TABLE Funcionarios (
  Funcionario_ID INT PRIMARY KEY,
  Nome VARCHAR(100),
  Cargo_ID INT,
  Departamento_ID INT,
  Salario DECIMAL(10, 2),
  Data_Contratacao DATE,
  Data_Nascimento DATE,
  FOREIGN KEY (Cargo_ID) REFERENCES Cargos(Cargo_ID), 
  FOREIGN KEY (Departamento_ID) REFERENCES Departamentos(Departamento_ID) 
);


CREATE TABLE Cargos (
  Cargo_ID INT PRIMARY KEY,
  Descricao VARCHAR(100),
  Salario_Base DECIMAL(10, 2),
  Nivel VARCHAR(50),
  Habilidades_Requeridas VARCHAR(255)
);


CREATE TABLE Departamentos (
  Departamento_ID INT PRIMARY KEY,
  Nome_Departamento VARCHAR(100),
  Gerente_ID INT,
  Andar INT,
  Telefone VARCHAR(20),
  FOREIGN KEY (Gerente_ID) REFERENCES Funcionarios(Funcionario_ID) 
);


INSERT INTO Funcionarios (Funcionario_ID, Nome, Cargo_ID, Departamento_ID, Salario, Data_Contratacao, Data_Nascimento)
VALUES
  (1, 'Nayanda', NULL, 3, 5000.00, '2023-05-15', '2003-01-09'),
  (2, 'Maria', 7, 3, 2500.00, '2022-08-20', '1996-04-12'),
  (3, 'Camila', 2, 1, 4800.00, '2024-01-10', '1997-09-05'),
  (4, 'Rodrigo', 2, 2, 6000.00, '2023-11-05', '1998-07-15'),
  (5, 'Luan', 3, 2, 5200.00, '2021-12-03', '1999-12-03'),
  (6, 'Larissa', 2, 1, 5300.00, '2023-02-18', '2000-03-20'),
  (7, 'Lucas', 3, 4, 6800.00, '2022-05-30', '2002-08-27'),
  (8, 'Niall', 3, 4, 7500.00, '2023-09-12', '1993-09-13'),
  (9, 'Harry', 2, 5, 4500.00, '2024-03-01', '1994-02-01'),
  (10, 'Liam', 3, 5, 5100.00, '2022-06-25', '1993-08-29'),
  (11, 'Zayn', 6, 5, 12000.00, '2021-01-01', '1993-01-12'), 
  (12, 'Louis', 6, 5, 12000.00, '2021-01-01', '1991-12-24'),
  (13, 'Betina', 1, 1, 5800.00, '2023-05-15', '1995-01-20'); 


INSERT INTO Cargos (Cargo_ID, Descricao, Salario_Base, Nivel, Habilidades_Requeridas)
VALUES
  (1, 'Analista de Sistemas', 5800.00, 'Analista', 'Conhecimento em análise de sistemas'),
  (2, 'Estagiário de TI', 2500.00, 'Estagiário', 'Conhecimento básico em tecnologia da informação'),
  (3, 'Analista Financeiro', 5500.00, 'Analista', 'Conhecimento em análise financeira'),
  (4, 'Gerente de TI', 7500.00, 'Gerente', 'Experiência em gestão de equipe de TI'),
  (5, 'Diretor de Tecnologia', 11000.00, 'Diretor', 'Experiência em liderança estratégica em TI'),
  (6, 'Diretor', 12000.00, 'Diretor', 'Experiência em liderança estratégica');


INSERT INTO Departamentos (Departamento_ID, Nome_Departamento, Gerente_ID, Andar, Telefone)
VALUES
  (1, 'Desenvolvimento de Sistemas', 1, 5, '(21) 9435-8744'), 
  (2, 'Estágio de TI', 2, 6, '(21) 9345-9874'),
  (3, 'Financeiro', 3, 7, '(21) 9876-3459'), 
  (4, 'Gerência de TI', 4, 8, '(21) 9984-2345'), 
  (5, 'Diretoria de TI', 5, 9, '(21) 9800-4348'); 

INSERT INTO Historico_Salarios (Historico_ID, Funcionario_ID, Salario, Data_Pagamento) VALUES
    (1, 1, 5000.00, '2024-03-31'),
    (2, 1, 5200.00, '2024-04-30'),
    (3, 1, 5500.00, '2024-05-31'),
    (4, 2, 2500.00, '2024-03-31'),
    (5, 2, 2700.00, '2024-04-30'),
    (6, 2, 3000.00, '2024-05-31'),
    (7, 3, 4800.00, '2024-03-31'),
    (8, 3, 5000.00, '2024-04-30'),
    (9, 3, 5200.00, '2024-05-31');


INSERT INTO Dependentes (Dependente_ID, Funcionario_ID, Nome, Data_Nascimento) VALUES
    (1, 1, 'Ana', '2010-01-15'),
    (2, 1, 'Pedro', '2015-06-20'),
    (3, 2, 'Mariana', '2012-03-10'),
    (4, 3, 'João', '2018-09-05'),
    (5, 3, 'Laura', '2020-04-25');

SELECT * FROM Funcionarios ORDER BY Nome;

SELECT * FROM Cargos ORDER BY Descricao;

SELECT * FROM Departamentos ORDER BY Nome_Departamento;


SELECT * FROM Departamentos WHERE Andar = 5;


SELECT *
FROM Funcionarios
WHERE Cargo_ID = (
        SELECT Cargo_ID
        FROM Cargos
        WHERE Nivel = 'Analista'
    )
AND Salario = (
        SELECT MAX(Salario)
        FROM Funcionarios
        WHERE Cargo_ID = (
                SELECT Cargo_ID
                FROM Cargos
                WHERE Nivel = 'Analista'
            )
    );



SELECT F.*
FROM Funcionarios F
JOIN Departamentos D ON F.Departamento_ID = D.Departamento_ID
JOIN Cargos C ON F.Cargo_ID = C.Cargo_ID
WHERE D.Nome_Departamento = 'Diretoria de TI'
AND F.Salario >= (
    SELECT Salario_Base
    FROM Cargos
    WHERE Descricao = 'Gerente de TI'
);




SELECT Nome_Departamento, COUNT(*) AS Num_Estagiarios
FROM Funcionarios F
JOIN Departamentos D ON F.Departamento_ID = D.Departamento_ID
JOIN Cargos C ON F.Cargo_ID = C.Cargo_ID
WHERE C.Descricao = 'Estagiário de TI'
GROUP BY Nome_Departamento
HAVING COUNT(*) = (
    SELECT COUNT(*)
    FROM Funcionarios F2
    JOIN Cargos C2 ON F2.Cargo_ID = C2.Cargo_ID
    WHERE C2.Descricao = 'Estagiário de TI'
    GROUP BY F2.Departamento_ID
    ORDER BY COUNT(*) DESC
    LIMIT 1
);


SELECT * FROM Funcionarios
WHERE Cargo_ID IS NULL;



SELECT * FROM Funcionarios
WHERE Departamento_ID IN (
    SELECT Departamento_ID
    FROM Departamentos
    WHERE Andar = (
        SELECT MAX(Andar)
        FROM Departamentos
    )
);



SELECT DISTINCT C.Descricao AS Cargo
FROM Funcionarios F
INNER JOIN Cargos C ON F.Cargo_ID = C.Cargo_ID
WHERE F.Salario BETWEEN 3000 AND 5000;



SELECT Descricao AS Cargo_Com_Salario_Mais_Baixo
FROM Cargos
WHERE Salario_Base = (
    SELECT MIN(Salario_Base) 
    FROM Cargos
);



SELECT Nome_Departamento
FROM Departamentos
WHERE Departamento_ID = (
    SELECT Departamento_ID
    FROM Funcionarios
    GROUP BY Departamento_ID
    ORDER BY MAX(Salario) DESC
    LIMIT 1
);




SELECT *
FROM Funcionarios
WHERE Salario > 5000.00
ORDER BY Nome ASC;


SELECT *
FROM Cargos
ORDER BY Nivel ASC;



SELECT *
FROM Departamentos
ORDER BY Nome_Departamento ASC;

