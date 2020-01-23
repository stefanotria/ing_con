from queryManager import Query
from recognition import Recognition
from dataset import Dataset

ds = Dataset(5)
rec = Recognition(ds)

predictions = rec.predictImages()

print("Ecco le opere riconosciute")
print(predictions)
print("Cerco informazioni per: ", predictions[0])
query = Query(predictions[0])
query.getAuthor()
query.getMuseum()
query.getDate()
query.getGenre()
query.getDimension()
query.getMovement()
query.buildUp()
query.runQuery()