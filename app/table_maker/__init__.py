# -*- coding: utf-8 -*-
"""
    table_maker
    ~~~~~~~~~~~
    Blueprint for converting CSV files into Tables.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
import csv
from StringIO import StringIO
from flask import Blueprint, render_template, current_app
from flask_wtf import Form
import prettytable
from wtforms import TextAreaField, SelectField, BooleanField
from wtforms.validators import Required


table_maker = Blueprint('table_maker', __name__, template_folder='templates')


#-----------------------------------------------------------------------------#
# Helper methods
#-----------------------------------------------------------------------------#
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    """Unicode CSV Reader.
       Taken from the https://docs.python.org/2/library/csv.html#examples
    """
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    """utf_8_encoder
       Taken from the https://docs.python.org/2/library/csv.html#examples
    """
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def process_string(csv_string, table_align='l', add_header=True):
    """Take a raw csv string and convert it into a table.

       :param csv_string: A CSV string to be converted into a table.
       :param table_align: The alignment for the contents of the table.
                           Valid arguments are 'l', 'c' and 'r'.
                           Optional, Defaults to 'l'
       :param add_header: If True the first row of the CSV data will be used as
                          a header. Optional, Defaults to True.

       :returns: An Ascii table of the passed in CSV data.
    """
    csv_io = StringIO(csv_string.strip())

    dialect = csv.Sniffer().sniff(csv_io.read(1024))
    csv_io.seek(0)
    current_app.logger.debug('CSV dialect is {}'.format(dialect))

    # csv reader expects the dialect delimiter and quotechar to both be a str
    # object not a unicode object.
    dialect.delimiter = str(dialect.delimiter)
    dialect.quotechar = str(dialect.quotechar)

    reader = unicode_csv_reader(csv_io, dialect)

    table = prettytable.PrettyTable()
    table.header = add_header

    if add_header:
        current_app.logger.debug('add_header is true so first row is a header')
        table.field_names = [x.strip() for x in reader.next()]

    for row in reader:
        table.add_row([x.strip() for x in row])

    table.align = table_align

    current_app.logger.debug('Table built without errors')
    return table.get_string()


#-----------------------------------------------------------------------------#
# Forms
#-----------------------------------------------------------------------------#
class csv_form(Form):
    # TODO - Write a validator for the CSV string
    csv_string = TextAreaField('CSV string', validators=[Required()])
    table_align = SelectField('Table Alignment',
                              choices=[('l', 'Left'),
                                       ('c', 'Centre'),
                                       ('r', 'Right')])
    add_header = BooleanField('Use Header', default='checked',
                              false_values=('false', '', 'n', 'f'))


#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@table_maker.route('/', methods=['GET', 'POST'])
def index():
    """Index for table_maker
       Will validate the form if it is valid will try and convert the csv to
       a table and return a rendered results page. If the form is invaid or if
       the request is a get request will return the form to be completed by the
       user.

       :returns: A form asking for CSV data or an ascii table.
    """
    form = csv_form()

    if form.validate_on_submit():
        current_app.logger.info('Form is valid, building table')
        table = process_string(form.csv_string.data,
                               form.table_align.data,
                               form.add_header.data)
        current_app.logger.info('Built table, sending response page')
        return render_template('table_maker/result.html', table=table)

    current_app.logger.debug('Rendering table_maker index')
    return render_template('table_maker/index.html', form=form)
