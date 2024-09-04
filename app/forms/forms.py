from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, validators
from wtforms.validators import NumberRange

# BookForm 
class BookForm(FlaskForm):
    title = StringField('Title', [validators.InputRequired()])
    author = StringField('Author', [validators.InputRequired()])
    description = StringField('Description')
    isbn = StringField('ISBN', [validators.InputRequired()])
    publisher = StringField('Publisher')
    publication_year = IntegerField('Publication Year')
    quantity = IntegerField('Quantity', [validators.InputRequired()])
    available_copies = IntegerField('Available Copies', [validators.InputRequired()])
    location = StringField('Location')
    genre = StringField('Genre')
    subject = StringField('Subject')

# MemberForm
class MemberForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired()])
    address = StringField('Address', [validators.InputRequired()])
    phone = StringField('Phone', [validators.InputRequired()])

# BookIssueForm
class BookIssueForm(FlaskForm):
    book_name = StringField('Book Name', [validators.InputRequired()])
    member_name = StringField('Member Name', [validators.InputRequired()])
    fee_per_day = IntegerField('Fee/Day', [validators.InputRequired()])

# BookReturnForm
class BookReturnForm(FlaskForm):
    amount_paid = IntegerField('Amount Paid', [validators.InputRequired()])

# ImportsForm
class ImportBooksForm(FlaskForm):
    no_of_books = IntegerField('No of Books', [validators.InputRequired()])
    quantity_per_book = IntegerField('Quantity Per Book', [validators.InputRequired()])
    title = StringField('Title')
    author = StringField('Author')
    isbn = StringField('ISBN')
    publisher = StringField('Publisher')
