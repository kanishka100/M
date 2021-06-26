import tkinter as tk
from tkinter import BOTH, LEFT, ttk, VERTICAL, RIGHT, Y, messagebox

from PIL import ImageTk, Image

from DataLayer import DALRecommendation


# ----------------main class-------------------
class Photos_display:
    def __init__(self, movie, recommendation, data, name, user_no):
        self.trending = []
        self.f = ('Verdana', 10, 'normal')
        self.heading = ('Times of roman', 14, 'bold')
        self.abc = tk.Tk()

        self.movie = movie
        self.recommendation = recommendation
        self.data = data

        self.user_no = user_no
        self.count = 0
        self.name = name

        self.abc.title('MovieFlix 🎬')
        self.abc.configure(bg='black')
        self.abc.geometry('960x600')

        # create a main frame
        main_frame = tk.Frame(self.abc, bg='black')
        main_frame.pack(fill=BOTH, expand=1)

        # create a canvas
        my_canvas = tk.Canvas(main_frame, bg='black')
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # add a scrollbar to the canvas
        y_scollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        y_scollbar.pack(side=RIGHT, fill=Y)
        # configure the canvas
        my_canvas.configure(yscrollcommand=y_scollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
        # create another frame inside the canavas
        self.second_frame = tk.Frame(my_canvas, bg='black')
        # add the new frame to a window in the canvas
        my_canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        self.Trending_Movies()

        if recommendation:
            self.count = len(recommendation.moviename)
            # print("\n The length of recommended movies :", self.count)
            self.Recommended_Movies()

        self.counter = len(movie.moviename)
        # print('\n total records for trending movies:', self.counter)
        self.counter1 = len(data.moviename)
        # print('\n total records for collaborative movies:', self.counter1)

        self.Collaborative()
        self.abc.mainloop()

    # --------------------------showing details of a specific movie------------------------
    def open_details(self, movie, poster, director, rating):
        self.flag = tk.Toplevel(self.abc)
        self.flag.title('Movie details 🎬')
        self.flag.geometry('260x450')
        self.flag.config(padx=30, pady=20, bg='black')
        self.single_movie = movie

        # image
        image = Image.open(poster)
        image1 = ImageTk.PhotoImage(image.resize((200, 280)))
        self.label = tk.Label(self.flag, image=image1)
        self.label.photo = image1
        self.label.place(x=0, y=0)

        self.movie_name = tk.Label(self.flag, text=self.single_movie, font=self.f, bg='black', fg='white')
        self.movie_name.place(x=10, y=300)
        movie_director = tk.Label(self.flag, text=f'Director:{director}', font=self.f, bg='black', fg='white')
        movie_director.place(x=10, y=320)
        current_rating = tk.Label(self.flag, text=f'Movie rating:{rating}', font=self.f, bg='black', fg='white')
        current_rating.place(x=10, y=340)

        movie_rating = tk.Label(self.flag, text=f'Enter movie rating', font=self.f, bg='black', fg='white')
        movie_rating.place(x=10, y=360)

        rating = [1, 2, 3, 4, 5]
        self.clicked = tk.IntVar()
        self.clicked.set(rating[0])
        self.drop = tk.OptionMenu(self.flag, self.clicked, *rating, command=self.rating_change)
        self.drop.config(bg='black', fg='white')
        self.drop.place(x=30, y=390)
        self.cancel = tk.Button(self.flag, text='cancel', command=self.flag.destroy, bg='black', fg='white')
        self.cancel.place(x=90, y=390)
        self.flag.grab_set()

    # -----------------------to change rating--------------------
    def rating_change(self, event):
        rating = self.clicked.get()
        print('Rating = ', rating)
        obj = DALRecommendation(self.user_no, self.name)
        success = obj.change_rating(rating, self.single_movie)
        if success:
            messagebox.showinfo('Rating Message', 'Rating Successfully Added.')
            self.flag.destroy()
        else:
            messagebox.showerror('Rating Error.', 'Rating already exists.')
            self.flag.destroy()

    # -------showing all collaborative movies------------------
    def all_collaborative_movies(self, images, names, directors, rating):

        self.flag1 = tk.Toplevel(self.abc)
        self.flag1.geometry('850x500')
        self.flag1.config(bg='black')

        # create a main frame
        main_frame1 = tk.Frame(self.flag1, bg='black')
        main_frame1.pack(fill=BOTH, expand=1)

        my_canvas = tk.Canvas(main_frame1, bg='black')
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        y_scollbar = ttk.Scrollbar(main_frame1, orient=VERTICAL, command=my_canvas.yview)
        y_scollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=y_scollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
        self.second_frame = tk.Frame(my_canvas, bg='black')
        my_canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        label = tk.Label(self.second_frame, text="Movies", font=self.f, bg='black', fg='white')
        label.grid(row=0, column=0)
        a = 0

        for m in range(0, 20, 2):
            for n in range(0, 5):
                if a < self.counter1:
                    filename = f"movie-poster/{images[a]}"
                    image = Image.open(filename)
                    image1 = ImageTk.PhotoImage(image.resize((150, 180)))
                    label = tk.Button(self.second_frame, image=image1, relief='flat', bg='black', fg='white',
                                      command=lambda a=a: self.open_details(names[a], f"movie-poster/{images[a]}",
                                                                            directors[a], rating[a]
                                                                            ))
                    label.photo = image1
                    label.grid(row=m + 1, column=n, padx=5, pady=15, sticky='NSEW')
                    movie_name = tk.Label(self.second_frame, text=names[a], bg='black', fg='white')
                    movie_name.grid(row=m + 2, column=n, padx=5, sticky='NSEW')
                    a += 1
        self.flag1.grab_set()

        # -------showing recommended movies-----------------

    def all_recommended_movies(self, images, names, directors, rating):

        self.flag1 = tk.Toplevel(self.abc)
        self.flag1.geometry('900x500')
        self.flag1.config(bg='black')
        # create a main frame
        main_frame1 = tk.Frame(self.flag1)
        main_frame1.pack(fill=BOTH, expand=1)

        # create a canvas
        my_canvas = tk.Canvas(main_frame1, bg='black')
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        y_scollbar = ttk.Scrollbar(main_frame1, orient=VERTICAL, command=my_canvas.yview)
        y_scollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=y_scollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
        self.second_frame = tk.Frame(my_canvas, bg='black')
        my_canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        # label
        label = tk.Label(self.second_frame, text="MOVIES", font=self.f, bg='black', fg='white')
        label.grid(row=0, column=0)
        a = 0

        for m in range(0, 20, 2):
            for n in range(0, 5):
                if a < self.count:
                    filename = f"movie-poster/{images[a]}"
                    image = Image.open(filename)
                    image1 = ImageTk.PhotoImage(image.resize((160, 200)))
                    label = tk.Button(self.second_frame, image=image1, relief='flat', bg='black', fg='white',
                                      command=lambda a=a: self.open_details(names[a]
                                                                            , f"movie-poster/{images[a]}",
                                                                            directors[a], rating[a]
                                                                            ))
                    label.photo = image1
                    label.grid(row=m + 1, column=n, padx=5, pady=15, sticky='NSEW')
                    movie_name = tk.Label(self.second_frame, text=names[a], bg='black', fg='white')
                    movie_name.grid(row=m + 2, column=n, padx=5, sticky='NSEW')
                    a += 1

        self.flag1.grab_set()

    # -------showing trending movies-----------------

    def all_trending_movies(self, images, names, directors, rating):

        self.flag1 = tk.Toplevel(self.abc)
        self.flag1.geometry('900x500')
        self.flag1.config(bg='black')
        # create a main frame
        main_frame1 = tk.Frame(self.flag1, bg='black')
        main_frame1.pack(fill=BOTH, expand=1)

        # create a canvas
        my_canvas = tk.Canvas(main_frame1, bg='black')
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        y_scollbar = ttk.Scrollbar(main_frame1, orient=VERTICAL, command=my_canvas.yview)
        y_scollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=y_scollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

        self.second_frame = tk.Frame(my_canvas, bg='black')
        my_canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        # label
        label = tk.Label(self.second_frame, text="MOVIES", font=self.f, bg='black', fg='white')
        label.grid(row=0, column=0)
        a = 0

        for m in range(0, 20, 2):
            for n in range(0, 5):
                if a < self.counter:
                    filename = f"movie-poster/{images[a]}"
                    image = Image.open(filename)
                    image1 = ImageTk.PhotoImage(image.resize((160, 200)))
                    label = tk.Button(self.second_frame, image=image1, relief='flat', bg='black', fg='white',
                                      command=lambda a=a: self.open_details(names[a]
                                                                            , f"movie-poster/{images[a]}",
                                                                            directors[a],
                                                                            rating[a]
                                                                            ))
                    label.photo = image1
                    label.grid(row=m + 1, column=n, padx=5, pady=15, sticky='NSEW')
                    movie_name = tk.Label(self.second_frame, text=names[a], bg='black', fg='white')
                    movie_name.grid(row=m + 2, column=n, padx=5, sticky='NSEW')
                    a += 1

        self.flag1.grab_set()

    # ---------------------trending movies---------------------
    def Trending_Movies(self):
        # print(self.movie.moviename)
        lb = tk.Label(self.second_frame, text="Trending Movies", font=self.heading, bg='black', fg='white')
        lb.grid(row=0, column=0)
        more_Movies = tk.Button(self.second_frame, text="More Movies", font=self.f, bg='black', fg='white',
                                command=lambda: self.all_trending_movies(self.movie.image, self.movie.moviename,
                                                                         self.movie.directorname, self.movie.rating))

        more_Movies.grid(row=0, column=4)

        for n in range(0, 5):
            print(self.movie.rating[n])
            filename = f"movie-poster/{self.movie.image[n]}"
            image = Image.open(filename)
            image1 = ImageTk.PhotoImage(image.resize((160, 180)))

            label = tk.Button(self.second_frame, image=image1, relief='flat', bg='black', fg='white',
                              command=lambda n=n: self.open_details(self.movie.moviename[n]
                                                                    , f"movie-poster/{self.movie.image[n]}",
                                                                    self.movie.directorname[n], self.movie.rating[n]
                                                                    ))
            label.photo = image1
            label.grid(row=1, column=n, padx=5, pady=15, sticky='NSEW')
            movie_name = tk.Label(self.second_frame, text=self.movie.moviename[n], bg='black', fg='white')
            movie_name.grid(row=3, column=n, padx=5, sticky='NSEW')

    # -----------------------recommended movies---------------------------
    def Recommended_Movies(self):
        lb = tk.Label(self.second_frame, text="Recommended Movies", font=self.heading, bg='black', fg='white', )
        lb.grid(row=4, column=0, pady=(20, 0))

        more_Movies = tk.Button(self.second_frame, text="More Movies", font=self.f, bg='black', fg='white',
                                command=lambda: self.all_recommended_movies(self.recommendation.image,
                                                                            self.recommendation.moviename,
                                                                            self.recommendation.directorname,
                                                                            self.recommendation.rating))
        more_Movies.grid(row=4, column=4, pady=(20, 0))

        for n in range(0, 5):
            # print(self.recommendation.directorname)
            filename = f"movie-poster/{self.recommendation.image[n]}"
            image = Image.open(filename)
            image1 = ImageTk.PhotoImage(image.resize((160, 200)))
            label = tk.Button(self.second_frame, image=image1, relief='flat', bg='black', fg='white',
                              command=lambda n=n: self.open_details(self.recommendation.moviename[n]
                                                                    , f"movie-poster/{self.recommendation.image[n]}",
                                                                    self.recommendation.directorname[n],
                                                                    self.recommendation.rating[n]
                                                                    ))

            label.photo = image1
            label.grid(row=7, column=n, padx=5, pady=15, sticky='NSEW')

            movie_name = tk.Label(self.second_frame, text=self.recommendation.moviename[n], bg='black', fg='white', )
            movie_name.grid(row=8, column=n, padx=5, sticky='NSEW')

    # -------------------collaborative -----------------------------
    def Collaborative(self):
        more_Movies = tk.Button(self.second_frame, text="More Movies", font=self.f, bg='black', fg='white',
                                command=lambda: self.all_collaborative_movies(self.data.image, self.data.moviename,
                                                                              self.data.directorname, self.data.rating))
        more_Movies.grid(row=13, column=4, pady=(20, 0))
        lb = tk.Label(self.second_frame, text="Collaborative Movies", font=self.heading, bg='black', fg='white', )
        lb.grid(row=13, column=0, pady=(20, 0))

        for n in range(0, 5):
            filename = f"movie-poster/{self.data.image[n]}"
            image = Image.open(filename)
            image1 = ImageTk.PhotoImage(image.resize((160, 180)))

            label = tk.Button(self.second_frame, image=image1, relief='flat', bg='black', fg='white',
                              command=lambda n=n: self.open_details(self.data.moviename[n]
                                                                    , f"movie-poster/{self.data.image[n]}",
                                                                    self.data.directorname[n], self.data.rating[n]
                                                                    ))
            label.photo = image1
            label.grid(row=15, column=n, padx=5, pady=15, sticky='NSEW')
            movie_name = tk.Label(self.second_frame, text=self.data.moviename[n], bg='black', fg='white', )
            movie_name.grid(row=16, column=n, padx=5, sticky='NSEW')

    # def b(self):
    #     self.lb = tk.Label(self.second_frame, text="All Movies", font=('Helvetica', 15, 'bold'))
    #     self.lb.grid(row=10, column=0, pady=(10, 0))
    #     a = 0
    #     for m in range(0, 7, 2):
    #         for n in range(5):
    #             filename = f"movie-poster/{self.all_movies.image[a]}"
    #             image = Image.open(filename)
    #             image1 = ImageTk.PhotoImage(image.resize((160, 200)))
    #             label = tk.Button(self.second_frame, image=image1)
    #             label.photo = image1
    #             label.grid(row=m + 11, column=n, padx=20, pady=(20, 0), sticky='NSEW')
    #
    #             movie_name = tk.Label(self.second_frame, text=self.all_movies.moviename[a])
    #             movie_name.grid(row=m + 12, column=n, padx=20, sticky='NSEW')
    #             a += 1
