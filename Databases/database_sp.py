#!/usr/bin/python3
import pymysql
import re


class Database:
    """
    Database class manages the connection and
    data transfer to and from MySQL Server
    """

    def __init__(self):
        config = self._get_configurations()
        self.host = config["host"]
        self.user = config["user"]
        self.passwd = config["passwd"]
        self.db = config["db"]
        self.conn = None
        self.cur = None

    @staticmethod
    def check_injections(sql):
        regex = "(\sor\s)|(\sand\s)|;|="
        if re.search(regex, sql.lower()):
            return True

        return False

    @staticmethod
    def _get_configurations():
        config_info = dict()

        file = open('my.cnf', 'r')

        for line in file:
            if re.search('(.=.)', line):
                line = line.strip('\n')
                line = line.split('=')
                config_info.update({line[0]: line[1]})

        return config_info

    def open_connection(self):
        """
        Opens a connection required for any other operation
        """
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)

    def close_connection(self):
        """
        Close the connection after you're done
        """
        self.conn.close()

    def get_genes(self):
        """
        Function calls a mysql stored procedure, which return al the entries in the genes table
        :return: Dictionary with all the results from the gene table
        """
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("call sp_get_genes()")
        self.conn.next_result()
        # self.cur.callproc('sp_get_genes')

        self.cur.close()

        return self.cur.fetchall()

    def get_tm_vs_probes(self):
        """
        SP which will divide the number of oligo entries by the number of entries with a unique melting temperature
        :return: result of (total count / count with unique temp)
        """

        self.cur = self.conn.cursor()
        self.cur.execute("call sp_get_tm_vs_probes(@temp)")
        self.cur.execute("select @temp")
        # self.cur.callproc('get_tm_vs_probes')

        self.cur.close()

        return self.cur.fetchall()[0][0]

    def mark_duplicate_oligos(self):
        """
        Calls a mysql stored procedure which will mark all the entries with a duplicate sequence present in oligo table
        :return: number of marked oligo's
        """
        self.cur = self.conn.cursor()
        self.cur.execute("call sp_mark_duplicate_oligos()")
        self.conn.next_result()
        # self.cur.callproc('sp_mark_duplicate_oligos')

        self.cur.close()

        return self.cur.fetchall()[0][0]

    def sp_create_matrix(self, temp, max_difference):
        """

        :param temp:
        :param max_difference:
        :return:
        """
        self.cur = self.conn.cursor()
        self.cur.execute("call sp_create_matrix({0},{1})".format(temp, max_difference))
        self.conn.next_result()

        self.cur.close()

        print('Microarray created with id: ' + str(self.cur.fetchall()[0][0]))

    def sp_create_probe(self, microarray_id, oligo_id):
        """

        :param microarray_id:
        :param oligo_id:
        """
        self.cur = self.conn.cursor()
        self.cur.execute("call sp_create_probe({0},{1})".format(microarray_id, oligo_id))

        self.cur.close()

    def sp_get_matrices_by_quality(self):
        """

        :return:
        """
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("call sp_get_matrices_by_quality()")
        self.conn.next_result()

        self.cur.close()

        return self.cur.fetchall()

    def sp_remove_overlapping_probes_from_matrix(self):
        self.cur = self.conn.cursor()
        self.cur.execute("sp_remove_overlapping_probes_from_matrix()")

        self.cur.close()

if __name__ == '__main__':
    db = Database()
    db.open_connection()
    print(db.get_genes())
    print(db.get_tm_vs_probes())
    print(db.mark_duplicate_oligos())

    db.sp_create_matrix(50, 5)
    db.sp_create_matrix(20, 5)
    db.sp_create_matrix(80, 5)

    print(db.sp_get_matrices_by_quality())

    db.close_connection()