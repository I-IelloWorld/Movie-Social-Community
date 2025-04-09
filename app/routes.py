import logging
import os
import json
from uuid import uuid4

import socketio
from flask_socketio import SocketIO, join_room, leave_room
from PIL import Image
from sqlalchemy import true, false
from sqlalchemy import or_

from app.bm25 import BM25User, BM25Movie
from app.functions import *
from app.models import *
from app.forms import LoginForm

from datetime import datetime, timedelta
from flask import render_template, redirect, flash, url_for, session, request, jsonify, send_from_directory, \
    current_app, Markup
from werkzeug.security import check_password_hash, generate_password_hash
from flask_avatars import Avatars
from sqlalchemy import and_, distinct

import math
import os
import jieba
import pickle
import logging
# from bm25 import BM25
import nltk
from nltk import PorterStemmer
from app import app, db, Config

from app.recommend_movie import movie_label
from app.recommend_user import user_label, russel_rao_similarity
from app.ML import Do_ALS
from app.user_recommend_usercf import load_user_item, user_cf, get_recommend_user_list

avatars = Avatars()

movie_labels = dict({
    '0': 'comedy',
    '1': 'action',
    '2': 'love',
    '3': 'cartoon',
    '4': 'science',
    '5': 'suspense',
    '6': 'war',
    '7': 'thriller'
})

"""main page part
"""
socketio = SocketIO()
socketio.init_app(app)


# main page
@app.route('/')
def home():
    movie_popular = Movie.query.filter(Movie.is_delete == 0).order_by(-Movie.popular).all()[0:7]
    print(movie_popular)
    movie_latest = Movie.query.filter(Movie.is_delete == 0).order_by(Movie.release_time.desc()).all()[0:7]
    movie_TopRated = Movie.query.filter(Movie.is_delete == 0).order_by(Movie.vote_average.desc()).all()[0:7]
    movie_MostViewed = Movie.query.filter(Movie.is_delete == 0).order_by(Movie.vote_count.desc()).all()[0:7]
    aaa = 1 or 2
    print(1)
    if islogined():
        user = User.query.filter(User.id == session["id"]).first()
        name = user.user_name
        authority = session.get('authority')
        user_id = session.get('id')
        recommend_list = []

        if session.get('recommend') == "Grade less than 3" or session.get('recommend') == "similarity":
            # put similarity algorithm here
            user_recommend = User.query.filter_by(id=user_id).first()
            user1 = []
            similarity = []

            if not user_recommend.comedy:
                user1.append(0)
            else:
                user1.append(1)
            if not user_recommend.action:
                user1.append(0)
            else:
                user1.append(1)
            if not user_recommend.love:
                user1.append(0)
            else:
                user1.append(1)
            if not user_recommend.cartoon:
                user1.append(0)
            else:
                user1.append(1)
            if not user_recommend.science:
                user1.append(0)
            else:
                user1.append(1)
            if not user_recommend.suspense:
                user1.append(0)
            else:
                user1.append(1)
            if not user_recommend.war:
                user1.append(0)
            else:
                user1.append(1)
            if not user_recommend.thriller:
                user1.append(0)
            else:
                user1.append(1)
            print(user1)
            print(movie_label)
            for movie in movie_label:
                print(movie_label[movie])
                a = {'movie_id': movie, 'score': russel_rao_similarity(user1, movie_label[movie])}
                similarity.append(a)

            final_similarity = sorted(similarity, key=lambda x: x['score'], reverse=True)
            print(final_similarity)

            for single_similarity in final_similarity:
                if len(recommend_list) < 8:
                    movie = Movie.query.filter_by(id=single_similarity['movie_id'], is_delete=0).first()
                    # recommendMovie = {'id': movie.id, 'movie_name': movie.movie_name, 'pic': movie.pic_path,
                    #                   'introduction': movie.introduction, 'popular': movie.popular,
                    #                   'vote_average': movie.vote_average,
                    #                   'comedy': movie.comedy, 'action': movie.action, 'love': movie.love,
                    #                   'cartoon': movie.cartoon,
                    #                   'science': movie.science, 'suspense': movie.suspense, 'war': movie.war,
                    #                   'thriller': movie.thriller}
                    recommend_list.append(movie)

        if session.get('recommend') == "Collaborative Filtering":
            all_grades = Movie_Grade.query.all()
            print(all_grades)
            grades = []
            for g in all_grades:
                grade = []
                grade.append(g.user_id)
                grade.append(g.movie_id)
                grade.append(g.grade)
                grades.append(grade)
            print(grades)
            recommend_movies = Do_ALS(grades, user_id, 8)
            print(recommend_movies)
            for rm in recommend_movies:
                m = Movie.query.filter_by(id=rm[0], is_delete=0).first()
                recommend_list.append(m)

        return render_template('index.html', islogin=islogined(), user=user, name=name,
                               movie_popular=movie_popular,
                               movie_latest=movie_latest, movie_TopRated=movie_TopRated,
                               movie_MostViewed=movie_MostViewed,
                               authority=authority, movie_labels=movie_labels, movie_label_value=movie_labels.values(),
                               recommend=recommend_list, state=session.get('recommend'))
    else:
        name = "visitor"
        authority = None

    print(movie_labels)
    print(movie_labels.values())

    return render_template('index.html', islogin=islogined(), name=name, movie_popular=movie_popular,
                           movie_latest=movie_latest, movie_TopRated=movie_TopRated, movie_MostViewed=movie_MostViewed,
                           authority=authority, movie_labels=movie_labels, movie_label_value=movie_labels.values())


@app.route('/change-recommendation-algorithm')
def recommend():
    if session.get('recommend') == "similarity" or session.get('recommend') == "Grade less than 3":
        grades = Movie_Grade.query.filter_by(user_id=session.get('id')).all()
        if len(grades) >= 3:
            session['recommend'] = "Collaborative Filtering"
        else:
            session['recommend'] = "Grade less than 3"
    else:
        session['recommend'] = "similarity"
    return redirect(url_for('home'))


