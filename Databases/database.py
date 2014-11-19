#!/usr/bin/python3
import pymysql


class Database:
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = None
        self.cur = None

    def open_connection(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)

    def close_connection(self):
        self.conn.close()

    def get_names(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT naam FROM studenten")
        self.cur.close()

        return [item[0] for item in self.cur.fetchall()]

    def get_students(self):
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("SELECT * FROM studenten")
        self.cur.close()

        return self.cur.fetchall()

    def get_results(self, stud_name):
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute(
            "SELECT e.* FROM studenten s INNER JOIN examens e ON e.stud_id = s.stud_id "
            "WHERE s.naam = '{0}'".format(stud_name))
        self.cur.close()

        return self.cur.fetchall()