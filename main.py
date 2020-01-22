import queryManager
import recognition

rec = recognition.Recognition()
rec.loadDataset()
model = rec.defineModel()
predictions = rec.predictImages(model)

print("Ecco le opere riconosciute")
print(predictions)

manager = queryManager.QueryManager("The Scream")
#author = manager.getAuthor()
museum = manager.getMuseum()
#date = manager.getDate()