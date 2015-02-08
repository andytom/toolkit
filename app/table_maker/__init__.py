import csv
from StringIO import StringIO
from flask import Blueprint, render_template, g
from flask_wtf import Form
import prettytable
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import Required


table_maker = Blueprint('table_maker', __name__, template_folder='templates')


#-----------------------------------------------------------------------------#
# Hooks
#-----------------------------------------------------------------------------#
@table_maker.before_request
def before_request():
    g.title = 'Table Maker'


#-----------------------------------------------------------------------------#
# Helper methods
#-----------------------------------------------------------------------------#
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def process_string(csv_string, table_align='l'):
    """Take a raw csv string and convert it into a table"""
    csv_io = StringIO(csv_string)

    dialect = csv.Sniffer().sniff(csv_io.read(1024))
    csv_io.seek(0)

    reader = unicode_csv_reader(csv_io, dialect)

    table = prettytable.PrettyTable()

    table.field_names = [x.strip() for x in reader.next()]

    for row in reader:
        table.add_row([x.strip() for x in row])

    table.align = table_align

    return table.get_string()


#-----------------------------------------------------------------------------#
# Forms
#-----------------------------------------------------------------------------#
class csv_form(Form):
    # TODO - Write a validator for the CSV string
    content = TextAreaField('CSV string', validators=[Required()])
    table_align = SelectField('Table Alignment',
                              choices=[
                                ('l', 'Left'),
                                ('c', 'Centre'),
                                ('r', 'Right')
                              ])


#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@table_maker.route('/', methods=['GET', 'POST'])
def index():
    form = csv_form()

    if form.validate_on_submit():
        table = process_string(form.content.data, form.table_align.data)
        return render_template('table_maker/result.html', table=table)
    return render_template('table_maker/index.html', form=form)
