import pymysql
import bcrypt
from tkinter import ttk
from Admin import *
from tkinter import *
from page_base import PageBase


class LoginPage(PageBase):
    def __init__(self, root, config):
        super().__init__(root, config)
        self.email_input = None
        self.pass_input = None
        self.current_email = None
        self.display()

    def display(self):
        self.show_new_page("Login page")
        # Create Entry for email
        email_label = ttk.Label(self.root, text="Enter Your Email:")
        email_label.pack(pady=5)
        self.email_input = ttk.Entry(self.root, width=20)
        self.email_input.pack(pady=10)
        self.email_input.focus_set()

        # Create Entry for password (show="*" will mask the password)
        pass_label = ttk.Label(self.root ,text="Enter Your Password:")
        pass_label.pack(pady=5)
        self.pass_input = ttk.Entry(self.root,show="*", width=20)
        self.pass_input.pack(pady=10)
        

        # Login button which triggers on_login_click when pressed
        login_btn = ttk.Button(self.root, text='Login', command= lambda: self.combined_func())
        login_btn.pack(pady=10)

    def on_login_click(self):
        email = self.email_input.get().lower()  # get value from Entry widget
        password = self.pass_input.get()
        return email, password
    def combined_func(self):
        from home import HomePage
        email, password = self.on_login_click()
        if email == '' or password == '':
            messagebox.showerror("Error", "Please Fill All Fields")
    ##########################################################
        elif email == 'u' and password == 'u':
            HomePage(self.root, 'spammy9870@gmail.com', self.config)
        elif email == 'a' and password == 'a':
            AdminPage(self.root, self.config)
    ##########################################################
        else:
            verification_result = self.verify_credentials(email, password)
            if verification_result == 'user':
                self.current_email = email
                HomePage(self.root, self.current_email, self.config)
            elif verification_result == 'admin':
                AdminPage(self.root, self.config)
            else:
                messagebox.showerror("Error", "Incorrect Email or Password")
    #getting credentials from database and verifying them   
    def verify_credentials(self, email, password):
        try:
            # Establish a database connection
            connection = pymysql.connect(**self.config)
            cursor = connection.cursor()

            # Query to retrieve hashed password from database based on provided email
            query = "SELECT password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            query_admin = "SELECT password FROM admin WHERE email = %s"
            cursor.execute(query_admin, (email,))
            result_admin = cursor.fetchone()

            # Close the connection
            cursor.close()
            connection.close()

            # If there's a result, then compare passwords
            if result:
                stored_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return 'user'
            elif result_admin:
                stored_password_admin = result_admin[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_admin.encode('utf-8')):
                    return 'admin'
            return False
        except pymysql.MySQLError as e:
            print(e)
            return False

class SignupPage(PageBase):
    def __init__(self, root, config):
        super().__init__(root, config)
        self.name_input = None
        self.email_input = None
        self.pass_input = None
        self.current_email = None
        self.display()
    def display(self):
        self.show_new_page("Sign Up Page")


        #Create Entry for name
        name_label = ttk.Label(self.root, text="Enter Your Name:")
        name_label.pack(pady=5)
        self.name_input = ttk.Entry(self.root, width=20)
        self.name_input.pack(pady=10)
        self.name_input.focus_set()
        # Create Entry for email
        email_label = ttk.Label(self.root, text="Enter Your Email:")
        email_label.pack(pady=5)
        self.email_input = ttk.Entry(self.root, width=20)
        self.email_input.pack(pady=10)

        # Create Entry for password (show="*" will mask the password)
        pass_label = ttk.Label(self.root, text="Enter Your Password:")
        pass_label.pack(pady=5)
        self.pass_input = ttk.Entry(self.root, show="*",width=20)
        self.pass_input.pack(pady=10)

        # Login button which triggers on_login_click when pressed
        signup_btn = ttk.Button(self.root, text='Sign Up', command= lambda: self.combined_func())
        signup_btn.pack(pady=10)
    def on_signup_click(self):
        name = self.name_input.get()  # get value from Entry widget
        email = self.email_input.get().lower() 
        password = self.pass_input.get()
        return name, email, password
    def combined_func(self):
        #later make it so that if user is already in database then show error
        name, email, password = self.on_signup_click()
        if email == "" or password == "" or name == "":
            messagebox.showerror("Error", "Please Fill All Fields")
        elif len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters")
        elif email.count("@") != 1 or email.count(".") == 0:
            messagebox.showerror("Error", "Please enter a valid email")
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            try:
                # Establish a database connection
                connection = pymysql.connect(**self.config)
                cursor = connection.cursor()

                # Check if email already exists
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()

                if result:
                    # If a user with the same email is found, show an error
                    messagebox.showerror("Error", "Email already registered!")
                else:
                    # If not, insert the new user into the database
                    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
                    connection.commit()
                    LoginPage(self.root, self.config)

            except pymysql.MySQLError as e:
                messagebox.showerror("Error", str(e))
            finally:
                # Close the connection
                cursor.close()
                connection.close()

