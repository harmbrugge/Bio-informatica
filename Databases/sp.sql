/*
SQL Script with stored procedures depends on database made by create.sql
 */

DROP PROCEDURE IF EXISTS sp_get_genes;
DROP PROCEDURE IF EXISTS sp_get_tm_vs_probes;
DROP PROCEDURE IF EXISTS sp_mark_duplicate_oligos;
DROP PROCEDURE IF EXISTS sp_get_oligos_by_tm;
DROP PROCEDURE IF EXISTS sp_create_matrix;
DROP PROCEDURE IF EXISTS sp_get_matrices_by_quality;
DROP PROCEDURE IF EXISTS sp_create_probe;
DROP PROCEDURE IF EXISTS sp_remove_overlapping_probes_from_matrix;

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
SP which will mark all the entries with a duplicate sequence present in oligo table
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

/*
SP which selects all oligo's within a melt_temp range (min, max)
 */

CREATE PROCEDURE sp_get_oligos_by_tm(IN min DOUBLE, IN max DOUBLE)
  BEGIN
    SELECT *
    FROM oligo
    WHERE temp_melt BETWEEN min AND max;
  END //

/*
SP to create a microarray:
IN Parameters: Melting temperature, max difference
    Will set the microarray table
    Will set the probe table for al possible probes within the temperature range

 */

CREATE PROCEDURE sp_create_matrix(IN melting_t DOUBLE, IN max_difference DOUBLE)
  BEGIN
    DECLARE finished INTEGER DEFAULT 0;

    DECLARE v_oligo_id INT;
    DECLARE v_microarray_id INT;

/* Get cursor with valid probes */
    DECLARE cursor_probes CURSOR FOR SELECT id
                                     FROM oligo
                                     WHERE temp_melt BETWEEN melting_t - max_difference AND melting_t + max_difference;

    DECLARE CONTINUE HANDLER
    FOR NOT FOUND SET finished = 1;

/* Set microarray tabel & get inserted primary key */
    INSERT INTO microarray (hybrid_temp) VALUES (melting_t);
    SELECT LAST_INSERT_ID()
    INTO v_microarray_id;

/* Loop over cursor */
    OPEN cursor_probes;
    get_probes: LOOP
      FETCH cursor_probes
      INTO v_oligo_id;

      IF finished = 1
      THEN
        LEAVE get_probes;
      END IF;
/* Use SP to insert the probe into the probe tabel */
      CALL sp_create_probe(v_microarray_id, v_oligo_id);

    END LOOP get_probes;

    SELECT v_microarray_id;

  END //

CREATE PROCEDURE sp_create_probe(IN v_microarray_id INT, IN v_oligo_id INT)

  BEGIN
    INSERT INTO probe (microarray_id, oligo_id) VALUES (v_microarray_id, v_oligo_id);
  END //


/*
SP will determine how many genes have zero or one probe(s).
Sets this information into the microarray table
and selects the table sorted by genes with zero probes desc and one probe asc.
 */

CREATE PROCEDURE sp_get_matrices_by_quality()
  BEGIN
    DECLARE finished INTEGER DEFAULT 0;

    DECLARE v_microarray_id INT;
    DECLARE v_probe_count_gene INT;
    DECLARE v_probe_count_gene_1 INT;
    DECLARE v_gene_count INT;

    DECLARE cursor_microarrays CURSOR FOR SELECT id
                                          FROM microarray;

    DECLARE CONTINUE HANDLER
    FOR NOT FOUND SET finished = 1;

/* Totale count van de genen */
    SELECT count(*)
    FROM gene
    INTO v_gene_count;

    OPEN cursor_microarrays;

/* Loop over alle microarray id's */
    get_microarrays: LOOP
      FETCH cursor_microarrays
      INTO v_microarray_id;

      IF finished = 1
      THEN
        LEAVE get_microarrays;
      END IF;

/* Selecteer de count van genen met probes
   in de variable probe_count_gene
  */
      SELECT count(*)
      FROM (
             SELECT COUNT(p.id)
             FROM gene g JOIN oligo o ON g.id = o.gene_id
               JOIN probe p ON p.oligo_id = o.id
             WHERE p.microarray_id = v_microarray_id
             GROUP BY g.id
             HAVING COUNT(p.id) > 0) AS micro_array_0_table
      INTO v_probe_count_gene;

/* Selecteer de count van genen met 1 probes
   in de variable v_probe_count_gene_1
  */
      SELECT count(*)
      FROM (
             SELECT COUNT(p.id)
             FROM gene g JOIN oligo o ON g.id = o.gene_id
               JOIN probe p ON p.oligo_id = o.id
             WHERE p.microarray_id = v_microarray_id
             GROUP BY g.id
             HAVING COUNT(p.id) = 1) AS micro_array_1_table
      INTO v_probe_count_gene_1;

/* Insert values into microarray table */
      UPDATE microarray
      SET gene_count_zero = v_gene_count - v_probe_count_gene, gene_count_one = v_probe_count_gene_1
      WHERE id = v_microarray_id;

    END LOOP get_microarrays;

/* Select query to get resultset
   (Uit de opdracht kon ik niet precies opmaken hoe er moest worden gesort)*/
    SELECT *
    FROM microarray
    ORDER BY gene_count_zero DESC, gene_count_one ASC;

  END //

/* Sp which will remove duplicate probes in a microarray */

CREATE PROCEDURE sp_remove_overlapping_probes_from_matrix(IN v_microarray_id INT)
  BEGIN

    CALL sp_mark_duplicate_oligos();
    DELETE FROM probe
    WHERE id IN (SELECT p.id
                 FROM probe p JOIN oligo o ON o.id = p.oligo_id
                 WHERE p.microarray_id = v_microarray_id AND o.duplicate = TRUE);

  END //

DELIMITER ;







