from app import db
from app.models import *
from flask import Flask

users = User.query.all()
user_label = {}
n = 1
for user in users:
    user_label[n] = []
    if not user.comedy:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    if not user.action:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    if not user.love:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    if not user.cartoon:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    if not user.science:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    if not user.suspense:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    if not user.war:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    if not user.thriller:
        user_label[n].append(0)
    else:
        user_label[n].append(1)
    n = n + 1

print(user_label)


def russel_rao_similarity(list1, list2):
    dist_counter = 0
    for n in range(len(list1)):
        if list1[n] == list2[n]:
            dist_counter += 1
    return dist_counter / len(list1)


# app = Flask(__name__)
# app.config['SECRET_KEY'] = '123'
#
# if __name__ == '__main__':
#     app.run(debug=True)
