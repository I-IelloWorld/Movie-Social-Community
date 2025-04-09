from app.models import *
from flask import session, Flask


# This function is use to reset the database into initialized
def set_db():
    db.drop_all()
    db.create_all()
    from app.models import User, Comment, Comment_Like, Movie, Movie_stage, Advise, Movie_Like, \
        Movie_Grade
    # Users
    admin = User(user_name='admin', email='admin123@gmail.com', authority=1, gender=1, comedy=0, action=1, love=0,
                 cartoon=0, science=0, suspense=0, war=0, thriller=1)
    admin.set_password('12345678')
    db.session.add(admin)

    user1 = User(user_name='user1', email='user1_123@gmail.com', gender=1, comedy=1, action=1, love=1,
                 cartoon=0, science=1, suspense=0, war=0, thriller=1)
    user1.set_password('12345678')
    db.session.add(user1)

    user2 = User(user_name='ctscts', email='2328267854@qq.com', gender=0, comedy=0, action=0, love=0,
                 cartoon=0, science=1, suspense=0, war=1, thriller=1)
    user2.set_password('Cts20010814')
    db.session.add(user2)

    user3 = User(user_name='wtjwtj', email='1342187631@qq.com', gender=0, comedy=1, action=1, love=0,
                 cartoon=0, science=1, suspense=0, war=1, thriller=1)
    user3.set_password('Wtj20010322')
    db.session.add(user3)

    user4 = User(user_name='user3', email='user3_123@qq.com', gender=0, comedy=1, action=1, love=1,
                 cartoon=0, science=1, suspense=0, war=0, thriller=0)
    user4.set_password('12345678')
    db.session.add(user4)

    user5 = User(user_name='user5', email='user5_123@qq.com', gender=0, comedy=1, action=1, love=0,
                 cartoon=0, science=1, suspense=0, war=1, thriller=1)
    user5.set_password('12345678')
    db.session.add(user5)

    user6 = User(user_name='user6', email='user6_123@qq.com', gender=1, comedy=0, action=1, love=0,
                 cartoon=1, science=1, suspense=1, war=0, thriller=1)
    user6.set_password('12345678')
    db.session.add(user6)

    user7 = User(user_name='user7', email='user7_123@qq.com', gender=1, comedy=1, action=1, love=0,
                 cartoon=0, science=1, suspense=0, war=1, thriller=1)
    user7.set_password('12345678')
    db.session.add(user7)

    user8 = User(user_name='user8', email='user8_123@qq.com', gender=0, comedy=0, action=1, love=0,
                 cartoon=1, science=0, suspense=1, war=0, thriller=0)
    user8.set_password('12345678')
    db.session.add(user8)

    user9 = User(user_name='user9', email='user9_123@qq.com', gender=1, comedy=1, action=0, love=0,
                 cartoon=0, science=1, suspense=1, war=0, thriller=1)
    user9.set_password('12345678')
    db.session.add(user9)

    user10 = User(user_name='user10', email='user10_123@qq.com', gender=1, comedy=1, action=0, love=0,
                  cartoon=1, science=1, suspense=0, war=1, thriller=1)
    user10.set_password('12345678')
    db.session.add(user10)

    # relationship
    friend1 = Friends(user_id=2, friend_id=3)
    friend2 = Friends(user_id=3, friend_id=2)
    db.session.add(friend1)
    db.session.add(friend2)

    # room
    room1 = Room(room='2*3', receiver=2, sender=3)
    room2 = Room(room='2*3', receiver=3, sender=2)
    db.session.add(room1)
    db.session.add(room2)

    # Movies
    # Movies
    movie1 = Movie(movie_name='Your name', popular='1369463', is_delete=0, comedy=0, action=0, love=1, cartoon=1,
                   science=0, release_time=datetime.strptime('2016-12-02', '%Y-%m-%d'),
                   introduction="They experience each other's life from the perspective of the other, with anger, "
                                "laughter, and heartwarming during this period. It's just that the two people don't "
                                "know that there are significant and insidious secrets hidden behind the identity "
                                "exchange.", vote_average=4.5, vote_count=2,
                   suspense=0, war=0, thriller=0,
                   pic_path='../static/stage photo/Your name.jpg')
    db.session.add(movie1)

    movie2 = Movie(movie_name='John Wick', popular='188765', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                   science=0, release_time=datetime.strptime('2014-10-24', '%Y-%m-%d'),
                   introduction="Extremely angry, John refused Tarasov's mediation and decided to take revenge alone."
                   , vote_average=5, vote_count=2,
                   suspense=1, war=0, thriller=1,
                   pic_path='../static/stage photo/John Wick.jpg')
    db.session.add(movie2)

    movie3 = Movie(movie_name='Transformers', popular='473955', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                   science=0, release_time=datetime.strptime('2007-07-11', '%Y-%m-%d'),
                   introduction="The advance forces of the Decepticons, Cyclones and Scorpions, attacked the US "
                                "military base in Qatar, and Optimus Prime arrived with other Autobots, "
                                "marking the beginning of a robot battle.", vote_average=4.5, vote_count=2,
                   suspense=1, war=1, thriller=1, pic_path='../static/stage photo/Transformers.jpg')
    db.session.add(movie3)

    movie4 = Movie(movie_name='The twilight', popular='479532', is_delete=0, comedy=0, action=1, love=1, cartoon=0,
                   science=0, release_time=datetime.strptime('2009-11-25', '%Y-%m-%d'),
                   introduction='In the shackles of a homicide case, a love between people and ghosts unfolds.'
                   , vote_average=5, vote_count=3,
                   suspense=1, war=0, thriller=1, pic_path='../static/stage photo/The twilight.jpg')
    db.session.add(movie4)

    movie5 = Movie(movie_name='Gray man', popular='43981', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                   science=0, release_time=datetime.strptime('2022-07-15', '%Y-%m-%d'),
                   introduction="The storyteller, known as 'The Grey Man,' Kurt Gentley (Ryan Gosling) "
                                "serves the CIA under the code name 'Mountain Six'.", vote_average=3, vote_count=6,
                   suspense=1, war=0, thriller=0, pic_path='../static/stage photo/Gray man.png')
    db.session.add(movie5)

    movie6 = Movie(movie_name='The Shawshank Redemption', popular='2821479', is_delete=0, comedy=0, action=0, love=1,
                   cartoon=0,
                   science=0, release_time=datetime.strptime('1994-09-10', '%Y-%m-%d'),
                   introduction='Depressed Andy did not despair. On a stormy night with thunder and lightning, '
                                'a prison escape plan hidden for decades allowed him to redeem himself and regain his '
                                'freedom! With his encouragement and help, his old friend Red bravely rushed towards '
                                'freedom.', vote_average=0, vote_count=0,
                   suspense=1, war=0, thriller=0, pic_path='../static/stage photo/The Shawshank Redemption.jpg')
    db.session.add(movie6)

    movie7 = Movie(movie_name='The Karate Kid', popular='133718', is_delete=0, comedy=0, action=1, love=0,
                   cartoon=0, suspense=0, war=0, thriller=0,
                   science=0, release_time=datetime.strptime('2010-06-10', '%Y-%m-%d'),
                   introduction="This film is based on a remake of the 1984 Hollywood film of the same name.",
                   vote_average=0, vote_count=0,
                   pic_path='../static/stage photo/The Karate Kid.jpg')
    db.session.add(movie7)

    movie8 = Movie(movie_name='The Pursuit of Happyness', popular='1488540', is_delete=0, comedy=0, action=0, love=1,
                   cartoon=0, suspense=0, war=0, thriller=0,
                   science=0, release_time=datetime.strptime('2008-01-17', '%Y-%m-%d'),
                   introduction="He firmly believes that happiness will come tomorrow.",
                   vote_average=0, vote_count=0,
                   pic_path='../static/stage photo/The Pursuit of Happyness.png')
    db.session.add(movie8)

    movie9 = Movie(movie_name="Harry Potter and the Sorcerer's Stone", popular='1155233', is_delete=0, comedy=0,
                   action=1, love=0,
                   cartoon=0, suspense=1, war=0, thriller=1,
                   science=0, release_time=datetime.strptime('2002-01-26', '%Y-%m-%d'),
                   introduction="Harry Potter is an orphan who was raised in foster care at his aunt's house and was "
                                "subjected to bullying. But on Harry's 11th birthday, he accidentally received an "
                                "admission notice from Hogwarts College.",
                   vote_average=0, vote_count=0,
                   pic_path="../static/stage photo/Harry Potter and the Sorcerer's Stone.png")
    db.session.add(movie9)

    movie10 = Movie(movie_name="Avatar", popular='1391059', is_delete=0, comedy=0,
                    action=1, love=0,
                    cartoon=0, suspense=0, war=0, thriller=0,
                    science=1, release_time=datetime.strptime('2010-01-04', '%Y-%m-%d'),
                    introduction="Former Navy soldier Jack Sally (Sam Worthington), who was injured and paralyzed "
                                 "during the battle, decided to replace his dead sibling brother to Pandora and "
                                 "manipulate Dr. Grace (Sigourney Weaver) to create an 'Avatar' hybrid creature using "
                                 "human genes combined with the local Na'vi tribe genetics.",
                    vote_average=0, vote_count=0,
                    pic_path="../static/stage photo/Avatar.png")
    db.session.add(movie10)

    movie11 = Movie(movie_name='Venom', popular='3012242000', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                    science=1, suspense=0, war=0, thriller=1, release_time=datetime.strptime('2018-9-28', '%Y-%m-%d'),
                    introduction="In the Life Foundation lab, Eddie finds evidence that Drake was experimenting on humans and was accidentally possessed by the alien life form Venom.",
                    vote_average=3.3, vote_count=3,
                    pic_path='../static/stage photo/venom.png')
    db.session.add(movie11)

    movie12 = Movie(movie_name='Free Guy', popular='3012242000', is_delete=0, comedy=1, action=1, love=0, cartoon=0,
                    science=1, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2021-8-11', '%Y-%m-%d'),
                    introduction="Bank teller Guy (Ryan Reynolds) discovers he's actually a background character in an open-world video game and decides to become a hero and rewrite his own story. ",
                    vote_average=4.5, vote_count=2,
                    pic_path='../static/stage photo/free guy.png')
    db.session.add(movie12)

    movie13 = Movie(movie_name='Titanic', popular='2076956', is_delete=0, comedy=0, action=0, love=1, cartoon=0,
                    science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('1997-12-19', '%Y-%m-%d'),
                    introduction="Titanic faces the fate of shipwreck, Rose and Jack's budding love will also experience the test of life and death. ",
                    vote_average=3.5, vote_count=2,
                    pic_path='../static/stage photo/Titanic.png')
    db.session.add(movie13)

    movie14 = Movie(movie_name='Green Book', popular='16010700009', is_delete=0, comedy=1, action=0, love=0, cartoon=0,
                    science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2018-11-16', '%Y-%m-%d'),
                    introduction="Tony is a slacker who works as a waiter in a nightclub. ",
                    vote_average=0, vote_count=0,
                    pic_path='../static/stage photo/Green Book.png')
    db.session.add(movie14)

    movie15 = Movie(movie_name='Forrest Gump', popular='2112749', is_delete=0, comedy=0, action=0, love=1, cartoon=0,
                    science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('1994-07-06', '%Y-%m-%d'),
                    introduction="Forrest Gump congenital retarded, but his mother often encouraged Forrest Gump stupid people have stupid blessing, to his self-improvement.",
                    vote_average=0, vote_count=0,
                    pic_path='../static/stage photo/Forrest Gump.png')
    db.session.add(movie15)

    movie16 = Movie(movie_name='Coco', popular='163001800', is_delete=0, comedy=1, action=0, love=0, cartoon=1,
                    science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2017-11-22', '%Y-%m-%d'),
                    introduction="In an accident, Miguel crossed into the land of the undead. Before the sun rose, he had to get the blessing of a relative, or he would be left in this world forever.",
                    vote_average=2.3, vote_count=3,
                    pic_path='../static/stage photo/Coco.png')
    db.session.add(movie16)

    movie17 = Movie(movie_name='Léon', popular='2247609', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                    science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('1994-09-14', '%Y-%m-%d'),
                    introduction="Leon is a lonely professional killer, one day, the neighbor girl Matilda knocks on his door, asking him to stay there temporarily to avoid being killed. ",
                    vote_average=5, vote_count=1,
                    pic_path='../static/stage photo/Léon.png')
    db.session.add(movie17)

    movie18 = Movie(movie_name='Spirited Away', popular='2189365', is_delete=0, comedy=0, action=0, love=0, cartoon=1,
                    science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2001-07-20', '%Y-%m-%d'),
                    introduction="Driving with her parents to their new home, Chihiro accidentally enters a mysterious tunnel on the outskirts of the city -- and they are transported to another strange world -- a medieval town. ",
                    vote_average=2.75, vote_count=4,
                    pic_path='../static/stage photo/Spirited Away.png')
    db.session.add(movie18)

    movie19 = Movie(movie_name='Interstellar ', popular='1782160', is_delete=0, comedy=0, action=0, love=0, cartoon=0,
                    science=1, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2014-11-07', '%Y-%m-%d'),
                    introduction="After being persuaded by Professor Brand, he and three other experts took a spacecraft to explore three of the most promising planets known. ",
                    vote_average=0, vote_count=0,
                    pic_path='../static/stage photo/Interstellar.png')
    db.session.add(movie19)

    movie20 = Movie(movie_name='Flipped', popular='1793552', is_delete=0, comedy=1, action=0, love=1, cartoon=0,
                    science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2010-09-10', '%Y-%m-%d'),
                    introduction="The Bryce family moved to town, and Julie, the girl next door, came to help. She fell in love with him at first sight and wanted his kiss.",
                    vote_average=3.5, vote_count=2,
                    pic_path='../static/stage photo/Flipped.png')
    db.session.add(movie20)

    movie202 = Movie(movie_name='Cinderella', popular='223892', is_delete=0, comedy=1, action=0, love=1, cartoon=1,
                     science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2021-09-03', '%Y-%m-%d'),
                     introduction="Rilla was completely reduced to being a slave to Madame Temani and a maid in her family. However, despite being oppressed and insulted by her relatives, Rilla still decided to stay and guard the family. In an accident, Rilla met a man, but she didn't know that the charming young man in front of her was a prince",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Cinderella.png')
    db.session.add(movie202)

    movie203 = Movie(movie_name='The Maze Runner', popular='216013', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                     science=1, suspense=0, war=0, thriller=1, release_time=datetime.strptime('2014-09-10', '%Y-%m-%d'),
                     introduction='They were all trapped in a maze, and a group of giant monsters threatened outside the wall. The maze gradually began to change, and everything fell into chaos. Thomas and Teresa decided to embark on the path of cracking the maze together to find out the chilling secret behind the maze.',
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/The Maze Runner.png')
    db.session.add(movie203)

    movie204 = Movie(movie_name='It chapter Two', popular='70801', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                     science=1, suspense=0, war=0, thriller=1, release_time=datetime.strptime('2019-09-06', '%Y-%m-%d'),
                     introduction="After the battle with the Joker (Bill Skarsg a rd) in 1989, the friends of the Wicked Alliance grew up separately, and they made an appointment that when darkness came again, they would gather again in Delhi to make the final decision with the Joker.",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/It chapter Two.png')
    db.session.add(movie204)

    movie205 = Movie(movie_name='Schindler List', popular='1081755', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                     science=0, suspense=0, war=1, thriller=0, release_time=datetime.strptime('1993-11-30', '%Y-%m-%d'),
                     introduction=" On the eve of Germany's defeat, the massacre of Jews became even crazier. Schindler listed 1200 German military officers and bought the lives of these Jews with all his money.",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Schindler List.png')
    db.session.add(movie205)

    movie206 = Movie(movie_name='Soul', popular='950402', is_delete=0, comedy=0, action=0, love=0, cartoon=1,
                     science=1, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2020-10-11', '%Y-%m-%d'),
                     introduction="What exactly shaped the real you? ",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Soul.png')
    db.session.add(movie206)

    movie207 = Movie(movie_name='Contratiempo', popular='1227873', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                     science=0, suspense=0, war=0, thriller=1, release_time=datetime.strptime('2016-09-23', '%Y-%m-%d'),
                     introduction="Driving away from the villa, there was an accident on the road. In order to cover up the truth of the incident, the two decided to sink the young Daniel Lian who died in the accident into the lake with his car. ",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Contratiempo.png')
    db.session.add(movie207)

    movie208 = Movie(movie_name='WALL·E', popular='1289368', is_delete=0, comedy=0, action=0, love=0, cartoon=0,
                     science=1, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2008-06-27', '%Y-%m-%d'),
                     introduction="Earthlings were forced to leave their hometown by spaceship for a long and boundless journey to the universe. ",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/WALL·E.png')
    db.session.add(movie208)

    movie209 = Movie(movie_name='Life of Pi', popular=' 1324690', is_delete=0, comedy=0, action=1, love=0, cartoon=0,
                     science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2012-11-21', '%Y-%m-%d'),
                     introduction="The story begins and ends in Montelou. ",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Life of Pi.png')
    db.session.add(movie209)

    movie210 = Movie(movie_name='Catch Me If You Can', popular='992380 ', is_delete=0, comedy=0, action=1, love=0,
                     cartoon=0,
                     science=0, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2002-12-25', '%Y-%m-%d'),
                     introduction="The youngest wanted person in FBI history. His criminal methods are vast and masterful. ",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Catch Me If You Can.png')
    db.session.add(movie210)

    movie211 = Movie(movie_name='Avengers: Endgame  ', popular='1047884', is_delete=0, comedy=0, action=1, love=0,
                     cartoon=0,
                     science=1, suspense=0, war=1, thriller=0, release_time=datetime.strptime('2019-04-24', '%Y-%m-%d'),
                     introduction="The ultimate showdown destined to be recorded in history, with superheroes following one another for the faith they hold in their hearts ",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Avengers Endgame.png')
    db.session.add(movie211)

    movie212 = Movie(movie_name='Big Hero 6', popular='988686 ', is_delete=0, comedy=0, action=1, love=1,
                     cartoon=1,
                     science=1, suspense=0, war=0, thriller=0, release_time=datetime.strptime('2014-11-07', '%Y-%m-%d'),
                     introduction="San Fransokyo, is a talented young man who loves to invent and create. With the encouragement of his brother Teddy, Xiao Hong participated in the entrance competition for robotics at the Institute of Technology hosted by Professor Robert Callahan. ",
                     vote_average=0, vote_count=0,
                     pic_path='../static/stage photo/Big Hero 6.png')
    db.session.add(movie212)

    # Movie likes
    movie_like1 = Movie_Like(user_id=3, movie_id=1)
    db.session.add(movie_like1)
    movie_like2 = Movie_Like(user_id=3, movie_id=5)
    db.session.add(movie_like2)
    movie_like3 = Movie_Like(user_id=3, movie_id=2)
    db.session.add(movie_like3)

    # Movie collect
    movie_collect1 = Movie_Collect(user_id=3, movie_id=1)
    db.session.add(movie_collect1)
    movie_collect2 = Movie_Collect(user_id=3, movie_id=5)
    db.session.add(movie_collect2)

    # Movie grade
    movie_grade1 = Movie_Grade(user_id=2, movie_id=1, grade=5)
    db.session.add(movie_grade1)
    movie_grade2 = Movie_Grade(user_id=2, movie_id=3, grade=4)
    db.session.add(movie_grade2)
    movie_grade19 = Movie_Grade(user_id=2, movie_id=16, grade=4)
    db.session.add(movie_grade19)
    movie_grade20 = Movie_Grade(user_id=2, movie_id=18, grade=5)
    db.session.add(movie_grade20)

    movie_grade3 = Movie_Grade(user_id=4, movie_id=3, grade=5)
    db.session.add(movie_grade3)
    movie_grade4 = Movie_Grade(user_id=4, movie_id=5, grade=3)
    db.session.add(movie_grade4)
    movie_grade21 = Movie_Grade(user_id=4, movie_id=11, grade=4)
    db.session.add(movie_grade21)
    movie_grade22 = Movie_Grade(user_id=4, movie_id=12, grade=4)
    db.session.add(movie_grade22)

    movie_grade5 = Movie_Grade(user_id=5, movie_id=5, grade=5)
    db.session.add(movie_grade5)
    movie_grade23 = Movie_Grade(user_id=5, movie_id=17, grade=5)
    db.session.add(movie_grade23)
    movie_grade24 = Movie_Grade(user_id=5, movie_id=16, grade=2)
    db.session.add(movie_grade24)
    movie_grade25 = Movie_Grade(user_id=5, movie_id=18, grade=2)
    db.session.add(movie_grade25)

    movie_grade6 = Movie_Grade(user_id=3, movie_id=5, grade=1)
    db.session.add(movie_grade6)
    movie_grade26 = Movie_Grade(user_id=3, movie_id=11, grade=2)
    db.session.add(movie_grade26)
    movie_grade27 = Movie_Grade(user_id=3, movie_id=20, grade=5)
    db.session.add(movie_grade27)
    movie_grade28 = Movie_Grade(user_id=3, movie_id=13, grade=5)
    db.session.add(movie_grade28)

    movie_grade7 = Movie_Grade(user_id=6, movie_id=2, grade=5)
    db.session.add(movie_grade7)
    movie_grade8 = Movie_Grade(user_id=6, movie_id=4, grade=5)
    db.session.add(movie_grade8)
    movie_grade9 = Movie_Grade(user_id=6, movie_id=5, grade=4)
    db.session.add(movie_grade9)
    movie_grade29 = Movie_Grade(user_id=6, movie_id=20, grade=2)
    db.session.add(movie_grade29)
    movie_grade30 = Movie_Grade(user_id=6, movie_id=13, grade=2)
    db.session.add(movie_grade30)

    movie_grade10 = Movie_Grade(user_id=7, movie_id=1, grade=4)
    db.session.add(movie_grade10)
    movie_grade11 = Movie_Grade(user_id=7, movie_id=4, grade=5)
    db.session.add(movie_grade11)
    movie_grade12 = Movie_Grade(user_id=7, movie_id=5, grade=3)
    db.session.add(movie_grade12)
    movie_grade31 = Movie_Grade(user_id=7, movie_id=16, grade=1)
    db.session.add(movie_grade31)
    movie_grade32 = Movie_Grade(user_id=7, movie_id=18, grade=2)
    db.session.add(movie_grade32)

    movie_grade13 = Movie_Grade(user_id=8, movie_id=2, grade=5)
    db.session.add(movie_grade13)
    movie_grade14 = Movie_Grade(user_id=8, movie_id=4, grade=5)
    db.session.add(movie_grade14)
    movie_grade15 = Movie_Grade(user_id=8, movie_id=5, grade=3)
    db.session.add(movie_grade15)
    movie_grade16 = Movie_Grade(user_id=8, movie_id=11, grade=4)
    db.session.add(movie_grade16)
    movie_grade17 = Movie_Grade(user_id=8, movie_id=12, grade=5)
    db.session.add(movie_grade17)
    movie_grade18 = Movie_Grade(user_id=8, movie_id=18, grade=2)
    db.session.add(movie_grade18)

    db.session.commit()


# This function is use to check whether the user is login
def islogined():
    # Check whether the user is logged into the web
    if session.get('username'):
        return True
    else:
        return False


