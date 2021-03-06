import threading
from pymongo import MongoClient

TIMER = 5 * 60

from MF import MatrixFactorization as mf

moranMongo = MongoClient('mongodb://galevgi:galgalgal@ds133981.mlab.com:33981/likeitarticle')
localMongo = MongoClient('mongodb://project57:likeit1234@127.0.0.1:27017/DB57')


def schedule():
    user = localMongo.DB57.users
    users = list(user.find())
    mf.MatrixFactorization.loadFileToData(users)
    mf.MatrixFactorization.makeMatrix()
    threading.Timer(TIMER, schedule).start()


if __name__ == '__main__':
    schedule()