@app.route('/movie_partition', methods=['GET', 'POST'])
def movie_partition():
    authority = None
    name = None
    if islogined():
        authority = session.get('authority')
        userID = session.get('id')
        user = User.query.filter_by(id=userID).first()
        name = user.user_name
    else:
        user = None

    label = request.args.get('label', None)
    print(label)
    print(label)
    page = request.args.get('page', 1, type=int)
    if label == '0':
        movie_partition = Movie.query.filter(Movie.comedy == 1).paginate(page, per_page=8, error_out=False)
    elif label == '1':
        movie_partition = Movie.query.filter(Movie.action == 1).paginate(page, per_page=8, error_out=False)
    elif label == '2':
        movie_partition = Movie.query.filter(Movie.love == 1).paginate(page, per_page=8, error_out=False)
    elif label == '3':
        movie_partition = Movie.query.filter(Movie.cartoon == 1).paginate(page, per_page=8, error_out=False)
    elif label == '4':
        movie_partition = Movie.query.filter(Movie.science == 1).paginate(page, per_page=8, error_out=False)
    elif label == '5':
        movie_partition = Movie.query.filter(Movie.suspense == 1).paginate(page, per_page=8, error_out=False)
    elif label == '6':
        movie_partition = Movie.query.filter(Movie.war == 1).paginate(page, per_page=8, error_out=False)
    elif label == '7':
        movie_partition = Movie.query.filter(Movie.thriller == 1).paginate(page, per_page=8, error_out=False)

    return render_template('category.html', movie_partition=movie_partition, authority=authority ,movie_labels=movie_labels,
                           movie_label_value=movie_labels.values(), user=user, label=label, name=name)


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()  # get the value from "GET"
        return render_template('sign-in.html', form=form)
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            user = form.name.data  # get the value from "POST"
            pwd = form.pwd.data  # get the value from "POST"
            checkuser = User.query.filter(User.user_name == user).first()
            if checkuser == None:
                print("1")
                return render_template("sign-in.html", msg="This username has not been registered", form=form)
            else:
                print("2")
                if checkuser.check_password(pwd):
                    # session['Logged_in'] = True
                    # session['user_info'] = user
                    session['id'] = checkuser.id
                    session['username'] = user
                    session['authority'] = checkuser.authority
                    session['recommend'] = "similarity"
                    return redirect('/')
                else:
                    return render_template("sign-in.html", msg='Incorrect user name or password', form=form)
        else:
            return render_template("sign-in.html", msg='Incorrect user name or password', form=form)


# registration
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html', movie_labels=movie_labels)
    if request.method == 'POST':
        if User.query.filter(User.user_name == request.form["username"]).first() == None:
            password_hash = generate_password_hash(request.form["password"])
            if request.form['gender'] == 'male':
                user = User(user_name=request.form["username"], email=request.form["email"], gender='1',
                            password_hash=password_hash, comedy=bool(request.form["comedy"]),
                            action=bool(request.form["action"]),
                            love=bool(request.form["love"]), cartoon=bool(request.form["cartoon"]),
                            science=bool(request.form["science"]),
                            suspense=bool(request.form["suspense"]), war=bool(request.form["war"]),
                            thriller=bool(request.form["thriller"]))
                firend1 = Friends()

            elif request.form['gender'] == 'female':
                user = User(user_name=request.form["username"], email=request.form["email"], gender='0',
                            password_hash=password_hash, comedy=bool(request.form["comedy"]),
                            action=bool(request.form["action"]),
                            love=bool(request.form["love"]), cartoon=bool(request.form["cartoon"]),
                            science=bool(request.form["science"]),
                            suspense=bool(request.form["suspense"]), war=bool(request.form["war"]),
                            thriller=bool(request.form["thriller"]))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('registration.html',
                                   message='The same registered user name exists, please replace it.',
                                   movie_labels=movie_labels)


# 更改密码
@app.route('/personal_page/change_pw', methods=['GET', 'POST'])
def change_pw():
    if islogined():
        user = User.query.filter(User.id == session.get('id')).first()
        if request.method == 'GET':
            return render_template('change_password.html', user=user)
        if request.method == 'POST':
            newpassword_hash = generate_password_hash(request.form["new password"])
            original_pw = request.form["original password"]
            new_pw = request.form["new password"]
            new_pw_cfm = request.form["new password confirm"]
            # 原始密码是否正确
            if user.check_password(original_pw):
                # 新密码是否两次相同
                if new_pw == new_pw_cfm:
                    user.password_hash = newpassword_hash
                    db.session.commit()
                    return redirect(url_for('personal'))
                else:
                    return "Please Make Sure Your Inputs same on New Password !!! "
            else:
                return "Wrong original password !!!"
    else:
        return redirect(url_for('login'))


# 更改个人信息
@app.route('/personal_page/change_info', methods=['GET', 'POST'])
def change_info():
    if islogined():
        user = User.query.filter(User.id == session.get('id')).first()
        # 备用，显示单词
        gen = "Not Know"
        if int(user.gender) == 0:
            gen = "Female"
        elif int(user.gender) == 1:
            gen = "Male"
        if request.method == 'GET':
            return render_template('change_Information.html', user=user, gen=gen, movie_labels=movie_labels)
        if request.method == 'POST':
            if request.form['gender'] == 'male':
                user.gender = '1'
            elif request.form['gender'] == 'female':
                user.gender = '0'
            user.thriller = bool(request.form["thriller"])
            user.user_name = request.form["username"]
            user.email = request.form["email"]
            user.comedy = bool(request.form["comedy"])
            user.action = bool(request.form["action"])
            user.love = bool(request.form["love"])
            user.cartoon = bool(request.form["cartoon"])
            user.science = bool(request.form["science"])
            user.suspense = bool(request.form["suspense"])
            user.war = bool(request.form["war"])
            user.introduction = request.form["textarea"]
            db.session.commit()
            return redirect(url_for('personal'))
    else:
        return redirect(url_for('login'))


# log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# IR部分 #########################################################

jieba.setLogLevel(log_level=logging.INFO)


@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    authority = None
    user1 = None
    name = None
    if islogined():
        userID = session.get('id')
        name = session.get('username')
        authority = session.get('authority')
        user1 = User.query.filter_by(id=userID).first()
    # 原内容
    user_bm25 = BM25User()
    # query_content = "1"  # 查询语句
    list = []
    result = user_bm25.cal_similarity_rank(session.get('search'))
    for line, score in result:
        li = line.split(' ')
        uid = int(li[0])
        user = User.query.filter(User.id == uid).first()
        list.append(user)
        print(line, score)
    print(list)
    # n = session.get('search')
    # user = User.query.all()
    # sql = "SELECT * FROM T_SECTION WHERE TITLE LIKE '%s'" % ('%%%s%%' % n)
    # user.exe
    # # search = "SELECT * FROM user WHERE user_name LIKE '%"+n+"%'"

    return render_template('search.html', userList=list, type='userSearch', movie_labels=movie_labels,
                           movie_label_value=movie_labels.values(), authority=authority, user=user1, name=name)


@app.route('/search_movie', methods=['GET', 'POST'])
def search_movie():
    # 原内容
    authority = None
    user = None
    name = None
    if islogined():
        userID = session.get('id')
        name = session.get('username')
        authority = session.get('authority')
        user = User.query.filter_by(id=userID).first()
    query_content = request.form['search']
    session['search'] = query_content
    print(query_content, 11)
    movie_bm25 = BM25Movie()
    # query_content = "Transformers"  # 查询语句
    result = movie_bm25.cal_similarity_rank(query_content)
    list = []
    for line, score in result:
        li = line.split(' ')
        mid = int(li[0])
        movie = Movie.query.filter(Movie.id == mid).first()
        list.append(movie)
        print(line, score)
    print(list)
    # return redirect('/')
    return render_template("search.html", movieList=list, type='movieSearch', movie_labels=movie_labels,
                           movie_label_value=movie_labels.values(),authority= authority,  name=name, user=user)


