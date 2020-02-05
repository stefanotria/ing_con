import pandas as pd
import csv
import numpy as np
from scipy import spatial


class Neighbors:
    dataset = {}
    instance = ""
    instance_vector = [1.45, 1.20, 1.75, 1.65]

    def __init__(self, instance):
        self.instance = instance
        with open('collection.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                r = row["Author"], row["Museum"], row["Genre"], row["Movement"]
                r = self.setWeights(r)
                dict = {row["Uri"]: r}
                self.dataset.update(dict)

    def setWeights(self, row):
        w = []
        # for index in range(len(row)):
        if (self.instance[0] == row[0]):
            w.append(1.45)
        else:
            w.append(0)
        if (self.instance[1] == row[1]):
            w.append(1.20)
        else:
            w.append(0)
        if (self.instance[2] == row[2]):
            w.append(1.75)
        else:
            w.append(0)
        if (self.instance[3] == row[3]):
            w.append(1.65)
        else:
            w.append(0)
        return w

    def getNeighbors(self, k):
        distance = []
        for index in self.dataset.keys():
            dist = self.getDistance(self.instance_vector, self.dataset.get(index))
            if dist > 0:
                distance.append((index, dist))
        distance.sort(key=lambda x: x[1])
        print(distance)

    def getDistance(self, vector1, vector2):
        cosine = 1 - spatial.distance.cosine(vector1, vector2)
        return cosine
        """vector1 = np.array(vector1)
        vector2 = np.array(vector2)
        return np.linalg.norm(vector1 - vector2)"""
