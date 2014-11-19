#!/usr/bin/python3
import cgi
#import database

host = "localhost"
username = "root"
schema = "test"
password = "Idg6a0ki!"

#db = database.Database(host, username, password, schema)
#db.open_connection()
#names = db.get_names()


print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers


print('<html>'
      '<head>'
      '<title>Harm Brugge - Studenten</title>'
      '<link rel="icon" href="../resources/img/dna.png"/>'
      '<link href="../resources/css/bootstrap.min.css" rel="stylesheet">'
      '<link href="../resources/css/main.css" rel="stylesheet">'
      '<script type="text/javascript" src="../resources/js/jquery.js"></script>'
      '<script src="../resources/js/bootstrap.min.js"></script>'
      '</head>'
      '<body>'
      '<div class="container shadow">'
      '<div class="logo">'
      '</div>'
      '<br/>'
      '<div class="row content">'
      '<div class="content-main">'
      '<br/>'
      '<p class="lead content-title">Studenten</p>')

#print(names)

print('</div>'
      '</div>'
      '</div>'
      '<div class="footer">'
      '<div class="container">'
      '<p class="text-muted">Copyright Harm Brugge 2014.</p>'
      '</div>'
      '</div>'
      '</body>'
      '</html>')

#arguments = cgi.FieldStorage()
#for i in arguments:
#    print(arguments[i].value)