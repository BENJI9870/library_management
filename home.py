from tkinter import ttk
from profile_ import *
from take_return import *
from main import MainPage
import datetime

class HomePage(PageBase):
    def __init__(self,root, current_email, config):
        super().__init__(root, config)
        self.current_email = current_email
        self.home()
#clearing the page for new page
    def buttons(self):
        btn1 = ttk.Button(self.root, text="View Profile", command=lambda: ViewProfilePage(self.root, self.current_email, self.config))
        btn1.place(relx=0.28,rely=0.4, relwidth=0.45,relheight=0.1)
        btn2 = ttk.Button(self.root, text="Edit Profile", command=lambda: EditProfilePage(self.root, self.current_email, self.config))
        btn2.place(relx=0.28,rely=0.5, relwidth=0.45,relheight=0.1)
        btn3 = ttk.Button(self.root, text="Check Out Book",command=lambda: CheckOutPage(self.root, self.current_email, self.config))
        btn3.place(relx=0.28,rely=0.6, relwidth=0.45,relheight=0.1)
        btn4 = ttk.Button(self.root, text="Return Book", command=lambda: ReturnBookPage(self.root, self.current_email, self.config))
        btn4.place(relx=0.28,rely=0.7, relwidth=0.45,relheight=0.1)
        btn5 = ttk.Button(self.root, text="Logout", command=lambda: MainPage(self.root, self.config))
        btn5.place(relx=0.28,rely=0.8, relwidth=0.45,relheight=0.1)
    def overdue(self):
        connection = pymysql.connect(**self.config)
        cursor = connection.cursor()
        cursor.execute('''
            SELECT c.due_date 
            FROM users u
            JOIN copies c ON u.user_id = c.checked_out_by
            WHERE u.email = %s
        ''', (self.current_email,))

        dates = [date[0] for date in cursor.fetchall()]
        cursor.close()
        connection.close()
        overdue = []
        for date in dates:
            if date < datetime.date.today():
                overdue.append(date)
        if len(overdue) == 1:
            messagebox.showwarning('Overdue Books', 'You have 1 overdue book')
        elif len(overdue) > 1:
            messagebox.showwarning('Overdue Books', f'You have {len(overdue)} overdue books')
    def home(self):
        self.show_new_page("Home Page")
        self.buttons()
        self.overdue()