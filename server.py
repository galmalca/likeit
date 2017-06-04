from bson import ObjectId
from bson import json_util
from flask import Flask
from pymongo import MongoClient
from CBsystem import CbFiltering as cb
from MF import MatrixFactorization as mf
import json
import threading
import requests

TIMER = 20 * 60
PORT = 3002
HOST = "10.10.248.57"
predictedPath = "predicted_ratings.dat"

app = Flask(__name__)

moranMongo = MongoClient('mongodb://galevgi:galgalgal@ds133981.mlab.com:33981/likeitarticle')
localMongo = MongoClient('mongodb://project57:likeit1234@127.0.0.1:27017/DB57')
articlesList = None


def raplaceRating(uid, aid, action):
    u = localMongo.DB57.users.find_one({"_id": ObjectId(uid)})
    if u is not None:
        i = 0
        for item in u['items']:
            if item == aid:
                u['rating'][i] = action
            i += 1
            localMongo.DB57.users.update_one({"_id": ObjectId(uid)},
                                             {
                                                 '$set': {'rating': u['rating']},
                                             }, upsert=False, )


def articleIsRated(uid, aid):
    u = localMongo.DB57.users.find_one({"_id": ObjectId(uid)})
    if u is not None:
        i = 0
        try:
            for item in u['items']:
                if item == aid:
                    return u['rating'][i]
                i += 1
            return -1
        except:
            return -1


def insertItemAndRating(uid, aid, action):
    u = localMongo.DB57.users.find_one({"_id": ObjectId(uid)})
    if u is not None:
        localMongo.DB57.users.update_one({"_id": ObjectId(uid)},
                                         {
                                             '$push': {'items': aid,
                                                       'rating': action},
                                         }, upsert=False, )
    return u

def insertitemToBlackList(uid,aid):
    u = localMongo.DB57.users.find_one({"_id": ObjectId(uid)})
    if u is not None:
        localMongo.DB57.users.update_one({"_id": ObjectId(uid)},
                                         {
                                             '$push': {'blackList': aid},
                                         }, upsert=False, )
    return u

def updateActionById(uid, aid, action):
    rating = articleIsRated(uid, aid)
    if action is 0:
        insertitemToBlackList(uid,aid)
    if action > rating:
        if rating is -1:
            insertItemAndRating(uid, aid, action)
            return "insertItemAndRating"
        else:
            raplaceRating(uid, aid, action)
            return "raplaceRating"
    return "not updated"


def numberOfOprations(uid):  # 1 for young user(oprations < 10) and 0 for old user
    u = localMongo.DB57.users.find_one({"_id": ObjectId(uid)})
    try:
        if u['oprationNumber'] < 10:
            return 1
        else:
            return 0
    except:
        return 0


def updateNumberOfOprations(uid):
    localMongo.DB57.users.update_one({"_id": ObjectId(uid)},
                                     {
                                         '$inc': {'oprationNumber': 1},
                                     }, upsert=False, )


def getAllArticles():
    user = moranMongo.likeitarticle.articles_db
    articles = list(user.find())
    return articles

def getBlackList(uid):
    u = localMongo.DB57.users.find_one({"_id": ObjectId(uid)})
    if u is None:
        return None
    return u['BlackList']

def schedule():
    global articlesList
    articlesList = getAllArticles()
    threading.Timer(TIMER, schedule).start()

def removeItemsFromBlackList(uid,resultList):
    try:
        list = getBlackList(uid)
        for item in list:
            if item in resultList:
                resultList.remove(item)
    except:None

def getFavoriteArticle(uid):
    u = localMongo.DB57.users.find_one({"_id": ObjectId(uid)})
    key = None
    try:
        maxRating = max(u['rating'])
        i = 0
        for rating in u['rating']:
            if rating == maxRating:
                key = u['items'][i]
            i += 1
        return key
    except:
        return "None"


def getSpecificArticle(aid):
    for i in range(len(articlesList)):
        if articlesList[i]["_id"] == ObjectId(aid):
            return str(i)
    return None


@app.route('/index', methods=['GET'])
def index():
    return "123"


@app.route('/opration/<uid>/<aid>/<action>', methods=['GET'])
def opration(uid, aid, action):
    try:
        user = localMongo.DB57.users
        u = user.find_one({"_id": ObjectId(uid)})
    except:
        return "error, user didnt found"
    if u is not None:
        updateActionById(uid, aid, action)
        updateNumberOfOprations(uid)
        return 'done'


@app.route('/getData/<uid>', methods=['GET', 'POST'])
def getData(uid):
    try:
        new = 0
        user = localMongo.DB57.users
        u = user.find_one({"_id": ObjectId(uid)})
        if u is None:
            new = 1
    except:
        return "error, db not connected / userid isn't an objectid"
    if new:
        user.insert({"_id": ObjectId(uid),
                     "oprationNumber": 0,
                     "items": [],
                     "rating": [],
                     "BlackList": []})
        req = requests.get('http://10.10.248.57:3003/getTenArticles')
        return json.dumps(req.json())
    elif numberOfOprations(uid):
        fav = getFavoriteArticle(uid)
        try:
            article = articlesList[int(getSpecificArticle(fav))]
        except:
            req = requests.get('http://10.10.248.57:3003/getTenArticles')
            return json.dumps(req.json())
        results = cb.CbFiltering.algo(article, articlesList)
        req = requests.get('http://10.10.248.57:3003/getFiveArticles')
        results.extend(req.json())
        removeItemsFromBlackList(uid,results)
        return json.dumps(results,indent=4, default=json_util.default)
    else:
        try:
            predict = mf.MatrixFactorization.livePrediction(predictedPath, articlesList, uid)
            removeItemsFromBlackList(uid, predict)
            return json.dumps(predict,indent=4, default=json_util.default)
        except:
            return "error"


if __name__ == '__main__':
    schedule()
    app.run(debug=True, port=PORT, host=HOST)
