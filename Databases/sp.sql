DROP PROCEDURE IF EXISTS sp_get_genes;
DROP PROCEDURE IF EXISTS sp_get_tm_vs_probes;
DROP PROCEDURE IF EXISTS sp_mark_duplicate_oligos;

DELIMITER //

CREATE PROCEDURE sp_get_genes()

  BEGIN
    SELECT
      external_id,
      sequence
    FROM gene;
  END //

CREATE PROCEDURE sp_get_tm_vs_probes(OUT out_param INT)

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

CREATE PROCEDURE sp_mark_duplicate_oligos()

  BEGIN
    UPDATE oligo
      RIGHT JOIN (SELECT
                    sequence,
                    id
                  FROM oligo
                  GROUP BY sequence
                  HAVING count(sequence) > 1) AS duplicates ON oligo.sequence = duplicates.sequence
    SET duplicate = TRUE;

  END //

DELIMITER ;
/*
Breid je sql script uit met een stored routine, sp_mark_duplicate_oligos, die oligo's/probes waarvan de
sequentie niet uniek is binnen het coderende genoom als zodanig kenmerkt. De benodigde informatie
krijgt deze stored procedure mee als parameters. Ook deze stored routine moet te benaderen zijn door
een functie in je python module.
 */


