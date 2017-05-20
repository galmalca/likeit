import numpy as np
from sklearn.neighbors import NearestNeighbors

# First let's create a dataset called X, with 6 records and 2 features each.
X = np.array([[-1, 2], [4, -4], [-2, 1], [-1, 3], [-3, 2], [-1, 4]])

# Next we will instantiate a nearest neighbor object, and call it nbrs. Then we will fit it to dataset X.
nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(X)

# Let's find the k-neighbors of each point in object X. To do that we call the kneighbors() function on object X.
distances, indices = nbrs.kneighbors(X)

# Let's print out the indices of neighbors for each record in object X.
print indices

print(nbrs.kneighbors([[-2, 4]]))