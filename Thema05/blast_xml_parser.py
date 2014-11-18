#!/usr/bin/python

'''
Reads a BLAST XML output file and inserts relevant information into the database

Parsing XML BLAST output using BioPythons NCBI XML parser results in a generator
object, i.e. it will give a new result (blast record) each time the records.next()
function is called. Two use cases are either converting to a list: 
blast_record_list = list(blast_records) or using it in a loop (very memory efficient)
as shown below in the process_blast_records() function. 

See the NCBIXML
manual for a list of all data elements stored and further usage examples:
http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc90, chapter 7
'''

import sys, os, pymysql, getpass

from Bio.Blast import NCBIXML

def read_blast_xml(xml_file_name):
    ''' Uses the BioPython NCBI XML parser to create a generator object '''
    result_handle = open(xml_file_name, 'r')
    return NCBIXML.parse(result_handle)

def parse_blast_records(blast_records):
    ''' PROTOTYPE function printing information on all BLAST records given in
        the blast_records generator object '''

    username = input('Username: ')

    # Connect to DB

    # Connectie locale database
    conn = pymysql.connect(host='localhost', user=username, passwd=getpass.getpass('Wachtwoord: '), db='Hbrugge')
    # Connectie voor bin netwerk
    #conn = pymysql.connect(host='mysql.bin', user=username, passwd=getpass.getpass('Wachtwoord: '), db=username[0:1].upper() + username[1:])
    cur = conn.cursor()

    # Voor het testen erg handig om eerst oude records te verwijderen
    cur.execute('delete from blasts')
    cur.connection.commit()
    
    # Counter om een unieke id zeker te stellen
    i = 1

    for record in blast_records:
        # De blast data verzamalen op een dict
        blast_data = {}

        fields = record.query.split('|')
        blast_data['orf_id'] = fields[0]

        for alignment in record.alignments:

            # standaard counter
            blast_data['id'] = i
            i += 1
            blast_data['blast_id'] = alignment.hit_id
            for hsp in alignment.hsps:

                blast_data['sequence'] = hsp.sbjct
                blast_data['midline'] = hsp.match
                blast_data['midline_length'] = hsp.align_length

                # hit_def geeft in sommige gevallen een hele hoop data die worden
                # met de volgende regels geparst
                hit_def = alignment.hit_def.split(']')[0]

                if 'RecName' in hit_def:
                    if '|' in hit_def:
                        blast_data['hit_def'] = hit_def.split('|')[-1][1:]
                    else:
                        blast_data['hit_def'] = hit_def.split('=')[-1]
                else:
                    blast_data['hit_def'] = hit_def 

                # Verder parsen van hit_def op virus type en en eiwit naam
                # Data komt niet altijd overeen, dus in except worden deze waardes op NA gezet
                try:
                    hit_def_fields = blast_data['hit_def'].split('[')
                    blast_data['protein'] = hit_def_fields[0]
                    hit_def_fields_2 = hit_def_fields[1].split('(')
                    blast_data['virus'] = hit_def_fields_2[0]
                    blast_data['location'] = hit_def_fields_2[1]
                    blast_data['classification'] = hit_def_fields_2[2]
            
                    if '(' in blast_data['protein']:
                        blast_data['protein'] = blast_data['protein'].split('-')[0]
                    
                    if '))' in blast_data['classification']:
                        blast_data['classification'] = blast_data['classification'].replace('))','')  
            
                except:
                    blast_data['protein'] = 'NA'
                    blast_data['virus'] = 'NA'
                    blast_data['location'] = 'NA'
                    blast_data['classification'] = 'NA'
                
                blast_data['hit_start'] = hsp.sbjct_start
                blast_data['hit_end'] = hsp.sbjct_end
                blast_data['length'] = alignment.length

                # hsp.gaps geeft als waarde (None, none), als hsp.gaps == int is dan 
                # wordt de waarde pas gezet
                blast_data['gaps'] = 0
                if type(hsp.gaps) == int:
                    blast_data['gaps'] = hsp.gaps

                blast_data['positives'] = hsp.positives
                blast_data['identities'] = hsp.identities
                blast_data['expect'] = hsp.expect
                blast_data['score'] = hsp.score
                blast_data['orf_start'] = hsp.query_start
                blast_data['orf_end'] = hsp.query_end

                # We gebruiken de .format() niet omdat deze niet goed werkend kregen
                cur.execute("INSERT INTO BLASTS (id, blast_id, orf_id, sequence, midline, midline_length, hit_start, hit_end, "
                            "protein_name, virus, virus_type, length, gaps, positives, identities, expect, score, orf_start, orf_end) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                            " %s, %s, %s, %s, %s, %s, %s, %s)", (blast_data['id'],
                                                                blast_data['blast_id'],
                                                                blast_data['orf_id'],
                                                                blast_data['sequence'],
                                                                blast_data['midline'],
                                                                blast_data['midline_length'],
                                                                blast_data['hit_start'],
                                                                blast_data['hit_end'],
                                                                blast_data['protein'],
                                                                blast_data['virus'],
                                                                blast_data['classification'],
                                                                blast_data['length'],
                                                                blast_data['gaps'],
                                                                blast_data['positives'], 
                                                                blast_data['identities'],
                                                                blast_data['expect'],
                                                                blast_data['score'],
                                                                blast_data['orf_start'],
                                                                blast_data['orf_end']))

    cur.connection.commit()          

    cur.close()
    conn.close()

def main():    
    
    # Read XML file
    blast_records = read_blast_xml(sys.argv[1])
    
    # Process records and writes to database
    parse_blast_records(blast_records)

if __name__ == '__main__':
    # Run main function
    main()
