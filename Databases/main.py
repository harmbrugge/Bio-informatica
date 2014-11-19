#!/usr/bin/python3
import database
import getpass


def main():
    #host = input('Host: ')
    #username = input('Gebruikersnaam: ')
    #schema = input('Schema: ')
    host = "localhost"
    username = "root"
    schema = "test"

    db = database.Database(host, username, getpass.getpass('Wachtwoord: '), schema)
    db.open_connection()
    students = db.get_students()
    results = db.get_results("hofman")
    names = db.get_names()
    print(names)


if __name__ == '__main__':
    main()