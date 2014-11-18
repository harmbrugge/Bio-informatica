#!/usr/bin/python3
import sys
import getpass
import os
#sys.path.append('/homes/hbrugge/pymysql/')
import pymysql


class Protein:

    def __init__(self, id, contig, start, stop, length, strand):
        self.id = id
        self.contig = contig
        self.start = start
        self.stop = stop
        self.length = length
        self.strand = strand

    def __str__(self):
        return '\nLengte:\n' + str(self.length) + '\n\nSequentie:\n' + self.seq

    def setSeq(self, seq):
        self.seq = seq

class DataBase:

    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def openConnection(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        self.cur = self.conn.cursor()

    def closeConnection(self):
        self.cur.close()
        self.conn.close()

    def writeProtein(self, protein):
        self.cur.execute('insert into orfs (id, contig_id, sequence, start, stop, strand) values (%s,%s,%s,%s,%s,%s)', (protein.id, protein.contig, protein.seq, protein.start, protein.stop, protein.strand))
        self.cur.connection.commit()

def readFile(fileToRead):

    '''	Leest een .fasta file met meerdere orfs en returnt een lijst
        met Protein objecten
    '''

    proteins = []
    proteinsObjs = []

    fo = open(fileToRead, "r+")

    i = 0
    for line in fo:
        if '>' in line:
            fields = line.split('|')
            position = fields[2].split('..')
            strand = 0
            if fields[4] == '+':
                strand = 1

            proteinsObjs.append(Protein(fields[0][1:],fields[1][6:],position[0],position[1],fields[3],strand))
            i += 1
            proteins.append('')
        else:
            proteins[i-1] += line.rstrip()

    fo.close()

    i2 = 0
    for protein in proteins:
        proteinsObjs[i2].setSeq(proteins[i2])
        i2 += 1

    return proteinsObjs

def writeToDb(proteins):
    ''' Verwacht een lijst met Protein objecten en schrijft ze weg in de database
    '''

    host = input('Host: ')
    username = input('Gebruikersnaam: ')
    schema = input('Schema: ')
    dataBase = DataBase(host, username, getpass.getpass('Wachtwoord: '), schema)

    try:
        dataBase.openConnection()
    except:
        sys.exit('Verbinding mislukt(verkeerde gebuikersnaam of wachtwoord?)')

    for protein in proteins:
        dataBase.writeProtein(protein)

    print('ORF\'s in database geladen...')

    dataBase.closeConnection()

def writeFasta(proteins):
    ''' Verwacht een lijst met Protein objecten en schrijft als single Fasta file
        weg in de map orfs
    '''

    if not os.path.isdir('orfs'):
        os.makedirs('orfs')

    for protein in proteins:
        # Maakt nieuw .fasta bestand aan
        fo = open('orfs/orf' + protein.id + '.fa', mode = 'w')
        # Eerste regel in het .fasta bestand + enter
        fo.write('>' + protein.id + '|Contig' + protein.contig + '|' + protein.start + '..' + protein.stop + '|' + str(protein.strand) +'\n')

        # Telt de sequentie op, en na 60 bp schrijft hij hem weg met een enter
        i = 0
        seqNew = ''
        for letter in protein.seq:
            seqNew += letter
            i += 1
            if i % 60 == 0:
                fo.write(seqNew + '\n')
                seqNew = ''
        # Schrijft laatste regel weg
        if len(seqNew) != 0:
            fo.write(seqNew)

        fo.close()

    print('ORF\'s naar map orfs\\ geschreven')


def main():

    # Checkt of er een commandline argument mee is gegeven
    if len(sys.argv) == 1:
        sys.exit('Geen bestand opgegeven')

    #Leest het ingevoerde bestand, de method readFile returnt een lijst met Protein objecten
    proteins = readFile(sys.argv[1])

    print('\n\nBestand', sys.argv[1], 'geladen')


    writeToDb(proteins)
    writeFasta(proteins)


if  __name__ =='__main__':main()
