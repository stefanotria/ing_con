import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class ContentNeighbor:
    ds = []
    predicted_label = ""
    uri = ""
    def __init__(self, content, code, predicted_label):
        self.predicted_label = predicted_label
        self.ds = pd.read_csv("collection.csv", usecols=["Uri", "Content"])
        self.uri = "http://www.wikidata.org/entity/" + code
        self.ds.loc[len(self.ds)] = [self.uri,content[0]]


    def createModel(self):
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(self.ds['Content'])

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        results = {}
        for idx, row in self.ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], self.ds['Uri'][i]) for i in similar_indices]
            results[row['Uri']] = similar_items[1:]
        return results

    def recommend(self, num, results):

        print("Recommending " + str(num) + " products similar to " + self.predicted_label + "...")
        print("-------")
        recs = results[self.uri][:num]
        for rec in recs:
            print("Recommended: " + rec[1] + " (score:" + str(rec[0]) + ")")
        recs2 = results[self.uri][:len(self.ds)]
        return recs2