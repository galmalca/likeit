import pandas as pd
import numpy as np
import json
import pickle

class MatrixFactorization:

    data = None

    def loadFileToData(filepath,self):
        with open(filepath) as data_file:
            movies_df = json.load(data_file)
        #check number of movies
        dict = {}
        for movie in movies_df:
            for i in range(len(movie['movie_id'])):
                if dict.get(movie['movie_id'][i])==None:
                    dict[movie['movie_id'][i]]=1
        MatrixFactorization.data = np.zeros((len(movies_df), len(dict)))
        for movie in movies_df:
            for j in range(len(movie['movie_id'])):
                self.data[movie['user_id'],movie['movie_id'][j]-1]=movie['rating'][j]



    def algo(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
        Q = Q.T
        for step in range(steps):
            for i in range(len(R)):
                for j in range(len(R[i])):
                    if R[i][j] > 0:
                        eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                        for k in range(K):
                            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
            eR = np.dot(P,Q)
            e = 0
            for i in range(len(R)):
                for j in range(len(R[i])):
                    if R[i][j] > 0:
                        e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                        for k in range(K):
                            e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
            if e < 0.001:
                break
        return P, Q.T

    def makeMatrix(self):
        self.loadFileToData('movie_ratings_data_set.json')
        R = self.data
        R = np.array(R)

        N = len(R)
        M = len(R[0])
        K = 2

        P = np.random.rand(N, K)
        Q = np.random.rand(M, K)

        nP, nQ = self.algo(R, P, Q, K)
        nR = np.dot(nP, nQ.T)

        pickle.dump(P, open("user_features.dat", "wb"))
        pickle.dump(Q, open("product_features.dat", "wb"))
        pickle.dump(nR, open("predicted_ratings.dat", "wb"))

        print(nR.shape)
        print(nR)

    #'user_features.dat''product_features.dat''predicted_ratings.dat'
    def livePrediction(self, pathToUersFeatures, pathToProductFeatures, pathToPredictedRatings, user_id):
        with open(pathToUersFeatures, 'rb') as f:
            U = pickle.load(f, encoding='latin1')
        with open(pathToProductFeatures, 'rb') as f:
            M = pickle.load(f, encoding='latin1')
        with open(pathToPredictedRatings, 'rb') as f:
            predicted_ratings = pickle.load(f, encoding='latin1')
        with open('movies.json') as data_file:
            movies_df = json.load(data_file)

        from operator import itemgetter
        user_id_to_search = user_id
        print("Movies we will recommend:")
        user_ratings = predicted_ratings[user_id_to_search - 1]
        i = 0
        for movie in movies_df:
            movie['rating'] = user_ratings[i]
            i += 1
        # movies_df = movies_df.sort(key=['rating'])
        sortedList = sorted(movies_df, key=itemgetter('rating'), reverse=True)
        # movies_df = movies_df(by=['rating'], ascending=False)

        print(sortedList[0:5])