@app.route('/search_movie/1', methods=['GET', 'POST'])
def search_movie_1():
    # 原内容
    authority = None
    user = None
    name = None
    if islogined():
        userID = session.get('id')
        name = session.get('username')
        authority = session.get('authority')
        user = User.query.filter_by(id=userID).first()
    query_content = session.get('search')
    movie_bm25 = BM25Movie()
    # query_content = "Transformers"  # 查询语句
    result = movie_bm25.cal_similarity_rank(query_content)
    list = []
    for line, score in result:
        li = line.split(' ')
        mid = int(li[0])
        movie = Movie.query.filter(Movie.id == mid).first()
        list.append(movie)
        print(line, score)
    print(list)
    # return redirect('/')
    return render_template("search.html", movieList=list, type='movieSearch', movie_labels=movie_labels,
                           movie_label_value=movie_labels.values(), authority= authority,  name=name, user=user)


# recommend friends
@app.route('/recommend_friends', methods=['GET', 'POST'])
def recommend_friends():
    session['recommend_friend'] = "by_tag"
    user_id = session.get('id')
    user_own = User.query.filter_by(id=user_id).first()
    name = user_own.user_name
    authority = user_own.authority
    user_recommend = User.query.filter_by(id=user_id).first()
    user1 = []
    similarity = []
    final_similarity = []
    recommend = []

    if not user_recommend.comedy:
        user1.append(0)
    else:
        user1.append(1)
    if not user_recommend.action:
        user1.append(0)
    else:
        user1.append(1)
    if not user_recommend.love:
        user1.append(0)
    else:
        user1.append(1)
    if not user_recommend.cartoon:
        user1.append(0)
    else:
        user1.append(1)
    if not user_recommend.science:
        user1.append(0)
    else:
        user1.append(1)
    if not user_recommend.suspense:
        user1.append(0)
    else:
        user1.append(1)
    if not user_recommend.war:
        user1.append(0)
    else:
        user1.append(1)
    if not user_recommend.thriller:
        user1.append(0)
    else:
        user1.append(1)
    n = 0
    for user in user_label:
        if user != user_id:
            a = {'user_id': user, 'score': russel_rao_similarity(user1, user_label[user])}
            similarity.append(a)
            n = n + 1
        else:
            n = n + 1

    final_similarity = sorted(similarity, key=lambda x: x['score'], reverse=True)
    print(final_similarity)

    for single_similarity in final_similarity:
        if User.query.filter_by(id=single_similarity['user_id'], authority=0).first():
            user = User.query.filter_by(id=single_similarity['user_id'], authority=0).first()
            print(user)
            exist1 = Friends.query.filter(Friends.user_id == session.get('id'), Friends.friend_id == user.id).first()
            exist2 = Friend_Application.query.filter(Friend_Application.sender == session.get('id'),
                                                     Friend_Application.receiver == user.id).first()
            print(exist1)
            print(exist2)
            if exist1 is None and exist2 is None:
                recommendUser = {'id': user.id, 'user_name': user.user_name, 'email': user.email, 'gender': user.gender,
                                 'icon': user.icon, 'introduction': user.introduction, 'authority': user.authority,
                                 'comedy': user.comedy, 'action': user.action, 'love': user.love,
                                 'cartoon': user.cartoon,
                                 'science': user.science, 'suspense': user.suspense, 'war': user.war,
                                 'thriller': user.thriller}
                recommend.append(recommendUser)

    page = request.args.get('page', 1, type=int)
    user_all = User.query.filter(User.id != session.get('id'), User.authority == 0).paginate(page, per_page=8,
                                                                                             error_out=False)

    return render_template("social-square.html", recommend=recommend, user_all=user_all, recommend_type="by_tag",
                           movie_labels=movie_labels, authority=authority, user=user_own, name=name)


# recommend friends
@app.route('/recommend_friends2', methods=['GET', 'POST'])
def recommend_friends2():
    recommend = []
    session['recommend_friend'] = "collaborative_filtering"
    user_id = session.get('id')
    user_own = User.query.filter_by(id=user_id).first()
    name = user_own.user_name
    authority = user_own.authority
    load_user_item()
    user_cf()
    if len(user_cf()) > 10:
        recommend1 = get_recommend_user_list(session.get('id'), 10, user_cf())
    else:
        recommend1 = get_recommend_user_list(session.get('id'), len(user_cf()), user_cf())

    recommend1.remove(session.get('id'))
    for a in recommend1:
        user = User.query.filter_by(id=a).first()
        recommendUser = {'id': user.id, 'user_name': user.user_name, 'email': user.email, 'gender': user.gender,
                         'icon': user.icon, 'introduction': user.introduction, 'authority': user.authority,
                         'comedy': user.comedy, 'action': user.action, 'love': user.love, 'cartoon': user.cartoon,
                         'science': user.science, 'suspense': user.suspense, 'war': user.war,
                         'thriller': user.thriller}
        recommend.append(recommendUser)

    page = request.args.get('page', 1, type=int)
    user_all = User.query.filter(User.id != session.get('id'), User.authority == 0).paginate(page, per_page=8,
                                                                                             error_out=False)

    return render_template("social-square.html", recommend=recommend, user_all=user_all, recommend_type="by_rate",
                           movie_labels=movie_labels, authority=authority, user=user_own, name=name)


"""personal page part
"""


# perform personal page
@app.route('/personal_page', methods=['GET'])
def personal():
    if islogined():
        user = User.query.filter(User.id == session.get('id')).first()

        # 个人页面最近点赞
        li = Movie_Like.query.filter(Movie_Like.user_id == user.id).order_by(-Movie_Like.id).all()
        reli = li[:5]
        recent_likes = []
        # 需要电影名称和icon
        for l in reli:
            m = Movie.query.filter(l.movie_id == Movie.id).first()
            recent_likes.append(m)

        # 个人兴趣百分比
        comedy_num = 0
        action_num = 0
        love_num = 0
        cartoon_num = 0
        science_num = 0
        suspense_num = 0
        war_num = 0
        thriller_num = 0
        total = 0
        for per in li:
            m = Movie.query.filter(Movie.id == per.movie_id).first()
            total += 1
            if m.comedy:
                comedy_num += 1
            if m.action:
                action_num += 1
            if m.love:
                love_num += 1
            if m.cartoon:
                cartoon_num += 1
            if m.science:
                science_num += 1
            if m.suspense:
                suspense_num += 1
            if m.war:
                war_num += 1
            if m.thriller:
                thriller_num += 1
        if total == 0:
            total = 1
        comedy_num = int(round(comedy_num / total, 2) * 100)
        action_num = int(round(action_num / total, 2) * 100)
        love_num = int(round(love_num / total, 2) * 100)
        cartoon_num = int(round(cartoon_num / total, 2) * 100)
        science_num = int(round(science_num / total, 2) * 100)
        suspense_num = int(round(suspense_num / total, 2) * 100)
        war_num = int(round(war_num / total, 2) * 100)
        thriller_num = int(round(thriller_num / total, 2) * 100)

        # 个人页面收藏
        coll = Movie_Collect.query.filter(Movie_Collect.user_id == user.id).order_by(-Movie_Collect.id).all()
        collect_num = len(coll)
        recoll = coll[:5]
        recent_coll = []
        # 需要电影名称和icon
        for c in recoll:
            n = Movie.query.filter(Movie.id == c.movie_id).first()
            recent_coll.append(n)

        # 高赞评论
        comments = Comment.query.filter(Comment.user_id == user.id).order_by(Comment.like_num.desc()).all()
        re_comm = comments[:6]
        high_comm = []
        for com in re_comm:
            pack = []
            movie = Movie.query.filter(Movie.id == com.movie_id).first()
            pack.append(com)
            pack.append(movie)
            high_comm.append(pack)
        print(high_comm)
        com_num = len(high_comm)

        comments = Comment.query.filter(Comment.user_id == user.id).all()
        comment_num = len(comments)

        friends = Friends.query.filter(Friends.user_id == user.id).all()
        friend_num = len(friends)

        return render_template('personal-home.html', user=user, like_history=recent_likes, collections=recent_coll,
                               collect_num=collect_num, comment_num=comment_num, friend_num=friend_num, total=total,
                               comedy_num=comedy_num, action_num=action_num, love_num=love_num, cartoon_num=cartoon_num,
                               science_num=science_num, suspense_num=suspense_num, war_num=war_num,
                               thriller_num=thriller_num, high_like_comments=high_comm, com_num=com_num)
    else:
        return redirect(url_for('login'))


