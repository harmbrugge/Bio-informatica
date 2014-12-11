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
    def _get_configurations():
        config_info = dict()

        file = open('config.my.cnf', 'r')

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

    def get_names(self):
        """
        Get student names
        :return: A list with all the student names from DB
        """
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT naam FROM studenten")
        self.cur.close()

        return [item[0] for item in self.cur.fetchall()]

    def get_students(self):
        """
        Gets all the information in studenten table
        :return: A list with dictionaries for every student, key will be the column name
        """
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("SELECT * FROM studenten")
        self.cur.close()

        return self.cur.fetchall()

    def get_results(self, stud_name):
        """
        Gets exam data for one student
        :param stud_name: Last name of student
        :return: A list with dictionaries for every exam, key will be the column name
        """
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute(
            "SELECT c.naam, e.cijfer, e.ex_datum "
            "FROM studenten s "
            "INNER JOIN examens e ON e.stud_id = s.stud_id "
            "INNER JOIN cursussen c ON c.cur_id = e.cur_id WHERE s.naam = '{0}' "
            "ORDER BY e.ex_datum DESC".format(stud_name))
        self.cur.close()

        return self.cur.fetchall()

    def get_genes(self):
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("call sp_get_genes()")
        self.conn.next_result()
        # self.cur.callproc('sp_get_genes')

        self.cur.close()

        return self.cur.fetchall()

    def get_tm_vs_probes(self):
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("call sp_get_tm_vs_probes(@temp)")
        self.cur.execute("select @temp")
        # self.cur.callproc('sp_get_genes')

        self.cur.close()

        return self.cur.fetchall()

    @staticmethod
    def check_injections(sql):
        regex = "(\sor\s)|(\sand\s)|;|="
        if re.search(regex, sql.lower()):
            return True

        return False

if __name__ == '__main__':
    database = Database()
    database.open_connection()
    genes = database.get_genes()
    print(genes)
    tm_vs_probes = database.get_tm_vs_probes()
    print(tm_vs_probes)
    database.close_connection()