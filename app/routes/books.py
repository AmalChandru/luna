from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app
from app.forms.forms import BookForm
from bson import ObjectId

# Create a Blueprint for book-related routes
books_bp = Blueprint('books', __name__, url_prefix='/books')


@books_bp.route('/')
def list_books():
    """List all books in the database."""
    db = current_app.db
    books = db.books.find()
    print(books)
    return render_template('books/list.html', books=books)

@books_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    """Add a new book to the database."""
    form = BookForm(request.form)  # Initialize the form with request data
    if request.method == 'POST' and form.validate():
        new_book = {
            'title': form.title.data,
            'author': form.author.data,
            'description': form.description.data,
            'isbn': form.isbn.data,
            'publisher': form.publisher.data,
            'publication_year': form.publication_year.data,
            'quantity': form.quantity.data,
            'available_copies': form.available_copies.data,
            'location': form.location.data,
            'genre': form.genre.data,
            'subject': form.subject.data
        }

        try:
            db = current_app.db
            db.books.insert_one(new_book)  # Insert the new book into the database
            flash('Book added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding book: {e}', 'error')  # Handle insertion errors

        return redirect(url_for('books.list_books'))  # Redirect to the book list
    return render_template('books/form.html', form=form)  # Render the form for adding a book

@books_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_book(id):
    """Edit an existing book in the database."""
    db = current_app.db
    book = db.books.find_one({"_id": ObjectId(id)})  # Fetch the book by ID
    form = BookForm(request.form, obj=book)  # Initialize the form with existing book data
    if request.method == 'POST' and form.validate():
        try:
            # Update book details in the database
            db.books.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        'title': form.title.data,
                        'author': form.author.data,
                        'description': form.description.data,
                        'isbn': form.isbn.data,
                        'publisher': form.publisher.data,
                        'publication_year': form.publication_year.data,
                        'quantity': form.quantity.data,
                        'available_copies': form.available_copies.data,
                        'location': form.location.data,
                        'genre': form.genre.data,
                        'subject': form.subject.data
                    }
                }
            )
            flash('Book updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating book: {e}', 'error')  # Handle update errors
        
        return redirect(url_for('books.list_books'))  # Redirect to the book list
    
    return render_template('/books/form.html', book=book, form=form)  # Render the form for editing a book

@books_bp.route('/delete_book/<id>', methods=['POST'])
def delete_book(id):
    """Delete a book from the database."""
    db = current_app.db
    try:
        db.books.delete_one({"_id": ObjectId(id)})  # Delete the book by ID
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting book: {e}', 'error')  # Handle deletion errors
    
    return redirect(url_for('books.list_books'))  # Redirect to the book list