@app.route('/personal_page/more_collection', methods=['GET'])
def more_collection():
    if islogined():
        user = User.query.filter(User.id == session.get('id')).first()

        collections = Movie_Collect.query.filter(Movie_Collect.user_id == user.id).all()
        coll_movies = []
        for c in collections:
            m1 = Movie.query.filter(Movie.id == c.movie_id).first()
            coll_movies.append(m1)

        return render_template('more_collection.html', user=user, collections=coll_movies, type='collection')

    else:
        return redirect(url_for('login'))


@app.route('/personal_page/more_like', methods=['GET'])
def more_like():
    if islogined():
        user = User.query.filter(User.id == session.get('id')).first()

        likes = Movie_Like.query.filter(Movie_Like.user_id == user.id).all()
        li_movies = []
        # 需要电影名称和icon
        for l in likes:
            m2 = Movie.query.filter(l.movie_id == Movie.id).first()
            li_movies.append(m2)

        return render_template('more_collection.html', user=user, likes=li_movies, type='like')

    else:
        return redirect(url_for('login'))


# other person's personal page
@app.route('/personal_page/<int:id>', methods=['GET', 'POST'])
def other_person(id):
    user = User.query.filter(User.id == id).first()
    current_user = session.get('id')
    exist = Friends.query.filter(Friends.user_id == current_user, Friends.friend_id == id).first()
    if exist == None:
        relationship = False
    else:
        relationship = True

    # 个人页面最近点赞
    li = Movie_Like.query.filter(Movie_Like.user_id == user.id).order_by(-Movie_Like.id).all()
    reli = li[:5]
    recent_likes = []
    # 需要电影名称和icon
    for l in reli:
        m = Movie.query.filter(l.movie_id == Movie.id).first()
        recent_likes.append(m)

    # 个人兴趣百分比
    comedy_num = 0
    action_num = 0
    love_num = 0
    cartoon_num = 0
    science_num = 0
    suspense_num = 0
    war_num = 0
    thriller_num = 0
    total = 0
    for per in li:
        m = Movie.query.filter(Movie.id == per.movie_id).first()
        total += 1
        if m.comedy:
            comedy_num += 1
        if m.action:
            action_num += 1
        if m.love:
            love_num += 1
        if m.cartoon:
            cartoon_num += 1
        if m.science:
            science_num += 1
        if m.suspense:
            suspense_num += 1
        if m.war:
            war_num += 1
        if m.thriller:
            thriller_num += 1
    if total == 0:
        total = 1
    comedy_num = int(round(comedy_num / total, 2) * 100)
    action_num = int(round(action_num / total, 2) * 100)
    love_num = int(round(love_num / total, 2) * 100)
    cartoon_num = int(round(cartoon_num / total, 2) * 100)
    science_num = int(round(science_num / total, 2) * 100)
    suspense_num = int(round(suspense_num / total, 2) * 100)
    war_num = int(round(war_num / total, 2) * 100)
    thriller_num = int(round(thriller_num / total, 2) * 100)

    # 个人页面收藏
    coll = Movie_Collect.query.filter(Movie_Collect.user_id == user.id).order_by(-Movie_Collect.id).all()
    collect_num = len(coll)
    recoll = coll[:5]
    recent_coll = []
    # 需要电影名称和icon
    for c in recoll:
        n = Movie.query.filter(Movie.id == c.movie_id).first()
        recent_coll.append(n)

    # 高赞评论
    comments = Comment.query.filter(Comment.user_id == user.id).order_by(Comment.like_num.desc()).all()
    re_comm = comments[:6]
    high_comm = []
    for com in re_comm:
        pack = []
        movie = Movie.query.filter(Movie.id == com.movie_id).first()
        pack.append(com)
        pack.append(movie)
        high_comm.append(pack)
    print(high_comm)
    com_num = len(high_comm)

    comments = Comment.query.filter(Comment.user_id == user.id).all()
    comment_num = len(comments)

    friends = Friends.query.filter(Friends.user_id == user.id).all()
    friend_num = len(friends)
    return render_template('personal-information.html', user=user, like_history=recent_likes, collections=recent_coll,
                           collect_num=collect_num, comment_num=comment_num, friend_num=friend_num, total=total,
                           comedy_num=comedy_num, action_num=action_num, love_num=love_num, cartoon_num=cartoon_num,
                           science_num=science_num, suspense_num=suspense_num, war_num=war_num,
                           thriller_num=thriller_num, high_like_comments=high_comm, com_num=com_num,
                           relationship=relationship)


# show friends
@app.route('/personal_page/friends', methods=['GET', 'POST'])
def friends():
    if islogined():
        # friends
        friends = Friends.query.filter(Friends.user_id == session.get('id')).all()
        friend_list = []
        for f in friends:
            friend = User.query.filter(User.id == f.friend_id).first()
            friend_list.append(friend)


        # applications
        applications = Friend_Application.query.filter(Friend_Application.receiver == session.get('id')).all()
        application_dic = {}
        senders_dic = {}
        if applications != []:
            status = "Y"
            for a in applications:
                application_dic[a.sender] = a.reason
                sender = User.query.filter(User.id == a.sender).first()
                senders_dic[a.sender] = sender
        else:
            status = "N"
        return render_template('friendlist.html', friends=friend_list, reasons=application_dic, senders=senders_dic,
                               status=status)
    else:
        return redirect(url_for('login'))


