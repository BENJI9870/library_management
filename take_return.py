from tkinter import *
from tkinter import ttk
from login import *
import datetime
from fuzzywuzzy import fuzz, process

class CheckOutPage(PageBase):
    def __init__(self, root, current_email, config):
        super().__init__(root, config)
        self.current_email = current_email
        self.connection = pymysql.connect(**self.config)
        self.display()
    def display(self):
        self.show_new_page("Check Out Page")
        self.root.geometry("1000x700")
        self.display_book_list()
    def retrieve_books(self):
        cursor = self.connection.cursor()

# SQL statement that fetches titles of available books with no repeats.
        sql = """
        SELECT DISTINCT b.title, b.author
        FROM books b
        JOIN copies c ON b.book_id = c.book_id
        WHERE c.status = 'Available'
        """

        cursor.execute(sql)
        all_rows = cursor.fetchall()
        books = [[row[0], row[1]] for row in all_rows]
        cursor.close()
        return books
    def on_checkout_book(self, tree):
        index = tree.selection()  # This will return the item ID of the selected row.
    
        if index:
            book_title = tree.item(index, "values")[0]
            # Remove from database
            self.checkout_book_from_db(book_title)
            from home import HomePage
            HomePage(self.root, self.current_email, self.config)
    def checkout_book_from_db(self,book_title):
        due_date = datetime.datetime.now() + datetime.timedelta(days = 90)
        cursor = self.connection.cursor()
        cursor.execute('SELECT book_id FROM books WHERE title = %s', (book_title,))
        book_id = cursor.fetchone()
        cursor.execute('SELECT user_id FROM users WHERE email = %s', (self.current_email,))
        user_id = cursor.fetchone()
        cursor.execute('''UPDATE copies 
                      SET status="Checked Out", 
                      checked_out_by=%s, 
                      due_date=%s 
                      WHERE book_id= %s LIMIT 1''', (user_id, due_date, book_id))
        self.connection.commit()
        messagebox.showinfo('Success', "Book checked out successfully")
    #trying to get books from database that were searched
    def search_book(self, search_input, books, tree):
        combined_titles_authors = [f"{book[0]} {book[1]}" for book in books]
        title_author_to_index = {title_author: index for index, title_author in enumerate(combined_titles_authors)}
        val = search_input.widget.get()
        if val == "":
            data = books
        else:
            # Notice the use of enumerate here.
            matches = process.extract(val, combined_titles_authors, limit=len(combined_titles_authors), scorer=fuzz.partial_ratio)
            
            # Now, we adjust how we get the index since it's part of the matched string.
            indices = [title_author_to_index[match[0]] for match in matches if match[1] > 75]
            
            # Combine indices and ensure uniqueness
            data = [books[index] for index in indices]
        self.update(data, tree)
    def update(self, data, tree):
        tree.delete(*tree.get_children())
        for item in data:
            tree.insert('', 'end', text="1", values=(item[0], item[1]))
            tree.pack()
        

    def display_book_list(self):
        books = self.retrieve_books()
        search_label = ttk.Label(self.root, text="Search:")
        search_label.pack(pady=5)
        search_input = ttk.Entry(self.root, width=20)
        search_input.pack(pady=10)
        search_input.bind('<KeyRelease>', lambda search_input: self.search_book(search_input, books, tree))
        search_input.focus_set()
        tree = ttk.Treeview(self.root, column=("c1", "c2"), show='headings', height=5)

        tree.column("# 1", anchor=W, width = 300)
        tree.heading("# 1", text="Title")
        tree.column("# 2", anchor=W)
        tree.heading("# 2", text="Author")
        self.update(books, tree)
        
 
        btn_checkout = ttk.Button(self.root, text = 'Check Out', command=lambda: self.on_checkout_book(tree))
        btn_checkout.pack(pady=20)

    def __del__(self):
        if self.connection:
            self.connection.close()

class ReturnBookPage(PageBase):
    def __init__(self, root, current_email, config):
        super().__init__(root, config)
        self.current_email = current_email
        self.connection = pymysql.connect(**self.config)
        self.display()
    def display(self):
        self.show_new_page("Return Page")
        self.root.geometry("1000x700")
        self.display_book_list()
    def retrieve_books(self):
        cursor = self.connection.cursor()
        sql = """
            SELECT b.title, b.author, c.due_date
            FROM copies c
            JOIN books b ON c.book_id = b.book_id
            WHERE c.checked_out_by = (
                SELECT user_id FROM users WHERE email = %s
            )
        """

        cursor.execute(sql, (self.current_email,))
        all_rows = cursor.fetchall()
        books =[[row[0], row[1], row[2]] for row in all_rows]
        cursor.close()
        return books
    def on_return_book(self, tree):
        index = tree.selection()  # This will return the item ID of the selected row.
    
        if index:
            book_title = tree.item(index, "values")[0]
            # Remove from database
            self.return_book_from_db(book_title)
            from home import HomePage
            HomePage(self.root, self.current_email, self.config)
    def return_book_from_db(self,book_title):
        cursor = self.connection.cursor()
        cursor.execute('SELECT book_id FROM books WHERE title = %s', (book_title,))
        book_id = cursor.fetchone()
        cursor.execute('UPDATE copies SET status="Available" WHERE book_id= %s LIMIT 1', (book_id,))
        cursor.execute('UPDATE copies SET checked_out_by=NULL WHERE book_id= %s LIMIT 1', (book_id,))
        self.connection.commit()
        cursor.close()
        messagebox.showinfo('Returned', "Book returned successfully")
    def search_book(self, search_input, books, tree):
        combined_titles_authors = [f"{book[0]} {book[1]}" for book in books]
        title_author_to_index = {title_author: index for index, title_author in enumerate(combined_titles_authors)}
        val = search_input.widget.get()
        if val == "":
            data = books
        else:
            # Notice the use of enumerate here.
            matches = process.extract(val, combined_titles_authors, limit=len(combined_titles_authors), scorer=fuzz.partial_ratio)
            
            # Now, we adjust how we get the index since it's part of the matched string.
            indices = [title_author_to_index[match[0]] for match in matches if match[1] > 75]
            
            # Combine indices and ensure uniqueness
            data = [books[index] for index in indices]
        self.update(data, tree)
    def update(self, data, tree):
        tree.delete(*tree.get_children())
        for item in data:
            tree.insert('', 'end', text="1", values=(item[0], item[1], item[2]))
            tree.pack()
    def display_book_list(self):
        books = self.retrieve_books()
        search_label = ttk.Label(self.root, text="Search:")
        search_label.pack(pady=5)
        search_input = ttk.Entry(self.root, width=20)
        search_input.pack(pady=10)
        search_input.bind('<KeyRelease>', lambda search_input: self.search_book(search_input, books, tree))
        search_input.focus_set()

        tree = ttk.Treeview(self.root, column=("c1", "c2", 'c3'), show='headings', height=5)

        tree.column("# 1", anchor=W, width = 300)
        tree.heading("# 1", text="Title")
        tree.column("# 2", anchor=W)
        tree.heading("# 2", text="Author")
        tree.column("# 3", anchor=W)
        self.update(books, tree)

        btn_remove = ttk.Button(self.root, text = 'Return', command=lambda: self.on_return_book(tree))
        btn_remove.pack(pady=20)
    def __del__(self):
        if self.connection:
            self.connection.close()