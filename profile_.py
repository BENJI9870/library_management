import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import *
from login import PageBase
import bcrypt
from tkinter import messagebox


class ViewProfilePage(PageBase):
    def __init__(self, root, current_email, config):
        super().__init__(root, config)
        self.current_email = current_email
        self.display()

    def display(self):
        self.root.title("View Profile")
        self.show_new_page("Your Profile")
        try:
            connection = pymysql.connect(**self.config)
            cursor = connection.cursor()

            # Fetch user's personal details
            cursor.execute("SELECT user_id, name FROM users WHERE email = %s", (self.current_email,))
            user_id = cursor.fetchone()

            if user_id:

                # Fetch books checked out by the user and their due dates
                cursor.execute("""
                SELECT b.title, b.author, b.ISBN, c.due_date 
                FROM books b
                JOIN copies c ON b.book_id = c.book_id
                WHERE c.checked_out_by = %s
            """, (user_id[0],))
            books_checked_out = cursor.fetchall()

            
            #close connection
            cursor.close()
            connection.close()

        except pymysql.MySQLError as e:
            print(e)
            return

        
        # Displaying user details
        ttk.Label(self.root, text="Name: " + user_id[1]).pack(pady=10)
        ttk.Label(self.root, text="Email: " + self.current_email).pack(pady=10)

        #create a tree widget
        

        # Displaying books checked out by the user
        if books_checked_out:
            ttk.Label(self.root, text="Books Checked Out:").pack(pady=10)
            tree = ttk.Treeview(self.root, column=("c1", "c2", "c3", 'c4'), show='headings', height=5)

            tree.column("# 1", anchor=W, width = 300)
            tree.heading("# 1", text="Title")
            tree.column("# 2", anchor=W)
            tree.heading("# 2", text="Author")
            tree.column("# 3", anchor=W)
            tree.heading("# 3", text="ISBN")
            tree.column("# 4", anchor=W)
            tree.heading("# 4", text="Due Date")
            for book in books_checked_out:
                tree.insert('', 'end', text="1", values=(book[0], book[1], book[2], book[3]))
                tree.pack()
        else:
            ttk.Label(self.root, text="No books currently checked out.").pack(pady=10)
        
        #go back
        from home import HomePage
        btn_back = ttk.Button(self.root, text = 'Go Back', command = lambda: HomePage(self.root, self.current_email, self.config))
        btn_back.pack(pady=10)

class EditProfilePage(PageBase):
    def __init__(self, root, current_email, config):
        super().__init__(root, config)
        self.current_email = current_email
        self.pass_input = None
        self.name_input = None
        self.email_input = None
        self.display()
    def display(self):
        self.show_new_page("Edit Profile")
        self.root.geometry("1000x700")
        self.display_account_details()
    def display_account_details(self):
        details = self.account()
        #change name
        ttk.Label(self.root, text = f'Change Name from \'{details[1]}\':').pack(pady=5)
        self.name_input = ttk.Entry(self.root, width=20)
        self.name_input.pack(pady=10)
        self.name_input.focus_set()
        name_btn = ttk.Button(self.root, text='Change Name', command= lambda: self.change_name())
        name_btn.pack(pady=10)
        #change email
        tk.Label(self.root, text = f'Change Email from \'{details[2]}\':').pack(pady=5)
        self.email_input = ttk.Entry(self.root, width=20)
        self.email_input.pack(pady=10)
        email_btn = ttk.Button(self.root, text='Change Email', command= lambda: self.change_email())
        email_btn.pack(pady=10)
        #change password
        tk.Label(self.root, text = f'Change Password:').pack(pady=5)
        self.pass_input = ttk.Entry(self.root, width=20)
        self.pass_input.pack(pady=10)
        pass_btn = ttk.Button(self.root, text='Change Password', command= lambda: self.change_password())
        pass_btn.pack(pady=10)
    def change_name(self):
        details = self.account()
        self.name_input = self.name_input.get().lower()
        if self.name_input == '':
            messagebox.showerror("Error", "Please Fill All Fields")
        elif self.name_input == details[1]:
            messagebox.showerror("Error", "Please Enter a New Name")
        else:
            connection = pymysql.connect(**self.config)
            cursor = connection.cursor()
            sql = """
                UPDATE users
                SET name = %s
                WHERE email = %s
            """
            cursor.execute(sql, (self.name_input, self.current_email))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Name changed successfully")
            ViewProfilePage(self.root, self.current_email, self.config)
    def change_email(self):
        details = self.account()
        if self.name_input.get() == '':
            messagebox.showerror("Error", "Please Fill All Fields")
        elif self.name_input.get() == details[2]:
            messagebox.showerror('Error', 'Please Enter a New Email')
        else:
            connection = pymysql.connect(**self.config)
            cursor = connection.cursor()
            sql = "UPDATE users SET email = %s WHERE email = %s"
            cursor.execute(sql, (self.email_input.get(), self.current_email))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Email changed successfully")
            ViewProfilePage(self.root, self.email_input, self.config)
    def change_password(self):
        details = self.account()
        self.pass_input = self.pass_input.get().encode('utf-8')
        if self.pass_input.get() == '':
            messagebox.showerror("Error", "Please Fill All Fields")
        elif bcrypt.checkpw(self.pass_input, details[3]):
            messagebox.showerror('Error', 'Please Enter a New Password')
        else:
            hashed = bcrypt.hashpw(self.pass_input, bcrypt.gensalt())
            connection = pymysql.connect(**self.config)
            cursor = connection.cursor()
            sql = "UPDATE users SET password = %s WHERE email = %s"
            cursor.execute(sql, (hashed, self.current_email))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "password changed successfully")
            ViewProfilePage(self.root, self.email_input, self.config)
    def account(self):
        connection = pymysql.connect(**self.config)
        cursor = connection.cursor()

        sql = """
            SELECT user_id, name, email, password
            FROM users
            WHERE email = %s
        """
        cursor.execute(sql, (self.current_email,))
        details = cursor.fetchone()
        cursor.close()
        connection.close()
        return details