#!/usr/bin/python3
import cgi
import database
import cgitb


class Website:
    """
    Class with building blocks for a website.
    HTML depends on Bootstrap 3 and custom css,
    installed in ../resources/
    """
    def __init__(self):
        self.header = None
        self.footer = None
        self.table = None

    def get_header(self, title):
        """
        Function to get HTML for header of web-site
        :param title: The title of the web-page
        :return: String with complete html before content
                 (call get_footer for html after content)
        """
        self.header = '<!DOCTYPE html>' \
                      '<html>' \
                      '<head>' \
                      '<title>Harm Brugge - ' + title + '</title>' \
                      '<link rel="icon" href="../resources/img/dna.png"/>' \
                      '<link href="../resources/css/bootstrap.min.css" rel="stylesheet">' \
                      '<link href="../resources/css/main.css" rel="stylesheet">' \
                      '<script type="text/javascript" src="../resources/js/jquery.js"></script>' \
                      '<script src="../resources/js/bootstrap.min.js"></script>' \
                      '<script type="text/javascript" src="../resources/js/bootbox.min.js"></script>' \
                      '</head>' \
                      '<body>' \
                      '<div class="container shadow">' \
                      '<div class="logo">' \
                      '<h1>Harm Brugge <span class="label label-warning">Bio-informatica</span></h1>' \
                      '</div>' \
                      '<br/>' \
                      '<div class="row content">' \
                      '<div class="content-main">' \
                      '<br/>' \
                      '<p class="lead content-title">' + title + '</p>'
        return self.header

    def get_footer(self):
        """
        Function for getting the footer after custom content
        :return: String of HTML
        """
        self.footer = '</div>' \
                      '</div>' \
                      '</div>' \
                      '<div class="footer">' \
                      '<div class="container">' \
                      '<p class="text-muted">Copyright Harm Brugge 2014.</p>' \
                      '</div>' \
                      '</div>' \
                      '</body>' \
                      '</html>'
        return self.footer

    def make_table(self, content):
        """
        Function creates a HTML table out of an iterable
        :param content: Will only work on a list or tuple of Dictionary's for now.
                        Keys must be the same for every item
        :return: String of HTML with table & content
        """
        html = '<table class="table table-condensed">'

        # Check for list or tuple
        if type(content) is list or type(content) is tuple:
            # If first item in list is dictionary continue
            if len(content) > 0:
                if type(content[0]) is dict:
                    # Make table header for every key
                    html += '<thead><tr>'
                    for key in content[0].keys():
                        html += '<th>' + key + '</th>'
                    html += '</tr></thead>'

                    # Make table body
                    html += '<tbody>'
                    for dictonary in content:
                        # New table row for every dict item in list
                        html += '<tr>'
                        # New column for every value in dictionary
                        for value in dictonary.values():
                            html += '<td>' + str(value) + '</td>'
                        html += '</tr>'
                    html += '</tbody>'
            else:
                html += 'No content available'

        html += '</table>'

        self.table = html

        return html


class StudentPage:
    def __init__(self):
        self.header = None
        self.footer = None
        self.table = None
        self.body = None

    def get_header(self):
        """
        Create header from Website class
        :return: String of HTML with header and title set to Students
        """
        self.header = Website().get_header("Students")
        return self.header

    def get_body(self, parameters):
        """
        Get body for student page
        :param parameters: URL parameters to determine if student is selected
        :return: String of HTML with table of all students and pop up with grades
                 if student is selected
        """
        self.body = '<div class="panel panel-default"><div class="panel-body">' \
                    '<table class="table table-hover"><thead><tr><th>Student</th></tr></thead>' \
                    '<tbody>'
        # Open db connection
        db = database.Database()
        db.open_connection()
        # Get student names from db and print table row with link for each student
        for name in db.get_names():
            self.body += '<tr><td><a href="index.cgi?content=students&student=' + name + '">' + name + '</a></td></tr>'

        self.body += '</tr></tbody>' \
                     '</table></div></div>'

        # Pop alert with exam results if student param exists
        if 'student' in parameters.keys():
            # Get student results from db
            results = db.get_results(parameters['student'].value)
            print('<script type="text/javascript">')
            print("bootbox.alert('<p class=\"lead text-center\">Exams: "
                  + parameters['student'].value + "</p>" + Website().make_table(results) + "')")
            print('</script>')

        db.close_connection()

        return self.body


def main():
    cgitb.enable()

    # Get url parameters
    parameters = cgi.FieldStorage()

    # Create Website object for required HTML
    html = Website()

    # Set content type
    print("Content-Type: text/html")
    print()

    # Determine content from url parameter
    if 'content' in parameters.keys():
        if parameters['content'].value == 'students':
            # Get header with title Students
            student_page = StudentPage()
            print(student_page.get_header())
            print(student_page.get_body(parameters))
    else:
        print(html.get_header("Title"))

    # End with footer
    print(html.get_footer())

if __name__ == '__main__':
    main()
