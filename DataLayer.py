import random

import pandas
import pyodbc
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from objectModel import Movie


class database_data:
    def __init__(self):
        self.con = pyodbc.connect(
            'driver={sql server};server=DESKTOP-H0RFELD\KANISHKASERVER;Database=RecommendationDB;uid=sa;pwd=kanishka123')

    def __del__(self):
        self.con.close()
        self.con = None

    def check(self, a):

        self.cur = self.con.cursor()
        q = "SELECT * from users where UserId Like ?"
        value = a
        self.cur.execute(q, value)
        if self.cur.fetchone() is not None:
            return False
        else:
            return True

    def register_user(self, obj):
        self.cur = self.con.cursor()
        query = "Insert into users values (?,?,?)"
        values = (obj.userid, obj.password, obj.name)
        self.cur.execute(query, values)
        self.con.commit()

    def password_exist(self, userid, password):
        self.cur = self.con.cursor()
        query = 'Select * from users where UserId Like ? and Password Like ?'
        values = (userid, password)
        self.cur.execute(query, values)
        records = self.cur.fetchall()

        if len(records) > 0:
            return True
        else:
            return False

    def authenticate(self, user_id, password):
        self.cur = self.con.cursor()
        values = (user_id, password)
        query = "Select * from users where UserId Like ? and Password Like ?"
        self.cur.execute(query, values)
        records = self.cur.fetchall()

        if len(records) > 0:
            record = records[0]
            name = record[1]
            user_no = record[0]
            name = record[3]
            return True, user_no, name


