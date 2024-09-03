from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.forms.forms import ImportBooksForm
import requests

# Create a Blueprint for import_books-related routes
import_books_bp = Blueprint('import_books', __name__, url_prefix='/import_books')

@import_books_bp.route('/', methods=['GET', 'POST'])
def import_books():
    form = ImportBooksForm(request.form)
    if request.method == 'POST' and form.validate():
        url = 'https://frappe.io/api/method/frappe-library?'
        parameters = build_parameters(form)

        no_of_books_imported, repeated_book_names, books_to_insert = 0, [], []
        while no_of_books_imported < form.no_of_books.data:
            db = current_app.db
            response = requests.get(url, params=parameters).json()
            if not response['message']:
                flash('No books found.', 'error')
                break
            
            no_of_books_imported, repeated_book_names = process_books(response['message'], form, db, books_to_insert, no_of_books_imported, repeated_book_names)

            try:
                if books_to_insert:
                    db.books.insert_many(books_to_insert)
            except Exception as e:
                flash(f"Error inserting books: {e}", 'error')

            flash_success_warning_message(no_of_books_imported, form.no_of_books.data, repeated_book_names)
            return redirect(url_for('books.list_books'))

    return render_template('import_books/form.html', form=form)

def build_parameters(form):
    parameters = {'page': 1}
    if form.title.data:
        parameters['title'] = form.title.data
    if form.author.data:
        parameters['authors'] = form.author.data
    if form.isbn.data:
        parameters['isbn'] = form.isbn.data
    if form.publisher.data:
        parameters['publisher'] = form.publisher.data
    return parameters

def process_books(books, form, db, books_to_insert, no_of_books_imported, repeated_book_names):
    for book in books[:form.no_of_books.data]:
        existing_book = db.books.find_one({'title': book['title']})
        if not existing_book:
            new_book = {
                'title': book['title'],
                'author': book['authors'],
                'description': '',
                'isbn': book['isbn'],
                'publisher': book['publisher'],
                'publication_year': book['publication_date'].split('/')[-1],
                'quantity': form.quantity_per_book.data,
                'available_copies': form.quantity_per_book.data,
                'location': '',
                'genre': '',
                'subject': ''
            }
            books_to_insert.append(new_book)
            no_of_books_imported += 1
        else:
            repeated_book_names.append(book['title'])
    return no_of_books_imported, repeated_book_names

def flash_success_warning_message(no_of_books_imported, total_books, repeated_book_names):
    msg = f"{no_of_books_imported}/{total_books} books have been imported. "
    msgType = 'success' if no_of_books_imported == total_books else 'warning'
    if repeated_book_names:
        msg += f"{len(repeated_book_names)} books were found with already existing IDs."
    else:
        msg += f"{total_books - no_of_books_imported} matching books were not found."
    flash(msg, msgType)


