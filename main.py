from tkinter import ttk
import PIL.Image
import PIL.ImageTk
from login import *
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Waterloo67!',
    'database': 'main'
}

# Create an instance of LoginPage which is defined in login.py
class MainPage(PageBase):
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.display()

    def display(self):
        self.show_new_page("")
        self.resize()
        self.header()
        self.buttons()

    def resize(self):
        global img
        image = PIL.Image.open("books.jpg")
        resize_image = image.resize((1000,700)) 
        self.img = PIL.ImageTk.PhotoImage(resize_image)
        label1 = Label(self.root, image=self.img)
        label1.image = self.img
        label1.pack()

    def header(self):
        headingFrame1 = Frame(self.root, bg="#fff9f3", bd=5)
        headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
        headingLabel = Label(headingFrame1, text="Welcome to \n Benji's Library", bg='black', fg='white', font=('Courier',24))
        headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    def buttons(self):
        btn1 = ttk.Button(self.root, text="Login", command=self.go_to_login)
        btn1.place(relx=0.28, rely=0.4, relwidth=0.45, relheight=0.1)
        btn2 = ttk.Button(self.root, text="Signup", command=self.go_to_signup)
        btn2.place(relx=0.28, rely=0.5, relwidth=0.45, relheight=0.1)

    def go_to_login(self):
        LoginPage(self.root, self.config)

    def go_to_signup(self):
        SignupPage(self.root, self.config)


if __name__ == '__main__':
    root = tk.Tk()
    app = MainPage(root, config)
    root.mainloop()