# add friends
@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    if islogined():
        if request.method == 'POST':
            request_user_id = request.form["userId"]
            reason = request.form["reason"]
            exist = Friend_Application.query.filter(Friend_Application.sender == session.get('id'),
                                                    Friend_Application.receiver == request_user_id).first()
            if exist == None:
                print(request_user_id)
                print(reason)
                application = Friend_Application(sender=session.get('id'), receiver=request_user_id, reason=reason)
                db.session.add(application)
                db.session.commit()
            if session.get("recommend_friend") == "collaborative_filtering":
                return redirect(url_for('recommend_friends2'))
            else:
                return redirect(url_for('recommend_friends'))
    else:
        return redirect(url_for('login'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    feedback = request.get_json()
    advise = Advise(user_id=session.get('id'), title=feedback['feedbackTitle'], text=feedback['feedback'])
    db.session.add(advise)
    db.session.commit()
    return 'feedback successfully!'

@app.route('/feedbackList', methods=['GET', 'POST'])
def feedbackList():
    page = request.args.get('page', 1, type=int)
    advise = Advise.query.paginate(page, per_page=12, error_out=False)
    if request.method == 'POST':
        advise_result = request.form.get("search_result")
        advise_searches = Advise.query.filter(Advise.title.like("%" + advise_result + "%"),
                                            User.authority == 0).paginate(
            page, per_page=8,
            error_out=False)
        if Advise.query.filter(Advise.title.like("%" + advise_result + "%")).all() == []:
            advise_searches = "0"
        return render_template('feedbackList.html', advise=advise, advise_searches=advise_searches)
    return render_template('feedbackList.html', advise=advise, advise_searches="1")


@app.route('/personal_page/friend_applications/accept/<int:id>', methods=['GET', 'POST'])
def friend_accept(id):
    if islogined():
        current_user = session.get('id')
        exist = Friends.query.filter(Friends.user_id == current_user, Friends.friend_id == id).first()
        print(exist)
        if exist == None:
            friend1 = Friends(user_id=current_user, friend_id=id)
            friend2 = Friends(user_id=id, friend_id=current_user)
            db.session.add(friend1)
            db.session.add(friend2)
            if current_user > id:
                room = str(id) + "*" + str(current_user)
                room1 = Room(room=room, receiver=current_user, sender=id)
                room2 = Room(room=room, receiver=id, sender=current_user)
            else:
                room = str(current_user) + "*" + str(id)
                room1 = Room(room=room, receiver=current_user, sender=id)
                room2 = Room(room=room, receiver=id, sender=current_user)
            db.session.add(room1)
            db.session.add(room2)
            db.session.commit()
            print(id)
            application = Friend_Application.query.filter(Friend_Application.sender == id,
                                                          Friend_Application.receiver == session.get('id')).first()
            print(application)
            db.session.delete(application)
            db.session.commit()
        return redirect(url_for('friends'))
    else:
        return redirect(url_for('login'))


@app.route('/personal_page/friend_applications/refuse/<int:id>', methods=['GET', 'POST'])
def friend_refuse(id):
    if islogined():
        current_user = session.get('id')
        exist = Friend_Application.query.filter(Friend_Application.receiver == current_user, Friend_Application.sender == id).first()
        if exist is not None:
            db.session.delete(exist)
            db.session.commit()
        return redirect(url_for('friends'))
    else:
        return redirect(url_for('login'))


@app.route('/personal_page/friend_delete/<int:id>', methods=['GET', 'POST'])
def friend_delete(id):
    if islogined():
        current_user = session.get('id')
        exist = Friends.query.filter(Friends.user_id == current_user, Friends.friend_id == id).first()
        if exist is not None:
            room_info = Room.query.filter(Room.receiver == current_user, Room.sender == id).first()
            room = room_info.room

            message = Mess.query.filter(Mess.room == room).first()
            print(message)
            if message is not None:
                messages = Mess.query.filter(Mess.room == room).all()
                for m in messages:
                    db.session.delete(m)
                db.session.commit()

            rooms = Room.query.filter(Room.room == room).all()
            for r in rooms:
                db.session.delete(r)
            db.session.commit()

            friend1 = Friends.query.filter(Friends.user_id == current_user, Friends.friend_id == id).first()
            friend2 = Friends.query.filter(Friends.user_id == id, Friends.friend_id == current_user).first()
            db.session.delete(friend1)
            db.session.delete(friend2)
            db.session.commit()
        return redirect(url_for('friends'))
    else:
        return redirect(url_for('login'))


# Online Chat
@app.route('/chat_list')
def chat_list():
    if islogined():
        user_id = session.get('id')
        friends_id = []
        friends_info = []
        # friends = Friends.query.filter_by(user_id=user_id).all()
        # for friend in friends:
        #     if user_id < friend.friend_id:
        #         room_id.append(str(user_id) + "*" + str(friend.friend_id))
        #     else:
        #         room_id.append(str(friend.friend_id) + "*" + str(user_id))
        rooms = Room.query.filter(or_(Room.receiver == user_id, Room.sender == user_id)).order_by(
            Room.change_time.desc()).all()
        for r in rooms:
            if r.receiver == user_id:
                friends_id.append([r.sender, r.unread, r.room])

        for f in friends_id:
            user_info = User.query.filter(User.id == f[0]).first()
            user_info.unread = f[1]
            user_info.room = f[2]
            room_2 = Room.query.filter(Room.sender == f[0], Room.receiver == user_id).first()
            user_info.unread = room_2.unread
            friends_info.append(user_info)

        return render_template('chatlist.html', friends_info=friends_info)

    else:
        return redirect(url_for('login'))


# contact
@app.route('/api/contact', methods=['GET', 'POST'])
def contact():
    room = request.get_json()
    print(11111111111111111111111, room)
    user_id = session.get('id')
    a = []
    room_id = room['room_id']
    session['room'] = room_id
    print(11111111111111111, session['room'])
    a = room_id.split('*')
    user_id_string = str(user_id)
    if user_id_string in a:
        a.remove(user_id_string)
    friend_id = a[0]
    user = User.query.filter_by(id=user_id).first()
    friend = User.query.filter_by(id=friend_id).first()
    room = Room.query.filter(Room.receiver == user.id).first()
    room.unread = 0
    message = Mess.query.filter(Mess.room == room_id).all()
    messages = []
    for i in message:
        message_dic = {}
        message_dic['author'] = i.author_id
        message_dic['content'] = i.content
        messages.append(message_dic)
    # return render_template('contact.html', self=user, contact_user=friend, message=message)

    room_unread = Room.query.filter(Room.receiver == user_id, Room.room == room_id).first()
    room_unread.unread = 0
    db.session.commit()

    return jsonify(
        {'self': user.id, 'self_name': user.user_name, 'contact_username': friend.user_name, 'contact_user': friend.id,
         'self_icon': user.icon,
         'contact_user_icon': friend.icon, 'message': messages})


@socketio.on('send msg')
def handle_message(data):
    print('sendMsg' + str(data))
    room_id = data.get('room')
    print(room_id)
    message = Mess(author_id=session['id'], room=room_id, content=data.get('message'))
    db.session.add(message)
    room = Room.query.filter_by(room=room_id, sender=session['id']).first()
    room.unread = room.unread + 1
    room.change_time = datetime.now()
    db.session.commit()
    data['message'] = data.get('message').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
    socketio.emit('send msg', data, to=room_id)


@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    join_room(room)
    socketio.emit('connect info', username + ' join room', to=room)


@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    socketio.emit('connect info', username + ' leave room', to=room)


# person avatar
# @app.route('/pic1_session_add')
# def add_pic1():
#     session['commodity_pic'] = 1
#     return redirect(url_for('upload'))
#
#
# @app.route('/pic2_session_add')
# def add_pic2():
#     session['commodity_pic'] = 2
#     return redirect(url_for('upload'))
#
#
# @app.route('/pic3_session_add')
# def add_pic3():
#     session['commodity_pic'] = 3
#     return redirect(url_for('upload'))

# upload icon
@app.route('/change-avatar/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        # raw_filename = avatars.save_avatar(f)
        path = current_app.config['AVATARS_SAVE_PATH']
        filename = session['username'] + '_raw.png'
        f.save(os.path.join(path, filename))
        session['u_filename'] = filename
        print(filename)
        # u = session['username']
        # user = User.query.filter(User.user_name == u).first()
        # user.icon = "../static/avatars/" + session['u_filename']
        # db.session.commit()
        return redirect("/change-avatar/crop/")
    return render_template('upload.html')


# crop icon
@app.route('/change-avatar/crop/', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        user = User.query.filter(User.id == session["id"]).first()
        filenames = avatars.crop_avatar(session['u_filename'], x, y, w, h)
        save_path = current_app.config['ICON_SAVE_PATH']
        filename = session['username'] + '_crop.png'
        url_s = filenames[0]
        url_m = filenames[1]
        url_l = filenames[2]
        path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], url_l)
        img = Image.open(path)
        img.save(os.path.join(save_path, filename))
        user.icon = "../static/avatars/" + filename
        db.session.commit()
        session.pop('u_filename', None)
        flash('Upload picture successfully', 'success')
        return redirect("/personal_page")
    # app.config.setdefault('AVATARS_CROP_BASE_WIDTH', 500)
    return render_template('crop_avatar.html')


"""movie detail part
"""


# single movie page
@app.route('/movie/<int:id>', methods=['GET', 'POST'])
# id 为 movie id， 通过电影id调取数据库中电影信息
def single_movie(id):
    # 通过电影id查询电影信息
    m = Movie.query.filter(Movie.id == id).first()
    grade_average = m.vote_average
    # sql = 'select * from movie'
    # a = id.toString
    # m = sql.query.get(a)
    # 电影在数据库中没查到
    # if m == None:
    #     print('Can not find this movie in database')
    #     return render_template("single-page-with-img.html", msg='Can not find this movie in database')
    # 电影确实在数据库中
    # else:
    #     print('Successful on finding this movie')
    # 检测是否被管理员下架
    # if m.is_delete == 0:
    print(m.movie_name)
    time = m.release_time.strftime("%Y-%m-%d")
    print(time)
    movie_message = str(' movie name is: ' + m.movie_name + ',' +
                        ' release time is: ' + time + ',' +
                        ' pic path is: ' + m.pic_path + ',' +
                        ' introduction is: ' + m.introduction + ',' +
                        # ' label is ' + m.label + ',' +
                        ' popular is: ' + str(m.popular) + ',' +
                        ' Vote_average' + str(m.vote_average) + ',' +
                        ' Vote_count' + str(m.vote_count))
    print(movie_message)

    if islogined():
        # 检测用户是否已经喜欢该电影
        # isCollected = False
        # isLiked = False
        userID = session.get('id')
        user = User.query.filter_by(id=userID).first()
        name = user.user_name
        print(userID)
        # userID = int(1)
        l = Movie_Like.query.filter(Movie_Like.user_id == userID, Movie_Like.movie_id == id).first()
        if l == None:
            isLiked = False
        else:
            isLiked = True
        print(isLiked)
        # 检测用户是否被封号
        isBanned = user_ban = User.query.filter(User.id == userID).first().ban
        # 检测用户是否已经收藏该电影
        L = Movie_Collect.query.filter(Movie_Collect.user_id == userID, Movie_Collect.movie_id == id).first()
        if L == None:
            isCollected = False
        else:
            isCollected = True
        print(isCollected, "377")

        authority = session.get('authority')

        movie_grade = Movie_Grade.query.filter(Movie_Grade.user_id == userID, Movie_Grade.movie_id == id).first()
        if movie_grade is None:
            grade = 0
        else:
            grade = movie_grade.grade

    else:
        authority = None
        isCollected = False
        grade = 0
        isLiked = False
        isBanned = False
        user = None
        name = None

    # 获取comment列表，向前端发送
    comments = Comment.query.filter(Comment.movie_id == id)

    # 需要信息：user_name,icon，title, text, time, likes
    commentlist = []
    for comment in comments:
        comment_dic = {}
        comment_time = comment.creat_time.strftime("%Y-%m-%d %H:%M:%S")
        # 找到user id，查找username，icon
        user1 = User.query.filter(User.id == comment.user_id).first()

        comment_dic['id'] = comment.id
        comment_dic['username'] = user1.user_name
        comment_dic['user_icon'] = user1.icon
        comment_dic['comment.title'] = comment.title
        comment_dic['text'] = comment.text
        comment_dic['time'] = comment_time
        comment_dic['likes'] = str(comment.like_num)
        if islogined():
            comment_like = Comment_Like.query.filter(Comment_Like.user_id == userID,
                                                     Comment_Like.comment_id == comment.id).first()
            if comment_like is not None:
                comment_dic['is_like'] = True
            else:
                comment_dic['is_like'] = False
        else:
            comment_dic['is_like'] = False

        movie_grade_2 = Movie_Grade.query.filter_by(user_id=comment.user_id, movie_id=comment.movie_id).first()
        if movie_grade_2 is not None:
            comment_dic['grade'] = movie_grade_2.grade
        else:
            comment_dic['grade'] = 0

        commentlist.append(comment_dic)

    return render_template("movie-detail.html", authority=authority, islogin=islogined(), movie=m, comments=comments,
                           commentlist=commentlist,
                           movie_labels=movie_labels, movie_label_value=movie_labels.values(),
                           isCollected=isCollected, isLiked=isLiked, isBanned=isBanned, grade=grade, grade2=grade / 2,
                           grade_average=grade_average, user=user, name=name)


# 介绍页面
@app.route('/about')
def about():
    authority = None
    user = None
    name = None
    if islogined():
        userID = session.get('id')
        authority = session.get('authority')
        user = User.query.filter_by(id=userID).first()
        name = user.user_name
    return render_template("about.html", authority=authority, islogin=islogined(), user=user, name=name,
                           movie_labels=movie_labels,
                           movie_label_value=movie_labels.values())
# 原来存在，后被管理员删除
# else:

#     print('But this movie was now deleted by manager. ')
#     return render_template("single-page-with-img.html", msg='this movie was now deleted by manager')

# 检查是否登录
@app.route('/isLogin', methods=['GET'])
def checkLogin():
    if request.method == 'GET':
        return jsonify({'isLogined': islogined()})
    return 1


# 判断是否喜欢
@app.route('/isliked', methods=['GET', 'POST'])
def check_like():
    if request.method == 'POST':
        if islogined():
            isLiked = request.get_json()
            movie_id = isLiked['movie_id']
            like_status = isLiked['like']
            user_id = session.get("id")
            if like_status == 1:
                movie_like = Movie_Like(user_id=user_id, movie_id=movie_id)
                db.session.add(movie_like)
                db.session.commit()
                return 'Like successfully!'
            else:
                movie_like = Movie_Like.query.filter_by(user_id=user_id, movie_id=movie_id).first()
                db.session.delete(movie_like)
                db.session.commit()
                return 'Cancel like successfully!'


@app.route('/isCollected', methods=['GET', 'POST'])
def check_collect():
    if request.method == 'POST':
        if islogined():
            isCollected = request.get_json()
            movie_id = isCollected['movie_id']
            collect_status = isCollected['collected']
            user_id = session.get("id")
            if collect_status == 1:
                movie_collect = Movie_Collect(user_id=user_id, movie_id=movie_id)
                db.session.add(movie_collect)
                db.session.commit()

                return 'Collect successfully!'
            else:
                movie_collect = Movie_Collect.query.filter_by(user_id=user_id, movie_id=movie_id).first()
                db.session.delete(movie_collect)
                db.session.commit()
                return 'Cancel collect successfully!'


# 发送评论 sent comment
@app.route('/movie/sent_comment', methods=['GET', 'POST'])
def sent_comment():
    if request.method == 'POST':
        commentData = request.get_json()
        print("comment:", commentData)
        if islogined():

            cmt = Comment(user_id=session.get("id"), movie_id=commentData["movie_id"],
                          title=commentData["commentTitle"],
                          text=commentData["comment"],
                          like_num=0)
            db.session.add(cmt)
            db.session.commit()
            print(cmt)
            return jsonify({'returnValue': 1})
        else:
            return jsonify({'returnValue': 0})


# 管理员删除电影界面
@app.route('/movie/delete_movie/<int:mid>', methods=['GET', 'POST'])
def deleteMovie(mid):
    user_id = session.get('id')
    movie_id = mid
    # movie_id = session.get('mid')
    user = User.query.filter_by(id=user_id).first()
    if user.authority == 1:
        movie = Movie.query.filter_by(id=movie_id).first()
        db.session.delete(movie)
        db.session.commit()
        # return "successful delete!"
        return redirect(url_for('home'))
    else:
        return "permission denied, Only the manager can delete a movie"


# 管理员在管理员页面删除电影界面
@app.route('/movie/delete_movie_alt/<int:mid>', methods=['GET', 'POST'])
def deleteMovie_alt(mid):
    user_id = session.get('id')
    movie_id = mid
    # movie_id = session.get('mid')
    user = User.query.filter_by(id=user_id).first()
    if user.authority == 1:
        movie = Movie.query.filter_by(id=movie_id).first()
        db.session.delete(movie)
        db.session.commit()
        # return "successful delete!"
        return redirect(url_for('delete_movie_page'))
    else:
        return "permission denied, Only the manager can delete a movie"


# 删除评论
@app.route('/movie/delete_comment/<int:cid>', methods=['GET', 'POST'])
def delete_comment(cid):
    user_id = session.get('id')
    user = User.query.filter_by(id=user_id).first()
    comment = Comment.query.filter_by(id=cid).first()
    comment_like = Comment_Like.query.filter_by(comment_id=cid).first()
    movie_id = comment.movie_id
    if user.authority == 1 or user.id == comment.user_id:
        db.session.delete(comment_like)
        db.session.delete(comment)
        db.session.commit()
        # return "successful delete!"
        return redirect(url_for('single_movie', id=movie_id))
    else:
        return "permission denied, Only the manager and sender can delete a comment"


# # 评论点赞
@app.route('/like_comment', methods=['GET', 'POST'])
def collect_comment():
    collect_comments = request.get_json()
    comment_id = collect_comments['comment_id']
    user_id = session.get('id')

    comment = Comment.query.filter_by(id=comment_id).first()
    if collect_comments['like']:
        comment.like_num = comment.like_num + 1
        comment_like = Comment_Like(user_id=user_id, comment_id=comment_id)
        db.session.add(comment_like)
        db.session.commit()
        return 'Like succeeded !'
    else:
        comment.like_num = comment.like_num - 1
        comment_like = Comment_Like.query.filter_by(user_id=user_id, comment_id=comment_id).first()
        db.session.delete(comment_like)
        db.session.commit()
        return 'Cancel like succeeded !'


# 管理员ban用户界面,搜索用户
@app.route('/administrator_ban', methods=['GET', 'POST'])
def administrator_ban():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.authority != 1).paginate(page, per_page=12, error_out=False)
    if request.method == 'POST':
        search_result = request.form.get("search_result")
        user_searches = User.query.filter(User.user_name.like("%" + search_result + "%"), User.authority == 0).paginate(
            page, per_page=8,
            error_out=False)
        if User.query.filter(User.user_name.like("%" + search_result + "%"), User.authority == 0).all() == []:
            user_searches = "0"
        return render_template('administrator-ban-user.html', users=users, user_searches=user_searches)

    return render_template('administrator-ban-user.html', users=users, user_searches="1")


# delete movie page
@app.route('/delete_movie_page', methods=['GET', 'POST'])
def delete_movie_page():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page, per_page=12, error_out=False)
    if request.method == 'POST':
        movie_result = request.form.get("search_result")
        movie_searches = Movie.query.filter(Movie.movie_name.like("%" + movie_result + "%"),
                                            User.authority == 0).paginate(
            page, per_page=8,
            error_out=False)
        if Movie.query.filter(Movie.movie_name.like("%" + movie_result + "%")).all() == []:
            movie_searches = "0"
        return render_template('delete-movie-page.html', movies=movies, movie_searches=movie_searches)
    return render_template('delete-movie-page.html', movies=movies, movie_searches="1")


