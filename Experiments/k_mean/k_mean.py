import numpy as np
from random import uniform

class DataTable:
    def __init__(self, width):
        self.num_columns = width
        self.data = np.empty(shape=(0, self.num_columns,), dtype=float)
        self.belongs_to = []

    def add_row(self, row):
        assert len(row) == self.num_columns
        self.data = np.append(self.data, [row,], axis=0)
        # All data points initially belong to the 0th centroid
        self.belongs_to.append(0)

    def assign_centroids(self, centroids):
        #  Returns number of points that have moved
        moved = 0
        shape = self.data.shape
        rows = shape[0]
        for index in range(rows):
            cur_point = self.data[index]
            new_cluster = self.__find_closest(cur_point, centroids)
            if new_cluster != self.belongs_to[index]:
                self.belongs_to[index] = new_cluster
                moved += 1

        return moved

    def __find_euclidian(self, p1, p2):
        return np.linalg.norm(p1 - p2)

    def __find_closest(self, point, centroids):
        min_distance = 9999999
        best_centroid = 0
        for c_idx in range(len(centroids)):
            centroid = centroids[c_idx]
            d = self.__find_euclidian(point, centroid)
            if d < min_distance:
                min_distance = d
                best_centroid = c_idx
        return best_centroid

    def find_distro(self):
        counts = {}
        centroids = {}
        for row_idx in range(len(self.belongs_to)):
            c_idx = self.belongs_to[row_idx]
            if c_idx in counts:
                counts[c_idx] += 1
                centroids[c_idx] += self.data[row_idx]
            else:
                counts[c_idx] = 1
                centroids[c_idx] = self.data[row_idx].copy()

        for c_idx in range(len(counts)):
            count = counts[c_idx]
            centroids[c_idx] = centroids[c_idx] / count

        return counts, centroids.items()

def get_data():
    dt = DataTable(2)
    with open("butterfly.dat") as d:
        for line in d.readlines():
            if line.startswith('#') or len(line) <= 1:
                continue
            parts = line.split(',')
            row = [int(p) for p in parts]
            dt.add_row(row)
    return dt


def __get_random_point(dt: DataTable):
    point = []
    mins = dt.data.min(axis=0)
    maxs = dt.data.max(axis=0)
    for dim in range(dt.num_columns):
        min = mins[dim]
        max = maxs[dim]
        p = uniform(min, max)
        point.append(p)
    return point


def init_clusters(K, dt: DataTable):
    centroids = []
    for c in range(K):
        centroids.append(__get_random_point(dt))
    return centroids


def print_centroids(centroids):
    for c in centroids:
        print(f"Centroid {c}")

def print_counts(counts):
    for c_idx in counts.keys():
        print(f"Cluster {c_idx} has {counts[c_idx]} items")


def main():
    K=2
    print(f"starting for K = {K}")
    d = get_data()
    centroids = init_clusters(K, d)
    print_centroids(centroids)

    keep_going = True
    while keep_going:
        moved = d.assign_centroids(centroids)
        counts, new_centroids = d.find_distro()
        print_centroids(new_centroids)
        print_counts(counts)
        if moved < 1:
            keep_going = False

if __name__ == "__main__":
    main()
