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
        total_books_requested = form.no_of_books.data
        parameters = build_parameters(form)

        no_of_books_imported, repeated_book_names, books_to_insert = 0, [], []
        page = 1

        while no_of_books_imported < total_books_requested:
            parameters['page'] = page
            response = requests.get(url, params=parameters).json()
            if not response['message']:
                flash('No books found.', 'error')
                break

            # Calculate how many books to process this page
            books_to_process = min(len(response['message']), total_books_requested - no_of_books_imported)
            no_of_books_imported, repeated_book_names = process_books(response['message'][:books_to_process], form, current_app.db, books_to_insert, no_of_books_imported, repeated_book_names)

            if no_of_books_imported >= total_books_requested:
                break
            
            page += 1  # Move to the next page

        # Sort books_to_insert based on user selection
        if form.sort_by.data == 'title':
            books_to_insert.sort(key=lambda x: x['title'])
            print("Books sorted by title:")
        elif form.sort_by.data == 'author':
            books_to_insert.sort(key=lambda x: x['author'])
            print("Books sorted by author:")

        insert_books(books_to_insert)

        flash_success_warning_message(no_of_books_imported, total_books_requested, repeated_book_names)
        return redirect(url_for('books.list_books'))

    return render_template('import_books/form.html', form=form)

def build_parameters(form):
    parameters = {}
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
            new_book = create_book_entry(book, form)  # Create a new book entry only if it doesn't exist
            books_to_insert.append(new_book)
            no_of_books_imported += 1
        else:
            # Increase the quantity of the existing book
            db.books.update_one({'title': book['title']}, {'$inc': {'quantity': form.quantity_per_book.data}})
            # Add the title to repeated_book_names only if it is not already present
            if book['title'] not in repeated_book_names:
                repeated_book_names.append(book['title'])
    return no_of_books_imported, repeated_book_names

def create_book_entry(book, form):
    """Create a new book entry."""
    return {
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

def insert_books(books_to_insert):
    """Insert books into the database."""
    if books_to_insert:
        try:
            current_app.db.books.insert_many(books_to_insert)
        except Exception as e:
            flash(f"Error inserting books: {e}", 'error')

def flash_success_warning_message(no_of_books_imported, total_books, repeated_book_names):
    msg = f"{no_of_books_imported}/{total_books} books have been imported. "
    msgType = 'success' if no_of_books_imported == total_books else 'warning'
    if repeated_book_names:
        msg += f"{len(repeated_book_names)} books were found with already existing IDs."
    else:
        msg += f"{total_books - no_of_books_imported} matching books were not found."
    flash(msg, msgType)


