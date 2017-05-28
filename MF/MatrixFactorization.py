import numpy as np
import json
import pickle


class MatrixFactorization:
    def __init__(self):
        pass

    data = None
    articles = None

    @classmethod
    def loadFileToData(cls, inputData):
        cls.articles = inputData
        # check number of movies
        dict = {}
        for item in cls.articles:
            for i in range(len(item['movie_id'])):
                if dict.get(item['movie_id'][i]) is None:
                    dict[item['movie_id'][i]] = 1

                cls.data = np.zeros((len(cls.articles), len(dict)))

        cls.data
        for item in cls.articles:
            for j in range(len(item['movie_id'])):
                cls.data[item['movie_id'], item['movie_id'][j] - 1] = item['rating'][j]

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

        # print(nR.shape)
        # print(nR)

    # 'user_features.dat'
    @classmethod
    def livePrediction(cls, pathToPredictedRatings, inputData, user_id):
        with open(pathToPredictedRatings, 'rb') as f:
            predicted_ratings = pickle.load(f)
        articlesMatrix = inputData

        from operator import itemgetter
        for j in range(len(cls.articles)):
            if cls.articles[j]["_id"] == user_id:
                break

        user_ratings = predicted_ratings[j]
        i = 0
        for item in articlesMatrix:
            item['rating'] = user_ratings[i]
            i += 1
        sortedList = sorted(articlesMatrix, key=itemgetter('rating'), reverse=True)

        print(sortedList[:30])
