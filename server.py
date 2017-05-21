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
mf = MatrixFactorization
cb = CbFiltering
dir_path = os.path.dirname(os.path.realpath(__file__))

def articleIsRated(uid,aid):
     u = mongo.db.users.find_one({"_id": ObjectId(uid)})
     if u is not None:
         return 123
         # print u[items]


def updateActionById(uid,action,aid):
    if action > articleIsRated(uid,aid):
        mongo.db.users.update_one({"_id": ObjectId(uid)},
                                  {
                                      '$add': {'items': aid},
                                      '$add': {'rating': action}
                                  }, upsert=False, )

@app.route('/add/<name>',methods=['GET'])
def add(name):
    user = mongo.db.users
    user.insert({'name': name})
    return name + ' added'

@app.route('/',methods=['GET'])
def index():
    return "123"

@app.route('/get/<name>', methods=['GET'])
def get(name):
    user = mongo.db.users
    u = user.find_one({'name':name})
    print u
    return str(u)

@app.route('/update/<id>/<name>',methods=['GET'])
def update(id,name):
    mongo.db.users.update_one({"_id":ObjectId(id)},
                        {
                            '$set':{'name':name}
                        }, upsert=False,)
    return 'updated'


@app.route('/task',methods=['GET'])
def task():
    df = cb.openFile(dir_path + '/CBsystem/data/40k_movies_data.json')
    return json.dumps(cb.algo(df[500], df))


@app.route('/opration/<uid>/<aid>/<action>',methods=['GET'])
def opration(uid,action):
    try:
        user = mongo.db.users
        u = user.find_one({"_id":ObjectId(uid)})
    except:
        return "error"
    if u is not None:
        return #data for new mikre kaze
    if action == 0:
        return
    if action == 1:
        return
    if action == 2:
        return
    if action == 3:
        return
    if action == 4:
        return
    if action == 5:
        return

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