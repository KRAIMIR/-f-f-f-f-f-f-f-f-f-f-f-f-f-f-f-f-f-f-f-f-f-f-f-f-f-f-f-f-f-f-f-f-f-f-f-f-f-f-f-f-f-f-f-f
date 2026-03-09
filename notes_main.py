from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from random import *
import json

notes = {}


app = QApplication([])
windows = QWidget()

windows.setWindowTitle('умненькие заметачки')
windows.resize(900,600)

notetext = QLabel('список заметачек')
listnotes = QListWidget()

createnote = QPushButton('создать заметку')
delnote = QPushButton('удалить заметку')
savenote = QPushButton('сохранить заметку')

tagtext = QLabel('Списачек тегав')
taglist = QListWidget()
taginput = QLineEdit()
taginput.setPlaceholderText('Введите тегочек')

addtag = QPushButton('добавить тег')
unbreaktag = QPushButton('открепить от заметки')
seektag = QPushButton('искать заметки по тегу')

textedet = QTextEdit()

baseV1 = QVBoxLayout()
baseV1.addWidget(textedet)
baseV2 = QVBoxLayout()
baseV2.addWidget(notetext)
baseV2.addWidget(listnotes)
horiz1 = QHBoxLayout()
horiz1.addWidget(createnote)
horiz1.addWidget(delnote)
baseV2.addLayout(horiz1)
horiz2 = QHBoxLayout()
horiz2.addWidget(savenote)
baseV2.addLayout(horiz2)
baseV2.addWidget(tagtext)
baseV2.addWidget(taglist)
baseV2.addWidget(taginput)
horiz3 = QHBoxLayout()
horiz4 = QHBoxLayout()
horiz3.addWidget(addtag)
horiz3.addWidget(unbreaktag)
horiz4.addWidget(seektag)
baseV2.addLayout(horiz3)
baseV2.addLayout(horiz4)
mainLayout = QHBoxLayout()
mainLayout.addLayout(baseV1)
mainLayout.addLayout(baseV2)
windows.setLayout(mainLayout)

windows.show()
def show_result():
    key = listnotes.selectedItems()[0].text()
    textedet.setText(notes[key]['текст'])
    taglist.clear()
    taglist.addItems(notes[key]['теги'])

def addnote():
    lmao,ok = QInputDialog.getText(windows, 'добавить заметку', 'название заметки')
    if ok and lmao != '':
        notes[lmao] = {"текст" : "", "теги" : []}
        listnotes.addItem(lmao)

def deletenote():
    if listnotes.selectedItems():
        key = listnotes.selectedItems()[0].text()
        del notes[key]
        listnotes.clear()
        taglist.clear()
        textedet.clear()
        listnotes.addItems(notes)
        with open('notes_main.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes, file)

def save_note():
        if listnotes.selectedItems():
            key = listnotes.selectedItems()[0].text()
            notes[key]['текст'] = textedet.toPlainText()
            with open('notes_main.json', 'w', encoding = 'utf-8') as file:
                json.dump(notes, file)


def add_tag():
    if listnotes.selectedItems():
        key = listnotes.selectedItems()[0].text()
        tag = taginput.text()
        if tag != ' ':
            notes[key]['теги'].append(tag)
            taglist.addItem(tag)
            taginput.clear()
            with open('notes_main.json', 'w', encoding = 'utf-8') as file:
                json.dump(notes, file)


def del_tag():
    if listnotes.selectedItems():
        key = listnotes.selectedItems()[0].text()
        tag = taglist.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        taglist.clear()
        taglist.addItems(notes[key]['теги'])
        with open('notes_main.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes, file)

def seektags():
    tag = taginput.text()
    if seektag.text() == 'искать заметки по тегу':
        lelele = {}
        for name in notes:
            if tag in notes[name]['теги']:
                lelele[name] = notes[name]
        seektag.setText('Сбросить поиск')
        listnotes.clear()
        taglist.clear()
        listnotes.addItems(lelele)
    elif seektag.text() == 'Сбросить поиск':
        taginput.clear()
        listnotes.clear()
        taglist.clear()
        listnotes.addItems(notes)
        seektag.setText('искать заметки по тегу')
        



delnote.clicked.connect(deletenote)
savenote.clicked.connect(save_note)
addtag.clicked.connect(add_tag)
unbreaktag.clicked.connect(del_tag)
seektag.clicked.connect(seektags)



createnote.clicked.connect(addnote)
listnotes.itemClicked.connect(show_result)
with open('notes_main.json', 'r', encoding = 'utf-8') as file:
    notes = json.load(file)
listnotes.addItems(notes)


app.exec_()
