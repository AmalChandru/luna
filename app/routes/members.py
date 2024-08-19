from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app
from app.forms.forms import MemberForm
from bson import ObjectId

# Create a Blueprint for member-related routes
members_bp = Blueprint('members', __name__, url_prefix='/members')


@members_bp.route('/')
def list_members():
    """List all members in the database"""
    db = current_app.db
    members = db.members.find()
    return render_template('members/list.html', members=members)

@members_bp.route('/add', methods=['GET', 'POST'])
def add_member():
    """Add a new member to the database"""
    form = MemberForm(request.form)
    if request.method == 'POST' and form.validate():
        new_member = {
            'name': form.name.data,
            'email': form.email.data,
            'address': form.address.data,
            'phone': form.phone.data,
            'no_of_books_borrowed': 0,
            'total_amount_spent': 0,
            'outstanding_debt': 0
        }

        try:
            db = current_app.db
            print(new_member)
            db.members.insert_one(new_member)  # Insert the new member into the database
            flash('Member added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding member: {e}', 'error')  # Handle insertion errors

        return redirect(url_for('members.list_members'))  # Redirect to the member list
    return render_template('members/form.html', form=form)

@members_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_member(id):
    """Edit an existing member in the database"""
    db = current_app.db
    member = db.members.find_one({"_id": ObjectId(id)})  # Fetch the member by ID
    form = MemberForm(request.form, obj=member)  # Initialize the form with existing member data
    print(form.validate())
    if request.method == 'POST' and form.validate():
        try:
            # Update member details in the database
            db.members.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        'name': form.name.data,
                        'email': form.email.data,
                        'address': form.address.data,
                        'phone': form.phone.data
                    }
                }
            )
            flash('Member updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating member: {e}', 'error')  # Handle update errors

        return redirect(url_for('members.list_members'))  # Redirect to the member list
    return render_template('members/form.html', member=member, form=form)

@members_bp.route('/delete_member/<id>', methods=['POST'])
def delete_member(id):
    """Delete a member from the database"""
    db = current_app.db
    try:
        db.members.delete_one({"_id": ObjectId(id)})  # Delete the member by ID
        flash('Member deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting member: {e}', 'error')  # Handle deletion errors

    return redirect(url_for('members.list_members'))  # Redirect to the member list