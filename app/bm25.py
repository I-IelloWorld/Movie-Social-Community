#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import os
import jieba
import pickle
import logging
from nltk import PorterStemmer


from app.models import Movie, User

jieba.setLogLevel(log_level=logging.INFO)


class BM25Param(object):
    def __init__(self, f, df, idf, length, avg_length, docs_list, line_length_list,k1=1.5, k2=1.0,b=0.75):
        """
        :param f:
        :param df:
        :param idf:
        :param length:
        :param avg_length:
        :param docs_list:
        :param line_length_list:
        :param k1: 可调整参数，[1.2, 2.0]
        :param k2: 可调整参数，[1.2, 2.0]
        :param b:
        """
        self.f = f
        self.df = df
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.idf = idf
        self.length = length
        self.avg_length = avg_length
        self.docs_list = docs_list
        self.line_length_list = line_length_list

    def __str__(self):
        return f"k1:{self.k1}, k2:{self.k2}, b:{self.b}"

# search by movie introduction and id (need stemming)
class BM25Movie(object):
    _param_pkl1 = "app/IRdata/param.pkl1"
    # 停止词
    _stop_words_path = "app/IRdata/stop_words.txt"
    #用户，电影数据集
    _movie_path = 'app/IRdata/movies.txt'
    #
    #
    # _param_pkl = "IRdata/param.pkl"
    # # 样例数据集
    # _docs_path = "IRdata/data.txt"
    # # 停止词
    # _stop_words_path = "IRdata/stop_words.txt"
    # #用户，电影数据集
    # _user_path = 'IRdata/users.txt'
    # _movie_path = 'IRdata/movies.txt'


    _stop_words = []

    def __init__(self, docs=""):
        self.docs = docs
        self.param: BM25Param = self._load_param()  #
    # 预生成stop words集
    def _load_stop_words(self):
        if not os.path.exists(self._stop_words_path):
            raise Exception(f"system stop words: {self._stop_words_path} not found")
        stop_words = []
        with open(self._stop_words_path, 'r', encoding='utf8') as reader:
            for line in reader:
                line = line.strip()
                stop_words.append(line)
        return stop_words

    def _build_param(self):
        stemmer = PorterStemmer()
        def _cal_param(reader_obj):
            f = []  # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
            df = {}  # 存储每个词及出现了该词的文档数量
            idf = {}  # 存储每个词的idf值
            lines = reader_obj.readlines()
            length = len(lines)
            words_count = 0
            docs_list = []
            line_length_list =[]
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                words = [word for word in jieba.lcut(line) if word and word not in self._stop_words]
                line_length_list.append(len(words))
                docs_list.append(line)
                words_count += len(words)
                tmp_dict = {}
                for word in words:
                    word = stemmer.stem(word.lower())
                    tmp_dict[word] = tmp_dict.get(word, 0) + 1
                f.append(tmp_dict)
                print('-------------------')
                print(tmp_dict)
                for word in tmp_dict.keys():
                    df[word] = df.get(word, 0) + 1
            for word, num in df.items():
                idf[word] = math.log(length - num + 0.5) - math.log(num + 0.5)
            param = BM25Param(f, df, idf, length, words_count / length, docs_list, line_length_list)
            return param

        # cal
        if self.docs:
            if not os.path.exists(self.docs):
                raise Exception(f"input docs {self.docs} not found")
            with open(self.docs, 'r', encoding='utf8') as reader:
                param = _cal_param(reader)

        else:
            # if not os.path.exists(self._docs_path):
            #     raise Exception(f"system docs {self._docs_path} not found")
            # with open(self._docs_path, 'r', encoding='utf8') as reader:
            #     param = _cal_param(reader)

            if not os.path.exists(self._movie_path):
                raise Exception(f"system docs {self._movie_path} not found")
            with open(self._movie_path, 'r', encoding='utf8') as reader:
                param = _cal_param(reader)
        print(param)
        with open(self._param_pkl1, 'wb') as writer:
            pickle.dump(param, writer)
        return param
    # 预加载
    def _load_param(self):
        self._stop_words = self._load_stop_words()
        if self.docs:
            param = self._build_param()
        else:
            if not os.path.exists(self._param_pkl1):
                param = self._build_param()
            else:
                with open(self._param_pkl1, 'rb') as reader:
                    param = pickle.load(reader)
        return param
    #算分
    def _cal_similarity(self, words, index):
        score = 0
        for word in words:
            if word not in self.param.f[index]:
                continue
            molecular = self.param.idf[word] * self.param.f[index][word] * (self.param.k1 + 1)
            denominator = self.param.f[index][word] + self.param.k1 * (1 - self.param.b +
                                                                       self.param.b * self.param.line_length_list[index] /
                                                                       self.param.avg_length)
            score += molecular / denominator
        return score

    def cal_similarity(self, query: str):
        """
        相似度计算，无排序结果
        :param query: 待查询结果
        :return: [(doc, score), ..]
        """
        words = [word for word in jieba.lcut(query) if word and word not in self._stop_words]
        score_list = []
        for index in range(self.param.length):
            score = self._cal_similarity(words, index)
            score_list.append((self.param.docs_list[index], score))
        return score_list

    def cal_similarity_rank(self, query: str):
        """
        相似度计算，排序
        :param query: 待查询结果
        :return: [(doc, score), ..]
        """
        result = self.cal_similarity(query)
        result.sort(key=lambda x: -x[1])
        return result


