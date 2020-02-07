from PIL import Image

import numpy as np
from tfidf import ContentNeighbor
from neighbors import Neighbors
from queryManager import Query
from recognition import Recognition
from dataset import Dataset
from collection import Collection

ds = Dataset(5)
rec = Recognition(ds)

# predictions = rec.predictImages()
# print("Ecco le opere riconosciute")
# print(predictions)

picture = "picture.jpg"
image = Image.open(picture)
predicted_class = rec.predictImage(image)

print(predicted_class)

predicted_label = ds.getLabelByClass('Artwork', predicted_class)  # Restituisce il nome
code = ds.getLabelByClass('Code', predicted_class)  # Restituisce il codice

print("Cerco informazioni per: " + predicted_label)
query = Query(code)
query.getAuthor()
query.getMuseum()
query.getDate()
query.getGenre()
query.getDimension()
query.getMovement()
query.buildUp()
response = query.runQuery()
print("risposta ", response)
info = query.getInfo(predicted_label, response["Author"])
print(info)
location = query.getLocation()

coll = query.createCollection(location["Location"])
Collection(coll, code)
cont = query.getContent()
instance = [response["Author"], response["Museum"], response["Genre"], response["Movement"]]

cb = ContentNeighbor(cont, code, predicted_label)
r = cb.createModel()
rectf = cb.recommend(5, r)
nn = Neighbors(instance)
nn.getNeighbors(3, rectf)
