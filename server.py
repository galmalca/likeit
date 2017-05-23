from bson import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from CBsystem import CbFiltering
from MF import MatrixFactorization
import os
import json
PORT = 3002
HOST = "10.10.248.57"


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_URI'] = 'mongodb://gal:12345@ds153715.mlab.com:53715/users'


mongo = PyMongo(app)
mf = MatrixFactorization.MatrixFactorization
cb = CbFiltering.CbFiltering
dir_path = os.path.dirname(os.path.realpath(__file__))

def raplaceRating(uid,aid,action):
    u = mongo.db.users.find_one({"_id": ObjectId(uid)})
    if u is not None:
        i=0
        for item in u['items']:
            if item == aid:
                u['rating'][i]=action
            i += 1
        mongo.db.users.update_one({"_id": ObjectId(uid)},
                                  {
                                      '$set': {'rating': u['rating']},
                                  }, upsert=False, )

def articleIsRated(uid, aid):
    u = mongo.db.users.find_one({"_id": ObjectId(uid)})
    if u is not None:
        i = 0
        for item in u['items']:
            if item == aid:
                return u['rating'][i]
            i += 1
        return -1

def insertItemAndRating(uid,aid,action):
    u = mongo.db.users.find_one({"_id": ObjectId(uid)})
    if u is not None:
        mongo.db.users.update_one({"_id": ObjectId(uid)},
                                {
                                  '$push': {'items': aid,
                                            'rating': action},
                                }, upsert=False, )
    return u

def updateActionById(uid, aid, action):
    rating = articleIsRated(uid, aid)
    if action > rating:
        if rating is -1:
            insertItemAndRating(uid, aid, action)
            return "insertItemAndRating"
        else:
            raplaceRating(uid, aid, action)
            return "raplaceRating"
    return "not updated"

@app.route('/add/<name>',methods=['POST'])
def add(name):
    user = mongo.db.users
    user.insert({'name': name,
                 'movie_id': {24,14,9,2,30,10,17,5},
                 'rating': {5,5,1,3,5,3,4,2}
                 })
    return name + ' added'

@app.route('/',methods=['GET'])
def index():
    return "123"

@app.route('/task',methods=['GET'])
def task():
    df = cb.openFile(dir_path + '/CBsystem/data/40k_movies_data.json')
    return json.dumps(cb.algo(df[500], df))


@app.route('/opration/<uid>/<aid>/<action>',methods=['GET'])
def opration(uid, aid, action):
    try:
        user = mongo.db.users
        u = user.find_one({"_id":ObjectId(uid)})
    except:
        return "error"
    if u is not None:
        updateActionById(uid, aid, action)

@app.route('/getData/<uid>',methods=['GET'])
def getData(uid):
    #check if user exist
    try:
        new = 0
        user = mongo.db.users
        u = user.find_one({"_id":ObjectId(uid)})
        if u is None:
            new = 1
    except:
        return "error"
    if new:
        user.insert({"_id": ObjectId(uid)})
        return 'new user + top 10 articles from home page'
        #write user to db + top 10 articles from home page
        return
    else:
        return 'top 5 articles + 5 from algo algo'
        #we return the top 5 articles + algo(the last article who this user visit)
        #change in the db his new's articles
        return
    return



if __name__=='__main__':
    app.run(debug=True,port=PORT,host=HOST)