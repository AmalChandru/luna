# Luna 🛸

Luna is a powerful library management application designed to help librarians manage books, members, and transactions efficiently. Built using Flask, MongoDB, Jinja, and Tailwind CSS, Luna provides a user-friendly interface and robust functionality for library operations. 
<p align="center">
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXl1eHpvdXEza3lyZHNza3l4bXBpZ2MycjFiOHp1MWR6eDh0ZTN2eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9dg/pBoI7kes1IANE0pD2f/giphy.gif" alt="Rick n Morty with Luna">
   <br>
   <strong>Wubba Lubba Dub Dub!</strong> - <em><small>Rick n' Morty discussing about Luna</small></em>
</p>

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Brewed with:](#brewed-with)
- [Contributing](#contributing)

## Features

- **📚 Book Management**: Add, edit, delete, and list books in the library.
- **👥 Member Management**: Register, update, and manage library members.
- **💳 Transaction Management**: Handle book issuance and returns with fee calculations.
- **📥 Data Import**: Bulk import books using the Frappe API interface.

## Installation

To get started with Luna, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AmalChandru/luna.git
   cd luna-library-management
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**:
   - Ensure you have MongoDB installed and running.
   - Update the database connection string in the [configuration file](./app/config/development.py).

5. **Run the application**:
   ```bash
   flask run
   ```

6. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000/books`.

## Usage

- Navigate through the application to manage books, members, and transactions.
- Use the provided API endpoints for programmatic access to the application features.

## API Endpoints

Here are some key API endpoints available in Luna:

### Books
- **List Books**: `GET /books/`
- **Add Book**: `POST /books/add`
- **Edit Book**: `POST /books/edit/<id>`
- **Delete Book**: `POST /books/delete_book/<id>`

### Members
- **List Members**: `GET /members/`
- **Add Member**: `POST /members/add`
- **Edit Member**: `POST /members/edit/<id>`
- **Delete Member**: `POST /members/delete_member/<id>`

### Transactions
- **List Transactions**: `GET /transactions/`
- **Create Transaction**: `POST /transactions/create`
- **Close Transaction**: `POST /transactions/close/<transaction_id>`

For more details please checkout [documentation guide](./docs/documentation.md)

## Brewed with:

- **[Windmill Dashboard](https://github.com/estevanmaito/windmill-dashboard)**: Multi-theme, accessible dashboard with Tailwind CSS. 🛠️
- **[The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)**: Engaging tutorial for learning Flask. 📚
- A generous splash of Coffee ☕ and a sprinkle of Love ❤️

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.


