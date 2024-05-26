# Library Management System (LMS)

Welcome to the Library Management System! This system is designed to help libraries manage their book collections, 
members, and borrowing/returning processes efficiently using Django, a high-level Python web framework and REST API framework.

## What is the Library Management System?

The Library Management System (LMS) is a comprehensive tool for managing a library's operations. It provides 
functionalities for book cataloging, member management, and tracking the borrowing and returning of books.

## Project Structure

### Models

In this project, we have the following models:

- **Book**: Represents a book in the library with details such as title, author, ISBN, and availability status.
- **Author**: Describes the author of a book with details like name and biography.
- **Genre**: Represents a category or genre that a book belongs to.
- **User**: Describes a library member with details like name, email, and membership ID.
- **Reservation**: Tracks the borrowing and returning of books by members, including the borrow date and return date.
- **Transaction**: Records the transactions between members and the library, including the book borrowed, member 
involved, and the transaction date.
- **UserStatistics**: Stores statistics about the user's borrowing history, such as the number of books borrowed and returned.

### Database Schema
My System has a sqlite3 database schema. Here we have the following relations:
- Many-to-Many relation between Book and Genre
- One-to-Many relation between Author and Book
- One-to-Many relation between User and Reservation
- One-to-Many relation between User and Transaction
- One-to-Many relation between User and UserStatistics
- Many-to-Many relation between User and Book


### URLs

URLs define the mapping between URL paths and views. Here are the main URLs (endpoints) in our project:

#### Library App (**/library/**) urls:
- **/books/**: Displays the list of books available in the library.
- **/books/<int:pk>**: Displays the details of a specific book.
- **/books/<int:pk>/reserve**: Allows users to reserve a book.
- **/reservations/<int:reservation_id>/return/**: Handles book returning.
- **/reservations/<int:pk>/mark-returned/**: Marks a book as returned.        
       
###### Statistics(**/statistics/**) urls: 
- **/popular-books/**: Displays the Top 10 popular books in the library.
- **/book-stats/**: Displays statistics about each book, how many times it was borrowed and returned.
- **/late-returned-books/**: Displays the list of Top 100 books that were returned late.
- **/late-returned-users/**: Displays the list of Top 100 users who returned books late.

#### User App (**/auth/**) urls:
- **/create-user/**: Allows users to register for an account.
- **users/<int:pk>/**: Displays the details of a specific user.
- **/login/**: Handles user authentication and login.
- **/books/<int:pk>/reserve**: Allows users to view a book list and reserve a book.
- **/statistics/**: Displays the statistics of the user's borrowing history.
- **/reserve/**: Allows users to reserve a book.


## Getting Started

To run this project locally, follow these steps:

1. Clone this repository to your local machine.
    ```bash
    git clone https://github.com/Gvantsie/Library_Management_System.git
    ```
2. Make sure you have Python installed.

3. Install project dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```
4. Apply migrations by running:
    ```bash
    python manage.py migrate
   ```
5. Run management command to generate fake books using Factory-boy:
    ```bash
    python manage.py import_books
    ```
6. Start the development server:
    ```bash
    python manage.py runserver
    ```
7. Open your web browser and go to `http://localhost:8000/home/` to access the application.


### Management Commands

The project includes the following management commands:

- **import_books**: Generates fake books using Factory-boy and threads to speed up the process.
- **cancel_expired_reservations**: Cancels expired reservations (reservations that were not picked up within 7 days)
- **overdue_reminder**: Sends an email reminder to users with overdue books.

To run a management command, use the following syntax:
```bash
python manage.py <command_name>
```

#### in future i want to make this project more user-friendly, optimized and easy to use.

>>Gvantsa (Gvantsie)
