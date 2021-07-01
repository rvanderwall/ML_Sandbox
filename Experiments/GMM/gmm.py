import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture


def show_data(data):
    plt.figure(figsize=(7, 7))
    plt.scatter(data["Weight"], data["Height"])
    plt.xlabel('Weight')
    plt.ylabel('Height')
    plt.title('Data Distribution')
    plt.show()


def show_labeled(data, labels):
    frame = pd.DataFrame(data)
    frame['cluster'] = labels
    frame.columns = ['Weight', 'Height', 'cluster']

    # plotting results
    color = ['blue', 'green', 'cyan', 'black']
    plt.clf()
    for k in range(0, 4):
        data = frame[frame["cluster"] == k]
        plt.scatter(data["Weight"], data["Height"], c=color[k])
    plt.show()


def k_mean(data):
    # training k-means model
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(data)

    # predictions from kmeans
    labels = kmeans.predict(data)
    show_labeled(data, labels)


def gmm_clustering(data):
    # plotting ends up adding a 'cluster' column which then
    # is used in the GMM clustering.  Get rid of it!
    data = data.drop(columns=['cluster'])

    # training gaussian mixture model
    gmm = GaussianMixture(n_components=4, init_params='kmeans')
    gmm.fit(data)

    # predictions from gmm
    labels = gmm.predict(data)
    show_labeled(data, labels)


def run():
    np.random.seed(31415)
    data = pd.read_csv('Clustering_gmm.csv')
    # show_data(data)

    k_mean(data)

    # data = pd.read_csv('Clustering_gmm.csv')
    gmm_clustering(data)


if __name__ == "__main__":
    run()
