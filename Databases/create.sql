 /*
SQL Script voor een database model voor de opslag van probes bedoelt voor
een microarray voor een bepaald organisme

DROP statements om de tabellen te verwijderen die reeds bestaan
*/

DROP TABLE IF EXISTS probe;
DROP TABLE IF EXISTS microarray;
DROP TABLE IF EXISTS oligo;
DROP TABLE IF EXISTS gene;
DROP TABLE IF EXISTS chromosome;
DROP TABLE IF EXISTS organism;


CREATE TABLE organism (
    /*
    Organism tabel:
        Met alleen een auto-increment id en een verplichte naam
    */
    id            INT         NOT NULL AUTO_INCREMENT,
    name          VARCHAR(45) NOT NULL,

    PRIMARY KEY (id)
    );


CREATE TABLE chromosome (
    /*
    Chromosome tabel:
        Auto increment id en een foreign key naar de organism tabel.
        Mogelijkheid om een external id en volledige sequentie op te slaan.
    */
    id            INT         NOT NULL AUTO_INCREMENT,
    organism_id   INT         NOT NULL,
    external_id   VARCHAR(45) NULL DEFAULT NULL,
    sequence      TEXT        NULL DEFAULT NULL,

    PRIMARY KEY (id),
    INDEX organism_id (organism_id),
    FOREIGN KEY (organism_id)
        REFERENCES organism(id)
    );


CREATE TABLE gene (
    /*
    Gene tabel:
        Auto increment id en een foreign key naar chromosome tabel.
        Verplichte external identifier en sequentie
        Mogelijkheid om de positie op het corresponderende chromosoom op te slaan
    */
    id            INT         NOT NULL AUTO_INCREMENT,
    chromosome_id INT         NOT NULL,
    external_id   VARCHAR(45) NOT NULL,
    sequence      TEXT        NOT NULL,
    start         INT         NULL DEFAULT NULL,
    stop          INT         NULL DEFAULT NULL,
    strand        CHAR(1)     NULL DEFAULT '+',

    PRIMARY KEY (id),
    INDEX chromosome_id (chromosome_id),
    FOREIGN KEY (chromosome_id)
        REFERENCES chromosome(id)
    );


CREATE TABLE oligo (
    /*
    Oligo tabel:
        Auto increment id en een foreign key naar gene tabel.
        Verplichte G/C percentage, smelttemperatuur en sequentie velden
    */
    id            INT         NOT NULL AUTO_INCREMENT,
    gene_id       INT         NOT NULL,
    cg_perc       DOUBLE      NOT NULL,
    temp_melt     DOUBLE      NOT NULL,
    sequence      CHAR(25)    NOT NULL,
    duplicate     BOOL        NULL DEFAULT FALSE,

    PRIMARY KEY (id),
    INDEX gene_id (gene_id),
    FOREIGN KEY (gene_id)
        REFERENCES gene(id)
    );


CREATE TABLE microarray (
    /*
    Microarray tabel:
        Auto increment id en een optionele optimale hybridisatie temperatuur
    */
    id            INT         NOT NULL AUTO_INCREMENT,
    hybrid_temp   INT         NULL DEFAULT NULL,

    PRIMARY KEY (id)
    );


CREATE TABLE probe (
    /*
    Probe tabel:
        Koppeltabel tussen oligo en microarray tabel
        pos x en y optioneel voor bepaling van de positie van de probe op de microarray
    */
    id            INT         NOT NULL AUTO_INCREMENT,
    microarray_id INT         NOT NULL,
    oligo_id      INT         NOT NULL,
    pos_x         INT         NULL DEFAULT 0,
    pos_y         INT         NULL DEFAULT 0,

    PRIMARY KEY (id),
    INDEX micro_oligo (microarray_id, oligo_id),
    FOREIGN KEY (microarray_id)
        REFERENCES microarray(id),
    FOREIGN KEY (oligo_id)
        REFERENCES oligo(id)
    );

insert into organism (id, name) values(1, 'Alien');

LOAD DATA LOCAL INFILE 'chromosomes.csv'
    INTO TABLE chromosome
    FIELDS
        TERMINATED BY ';'
    IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'genes.csv'
    INTO TABLE gene
    FIELDS
        TERMINATED BY ';'
    IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'probes.csv'
    INTO TABLE oligo
    FIELDS
        TERMINATED BY ';'
    IGNORE 1 LINES;