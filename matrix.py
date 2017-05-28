import threading
from pymongo import MongoClient

TIMER = 5 * 60

from MF import MatrixFactorization as mf

moranMongo = MongoClient('mongodb://galevgi:galgalgal@ds133981.mlab.com:33981/likeitarticle')
localMongo = MongoClient('mongodb://gal:12345@ds153715.mlab.com:53715/users')


def schedule():
    user = localMongo.users.users
    articles = list(user.find())
    print articles
    mf.MatrixFactorization.loadFileToData(articles)
    mf.MatrixFactorization.makeMatrix()
    threading.Timer(TIMER, schedule).start()


if __name__ == '__main__':
    schedule()
