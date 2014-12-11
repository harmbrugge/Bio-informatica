DROP PROCEDURE IF EXISTS sp_get_genes;
DROP PROCEDURE IF EXISTS sp_get_tm_vs_probes;
DROP PROCEDURE IF EXISTS sp2;

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

    SELECT
      count(*)
    FROM oligo
    INTO oligo_count;
    SELECT
      count(DISTINCT temp_melt)
    FROM oligo
    INTO oligo_unique_count;

    SELECT
      oligo_count / oligo_unique_count
    INTO out_param;

  END //

DELIMITER ;


