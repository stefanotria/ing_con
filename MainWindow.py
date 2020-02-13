from tkinter import *

from tkinter.filedialog import askopenfilename

from PIL import Image
from recognition import Recognition
from dataset import Dataset

from tfidf import ContentNeighbor
from neighbors import Neighbors
from queryManager import Query

from collection import Collection

from InformationWindow import InformationWindow


class MainWindow(Frame):

    def __init__(self, master):
        master.resizable(False, False)
        self.master = master

        self.master.title("Riconoscimento quadri")

        label = Label(self.master,
                      text="Benvenuto, inizia il riconoscimento.\nPer farlo seleziona l'immagine da riconoscere.",
                      font=('', 16, 'bold'))
        label.grid(row=0, column=0, padx=20, sticky=N)

        button = Button(self.master, text='Seleziona immagine da riconoscere', command=self.initial)
        button.grid(row=1, padx=20, pady=20)

    def initial(self):
        ds = Dataset(5)
        rec = Recognition(ds)

        filename = askopenfilename(filetypes=[("Image JPG", "*.jpg")])
        image = Image.open(str(filename))
        predicted_class = rec.predictImage(image)

        print(predicted_class)

        predicted_label = ds.getLabelByClass('Artwork', predicted_class)  # Restituisce il nome
        code = ds.getLabelByClass('Code', predicted_class)  # Restituisce il codice

        self.getInformations(predicted_label, code, str(filename))

    def getInformations(self, painting, code, picture):

        print("Cerco informazioni per: " + painting)
        query = Query(code)
        query.getAuthor()
        query.getMuseum()
        query.getDate()
        query.getGenre()
        query.getDimension()
        query.getMovement()
        query.buildUp()
        response = query.runQuery()

        info = query.getInfo(painting, response["Author"])
        print(info)
        location = query.getLocation()

        coll = query.createCollection(location["Location"])
        Collection(coll, code)
        cont = query.getContent()
        instance = [response["Author"], response["Museum"], response["Genre"], response["Movement"]]

        cb = ContentNeighbor(cont, code, painting)
        r = cb.createModel()
        rectf = cb.recommend(5, r)
        nn = Neighbors(instance)
        neighbors = nn.getNeighbors(6, rectf)

        newWindow = Toplevel(self.master)
        informationWindow = InformationWindow(newWindow, painting, code, picture, response, info, neighbors)


def main():
    root = Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
