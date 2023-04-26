###------- K-Means

# Import necessary libraries
import numpy as np
from sklearn.cluster import KMeans

# Generate some example data
# Replace this with your own data
X = np.random.rand(100, 2) * 10

# Define the number of clusters (K)
k = 3

# Initialize the KMeans object with the desired number of clusters
kmeans = KMeans(n_clusters=k)

# Fit the KMeans model to the data
kmeans.fit(X)

# Get the cluster labels for each data point
labels = kmeans.labels_

# Get the coordinates of the cluster centroids
centroids = kmeans.cluster_centers_

# Print the cluster labels and centroids
print("Cluster Labels: ", labels)
print("Cluster Centroids: ", centroids)


##------- Hierarchical clustering 

# Import necessary libraries
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# Generate some example data
# Replace this with your own data
X = np.random.rand(10, 2) * 10

# Define the linkage method and distance metric
method = 'ward'
metric = 'euclidean'

# Perform hierarchical clustering
Z = linkage(X, method=method, metric=metric)

# Plot a dendrogram of the clustering results
dendrogram(Z)
plt.title("Agglomerative Hierarchical Clustering")
plt.show()