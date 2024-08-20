from wtforms import Form, StringField, IntegerField, validators
from wtforms.validators import NumberRange

# BookForm 
class BookForm(Form):
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
class MemberForm(Form):
    name = StringField('Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired()])
    address = StringField('Address', [validators.InputRequired()])
    phone = StringField('Phone', [validators.InputRequired()])

# TransactionForm
class TransactionForm(Form):
    book_name = StringField('Book Name', [validators.InputRequired()])
    member_name = StringField('Member Name', [validators.InputRequired()])
    fee_per_day = IntegerField('Fee/Day', [validators.InputRequired()])
    issue_date = StringField('Issue Date')
    return_date = StringField('Return Date')
    total_fee = IntegerField('Total Fee')
    amount_paid = IntegerField('Amount Paid', [validators.InputRequired()])
    status = StringField('Status')

# BookIssueForm
class BookIssueForm(Form):
    book_name = StringField('Book Name', [validators.InputRequired()])
    member_name = StringField('Member Name', [validators.InputRequired()])
    fee_per_day = IntegerField('Fee/Day', [validators.InputRequired()])

# BookReturnForm
class BookReturnForm(Form):
    amount_paid = IntegerField('Amount Paid', [validators.InputRequired()])

# ImportsForm
class ImportBooksForm(Form):
    no_of_books = IntegerField('No of Books', [validators.InputRequired(), NumberRange(min=1, max=20)])
    quantity_per_book = IntegerField('Quantity Per Book', [validators.InputRequired()])
    title = StringField('Title')
    author = StringField('Author')
    isbn = StringField('ISBN')
    publisher = StringField('Publisher')
