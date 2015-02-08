from io import StringIO
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
def process_string(csv_string, table_align='l'):
    """Take a raw csv string and convert it into a table"""
    # TODO - Does this work with non ASCII characters?
    csv_io = StringIO(csv_string)

    table = prettytable.from_csv(csv_io)

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
