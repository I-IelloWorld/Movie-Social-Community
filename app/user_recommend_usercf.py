import numpy as np
import pandas as pd
from app import db
from app.models import *
from flask import Flask
# from sklearn.metrics.pairwise import cosine_similarity


def load_user_item():
    items = {}
    movies = Movie.query.all()
    user1 = User.query.filter_by(authority=0).all()

    for movie in movies:
        movie_grades = Movie_Grade.query.filter_by(movie_id=movie.id).all()
        items[movie.movie_name] = {}
        for user in user1:
            if Movie_Grade.query.filter_by(movie_id=movie.id, user_id=user.id).first():
                a = Movie_Grade.query.filter_by(movie_id=movie.id, user_id=user.id).first()
                items[movie.movie_name][user.id] = a.grade
            else:
                items[movie.movie_name][user.id] = movie.vote_average

    users = {}
    for user in user1:
        movie_grades = Movie_Grade.query.filter_by(movie_id=movie.id).all()
        users[user.id] = {}
        for movie in movies:
            if Movie_Grade.query.filter_by(movie_id=movie.id, user_id=user.id).first():
                b = Movie_Grade.query.filter_by(movie_id=movie.id, user_id=user.id).first()
                users[user.id][movie.movie_name] = b.grade
            else:
                users[user.id][movie.movie_name] = movie.vote_average

    # print(items)
    # print(users)
    return items, users

    # items = {
    #     'A': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    #     'B': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    #     'C': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    #     'D': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    #     'E': {2: 0, 3: 0, 4: 0, 5: 0}
    # }
    # users = {
    #     1: {'A': 0, 'B': 0, 'C': 0, 'D': 0},
    #     2: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0},
    #     3: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0},
    #     4: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0},
    #     5: {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
    # }
    # return items, users


# def matrix_list(i):
#     n = 1
#     list_temp = []
#     while n <= len(i):
#         list_temp.append(n)
#         n += 1
#     return list_temp

matrix_list = []
user2 = User.query.filter_by(authority=0).all()
for user in user2:
    matrix_list.append(user.id)
# print(1111111111111111111111111111111111111)
# print(matrix_list)



def user_cf():
    items, users = load_user_item()
    # print(999999999999999999999999999999999999999999)
    # print(users)
    similarity_matrix = pd.DataFrame(np.zeros((len(users), len(users))),
                                     index=matrix_list, columns=matrix_list)
    for user_id in users:
        for other_user_id in users:
            user_vector = []
            otheruser_vector = []
            if user_id != other_user_id:
                for item_id in items:
                    item_rating = items[item_id]
                    if user_id in item_rating and other_user_id in item_rating:
                        user_vector.append(item_rating[user_id])
                        otheruser_vector.append(item_rating[other_user_id])

                similarity_matrix[user_id][other_user_id] = np.corrcoef(np.array(user_vector),
                                                                        np.array(otheruser_vector))[0][1]
    return similarity_matrix


def get_recommend_user_list(j, n, similarity_matrix):
    similarity_users = similarity_matrix[j].sort_values(ascending=False)[:n].index.tolist()
    return similarity_users


# print(load_user_item())
# print(user_cf())
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

if __name__ == '__main__':
    app.run(debug=True)