# 管理员页面
@app.route('/administrator', methods=['GET', 'POST'])
def administrator():
    return render_template('administrator.html')


#
#
# 管理员禁用用户
@app.route('/ban', methods=['GET', 'POST'])
def ban():
    user_ban_get = request.get_json()
    user_ben_get_id = user_ban_get["id"]
    user_ban = User.query.filter(User.id == user_ben_get_id).first()
    if user_ban.ban == 0:
        user_ban.ban = 1
    else:
        user_ban.ban = 0
    db.session.commit()
    return "1"


# 打分
@app.route('/movie/sent_rate', methods=['GET', 'POST'])
def sent_rate():
    rate_information = request.get_json()
    movie_id = rate_information['movie_id']
    rate = rate_information['rate']
    user_id = session.get('id')
    movie_grade = Movie_Grade.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie_grade is not None:
        movie.vote_average = (movie.vote_average * movie.vote_count - movie_grade.grade + rate) / movie.vote_count
        db.session.delete(movie_grade)
        movie_rate = Movie_Grade(user_id=user_id, movie_id=movie_id, grade=rate)
        db.session.add(movie_rate)
        db.session.commit()
        return 'Grade changed !'
    else:
        movie_rate = Movie_Grade(user_id=user_id, movie_id=movie_id, grade=rate)
        db.session.add(movie_rate)
        if movie.vote_count == 0:
            movie.vote_count += 1
            movie.vote_average = rate
        else:
            movie.vote_average = (movie.vote_average * movie.vote_count + rate) / (movie.vote_count + 1)
            movie.vote_count += 1

        db.session.commit()
        return 'Grade successfully !'


