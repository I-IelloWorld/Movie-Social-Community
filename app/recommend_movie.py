from app import db
from app.models import *
from flask import Flask

movies = Movie.query.all()
movie_label = {}
n = 1
for movie in movies:
    movie_label[n] = []
    if not movie.comedy:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    if not movie.action:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    if not movie.love:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    if not movie.cartoon:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    if not movie.science:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    if not movie.suspense:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    if not movie.war:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    if not movie.thriller:
        movie_label[n].append(0)
    else:
        movie_label[n].append(1)
    n = n + 1

print(movie_label)


def russel_rao_similarity(list1, list2):
    dist_counter = 0
    for n in range(len(list1)):
        if list1[n] == list2[n]:
            dist_counter += 1
    return dist_counter / len(list1)


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

if __name__ == '__main__':
    app.run(debug=True)
