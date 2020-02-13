from __future__ import division

from tkinter import *

from PIL import ImageTk, Image

from functools import partial

import webbrowser


class InformationWindow():

    def __init__(self, master, painting, code, picture, response, info, neighbors):
        master.resizable(False, False)
        self.master = master

        self.master.title(painting)
        self.showResults(painting, code, picture, response, info, neighbors)

    def showResults(self, painting, code, picture, response, info, neighbors):
        # -- SHOW RESULTS --

        Label(self.master,
              text=painting + " - " + code,
              font=('', 25, 'bold')).grid(row=0, sticky=W + E + N + S)

        content_menu = Frame(self.master, width=100, height=75)
        content_menu.grid(row=1, sticky=N)

        image_menu = Frame(content_menu, width=400, height=400, borderwidth=1, relief="flat", highlightcolor="black")
        image_menu.grid(row=0, column=0, rowspan=2, sticky=W + E + N + S, padx=20, ipadx=10, ipady=10)

        print("PICTURE " + picture)
        img = Image.open(picture)

        width = 0
        height = 0

        if img.width > img.height:
            molt = 400 / img.width
            width = 400
            height = img.height * molt
        else:
            molt = 400 / img.height
            height = 400
            width = img.width * molt

        img = img.resize((int(width), int(height)), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        imageLabel = Label(image_menu, image=image)
        imageLabel.image = image

        if width > height:
            imageLabel.grid(row=0, column=0, sticky=W + E)
        else:
            imageLabel.grid(row=0, column=0, sticky=N + S)

        information_menu = Frame(content_menu, height=20, width=20, borderwidth=1, relief="flat",
                                 highlightcolor="black")
        information_menu.grid(row=0, column=1, sticky=W + E + N + S)

        Label(information_menu, text="Informations", font=('', 16, 'bold')).grid(row=0, column=0, padx=20,
                                                                                          sticky=W + E + N + S, columnspan=2)

        for index, (key, value) in enumerate(response.items()):
            print(str(index) + " - " + key + " - " + value)
            Label(information_menu, text=key, font=('', 14, 'bold')).grid(row=1 + index, column=0, padx=20,
                                                                          sticky=W + E + N + S)
            Label(information_menu, text=value).grid(row=1 + index, column=1, padx=20, sticky=W + E + N + S)

        descriptionText = Text(content_menu, height=10, width=20, wrap='word', font=('', 12))
        vertscroll = Scrollbar(content_menu)
        vertscroll.config(command=descriptionText.yview)
        descriptionText.config(yscrollcommand=vertscroll.set)
        descriptionText.grid(column=1, row=1, sticky=W + E + N + S, pady=20)
        vertscroll.grid(column=2, row=1, sticky='NS', pady=20)

        descriptionText.insert('1.0', info['Description'])

        if "Description" not in info:
            descriptionText.insert('1.0', 'No description')
        elif info['Description'] == '':
            descriptionText.insert('1.0', 'No description')
        else:
            descriptionText.insert('1.0', info['Description'])

        descriptionText.config(state=DISABLED)

        rec_menu = Frame(content_menu, borderwidth=1, relief="flat", highlightcolor="black")
        rec_menu.grid(row=0, column=3, sticky=W + E + N + S)

        Label(rec_menu, text="Similar Paintings Recommended", font=('', 16, 'bold')).grid(row=0, column=1, padx=20,
                                                                                          sticky=W + E + N + S, columnspan=2)
        i = 1
        for (nn) in neighbors:
            print(nn[0] + " - " + str(nn[1]))
            Button(rec_menu, text=nn[0], command=partial(self.openLink, nn[0])).grid(row=i, column=1, padx=20,
                                                                                     sticky=W + E + N + S)
            Label(rec_menu, text=nn[1]).grid(row=i, column=2, padx=20, sticky=W + E + N + S)
            Label(rec_menu, text=nn[2]).grid(row=i, column=2, padx=20, sticky=W + E + N + S)
            i += 1

    def openLink(self, link):
        webbrowser.open(link)
