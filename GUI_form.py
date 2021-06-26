import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from DataLayer import database_data, DALRecommendation
from Movie_images import Photos_display
from objectModel import Users


class Registration_form:

    def check(self, obj):
        self.response = True
        self.msg1.config(text="")
        self.msg2.config(text="")
        self.msg3.config(text="")
        self.msg4.config(text="")
        if self.user_id_value.get() == "":
            self.msg1.config(text='Please enter the user id.')
            self.response = False
        else:
            d_obj = database_data()
            self.response = d_obj.check(obj)
            if not self.response:
                self.msg1.config(text='User id already exists.')
                self.response = False

        if self.password.get() == "":
            self.msg2.config(text="Please enter the password.")
            self.response = False

        if self.confirm_pwd_.get() == "":
            self.msg3.config(text="Please enter the password.")
            self.response = False
        elif self.password.get() != self.confirm_pwd_.get():
            self.msg3.config(text='Password mismatch.')
            self.response = False

        if self.name.get() == "":
            self.msg4.config(text='Please enter name.')
            self.response = False

        return self.response

    def register_user(self):
        obj1 = Users()
        obj1.userid = self.user_id_value.get()
        obj1.password = self.password.get()
        obj1.name = self.name.get()

        if self.check(obj1.userid):
            # passing values to db
            db_obj = database_data()
            db_obj.register_user(obj1)
            tk.messagebox.showinfo("Success", "Registration successful.")
            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry3.delete(0, tk.END)
            self.entry4.delete(0, tk.END)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Register 👤')

        # self.root.geometry('500x400')
        self.root.config(padx=20, pady=20, bg='black')
        # canvas
        self.canvas = tk.Canvas(width=190, height=200, highlightthickness=0, bg='black')
        # image on canvas
        logo = tk.PhotoImage(file="3.png")
        image_on_canvas = self.canvas.create_image(90, 90, image=logo)
        self.canvas.grid(row=0, column=1)
        # text-fields
        self.user_id_value = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm_pwd_ = tk.StringVar()
        self.name = tk.StringVar()

        # labels for displaying errors
        self.msg1 = tk.Label(self.root, fg='red', bg='black')
        self.msg1.grid(row=1, column=2)

        self.msg2 = tk.Label(self.root, fg='red', bg='black')
        self.msg2.grid(row=2, column=2)

        self.msg3 = tk.Label(self.root, fg='red', bg='black')
        self.msg3.grid(row=3, column=2)

        self.msg4 = tk.Label(self.root, fg='red', bg='black')
        self.msg4.grid(row=4, column=2)

        # labels and entry fields
        self.userid = tk.Label(self.root, text='User ID', bg='black', fg='white')
        self.entry1 = tk.Entry(self.root, textvariable=self.user_id_value, width=22)
        self.userid.grid(row=1, column=0, pady=5)
        self.entry1.grid(row=1, column=1, pady=5)

        self.pwd = tk.Label(self.root, text='Password', bg='black', fg='white')
        self.entry2 = tk.Entry(self.root, show="*", textvariable=self.password, width=22)
        self.pwd.grid(row=2, column=0, pady=5)
        self.entry2.grid(row=2, column=1, pady=5)

        self.confirm_pwd = tk.Label(self.root, text='Confirm Password', bg='black', fg='white')
        self.entry3 = tk.Entry(self.root, show="*", textvariable=self.confirm_pwd_, width=22)
        self.confirm_pwd.grid(row=3, column=0, pady=5)
        self.entry3.grid(row=3, column=1, pady=5)

        self.Name = tk.Label(self.root, text='Name', bg='black', fg='white')
        self.entry4 = tk.Entry(self.root, textvariable=self.name, width=22)
        self.Name.grid(row=4, column=0, pady=5)
        self.entry4.grid(row=4, column=1, pady=5)

        # buttons
        self.register = tk.Button(self.root, text="Register", highlightthickness=0, relief='flat', width=20,
                                  bg='blue', fg='white',
                                  command=self.register_user)
        self.register.grid(row=6, column=1, pady=10)

        self.cancel = tk.Button(self.root, text='Cancel', bg='blue', fg='white', highlightthickness=0, relief='flat',
                                width=25,
                                command=self.root.destroy)
        self.cancel.grid(row=6, column=0, pady=10)

        self.login = tk.Button(self.root, text="Existing user?", bg='blue', fg='white', highlightthickness=0,
                               relief='flat',
                               width=20, command=self.login_)
        self.login.grid(row=6, column=2, pady=10)

        self.root.mainloop()

    def login_(self):
        self.root.destroy()
        login_form = Login_Form()


