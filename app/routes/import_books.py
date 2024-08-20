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
        parameters = {'page': 1}
        if form.title.data:
            parameters['title'] = form.title.data
        if form.author.data:
            parameters['authors'] = form.author.data
        if form.isbn.data:
            parameters['isbn'] = form.isbn.data
        if form.publisher.data:
            parameters['publisher'] = form.publisher.data

        no_of_books_imported = 0
        repeated_book_names = []
        books_to_insert = []
        while no_of_books_imported < form.no_of_books.data:
            db = current_app.db
            response = requests.get(url, params=parameters)
            response = response.json()
            if not response['message']:
                break
            
            for book in response['message'][:form.no_of_books.data]: # import only form.no_of_books.data books
                # Check if book with same ID already exists
                existing_book = db.books.find_one({'title': book['title']})
                if not existing_book:
                    # Create new book document
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
            
            try:
                if len(books_to_insert) > 0: 
                    db.books.insert_many(books_to_insert)
            except Exception as e:
                flash(f"Error inserting books: {e}", 'error')

            # Flash Success/Warning Message
            msg = str(no_of_books_imported) + "/" + str(form.no_of_books.data) + " books have been imported. "
            msgType = 'success'
            if no_of_books_imported != form.no_of_books.data:
                msgType = 'warning'
            if len(repeated_book_names) > 0:
                msg += str(len(repeated_book_names)) + " books were found with already existing IDs."
            else:
                msg += str(form.no_of_books.data - no_of_books_imported) + " matching books were not found."

            flash(msg, msgType)
            return redirect(url_for('books.list_books'))

    return render_template('import_books/form.html', form=form)