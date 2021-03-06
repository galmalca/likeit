import numpy as np
import json
import pickle


class MatrixFactorization:
    def __init__(self):
        pass

    data = None
    users = None
    dict = {}

    @classmethod
    def loadFileToData(cls, inputData):
        cls.users = inputData
        # check number of movies
        dict = {}
        k = 0
        for user in cls.users:
            for i in range(len(user['items'])):
                if dict.get(user['items'][i]) is None:
                    dict[user['items'][i]] = k
                    k += 1

        cls.data = np.zeros((len(cls.users), len(dict)))
        i = 0
        for item in cls.users:
            for j in range(len(item['items'])):
                cls.data[i, dict[item['items'][j]]] = item['rating'][j]
            i += 1
        cls.dict = dict



    @classmethod
    def algo(cls, R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
        Q = Q.T
        for step in range(steps):
            for i in range(len(R)):
                for j in range(len(R[i])):
                    if R[i][j] > 0:
                        eij = R[i][j] - np.dot(P[i, :], Q[:, j])
                        for k in range(K):
                            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
            eR = np.dot(P, Q)
            e = 0
            for i in range(len(R)):
                for j in range(len(R[i])):
                    if R[i][j] > 0:
                        e += pow(R[i][j] - np.dot(P[i, :], Q[:, j]), 2)
                        for k in range(K):
                            e += (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
            if e < 0.001:
                break
        return P, Q.T

    @classmethod
    def makeMatrix(cls):
        R = cls.data
        R = np.array(R)

        N = len(R)
        M = len(R[0])
        K = 2

        P = np.random.rand(N, K)
        Q = np.random.rand(M, K)

        nP, nQ = MatrixFactorization.algo(R, P, Q, K)
        nR = np.dot(nP, nQ.T)

        pickle.dump(P, open("user_features.dat", "wb"))
        pickle.dump(Q, open("product_features.dat", "wb"))
        pickle.dump(nR, open("predicted_ratings.dat", "wb"))
        #
        # print(nR.shape)
        # print(nR)

    # 'user_features.dat'
    @classmethod
    def livePrediction(cls, pathToPredictedRatings, inputData, user_id):
        with open(pathToPredictedRatings, 'rb') as f:
            predicted_ratings = pickle.load(f)
        articlesMatrix = inputData #the table of the articles(moran articles)

        from operator import itemgetter
        for j in range(len(cls.users)):
            if cls.users[j]["_id"] == user_id:
                break
        user_ratings = predicted_ratings[j-1] #the vector of the specific user in the predicted matrix
        i = 0
        for item in articlesMatrix:
            try:
                item['rating'] = user_ratings[cls.dict.get(str(item['_id']),0)]
            except:None
            i += 1
        sortedList = sorted(articlesMatrix, key=itemgetter('rating'), reverse=True)

        return sortedList[:20]