class DALRecommendation:
    def __init__(self, userno, name):
        self.con = pyodbc.connect(
            'driver={sql server};server=DESKTOP-H0RFELD\KANISHKASERVER;Database=RecommendationDB;uid=sa;pwd=kanishka123')
        self.user_no = userno
        self.name = name
        self.record_list = []

    def __del__(self):
        self.con.close()
        self.con = None

    def change_rating(self, rating, movie_name):
        self.cur = self.con.cursor()
        query = f'Select MovieNo from Movies where MovieName LIKE ?'
        value = movie_name
        self.cur.execute(query, value)
        movie_no = self.cur.fetchone()
        movieno = movie_no[0]


        q = f'Select * from Ratings where MovieNo LIKE ? and UserNo LIKE ?'
        value2 = (str(movieno), str(self.user_no))
        self.cur.execute(q, value2)
        record = self.cur.fetchall()

        if len(record) > 0:
            return False
        else:
            query = 'Insert into Ratings values(?,?,?)'
            values = (str(movieno), str(self.user_no), rating)
            self.cur.execute(query, values)
            self.con.commit()
            return True

    def get_trending_movie(self):
        self.cur = self.con.cursor()
        query = f'Select  M.MovieNo, M.MovieName, M.image,D.DirectorName, isNULL((Select AVG (Rating) from Ratings where \
         MovieNo=M.MovieNo),0) as [Rating] from Movies as [M] ,Directors as [D] where M.DirectorNo = D.DirectorNo and M.MovieNo \
         NOT IN (Select MovieNo from Ratings where UserNo Like {self.user_no}) order by Rating DESC'
        self.cur.execute(query)
        self.record_list = self.cur.fetchall()

        if len(self.record_list) < 0:
            print("No movie found")
        else:

            movie = Movie()
            for record in self.record_list:
                movie.movieno.append(record[0])
                movie.moviename.append(record[1])
                movie.image.append(record[2])
                movie.rating.append(record[4])
                movie.directorname.append(record[3])

            return movie

    def get_user_movie(self):
        # getting all columns
        query = f'select M.MovieNo, M.MovieName,M.genre,M.image,D.DirectorName from Movies as\
         [M],Directors as [D]  where M.DirectorNo = D.DirectorNo and M.MovieNo in \
         (Select MovieNo from Ratings where UserNo LIKE {self.user_no} and Rating>0)'
        df = pandas.read_sql_query(query, self.con)
        if df.empty:
            return False
        else:

            # getting all actors names
            query2 = f'select M.MovieNo, A.Name from Actors as [A],Movies as [M] ,Cast as [C] \
            where C.MovieNo=M.MovieNo and C.ActorNo = A.ActorNo'
            data = pandas.read_sql_query(query2, self.con)


            # joining actors who worked together
            data['Cast'] = data.groupby(['MovieNo'])['Name'].transform(lambda x: ' '.join(x))
            data.drop_duplicates(subset="MovieNo", keep='first', inplace=True)
            data.drop(['Name'], axis=1, inplace=True)


            # merging together the actors + the additional data
            self.df3 = pandas.merge(df, data, on="MovieNo")

            # Machine learning part
            obj = CountVectorizer()
            matrix = obj.fit_transform(self.df3['Cast'] + self.df3['DirectorName'] + self.df3['genre'])
            cosine = cosine_similarity(matrix)
            self.cos_sim_df = pandas.DataFrame(cosine, index=self.df3.MovieName, columns=self.df3.MovieName)


            # randomly choosing movie from dataframe
            moviename = df['MovieName']
            selected_movie = random.choice(moviename)

            # calling method to select movie
            result = self.recommend_movies(selected_movie)


            self.kanishka = []
            for r in result:
                query = 'Select  M.MovieNo, M.MovieName, M.image,M.Genre,D.DirectorName, isNULL((Select AVG (Rating) from Ratings where \
                MovieNo=M.MovieNo),0) as [Rating] from Movies as [M] ,Directors as [D] where M.DirectorNo = D.DirectorNo \
                and M.MovieName LIKE ?'
                self.cur.execute(query, r)
                self.kanishka.append(self.cur.fetchall())
            print('kati:::\n\n', self.kanishka)

            if len(self.kanishka) < 0:
                print("No movie found")
            else:
                # print(self.record_list)
                recommendaded = Movie()
                for record in self.kanishka:
                    for value in record:
                        recommendaded.movieno.append(value[0])
                        recommendaded.moviename.append(value[1])
                        recommendaded.genre.append(value[3])
                        recommendaded.directorname.append(value[4])
                        recommendaded.rating.append(value[5])
                        recommendaded.image.append(value[2])
                return recommendaded

    def recommend_movies(self, movie_name):
        copy_data = self.df3.set_index('MovieName')
        indices = pandas.Series(copy_data.index)
        index = indices[indices == movie_name].values[0]
        similarity_scores = pandas.Series(self.cos_sim_df[index]).sort_values(ascending=False)
        top_5_movies = list(similarity_scores.iloc[0:].index)


        return top_5_movies

    # def get_all_movie(self):
    #     query = 'select M.MovieNo,M.MovieName,D.DirectorName,M.Genre,M.image from Movies as[M],Directors as\
    #      [D] where M.DirectorNo=D.DirectorNo'
    #     self.cur.execute(query)
    #     self.record_list = self.cur.fetchall()
    #
    #     if len(self.record_list) < 0:
    #         print("No movie found")
    #     else:
    #         # print(self.record_list)
    #         all_movies = Movie()
    #         for record in self.record_list:
    #             all_movies.movieno.append(record[0])
    #             all_movies.moviename.append(record[1])
    #             all_movies.genre.append(record[3])
    #             all_movies.directorname.append(record[2])
    #             all_movies.image.append(record[4])
    #
    #         # print(all_movies.moviename, all_movies.image)
    #         return all_movies

    def collaborative_filtering(self):
        query = 'Select U.UserId,M.MovieName,R.Rating from users as [U],Movies as [M],Ratings as [R] \
        where U.UserNo=R.UserNo and R.MovieNo=M.MovieNo '
        df = pandas.read_sql_query(query, self.con)


        ratings_df = pandas.DataFrame(df.groupby('MovieName')['Rating'].mean())
        # print("Grouping as per ratings=", ratings_df)
        ratings_df['NOR'] = df.groupby('MovieName')['Rating'].count()
        matrix = df.pivot_table(index='UserId', columns='MovieName', values='Rating')

        ratings_df.sort_values('NOR', ascending=False)

        v = random.choice(ratings_df.index)

        chosen_movie = matrix[v]
        corr = matrix.corrwith(chosen_movie)
        corr_df1 = pandas.DataFrame(corr, columns=['Correlation'])

        corr_df1 = corr_df1.join(ratings_df['NOR'])

        sorted_corr_data = corr_df1[corr_df1['NOR'] > 1].sort_values(by='Correlation', ascending=False)


        data = []
        for row in sorted_corr_data.index:
            data.append(row)

        self.result = []

        for r in data:
            query = 'Select  M.MovieNo, M.MovieName, M.image,M.Genre,D.DirectorName, isNULL((Select AVG (Rating) from Ratings where \
                MovieNo=M.MovieNo),0) as [Rating] from Movies as [M] ,Directors as [D] where M.DirectorNo = D.DirectorNo \
                and M.MovieName LIKE ? '
            self.cur.execute(query, r)
            self.result.append(self.cur.fetchall())


        if len(self.result) < 0:
            print("No movie found")
        else:

            collaborative = Movie()
            for record in self.result:
                for value in record:
                    collaborative.movieno.append(value[0])
                    collaborative.moviename.append(value[1])
                    collaborative.genre.append(value[3])
                    collaborative.directorname.append(value[4])
                    collaborative.image.append(value[2])
                    collaborative.rating.append(value[5])

            return collaborative
