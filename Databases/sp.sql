/*
SQL Script with stored procedures depends on database made by create.sql
 */

DROP PROCEDURE IF EXISTS sp_get_genes;
DROP PROCEDURE IF EXISTS sp_get_tm_vs_probes;
DROP PROCEDURE IF EXISTS sp_mark_duplicate_oligos;
DROP PROCEDURE IF EXISTS sp_get_oligos_by_tm;

DELIMITER //

/*
SP to get all entries from gene table
 */

CREATE PROCEDURE sp_get_genes()

  BEGIN
    SELECT
      external_id,
      sequence
    FROM gene;
  END //

/*
SP which will divide the number of oligo entries by the number of enties with a unique melting temperature
 */

CREATE PROCEDURE sp_get_tm_vs_probes(OUT out_param DOUBLE)

  BEGIN
    DECLARE oligo_count INT;
    DECLARE oligo_unique_count INT;

    SELECT count(*)
    FROM oligo
    INTO oligo_count;
    SELECT count(DISTINCT temp_melt)
    FROM oligo
    INTO oligo_unique_count;

    SELECT oligo_count / oligo_unique_count
    INTO out_param;

  END //

/*
SP which will mark all the enties with a duplicate sequence present in oligo table
return: number of marked oligo's
 */

CREATE PROCEDURE sp_mark_duplicate_oligos()

  BEGIN
    UPDATE oligo
    SET duplicate = FALSE;

    UPDATE oligo
      RIGHT JOIN (SELECT
                    sequence,
                    id
                  FROM oligo
                  GROUP BY sequence
                  HAVING count(sequence) > 1) AS duplicates ON oligo.sequence = duplicates.sequence
    SET duplicate = TRUE;

    SELECT count(*)
    FROM oligo
    WHERE duplicate = TRUE;

  END //

CREATE PROCEDURE sp_get_oligos_by_tm(IN min DOUBLE, IN max DOUBLE)
  BEGIN
    SELECT *
    FROM oligo
    WHERE cg_perc BETWEEN min AND max;
  END //

CREATE PROCEDURE sp_create_matrix(IN melting_t DOUBLE, IN max_difference DOUBLE, OUT id INT)
  BEGIN
    DECLARE finished INTEGER DEFAULT 0;
    DECLARE test varchar(255) DEFAULT '';


    DECLARE probes CURSOR FOR SELECT *
                              FROM oligo
                              WHERE cg_perc BETWEEN melting_t - max_difference AND melting_t + max_difference;

    DECLARE CONTINUE HANDLER
    FOR NOT FOUND SET finished = 1;

    OPEN probes;


  END //







