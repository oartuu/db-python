CREATE DATABASE rpg;

USE rpg;

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL
);


CREATE TABLE combatentes (
    id_combatente SERIAL PRIMARY KEY,
    nome_combatente VARCHAR(100) NOT NULL,
    habilidade VARCHAR(100)
);

INSERT INTO combatentes (nome_combatente, quilombo, habilidade) VALUES
    ('Ganga Zumba', 'Palmares', 'Liderança'),
    ('Zumbi dos Palmares', 'Palmares', 'Estrategista'),
    ('Dandara dos Palmares', 'Palmares', 'Guerrilha'),
    ('Aqualtune', 'Palmares', 'Coragem'),
    ('Ganga Zona', 'Palmares', 'Habilidade em armas'),
    ('Zabelê', 'Palmares', 'Resistência'),
    ('Andalaquituche', 'Palmares', 'Estrategista'),
    ('Luiz Gonzaga Pinto da Gama', 'Palmares', 'Intelectual'),
    ('Domingos Jorge Velho', 'Portugal', 'Caçador de escravos');
