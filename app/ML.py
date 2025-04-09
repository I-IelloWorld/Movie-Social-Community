from app.ALS.pyALS import ALS


def Do_ALS(grades, id, num):
    # 训练模型
    model = ALS()
    model.fit(grades, k=5, max_iter=5)

    # 商品推荐
    print("Showing the predictions of users...")
    # Predictions
    user_ids = [id, id]
    predictions = model.predict(user_ids, n_items=num)
    for user_id, prediction in zip(user_ids, predictions):
        _prediction = [format_prediction(item_id, score)
                       for item_id, score in prediction]
        print("User id:%d recommedation: %s" % (user_id, _prediction))
        recommend = _prediction
    return recommend



def format_prediction(item_id, score):
    return [item_id, score]
    # return "item_id:%d score:%.2f" % (item_id, score)

# def Do_ALS(grades, id, num):
#     rawRatings = sc.parallelize(grades)
#     rawRatings.collect()
#     ratings = rawRatings.map(lambda x: (x[0], x[1], x[2]))
#     model = ALS.train(ratings, 50, 10, 0.01)
#     top = model.recommendProducts(id, num)
#     return top

