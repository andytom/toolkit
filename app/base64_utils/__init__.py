# -*- coding: utf-8 -*-
"""
    base64_util
    ~~~~~~~~~~~
    Blueprint for working with Base64 encoded files.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
import uuid
import base64
import StringIO
import magic
import mimetypes
from flask import Blueprint, render_template, send_file, current_app
from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required


base64_utils = Blueprint('base64_utils', __name__, template_folder='templates')


#-----------------------------------------------------------------------------#
# Helper Methods
#-----------------------------------------------------------------------------#
def create_filename(extention):
    """Create a unique filename with the passed extention

       :param extention: The extention to add to the filename needs to have
                         the preceding '.' eg. '.txt'

       :returns: A unique filename with the passed extention
    """
    random_string = unicode(uuid.uuid4())
    return u''.join([random_string, extention])


def guess_extention(bin_data):
    """Guess the extention of the passed in binary data.
       Will default to '.dat' if it can't work it out and will pick more common
       extentions when they are availabe.

       :param bin_data: The binary data as if you had read it in from a file.
                        eg open("example.unknown").read()

       :returns: The guessed extention of the file includes a '.'
    """
    mime_type = magic.from_buffer(bin_data, mime=True)
    current_app.logger.debug('Guessed Mime is {}'.format(mime_type))

    ext_list = mimetypes.guess_all_extensions(mime_type)
    current_app.logger.debug('Possible extentions are {}'.format(ext_list))

    if len(ext_list) == 0:
        # Default to '.dat' if we don't get anything
        current_app.logger.debug('No extentions, returning .dat')
        return '.dat'

    # Pick the more common extentions when they are available
    PREFERED_EXTS = ['.txt']
    for prefered_ext in PREFERED_EXTS:
        if prefered_ext in ext_list:
            current_app.logger.debug('Using prefered extentions '
                                     '{}'.format(prefered_ext))
            return prefered_ext

    # If not use the first in the list
    current_app.logger.debug('Returning {}'.format(ext_list[0]))
    return ext_list[0]


def base64_to_stringio(base64_string, filename=None):
    """Decode the Base64 string and write it to a stringIO

       :param base64_string: The binary data of as file encoded in base64.
       :param filename: The filename of the encoded file, Optional if not
                        if not passed a random string will be generated and
                        the filetype will be guessed.

       :returns: A tuple containing the decoded files as a StringIO and
                 the filename.
    """
    bin_data = base64.b64decode(base64_string)

    if not filename:
        current_app.logger.debug('filename is None, creating one')
        extention = guess_extention(bin_data)
        filename = create_filename(extention)
        current_app.logger.debug('filename created is {}'.format(filename))

    strIO = StringIO.StringIO()
    strIO.write(bin_data)
    strIO.seek(0)

    return strIO, filename


#-----------------------------------------------------------------------------#
# Forms
#-----------------------------------------------------------------------------#
class decode_form(Form):
    # TODO - Write a custom validator for checking the contents of the data is
    # a valid base64 string.
    content = TextAreaField('Base64', validators=[Required()])
    filename = TextField('Filename')


#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@base64_utils.route('/', methods=['GET', 'POST'])
def index():
    """Index for base64_utils.
       On submission it checks that the form is valid, if it is decodes base64
       encoded file and returns it as an attachement. If the form is not valid
       it is returned to the user for further input.

       :returns: A form that need to be completed, or a base64 decoded file
                 as an attachement.
    """
    form = decode_form()

    if form.validate_on_submit():
        current_app.logger.info('Submitted Form is valid trying to process it')
        strIO, filename = base64_to_stringio(form.content.data,
                                             form.filename.data)
        current_app.logger.info('Processed Form sending file')
        return send_file(strIO,
                         attachment_filename=filename,
                         as_attachment=True)

    current_app.logger.info('Rendering decode template')
    return render_template('base64_utils/decode.html', form=form)