# comment id
# user id

# movie upload
@app.route('/movie/upload', methods=['GET', 'POST'])
def movie_upload():
    # if session.get('authority') == 1:
    if request.method == 'GET':
        return render_template('post.html')
    else:
        session.pop('u_movie_name', None)
        session.pop('u_release_time', None)
        session.pop('u_introduction', None)
        session.pop('u_comedy', None)
        session.pop('u_action', None)
        session.pop('u_love', None)
        session.pop('u_cartoon', None)
        session.pop('u_science', None)
        session.pop('u_suspense', None)
        session.pop('u_war', None)
        session.pop('u_thriller', None)
        session.pop('u_popular', None)
        print(request.form)
        session['u_movie_name'] = request.form['movie_name']
        session['u_release_time'] = request.form['time']
        session['u_introduction'] = request.form['intro']
        session['u_popular'] = request.form['popular']
        print('start')
        if 'comedy' in request.form:
            session['u_comedy'] = True
            print(session['u_comedy'])
        else:
            session['u_comedy'] = False
        if 'action' in request.form:
            session['u_action'] = True
            print(session['u_action'])
        else:
            session['u_action'] = False
        if 'love' in request.form:
            session['u_love'] = True
            print(session['u_love'])
        else:
            session['u_love'] = False
        if 'cartoon' in request.form:
            session['u_cartoon'] = True
            print(session['u_cartoon'])
        else:
            session['u_cartoon'] = False
        if 'science' in request.form:
            session['u_science'] = True
            print(session['u_science'])
        else:
            session['u_science'] = False
        if 'suspense' in request.form:
            session['u_suspense'] = True
            print(session['u_suspense'])
        else:
            session['u_suspense'] = False
        if 'war' in request.form:
            session['u_war'] = True
            print(session['u_war'])
        else:
            session['u_war'] = False
        if 'thriller' in request.form:
            session['u_thriller'] = True
            print(session['u_thriller'])
        else:
            session['u_thriller'] = False
        return redirect(url_for('upload_movie'))


