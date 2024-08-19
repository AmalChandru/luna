from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app
from app.forms.forms import BookIssueForm, BookReturnForm
from datetime import datetime
from bson import ObjectId

# Create a Blueprint for transaction-related routes
transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.route('/')
def list_transactions():
    """List all transactions in the database"""
    db = current_app.db
    transactions = db.transactions.find()
    return render_template('transactions/list.html', transactions=transactions)

def is_transaction_valid(book, member):
    """Check if the transaction can be created based on book availability and member debt."""
    return book and book['available_copies'] >= 1 and member and member['outstanding_debt'] < 500

def decrement_book_copies(book_name):
    """Decrease the available copies of the specified book by 1."""
    db = current_app.db
    db.books.update_one(
        {'title': book_name},
        {'$inc': {'available_copies': -1}}  # Decrease available quantity by 1
    )

def increment_member_books(member_name):
    """Increase the number of books borrowed by the specified member by 1."""
    db = current_app.db
    db.members.update_one(
        {'name': member_name},
        {'$inc': {'no_of_books_borrowed': 1}}  # Increase the borrowed book quantity by 1
    )

def create_new_transaction(form):
    """Create a new transaction record based on the form data."""
    return {
        'book_name': form.book_name.data,
        'member_name': form.member_name.data,
        'fee_per_day': form.fee_per_day.data,
        'issue_date': datetime.now().strftime('%Y-%m-%d'),
        'return_date': '',
        'total_fee': 0,
        'amount_paid': 0,
        'status': 'Return'
    }

@transactions_bp.route('/create', methods=['GET', 'POST'])
def create_transaction():
    """Create a new transaction in the database"""
    db = current_app.db
    books = db.books.find()  # Fetch all books from the database
    members = db.members.find()  # Fetch all members from the database
    form = BookIssueForm(request.form)

    if request.method == 'POST' and form.validate():
        book = db.books.find_one({'title': form.book_name.data})
        member = db.members.find_one({'name': form.member_name.data})

        if is_transaction_valid(book, member):
            new_transaction = create_new_transaction(form)

            try:
                decrement_book_copies(form.book_name.data)
                increment_member_books(form.member_name.data)
                db.transactions.insert_one(new_transaction)  # Insert the new transaction into the database
                flash('Transaction created successfully!', 'success')
            except Exception as e:
                flash(f'Error creating transaction: {e}', 'error')  # Handle insertion errors
        else:
            flash('Transaction cannot be created: Check book availability or member debt.', 'error')

        return redirect(url_for('transactions.list_transactions'))  # Redirect to the transaction list

    return render_template('transactions/issue.html', books=books, members=members)

def update_transaction_record(transaction_id, amount_paid, transaction_info):
    """Update the transaction record in the database."""
    db = current_app.db
    db.transactions.update_one(
        {'_id': ObjectId(transaction_id)},
        {
            '$set': {
                'return_date': datetime.now().strftime('%Y-%m-%d'),
                'total_fee': float(transaction_info['amount_due']),
                'amount_paid': amount_paid,
                'status': 'Closed'
            }
        }
    )

def update_member_record(transaction, amount_paid, transaction_info):
    """Update the member's record in the database."""
    db = current_app.db
    db.members.update_one(
        {'name': transaction['member_name']},
        {
            '$inc': {
                'no_of_books_borrowed': -1,
                'total_amount_spent': amount_paid,
                'outstanding_debt': transaction_info['amount_due'] - amount_paid
            }
        }
    )

def increment_book_copies(transaction):
    """Increment the available copies of the specified book by 1."""
    db = current_app.db
    db.books.update_one(
        {'title': transaction['book_name']},
        {
            '$inc': {
                'available_copies': 1
            }
        }
    )

@transactions_bp.route('/close/<transaction_id>', methods=['GET', 'POST'])
def close_transaction(transaction_id):
    db = current_app.db
    transaction = db.transactions.find_one({'_id': ObjectId(transaction_id)})  # Fetch the transaction record from the database
    
    # Calculate transaction info based on the existing record
    issue_date = datetime.strptime(transaction['issue_date'], '%Y-%m-%d')
    days_rented = (datetime.now() - issue_date).days  # Calculate days rented
    transaction_info = {
        '_id': transaction['_id'],
        'per_day_fee': transaction['fee_per_day'],
        'borrowed_on': issue_date.strftime('%Y-%m-%d'),
        'rented_for': days_rented,
        'amount_due': transaction['fee_per_day'] * days_rented
    }
    
    if request.method == 'GET':
        return render_template('transactions/return.html', transaction_info=transaction_info)
    
    if request.method == 'POST':
        form = BookReturnForm(request.form)
        amount_paid = float(form.amount_paid.data)  # Get the amount paid from the form

        try:
            update_transaction_record(transaction_id, amount_paid, transaction_info)
            update_member_record(transaction, amount_paid, transaction_info)
            increment_book_copies(transaction)

            flash('Transaction closed successfully!', 'success')
        except Exception as e:
            flash(f'Error closing transaction: {e}', 'error')  # Handle any errors during the update process

        return redirect(url_for('transactions.list_transactions'))