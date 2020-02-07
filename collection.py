import pandas as pd
import csv
import numpy as np
import io
from queryManager import Query


class Collection:
    path = "collection.csv"

    def __init__(self, results, code):
        self.orderResults(results)
        results = self.compactContent(results)

        results = self.trimItSelf(results, code)

        df = pd.DataFrame(results, columns=['Uri', 'Paint', 'Author', 'Museum', 'Genre', 'Movement', 'Content'])
        df.to_csv(self.path, index=False)

    def orderResults(self, results):
        for index in range(0, len(results)):
            for j in range(index + 1, len(results)):
                if (results[j][0] > results[index][0]):
                    temp = results[index]
                    results[index] = results[j]
                    results[j] = temp

    def compactContent(self, results):
        r = []
        flag = 0
        index = 0
        while (index < len(results) - 1):
            val = results[index]
            flag = index + 1
            while (results[flag][0] == results[index][0]):
                results[index][6] = results[index][6] + " " + results[flag][6]
                if (flag < len(results) - 1):
                    flag += 1
                else:
                    break
            r.append(results[index])
            index = flag
        return r

    def trimItSelf(self, results, code):
        index = -1
        i = 0
        while i < len(results):
            uri = results[i][0]
            if code in uri:
                index = i
                break
            i += 1
        if index != -1:
            results = np.delete(results, index, axis=0)
        return results

