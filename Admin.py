from tkinter import *
from tkinter import messagebox
import pymysql
from tkinter import ttk
import tkinter as tk
from page_base import PageBase

class AdminPage(PageBase):
    def __init__(self, root, config):
        super().__init__(root, config)
        self.display()
        self.buttons()
    def display(self):
        self.show_new_page("Admin Page")
        self.root.configure(bg='#B0B5F7')
    def buttons(self):
        btn1 = Button(self.root, text = 'Add Book', bg='#c1d0e2', fg='black', command=lambda: AddBookPage(self.root, self.config))
        btn1.place(relx=0.28,rely=0.4, relwidth=0.45,relheight=0.1)
        btn2 = Button(self.root, text = 'Remove Book', bg='#c1d0e2', fg='black', command=lambda: RemoveBookPage(self.root, self.config))
        btn2.place(relx=0.28,rely=0.5, relwidth=0.45,relheight=0.1)


class AddBookPage(PageBase):
    def __init__(self, root, config):
        super().__init__(root, config)
        self.title_input = None
        self.author_input = None
        self.isbn_input = None
        self.display()
    def display(self):
        self.show_new_page("Add Book Page")
        self.root.configure(bg='#B0B5F7')
        #create entry for all variables
        title_label = ttk.Label(self.root, text="Enter the book's title:")
        title_label.pack(pady=5)
        self.title_input = ttk.Entry(self.root, width=20)
        self.title_input.pack(pady=10)
        self.title_input.focus_set()

        author_label = ttk.Label(self.root, text="Enter the book's author:")
        author_label.pack(pady=5)
        self.author_input = ttk.Entry(self.root, width=20)
        self.author_input.pack(pady=10)

        isbn_label = ttk.Label(self.root, text="Enter the book's ISBN:")
        isbn_label.pack(pady=5)
        self.isbn_input = ttk.Entry(self.root, width=20)
        self.isbn_input.pack(pady=10)

        #add button
        add_btn = ttk.Button(self.root, text='Add', command= lambda: self.combined_func())
        add_btn.pack(pady=10)
    def add_book(self, title, author, ISBN):
        connection = pymysql.connect(host='localhost', user='root', password='Waterloo67!', database='main')
        try:
            with connection.cursor() as cursor:
                # Check if the book already exists in the 'Books' table
                cursor.execute("SELECT book_id FROM books WHERE title = %s AND author = %s AND ISBN = %s", (title, author, ISBN))
                result = cursor.fetchone()

                # If the book doesn't exist, insert it
                if not result:
                    cursor.execute("INSERT INTO books (title, author, ISBN) VALUES (%s, %s, %s)", (title, author, ISBN))
                    # Get the last inserted book_id
                    book_id = cursor.lastrowid
                else:
                    book_id = result[0]

                # Add a new copy of the book to the 'Copies' table with status "Available"
                cursor.execute("INSERT INTO copies (book_id, status) VALUES (%s, 'Available')", (book_id,))
                connection.commit()

                print(f"Book '{title}' added/incremented successfully!")

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            connection.rollback()

    def add_book_click(self):
        title = self.title_input.get()
        author = self.author_input.get()
        isbn = self.isbn_input.get()
        return title, author, isbn
    def combined_func(self):
        title, author, isbn = self.add_book_click()
        if title == '' or author == '' or isbn == '':
            messagebox.showerror("Error", "Please Fill All Fields")
        else:
            self.add_book(title, author, isbn)
            messagebox.showinfo('Success', "Book added successfully")
            AdminPage(self.root, self.config)

class RemoveBookPage(PageBase):
    def __init__(self, root, config):
        super().__init__(root, config)
        self.connection = pymysql.connect(host='localhost', user='root', 
                                     password='Waterloo67!', database='main')
        self.title_input = None
        self.author_input = None
        self.isbn_input = None
        self.display()
    def display(self):
        self.show_new_page("Remove Book Page")
        self.root.configure(bg='#B0B5F7')
        self.display_book_list()

    def retrieve_books(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT title FROM books")
        books = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return books

    def on_remove_book(self, listbox):
        index = listbox.curselection()
        if index:
            book_title = listbox.get(index)
            #remove from database
            self.remove_book_from_db(book_title)
            #remove from listbox
            listbox.delete(index[0])
    def remove_book_from_db(self,book_title):
        cursor = self.connection.cursor()
        cursor.execute('SELECT book_id FROM books WHERE title = %s', (book_title,))
        book_id = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM copies WHERE book_id = %s', (book_id,))
        num_copies = cursor.fetchone()[0]

        if num_copies > 1:
            cursor.execute('DELETE FROM copies WHERE book_id = %s LIMIT 1', (book_id,))
            messagebox.showinfo("Success", "Copy removed successfully")
            self.connection.commit()
        elif num_copies == 1:
            cursor.execute('DELETE FROM copies WHERE book_id = %s', (book_id,))
            cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
            self.connection.commit()
            messagebox.showinfo("Success", "Book removed successfully")
        else:
            print('Error: No copies of this book exist in the database.')
        

    def display_book_list(self):
        frame = Frame(self.root)
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        books = self.retrieve_books()

        listbox = Listbox(frame)
        listbox.pack(side = tk.LEFT, fill=tk.BOTH, expand=True)

        for book in books:
            listbox.insert(tk.END, book)
        

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.focus_set()

        btn_remove = ttk.Button(self.root, text = 'Remove Book', command=lambda: self.on_remove_book(listbox))
        btn_remove.pack(pady=20)
    def __del__(self):
        if self.connection:
            self.connection.close()