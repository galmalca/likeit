from bson import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from CBsystem import cbFiltering
import os
import json
PORT = 3002
HOST = "193.106.55.57"


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_URI'] = 'mongodb://gal:12345@ds153715.mlab.com:53715/users'


mongo = PyMongo(app)
dir_path = os.path.dirname(os.path.realpath(__file__))

def updateActionById(uid,action,aid):
    mongo.db.users.update_one({"_id": ObjectId(uid)},
                              {
                                  '$add': {'items':aid},
                                  '$add': {'rating':action}
                              }, upsert=False, )

@app.route('/add/<name>',methods=['GET'])
def add(name):
    user = mongo.db.users
    user.insert({'name': name})
    return name + ' added'

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
    df = cbFiltering.openFile(dir_path + '/CBsystem/data/40k_movies_data.json')
    return json.dumps(cbFiltering.algo(df[500], df))


@app.route('/opration/<uid>/<aid>/<action>',methods=['GET'])
def opration(uid,action):
    try:
        user = mongo.db.users
        u = user.find_one({"_id":ObjectId(uid)})
        new = 0
        if u is None:
            new = 1
            user.insert({"_id": ObjectId(uid),
                        'items':[],
                        'rating':[]
                         })
            return uid + ' added'
        print u
        return 'founded'
    except:
        return "error"
    if new:
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
        user = mongo.db.users
        u = user.find_one({"_id":ObjectId(uid)})
        if u is None:
            new = 1
            user.insert({"_id": ObjectId(uid)})
            return uid + ' added'
        new = 0
        print u
        return 'founded'
    except:
        return "error"
    if new:
        #write user to db + top 10 articles from home page
        return
    else:
        #we return the top 5 articles + algo(the last article who this user visit)
        #change in the db his new's articles
        return
    return




if __name__=='__main__':
    app.run(debug=True,port=PORT,host=HOST)