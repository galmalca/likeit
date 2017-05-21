import numpy as np
import numpy.ma as ma
import theano
from theano import tensor as T
import json
import time

floatX = theano.config.floatX

with open('movie_ratings_data_set.json') as data_file:
    movies_df = json.load(data_file)


#check number of movies
dict = {}
for movie in movies_df:
    for i in range(len(movie['movie_id'])):
        if dict.get(movie['movie_id'][i])==None:
            dict[movie['movie_id'][i]]=1


a = np.zeros((len(movies_df), len(dict)))


for movie in movies_df:
    for j in range(len(movie['movie_id'])):
        a[movie['user_id'],movie['movie_id'][j]-1]=movie['rating'][j]



def getmask(D):
  return ma.getmaskarray(D) if ma.isMA(D) else np.zeros(D.shape, dtype=bool)


def matrix_factorization_bgd(
    D, P, Q, steps=5000, alpha=0.0002, beta=0.02):
  P = theano.shared(P.astype(floatX))
  Q = theano.shared(Q.astype(floatX))
  X = T.matrix()
  error = T.sum(T.sqr(~getmask(D) * (P.dot(Q) - X)))
  regularization = (beta/2.0) * (T.sum(T.sqr(P)) + T.sum(T.sqr(Q)))
  cost = error + regularization
  gp, gq = T.grad(cost=cost, wrt=[P, Q])
  train = theano.function(inputs=[X],
                          outputs=cost,
                          updates=[(P, P - gp * alpha), (Q, Q - gq * alpha)])
  for _ in range(steps):
    train(D)
  return P.get_value(), Q.get_value()


def matrix_factorization_sgd(
    D, P, Q, steps=5000, alpha=0.0002, beta=0.02):
  P = theano.shared(P.astype(floatX))
  Q = theano.shared(Q.astype(floatX))
  P_i = T.vector()
  Q_j = T.vector()
  i = T.iscalar()
  j = T.iscalar()
  x = T.scalar()
  error = T.sqr(P_i.dot(Q_j) - x)
  regularization = (beta/2.0) * (P_i.dot(P_i) + Q_j.dot(Q_j))
  cost = error + regularization
  gp, gq = T.grad(cost=cost, wrt=[P_i, Q_j])
  train = theano.function(inputs=[i, j, x],
                          givens=[(P_i, P[i, :]), (Q_j, Q[:, j])],
                          updates=[(P, T.inc_subtensor(P[i, :], -gp * alpha)),
                                   (Q, T.inc_subtensor(Q[:, j], -gq * alpha))])
  for _ in range(steps):
    for (row, col), val in np.ndenumerate(D):
      if not getmask(D)[row, col]:
        train(row, col, val)
  return P.get_value(), Q.get_value()


def matrix_factorization_quux(
    D, P, Q, steps=5000, alpha=0.0002, beta=0.02):
  K = P.shape[1]
  P = np.copy(P)
  Q = np.copy(Q)
  for step in range(steps):
    for i in range(len(D)):
      for j in range(len(D[i])):
        if not getmask(D)[i, j]:
          eij = D[i, j] - np.dot(P[i, :], Q[:, j])
          for k in range(K):
            P[i, k] = P[i, k] + alpha * (2 * eij * Q[k, j] - beta * P[i, k])
            Q[k, j] = Q[k, j] + alpha * (2 * eij * P[i, k] - beta * Q[k, j])
  return P, Q


if __name__ == '__main__':
  D = a
  D = np.array(D)
  D = ma.masked_array(D, mask=D==-1)
  m, n = D.shape
  K = 2
  P = np.random.rand(m, K)
  Q = np.random.rand(K, n)
	
  start = time.time()
  np.set_printoptions(formatter={'all': lambda x: str(x).rjust(2)})
  print 'Ratings Matrix\n', D, '\n'

  np.set_printoptions(precision = 2, formatter=None)
  end = time.time()
  print end-start

  start = time.time()
  P_theano_bgd, Q_theano_bgd = matrix_factorization_bgd(D, P, Q)
  print 'Theano Batch Gradient Descent\n',\
    np.dot(P_theano_bgd, Q_theano_bgd), '\n'
  end = time.time()
  print end-start	

  start = time.time()
  P_theano_sgd, Q_theano_sgd = matrix_factorization_sgd(D, P, Q)
  print 'Theano Stochastic Gradient Descent\n',\
    np.dot(P_theano_sgd, Q_theano_sgd), '\n'
  end = time.time()
  print end-start

  start = time.time()
  P_quux, Q_quux = matrix_factorization_quux(D, P, Q)
  print 'quuxlabs\n', np.dot(P_quux, Q_quux), '\n'
  end = time.time()
  print end-start
