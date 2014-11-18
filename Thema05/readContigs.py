#!/usr/bin/python3
import sys
import getpass
import os
import pymysql


class Contig:
    seq = ''
    length = 0
    percentages = {}

    def __init__(self, seq):
        self.seq = seq
        Contig.seq += seq
        self.length = len(seq)
        Contig.length += self.length

    def __str__(self):
        return '\nLengte:\n' + str(self.length) + 'bp\n\nPercentages basen:\n' + str(
            self.percentages) + '\n\nSequentie:\n' + self.seq

    def set_perc(self):
        self.percentages = {nuc: self._calculate_percentage(nuc) for nuc in ['A', 'C', 'G', 'T']}

    def _calculate_percentage(self, nuc):
        return 100 / self.length * self.seq.count(nuc)

    def getPerc(self, nuc):
        return self.percentages[nuc]


class DataBase:
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def open_connection(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def write_contig(self, contig, id):
        self.cur.execute('insert into contigs (id, sequence, length) values (%s,%s,%s)',
                         (id, contig.seq, contig.length))
        self.cur.connection.commit()


def read_file(file_to_read):
    """	Leest een .fasta file met meerdere contigs en returnt een lijst
        met Contig objecten	"""
    fo = open(file_to_read, "r")

    # Leest het bestand en laadt iedere contig op de lijst contigs[]
    contigs = []
    i = 0
    for line in fo:
        if 'Consensus' in line:
            contigs.append('')
            i += 1
        else:
            contigs[i - 1] += line.rstrip()

    # Maakt van iedere list entry een Contig object
    contig_objs = []
    for contig in contigs:
        contig_objs.append(Contig(contig))

    fo.close()

    return contig_objs


def show_contig(contigs):
    """	Verwacht een lijst met Contig objecten en print een contig naar keuze
    """
    contig_show = input('Welke contig? 1 t/m ' + str(len(contigs)) + ': ')

    if contig_show.isdigit():
        contig_show = int(contig_show)
        if contig_show in range(0, len(contigs) + 1):
            contigs[contig_show - 1].set_perc()
            print(contigs[contig_show - 1])
            show_contig(contigs)
    else:
        print('Voer een getal in!')
        show_contig(contigs)


def write_to_db(contigs):
    """ Verwacht een lijst met Contig objecten en schrijft ze weg in de database
    """
    host = input('Host: ')
    username = input('Gebruikersnaam: ')
    schema = input('Schema: ')
    database = DataBase(host, username, getpass.getpass('Wachtwoord: '), schema)

    try:
        database.open_connection()
    except:
        sys.exit('Verbinding mislukt(verkeerde gebuikersnaam of wachtwoord?)')

    i = 1
    for contig in contigs:
        database.write_contig(contig, i)
        i += 1

    print('Contigs in database geladen')

    database.close_connection()


def write_fasta(contigs):
    """ Verwacht een lijst met Contig objecten en schrijft als single Fasta file
        weg in de map contigs """

    if not os.path.isdir('contigs'):
        os.makedirs('contigs')

    i = 1
    for contig in contigs:
        # Maakt nieuw .fasta bestand aan
        fo = open('contigs/contig' + str(i) + '.fa', mode='w')
        # Eerste regel in het .fasta bestand + enter
        fo.write('>Consensus_' + str(i) + '\n')

        # Telt de sequentie op, en na 60 bp schrijft hij hem weg met een enter
        i2 = 0
        seq_new = ''
        for letter in contig.seq:
            seq_new += letter
            i2 += 1
            if i2 % 60 == 0:
                fo.write(seq_new + '\n')
                seq_new = ''
        # Schrijft laatste regel weg
        if len(seq_new) != 0:
            fo.write(seq_new)

        fo.close()
        i += 1


def main():
    # Checkt of er een commandline argument mee is gegeven
    if len(sys.argv) == 1:
        sys.exit('Geen bestand opgegeven')

    # Leest het ingevoerde bestand, de method readFile returnt een lijst met Contig objecten
    contigs = read_file(sys.argv[1])

    print('\n\nBestand', sys.argv[1], 'geladen')
    print('Aantal contigs:', len(contigs))
    print('Totale lengte:', str(Contig.length) + 'bp')

    # Gebruiker kiest actie
    action = input('1: Contigs laten zien\n2: Wegschrijven in DB:\n3: Wegschrijven als single fasta\n')

    if action == '1':
        show_contig(contigs)
    elif action == '2':
        write_to_db(contigs)
    elif action == '3':
        write_fasta(contigs)


if __name__ == '__main__':
    main()
