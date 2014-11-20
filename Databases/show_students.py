#!/usr/bin/python3
import cgi
import database
import website


def main():
    """
    Cgi content-type : HTML for student page
    Shows a table with all the student names
    Pop-up with exam results if student is clicked
    """
    # Open db connection
    db = database.Database("mysql.bin", "hbrugge", "Idg6a0ki!", "Hbrugge")
    db.open_connection()

    # Get url parameters
    parameters = cgi.FieldStorage()

    # Create Website object for required HTML
    html = website.Website()

    # Set content type
    print("Content-Type: text/html")
    print()

    # Get header with title Students
    print(html.get_header("Studenten"))

    # Create table in a panel
    print('<div class="panel panel-default"><div class="panel-body">')
    print('<table class="table table-hover"><thead><tr><th>Student</th></tr></thead>')
    print('<tbody>')
    # Get student names from db and print table row with link for every student
    for name in db.get_names():
        print('<tr><td><a href="show_students.py?student=' + name + '">' + name + '</a></td></tr>')
    print('</tr>')
    print('</tbody>')
    print('</table>')
    print('</div></div>')

    # Pop alert with exam results if student param exists
    if 'student' in parameters.keys():
        # Get student results from db
        results = db.get_results(parameters['student'].value)
        print('<script type="text/javascript">')
        print("bootbox.alert('<p class=\"lead text-center\">Exams: "
              + parameters['student'].value + "</p>" + html.make_table(results) + "')")
        print('</script>')

    # End with footer
    print(html.get_footer())

    # Close db connection
    db.close_connection()


if __name__ == '__main__':
    main()
