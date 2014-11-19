#!/usr/bin/python3
import cgi
import database
import website


def main():
    # Open connection
    db = database.Database("mysql.bin", "hbrugge", "Idg6a0ki!", "Hbrugge")
    db.open_connection()

    # Get student names
    names = db.get_names()

    # Get url parameters
    parameters = cgi.FieldStorage()
    results = ()
    if 'student' in parameters.keys():
        results = db.get_results(parameters['student'].value)

    # Close connection
    db.close_connection()

    html = website.Website()

    print("Content-Type: text/html")
    print()

    print(html.get_header("Studenten"))

    print('<div class="panel panel-default"><div class="panel-body">')
    print('<table class="table table-hover"><thead><tr><th>Student</th></tr></thead>')
    print('<tbody>')
    for name in names:
        print('<tr><td><a href="show_students.py?student=' + name + '">' + name + '</a></td></tr>')
    print('</tr>')
    print('</tbody>')
    print('</table>')
    print('</div></div>')

    if 'student' in parameters.keys():
        print('<script type="text/javascript">')
        print('bootbox.alert("' + str(results) + '")')
        print('</script>')

    print(html.get_footer())


if __name__ == '__main__':
    main()
