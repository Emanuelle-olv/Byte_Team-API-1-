USE apibyte;

CREATE TABLE vereadores (
    id INT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE partidos (
    id INT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE comissoes (
    id INT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE comentarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    comentario VARCHAR(2000) NOT NULL,
    vereador_id INT NULL,  -- Campo que aceita NULL
    partido_id INT NULL,   -- Campo que aceita NULL
    comissao_id INT NULL,  -- Campo que aceita NULL
    curtidas INT DEFAULT 0,
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vereador_id) REFERENCES vereadores(id),
    FOREIGN KEY (partido_id) REFERENCES partidos(id),
    FOREIGN KEY (comissao_id) REFERENCES comissoes(id)
);


INSERT INTO vereadores (id, nome) VALUES
(35, 'Amélia Naomi'),
(238, 'Dr. José Claudio'),
(38, 'Dulce Rita'),
(247, 'Fabião Zagueiro'),
(40, 'Fernando Petiti'),
(43, 'Juliana Fraga'),
(246, 'Junior da Farmácia'),
(44, 'Juvenil Silvério'),
(45, 'Lino Bispo'),
(47, 'Marcão da Academia'),
(244, 'Marcelo Garcia'),
(242, 'Milton Vieira Filho'),
(243, 'Rafael Pascucci'),
(245, 'Renato Santiago'),
(50, 'Robertinho da Padaria'),
(240, 'Roberto Chagas'),
(234, 'Roberto do Eleven'),
(249, 'Rogério da ACASEM'),
(239, 'Thomaz Henrique'),
(55, 'Walter Hayashi'),
(237, 'Zé Luís');


INSERT INTO partidos (id, nome) VALUES
(1, 'Avante'),
(2, 'Cidadania'),
(3, 'Democracia Cristã (DC)'),
(4, 'Movimento Democrático Brasileiro (MDB)'),
(5, 'Partido Comunista Brasileiro (PCB)'),
(6, 'Partido Comunista do Brasil (PCdoB)'),
(7, 'Partido da Causa Operária (PCO)'),
(8, 'Partido da Mulher Brasileira (PMB)'),
(9, 'Partido da Renovação Democrática (PRD)'),
(10, 'Partido Democrático Trabalhista (PDT)'),
(11, 'Partido Liberal (PL)'),
(12, 'Partido Novo (NOVO)'),
(13, 'Partido Progressistas (PP)'),
(14, 'Partido Republicano da Ordem Social (PROS)'),
(15, 'Partido Renovador Trabalhista Brasileiro (PRTB)'),
(16, 'Partido Social Cristão (PSC)'),
(17, 'Partido Social Democrático (PSD)'),
(18, 'Partido Social Democracia Brasileira (PSDB)'),
(19, 'Partido Socialista Brasileiro (PSB)'),
(20, 'Partido Socialismo e Liberdade (PSOL)'),
(21, 'Partido Socialista dos Trabalhadores Unificado (PSTU)'),
(22, 'Partido Trabalhista Brasileiro (PTB)'),
(23, 'Partido dos Trabalhadores (PT)'),
(24, 'Podemos (PODE)'),
(25, 'Rede Sustentabilidade (REDE)'),
(26, 'Republicanos'),
(27, 'Solidariedade'),
(28, 'Unidade Popular (UP)'),
(29, 'União Brasil'),
(30, 'Aliança pelo Brasil (em formação)'),
(31, 'Patriota'),
(32, 'Partido Verde (PV)'),
(33, 'Progressistas (PP)');


INSERT INTO comissoes (id, nome) VALUES
(37, 'Comissão de Cultura e Esportes'),
(43, 'Comissão de Economia, Finanças e Orçamento'),
(26, 'Comissão de Educação e Promoção Social'),
(40, 'Comissão de Ética'),
(39, 'Comissão de Justiça, Redação e Direitos Humanos'),
(42, 'Comissão de Meio Ambiente'),
(41, 'Comissão de Planejamento Urbano, Obras e Transportes'),
(38, 'Comissão de Saúde');