# else:
#     return redirect(url_for('/'))

# config of avatar
@app.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


# upload movie
@app.route('/movie/upload/pic', methods=['GET', 'POST'])
def upload_movie():
    if request.method == 'POST':
        f = request.files.get('file')
        # raw_filename = avatars.save_avatar(f)
        path = current_app.config['AVATARS_SAVE_PATH']
        filename = session['u_movie_name'] + '_raw.png'
        f.save(os.path.join(path, filename))
        session['m_filename'] = filename
        print(filename)
        return redirect("/movie/upload/pic/crop/")
    return render_template('upload.html')


# crop movie
@app.route('/movie/upload/pic/crop/', methods=['GET', 'POST'])
def crop_movie():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        print(x, y, w, h)
        filenames = avatars.crop_avatar(session['m_filename'], x, y, str(round(int(w) * 9 / 14)), h)
        save_path = current_app.config['MOVIE_SAVE_PATH']
        filename = session['u_movie_name'] + '_crop.png'
        url_s = filenames[0]
        url_m = filenames[1]
        url_l = filenames[2]
        path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], url_l)
        img = Image.open(path)
        img.save(os.path.join(save_path, filename))

        movie_path = "../static/stage photo/" + filename
        dt = datetime.strptime(session.get('u_release_time'), '%Y-%m-%d')
        movie = Movie(movie_name=session.get('u_movie_name'), release_time=dt, pic_path=movie_path,
                      introduction=session.get('u_introduction'), popular=session.get('u_popular'),
                      comedy=session.get('u_comedy'), action=session.get('u_action'), love=session.get('u_love'),
                      cartoon=session.get('u_cartoon'), science=session.get('u_science'),
                      suspense=session.get('u_suspense'),
                      war=session.get('u_war'), thriller=session.get('u_thriller'))
        db.session.add(movie)
        db.session.commit()
        session.pop('m_filename', None)
        session.pop('u_movie_name', None)
        session.pop('u_release_time', None)
        session.pop('u_introduction', None)
        session.pop('u_comedy', None)
        session.pop('u_action', None)
        session.pop('u_love', None)
        session.pop('u_cartoon', None)
        session.pop('u_science', None)
        session.pop('u_suspense', None)
        session.pop('u_war', None)
        session.pop('u_thriller', None)
        session.pop('u_popular', None)
        flash('Upload picture successfully', 'success')
        return redirect("/")
    # app.config.setdefault('AVATARS_CROP_BASE_WIDTH', 1500)
    return render_template('crop_movie.html')
    # myfunction=jcrop_js


"""reset IR data file
"""


@app.route('/reset_ir')
def reset_ir():
    if os.path.exists('app/IRdata/param.pkl1'):
        os.remove('app/IRdata/param.pkl1')
    if os.path.exists('app/IRdata/param.pkl2'):
        os.remove('app/IRdata/param.pkl2')

    stop_word = []  # 空的
    with open('app/IRdata/stop_words.txt', encoding='utf-8') as f:
        content = f.read()
        print('-----------------------------------')
        stop_word = content.split('\n')
        print(stop_word)

    # 读取movie数据库到movies.txt
    with open('app/IRdata/movies.txt', 'w', encoding='utf_8') as movie_intro:
        stemmer = PorterStemmer()
        movies = Movie.query.all()
        movies_text = ''

        for movie in movies:
            movie_text = movie.movie_name.lower() + ' ' + movie.introduction.lower() + ' ' + movie.movie_name.lower()
            words = movie_text.split(' ')
            for i in range(len(words)):
                w = words[i]
                if w not in stop_word:
                    word = stemmer.stem(words[i])
                    words[i] = word
                text = ''
                for wo in words:
                    text += ' ' + wo
                movie_text = str(movie.id) + text + '\n'
            movies_text += movie_text
        movie_intro.write(movies_text)

    # 读取user数据库到users.txt
    with open('app/IRdata/users.txt', 'w', encoding='utf_8') as user_id_name:
        users = User.query.all()
        user_text = ''
        for user in users:
            if user.user_name != 'admin':
                user_text += str(user.id) + ' ' + user.user_name + ' ' + str(user.id) + '\n'
        user_id_name.write(user_text)

    return redirect('/')


"""reset the database
"""


@app.route('/reset_db')
def reset_db():
    set_db()
    return redirect('/')

# @staticmethod
# def jcrop_js(js_url=None, with_jquery=True):
#     """Load jcrop Javascript file.
#
#     :param js_url: The custom JavaScript URL.
#     :param with_jquery: Include jQuery or not, default to ``True``.
#     """
#     serve_local = current_app.config['AVATARS_SERVE_LOCAL']
#
#     if js_url is None:
#         if serve_local:
#             js_url = url_for('static', filename='js/jquery.Jcrop.min.js')
#         else:
#             js_url = 'https://cdn.jsdelivr.net/npm/jcrop-0.9.12@0.9.12/js/jquery.Jcrop.min.js'
#
#     if with_jquery:
#         if serve_local:
#             jquery = '<script src="%s"></script>' % url_for('avatars.static', filename='jcrop/js/jquery.min.js')
#         else:
#             jquery = '<script src="https://cdn.jsdelivr.net/npm/jcrop-0.9.12@0.9.12/js/jquery.min.js"></script>'
#     else:
#         jquery = ''
#     return Markup('''%s\n<script src="%s"></script>
#     ''' % (jquery, js_url))