# search by user name and id (without stemming)
class BM25User(object):
    _param_pkl2 = "app/IRdata/param.pkl2"
    # 停止词
    _stop_words_path = "app/IRdata/stop_words.txt"
    #数据集
    _user_path = 'app/IRdata/users.txt'


    _stop_words = []

    def __init__(self, docs=""):
        self.docs = docs
        self.param: BM25Param = self._load_param()  #
    # 预生成stop words集
    def _load_stop_words(self):
        if not os.path.exists(self._stop_words_path):
            raise Exception(f"system stop words: {self._stop_words_path} not found")
        stop_words = []
        with open(self._stop_words_path, 'r', encoding='utf8') as reader:
            for line in reader:
                line = line.strip()
                stop_words.append(line)
        return stop_words

    def _build_param(self):

        def _cal_param(reader_obj):
            f = []  # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
            df = {}  # 存储每个词及出现了该词的文档数量
            idf = {}  # 存储每个词的idf值
            lines = reader_obj.readlines()
            length = len(lines)
            words_count = 0
            docs_list = []
            line_length_list =[]
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                words = [word for word in jieba.lcut(line) if word and word not in self._stop_words]
                line_length_list.append(len(words))
                docs_list.append(line)
                words_count += len(words)
                tmp_dict = {}
                for word in words:
                    tmp_dict[word] = tmp_dict.get(word, 0) + 1
                f.append(tmp_dict)
                for word in tmp_dict.keys():
                    df[word] = df.get(word, 0) + 1
            for word, num in df.items():
                idf[word] = math.log(length - num + 0.5) - math.log(num + 0.5)
            param = BM25Param(f, df, idf, length, words_count / length, docs_list, line_length_list)
            return param

        # cal
        if self.docs:
            if not os.path.exists(self.docs):
                raise Exception(f"input docs {self.docs} not found")
            with open(self.docs, 'r', encoding='utf8') as reader:
                param = _cal_param(reader)

        else:
            # if not os.path.exists(self._docs_path):
            #     raise Exception(f"system docs {self._docs_path} not found")
            # with open(self._docs_path, 'r', encoding='utf8') as reader:
            #     param = _cal_param(reader)

            if not os.path.exists(self._user_path):
                raise Exception(f"system docs {self._user_path} not found")
            with open(self._user_path, 'r', encoding='utf8') as reader:
                param = _cal_param(reader)

        with open(self._param_pkl2, 'wb') as writer:
            pickle.dump(param, writer)
        return param
    # 预加载
    def _load_param(self):
        self._stop_words = self._load_stop_words()
        if self.docs:
            param = self._build_param()
        else:
            if not os.path.exists(self._param_pkl2):
                param = self._build_param()
            else:
                with open(self._param_pkl2, 'rb') as reader:
                    param = pickle.load(reader)
        return param
    #算分
    def _cal_similarity(self, words, index):
        score = 0
        for word in words:
            if word not in self.param.f[index]:
                continue
            molecular = self.param.idf[word] * self.param.f[index][word] * (self.param.k1 + 1)
            denominator = self.param.f[index][word] + self.param.k1 * (1 - self.param.b +
                                                                       self.param.b * self.param.line_length_list[index] /
                                                                       self.param.avg_length)
            score += molecular / denominator
        return score

    def cal_similarity(self, query: str):
        """
        相似度计算，无排序结果
        :param query: 待查询结果
        :return: [(doc, score), ..]
        """
        words = [word for word in jieba.lcut(query) if word and word not in self._stop_words]
        score_list = []
        for index in range(self.param.length):
            score = self._cal_similarity(words, index)
            score_list.append((self.param.docs_list[index], score))
        return score_list

    def cal_similarity_rank(self, query: str):
        """
        相似度计算，排序
        :param query: 待查询结果
        :return: [(doc, score), ..]
        """
        result = self.cal_similarity(query)
        result.sort(key=lambda x: -x[1])
        return result






if __name__ == '__main__':
    # 读取movie数据库到movies.txt
    with open ('IRdata/movies.txt', 'w') as movie_intro:
        movies = Movie.query.all()
        movie_text = ''
        for movie in movies:
            movie_text += str(movie.id) + ' ' + movie.movie_name + ' ' + movie.introduction + ' ' + movie.movie_name + '\n'
        movie_intro.write(movie_text)


    # 读取user数据库到users.txt
    with open ('IRdata/users.txt', 'w') as user_id_name:
        users = User.query.all()
        user_text = ''
        for user in users:
            user_text += str(user.id) + ' ' + user.user_name + ' ' + str(user.id) + '\n'
        user_id_name.write(user_text)


    # 测试
    # bm25 = BM25()
    # query_content = "Your name"  # 查询语句
    # # result = bm25.cal_similarity(query_content)
    # # for line, score in result:
    # #     print(line, score)
    # # print("**"*20)
    # result = bm25.cal_similarity_rank(query_content)
    # for line, score in result:
    #     print(line, score)
