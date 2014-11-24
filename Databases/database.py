#!/usr/bin/python3
import pymysql


class Database:
    """
    Database class manages the connection and
    data transfer to and from MySQL Server
    """

    def __init__(self):
        self.host = "mysql.bin"
        self.user = "hbrugge"
        self.passwd = "Idg6a0ki!"
        self.db = "Hbrugge"
        self.conn = None
        self.cur = None

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

        self.cur.execute(
            "SELECT c.naam, e.cijfer, e.ex_datum "
            "FROM studenten s "
            "INNER JOIN examens e ON e.stud_id = s.stud_id "
            "INNER JOIN cursussen c ON c.cur_id = e.cur_id WHERE s.naam = '{0}' "
            "ORDER BY e.ex_datum DESC".format(stud_name))
        self.cur.close()

        return self.cur.fetchall()

    def check_injections(self, sql):
        
        pass