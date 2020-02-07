from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk

import numpy as np
from tfidf import ContentNeighbor
from neighbors import Neighbors
from queryManager import Query
from recognition import Recognition
from dataset import Dataset
from collection import Collection

from functools import partial

import webbrowser


def main():
    ds = Dataset(5)
    rec = Recognition(ds)

    filename = askopenfilename(filetypes=[("Image JPG", "*.jpg")])
    image = Image.open(str(filename))
    predicted_class = rec.predictImage(image)

    print(predicted_class)

    predicted_label = ds.getLabelByClass('Artwork', predicted_class)  # Restituisce il nome
    code = ds.getLabelByClass('Code', predicted_class)  # Restituisce il codice

    showResults(predicted_label, str(filename), code)


def showResults(label, picture, code):
    results_window = Toplevel()
    results_window.title(label)

    results_menu = Frame(results_window)
    results_menu.grid(row=0, column=0,
                      padx=20, sticky=N)

    Label(results_menu,
          text=label + " - " + code,
          font=('', 25, 'bold')).grid(row=0, sticky=W + E + N + S)

    print("Cerco informazioni per: " + label)
    query = Query(code)
    query.getAuthor()
    query.getMuseum()
    query.getDate()
    query.getGenre()
    query.getDimension()
    query.getMovement()
    query.buildUp()
    response = query.runQuery()
    info = query.getInfo(label, response["Author"])
    print(info)
    location = query.getLocation()

    content_menu = Frame(results_window)
    content_menu.grid(row=1, sticky=N)

    #CODICE PER VISUALIZZARE L'IMMAGINE
    """image_menu = Frame(content_menu)
    image_menu.grid(row=0, column=0, sticky=W + E + N + S)

    image = ImageTk.PhotoImage(Image.open(picture))
    imageLabel = Label(image_menu, image=image)
    imageLabel.grid(row=0, column=0, rowspan=2, sticky=W + E + N + S)"""

    information_menu = Frame(content_menu)
    information_menu.grid(row=0, column=0, sticky=W + E + N + S)

    for index, (key, value) in enumerate(response.items()):
        print(str(index) + " - " + key + " - " + value)
        Label(information_menu, text=key, font=('', 14, 'bold')).grid(row=0 + index, column=1, padx=20,
                                                                      sticky=W + E + N + S)
        Label(information_menu, text=value).grid(row=0 + index, column=2, padx=20, sticky=W + E + N + S)

    description_menu = Frame(content_menu)
    description_menu.grid(row=1, column=0, sticky=W + E + N + S)

    if "Description" not in info:
        Label(description_menu, text='No description', font=('', 14, 'italic')).grid(row=0, column=0, padx=20, ipadx=20, pady=20,
                                                                       ipady=20,
                                                                       sticky=W + E + N + S)
    elif info['Description'] == '':
        Label(description_menu, text='No description', font=('', 14, 'italic')).grid(row=0, column=0, padx=20, ipadx=20, pady=20,
                                                                       ipady=20,
                                                                       sticky=W + E + N + S)
    else:
        Label(description_menu, text=info['Description']).grid(row=0, column=0, padx=20, ipadx=20, pady=20, ipady=20,
                                                               sticky=W + E + N + S)

    rec_menu = Frame(content_menu)
    rec_menu.grid(row=0, column=1, sticky=W + E + N + S)

    coll = query.createCollection(location["Location"])
    Collection(coll, code)
    cont = query.getContent()
    instance = [response["Author"], response["Museum"], response["Genre"], response["Movement"]]

    cb = ContentNeighbor(cont, code, label)
    r = cb.createModel()
    rectf = cb.recommend(5, r)
    nn = Neighbors(instance)
    neighbors = nn.getNeighbors(3, rectf)

    i = 0
    for (p, s) in neighbors:
        print(p + " - " + str(s))
        Button(rec_menu, text=p, command=partial(openLink, p)).grid(row=i, column=1, padx=20, sticky=W + E + N + S)
        Label(rec_menu, text=s).grid(row=i, column=2, padx=20, sticky=W + E + N + S)
        i += 1


def openLink(link):
    webbrowser.open(link)


main_window = Tk()
main_window.title("Riconoscimento quadri")

top_menu = Frame(main_window)
top_menu.grid(row=0, column=0,
              padx=20, sticky=N)
Label(top_menu,
      text="Benvenuto, inizia il riconoscimento.\nPer farlo seleziona l'immagine da riconoscere.",
      font=('', 16, 'bold')).grid()

menu = Frame(main_window)
menu.grid(sticky=N)
Button(menu, text='Seleziona immagine da riconoscere', command=main).grid(row=1, padx=20, pady=20)

main_window.mainloop()
