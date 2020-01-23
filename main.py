from PIL import Image

import numpy as np

from queryManager import Query
from recognition import Recognition
from dataset import Dataset

ds = Dataset(5)
rec = Recognition(ds)

# predictions = rec.predictImages()
# print("Ecco le opere riconosciute")
# print(predictions)

picture = "picture.jpg"
image = Image.open(picture)
predicted_class = rec.predictImage(image)

print(predicted_class)

predicted_label = ds.getLabelByClass('Artwork', predicted_class) #Restituisce il nome
code = ds.getLabelByClass('Code', predicted_class) #Restituisce il codice

print("Cerco informazioni per: " + predicted_label)
query = Query(predicted_label)
query.getAuthor()
query.getMuseum()
query.getDate()
query.getGenre()
query.getDimension()
query.getMovement()
query.buildUp()
query.runQuery()
query.getInfo()
