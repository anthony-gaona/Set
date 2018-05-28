from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from glob import glob
from random import randint


# ======================Classes======================
# ---------------------Card---------------------
class Card:
    #"""docstring for Card."""

    def __init__(self, file):
        #super(Card, self).__init__()

        self.file = str(file)

        filename = file.replace('Cards/', '')
        self.filename = filename

        properties = filename.replace('.png', '')
        properties = properties.split('_')[1]
        properties = properties.split('-')

        self.shape, self.color, self.fill, self.count = properties


# ---------------------Card---------------------

# -------------------Matching-------------------
class Matching:

    def __init__(self, card1, card2, card3):

        self.arrCard1 = [card1.shape, card1.color,
                         card1.fill, card1.count]

        self.arrCard2 = [card2.shape, card2.color,
                         card2.fill, card2.count]

        self.arrCard3 = [card3.shape, card3.color,
                         card3.fill, card3.count]

    def find_match(self):

        shapes = ["Circle", "Squiggle", "Diamond"]
        colors = ["Red", "Blue", "Green"]
        fills = ["Solid", "Striped", "Empty"]
        counts = ["1", "2", "3"]
        
        arrTargetCard = []
        # ------------Shapes------------
        if self.arrCard1[0] == self.arrCard2[0]:
            # match
            arrTargetCard.append(self.arrCard1[0])
        else:
            # not match
            for shape in shapes:
                if shape != self.arrCard1[0] and shape != self.arrCard2[0]:
                    arrTargetCard.append(shape)
        # ------------Shapes------------

        # ------------Colors------------
        if self.arrCard1[1] == self.arrCard2[1]:
            # match
            arrTargetCard.append(self.arrCard1[1])
        else:
            # not match
            for color in colors:
                if color != self.arrCard1[1] and color != self.arrCard2[1]:
                    arrTargetCard.append(color)
        # ------------Colors------------

        # -------------Fills------------
        if self.arrCard1[2] == self.arrCard2[2]:
            # match
            arrTargetCard.append(self.arrCard1[2])
        else:
            # not match
            for fill in fills:
                if fill != self.arrCard1[2] and fill != self.arrCard2[2]:
                    arrTargetCard.append(fill)
        # -------------Fills------------

        # ------------Counts------------
        if self.arrCard1[3] == self.arrCard2[3]:
            # match
            arrTargetCard.append(self.arrCard1[3])
        else:
            # not match
            for count in counts:
                if count != self.arrCard1[3] and count != self.arrCard2[3]:
                    arrTargetCard.append(count)
        # ------------Counts------------

        # ------------Fen's Special Rule------------
        if self.arrCard1 == self.arrCard2:
            # Printed value if all four characteristics of
            # the first two cards are the same.
            # BUT this will never happen because that
            # would require two perfectly identical cards. (:
            print("Fen is so")
        else:
            if self.arrCard1[0] != self.arrCard2[0] and \
               self.arrCard1[1] != self.arrCard2[1] and \
               self.arrCard1[2] != self.arrCard2[2] and \
               self.arrCard1[3] != self.arrCard2[3]:
                # Printed value if all four characteristics of
                # the first two cards are different.
                print(1337)
        # ------------Fen's Special Rule------------

        return arrTargetCard

    def compare_set(self):
        arrTargetCard = self.find_match()

        if arrTargetCard == self.arrCard3:
            messagebox._show(title="Set", message="Set!")
        else:
            messagebox._show(title="Set", message="WRONG.")

# -------------------Matching-------------------

# ------------------CardButton------------------
class CardButton:

    def __init__(self, card_number, card):
        self.boolBoxChecked = BooleanVar()
        self.boolBoxChecked.set(False)
        intCardWidth = 250
        intCardHeight = 150
        self.button = Checkbutton(root, indicatoron=False, highlightbackground="#161616",
                                  command=self.select_card,
                                  variable=self.boolBoxChecked, borderwidth=0,
                                  relief="flat", background="#161616")
        self.card_number = card_number
        self.card = card
        self.cardfile = card.file
        pilPhoto = Image.open(self.cardfile)
        pilPhoto = pilPhoto.resize((intCardWidth, intCardHeight), Image.ANTIALIAS)
        self.tkPhoto = ImageTk.PhotoImage(pilPhoto)
        self.button.config(image=self.tkPhoto)
        self.button.grid(row=(int(card_number / 3) + 1), column=(card_number % 3),
                         sticky=("N", "S", "E", "W"))

    def select_card(self):
        if self.boolBoxChecked.get():
            self.button.config(highlightbackground="blue")
            if len(arrSelectedCards) <= 1:
                arrSelectedCards.append(self.card)
            else:
                arrSelectedCards.append(self.card)
                matching = Matching(arrSelectedCards[0], arrSelectedCards[1], arrSelectedCards[2])
                matching.compare_set()
                reset_cards()
        else:
            self.button.config(highlightbackground="#161616", background="#161616")
            if self.card in arrSelectedCards:
                arrSelectedCards.remove(self.card)

    def deselect_card(self):
        if self.boolBoxChecked.get():
            self.boolBoxChecked.set(False)
            self.button.config(highlightbackground="#161616", background="#161616")


# ------------------CardButton------------------

# =======================Functions========================
# -------------------new_cards------------------
def new_cards():
    arrCards.clear()
    arrButtons.clear()
    arrIndexes = []
    arrSelectedCards.clear()
    x = 0
    while len(arrCards) < 12:
        number = randint(0, (len(arrCardFiles) - 1))
        if number not in arrIndexes:
            arrIndexes.append(number)
            arrCards.append(Card(arrCardFiles[number]))
            arrButtons.append(CardButton(x, arrCards[x]))
            x += 1
# -------------------new_cards------------------

# ------------------reset_cards-----------------
def reset_cards():
    arrSelectedCards.clear()
    for button in arrButtons:
        button.deselect_card()
# ------------------reset_cards-----------------

# =========================Launch=========================
# initialize variables
arrCards = []
arrCardFiles = glob("Cards/Card_*.png")
arrButtons = []
arrSelectedCards = []


# -------------------Build UI-------------------
root = Tk()

root.minsize(width=765, height=700)
root.config(background="#6b6c6d")

new_cards()

# build "New Cards" button
butNewCards = Button(root, text="New Cards", relief="flat", command=new_cards)
butNewCards.grid(row=0, column=1, sticky=("N", "S", "E", "W"))

# format grid
for row in range(0, 5):
    Grid.rowconfigure(root, row, weight=1)
for column in range(0, 3):
    Grid.columnconfigure(root, column, weight=1)

# launch app
root.mainloop()
# -------------------Build UI-------------------