class Login_Form:

    def add(self):
        self.msg1.config(text="")
        self.msg2.config(text="")
        r = True

        if len(self.id_value.get()) == 0:
            print(self.id_value.get())
            self.msg1.config(text="User id can't be empty.")
            r = False
        # yha check krna weather userid exist or not.
        else:
            o = database_data()
            self.response = o.check(self.id_value.get())
            if self.response:
                self.msg1.config(text='User id doesn\'t  exist.')
                r = False

        if self.Pwd.get() != "":
            print(self.Pwd.get())
            psd_check = database_data()
            r = psd_check.password_exist(self.id_value.get(), self.Pwd.get())
            if not r:
                tk.messagebox.showerror("Login error", "Incorrect user id or password.")

        elif self.Pwd.get() == "":
            self.msg2.config(text="Password can't be empty.")
            r = False

        if r:
            l = database_data()
            response, user_no_value, name = l.authenticate(self.id_value.get(), self.Pwd.get())

            dal_object1 = DALRecommendation(user_no_value, name)
            # to get trending movies
            movies = dal_object1.get_trending_movie()
            # to get recommendation on the basis of a random movie
            recommendations = dal_object1.get_user_movie()
            if not recommendations:
                print('no movies')

            data = dal_object1.collaborative_filtering()

            # all movies
            # all_movies = dal_object1.get_all_movie()

            self.window.destroy()
            # ---------------------------------- displaying movies---------------------------------------
            a = Photos_display(movies, recommendations, data, name, user_no_value)

    def register(self):
        self.window.destroy()
        new_obj = Registration_form()

    def __init__(self):

        self.window = tk.Tk()
        self.window.title('Login')
        self.window.geometry('520x220')
        self.window.maxsize(width=520, height=220)
        self.window.config(bg='black')

        # image on label
        filename = "new.jpeg"
        image = Image.open(filename)
        logo = ImageTk.PhotoImage(image.resize((160, 190)))
        label = tk.Label(image=logo, bg='black')
        label.photo = logo
        label.place(x=0, y=0)

        # labels for displaying errors
        self.msg1 = tk.Label(self.window, fg='red', bg='black')
        self.msg1.place(x=370, y=40)
        self.msg2 = tk.Label(self.window, fg='red', bg='black')
        self.msg2.place(x=370, y=70)

        # text-variables
        self.id_value = tk.StringVar()
        self.Pwd = tk.StringVar()

        # labels and entry fields
        self.userid = tk.Label(self.window, text='User ID', bg='black', fg='white')
        self.entry1 = tk.Entry(self.window, textvariable=self.id_value)
        self.userid.place(x=170, y=40)
        self.entry1.place(x=240, y=40)

        self.pwd = tk.Label(self.window, text='Password', bg='black', fg='white')
        self.entry2 = tk.Entry(self.window, textvariable=self.Pwd, show="*")
        self.pwd.place(x=170, y=70)
        self.entry2.place(x=240, y=70)

        # Buttons
        self.cancel = tk.Button(self.window, text='Cancel', highlightthickness=0, bg='blue', fg='white',
                                relief='flat', width=10,
                                command=self.window.destroy)
        self.cancel.place(x=150, y=125)

        self.login = tk.Button(self.window, text="Login", highlightthickness=0, bg='blue', fg='white', relief='flat',
                               width=10,
                               command=self.add)
        self.login.place(x=240, y=125)

        self.new_user = tk.Button(self.window, text="New user?", highlightthickness=0, bg='blue', fg='white',
                                  relief='flat', width=10,
                                  command=self.register)
        self.new_user.place(x=330, y=125)

        self.m = tk.Label(self.window, text="New to MovieFlix? Register now!", font=('Times of roman', 8, 'normal'),
                          fg='red', bg='black')
        self.m.place(x=0, y=190)

        self.window.mainloop()


obj = Login_Form()
