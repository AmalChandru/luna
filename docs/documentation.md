## Luna 🛸: Library Management Application Guide

Welcome to the Luna library management application! This guide will help you navigate the system efficiently, allowing you to manage books, members, and transactions with ease. Let’s dive in! 📚✨

### 📖 Books Management
#### List Books
- **Endpoint**: `/books/`
- **Method**: `GET`
- **Description**: Retrieve a list of all books in the database.

#### Add Book
- **Endpoint**: `/books/add`
- **Method**: `GET, POST`
- **Description**: Add a new book to the library.
- **Parameters**: 
  - `title`
  - `author`
  - `description`
  - `isbn`
  - `publisher`
  - `publication_year`
  - `quantity`
  - `available_copies`
  - `location`
  - `genre`
  - `subject`
- **Form**: Utilize `BookForm` for data entry.

#### Edit Book
- **Endpoint**: `/books/edit/<id>`
- **Method**: `GET, POST`
- **Description**: Modify details of an existing book.
- **Parameters**: 
  - `id` (Book ID)
- **Form**: Use `BookForm` for updates.

#### Delete Book
- **Endpoint**: `/books/delete_book/<id>`
- **Method**: `POST`
- **Description**: Remove a book from the library.
- **Parameters**: 
  - `id` (Book ID)

#### Example Book Record
```json
{
  "_id": {
    "$oid": "66bdd4c978892e02d02202d8"
  },
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "description": "A novel set in the Roaring Twenties that tells the story of Jay Gatsby's unrequited love for Daisy Buchanan.",
  "isbn": "9780743273565",
  "publisher": "Scribner",
  "publication_year": 1925,
  "quantity": 5,
  "available_copies": 2,
  "location": "Shelf A2",
  "genre": "Fiction",
  "subject": "African Literature"
}
```

---

### 🧑‍🤝‍🧑 Members Management
#### List Members
- **Endpoint**: `/members/`
- **Method**: `GET`
- **Description**: Retrieve a list of all library members.

#### Add Member
- **Endpoint**: `/members/add`
- **Method**: `GET, POST`
- **Description**: Register a new member.
- **Parameters**: 
  - `name`
  - `email`
  - `address`
  - `phone`
- **Form**: Use `MemberForm` for data entry.

#### Edit Member
- **Endpoint**: `/members/edit/<id>`
- **Method**: `GET, POST`
- **Description**: Update member information.
- **Parameters**: 
  - `id` (Member ID)
- **Form**: Use `MemberForm` for updates.

#### Delete Member
- **Endpoint**: `/members/delete_member/<id>`
- **Method**: `POST`
- **Description**: Remove a member from the library.
- **Parameters**: 
  - `id` (Member ID)

#### Example Member Record
```json
{
  "_id": {
    "$oid": "66c2063c36dd1e550b4152e6"
  },
  "name": "John Doe",
  "email": "johndoe@example.com",
  "address": "123 Main St, Springfield",
  "phone": "555-1234",
  "no_of_books_borrowed": 14,
  "book_borrowed": "1984, To Kill a Mockingbird, The Great Gatsby",
  "total_amount_spent": 95,
  "outstanding_debt": 52
}
```

---

### 💳 Transactions Management
#### List Transactions
- **Endpoint**: `/transactions/`
- **Method**: `GET`
- **Description**: Retrieve a list of all transactions.

#### Create Transaction
- **Endpoint**: `/transactions/create`
- **Method**: `GET, POST`
- **Description**: Initiate a new book issuance transaction.
- **Parameters**: 
  - `book_name`
  - `member_name`
  - `fee_per_day`
- **Form**: Use `BookIssueForm` for data entry.

#### Close Transaction
- **Endpoint**: `/transactions/close/<transaction_id>`
- **Method**: `GET, POST`
- **Description**: Finalize a transaction and process the book return.
- **Parameters**: 
  - `transaction_id` (Transaction ID)
- **Form**: Use `BookReturnForm` for data entry.

#### Example Transaction Record
```json
{
  "_id": {
    "$oid": "66c31ddf639f1604006be087"
  },
  "book_name": "The Great Gatsby",
  "member_name": "John Doe",
  "fee_per_day": 1,
  "issue_date": "2024-08-18",
  "return_date": "2024-08-19",
  "total_fee": 1,
  "amount_paid": 1,
  "status": "Closed"
}
```

---

### 🌐 Integration with Frappe API

The application allows for bulk book imports via the Frappe API.

- **API Details**: Fetches 20 books at a time, accepting parameters like `title`, `authors`, `isbn`, `publisher`, and `page`.
- **Implementation**: An interface is provided to specify the number of books to import and any additional parameters.

---

### 🛠️ Usage Guidelines

1. **CRUD Operations**: Utilize the endpoints to manage books and members effectively.
2. **Transaction Management**: Handle book issuances and returns while monitoring members' outstanding debts (max Rs. 500).
3. **Data Import**: Leverage the Frappe API for efficient bulk book imports.

---

### ⚠️ Error Handling

To ensure smooth operation and troubleshooting:

- Set `LOGGING_LEVEL` to `DEBUG` in your configuration for detailed logging.

---
