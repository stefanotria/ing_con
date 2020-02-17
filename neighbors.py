import csv
from scipy import spatial


class Neighbors:
    dataset = {}
    instance = ""
    motivation = ""
    instance_vector = [0.45, 0.20, 0.75, 0.65]

    def __init__(self, instance): # codePainting: quadro predetto
        self.instance = instance
        with open('collection.csv', mode='r', encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                r = row["Author"], row["Museum"], row["Genre"], row["Movement"]
                r = self.setWeights(r)
                v = [r , self.motivation]
                dict = {row["Uri"]: v}
                self.dataset.update(dict)

    def setWeights(self, row):
        w = []
        self.motivation = ""
        # for index in range(len(row)):
        if self.instance[0] == row[0]:
            w.append(0.45)
            self.motivation += "Author, "
        else:
            w.append(0)
        if self.instance[1] == row[1]:
            w.append(0.20)
            self.motivation += "Museum, "
        else:
            w.append(0)
        if self.instance[2] == row[2]:
            w.append(0.75)
            self.motivation += "Genre, "
        else:
            w.append(0)
        if self.instance[3] == row[3]:
            w.append(0.65)
            self.motivation += "Movement, "
        else:
            w.append(0)
        return w

    def getNeighbors(self, k, recs):
        distance = []
        for index in self.dataset.keys():
            dist = self.getDistance(self.instance_vector, self.dataset.get(index)[0])
            if dist > 0:
                self.motivation = self.dataset.get(index)[1]
                for rec in recs:
                    if (index == rec[1]):
                        dist = (dist + rec[0]/2)
                        self.motivation += "Similar content"
                distance.append((index, dist, self.motivation))
        distance.sort(key=lambda x: x[1])
        distance.reverse()
        del distance[k:]

        return distance

    def getDistance(self, vector1, vector2):
        cosine = 1 - spatial.distance.cosine(vector1, vector2)
        return cosine
