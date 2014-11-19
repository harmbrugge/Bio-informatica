#!/usr/bin/python3


class Website:
    def __init__(self):
        self.header = None
        self.footer = None

    def get_header(self, title):
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
                      '</div>' \
                      '<br/>' \
                      '<div class="row content">' \
                      '<div class="content-main">' \
                      '<br/>' \
                      '<p class="lead content-title">' + title + '</p>'
        return self.header

    def get_footer(self):
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

    def make_table(self, dictionary):
        pass