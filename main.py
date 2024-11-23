from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from ui import Ui_MainWindow
from qt_material import apply_stylesheet
import json
from datetime import datetime





class SmartNotes(QMainWindow):
    def   __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_notes()
        self.name = "Нова нотатка"
        self.ui.notes_list.itemClicked.connect(self.show_note)
        self.ui.save_btn.clicked.connect(self.save_note)
        self.ui.new_note.clicked.connect(self.new_note)
        self.ui.delete_btn.clicked.connect(self.del_note)
        self.ui.pushButton.clicked.connect(self.search_note)
        self.ui.search_line.textChanged.connect(self.search_note)
    
    def load_notes(self):
        self.ui.notes_list.clear()
        try:
            with open("notes.json", 'r', encoding="utf-8") as file:
                self.notes = json.load(file)    
        except Exception:
            self.notes= {
                 "Нова нотатка": {
                     "text": "Тут буде текст вашої нотатки",

                },
            }
        self.show_note_list(self.notes)
    
    def show_note_list (self, notes):              
        for title, note in notes.items():
            item = QListWidgetItem(title)
            if "datetime" in note:
                tip = f"Збережено: {note['datetime']}"
                item.setToolTip(tip)
            self.ui.notes_list.addItem(item)


    
    def show_note(self):
        self.name= self.ui.notes_list.selectedItems()[0].text()
        self.ui.note_title.setText(self.name)
        self.ui.note_text.setText(self.notes[self.name]["text"])

    def new_note(self):
        self.ui.note_title.clear()
        self.ui.note_text.clear()
        self.name = "Нова нотатка"

    def del_note(self):
        
        if self.name in self.notes:
            del self.notes[self.name]
        
            with open("notes.json", 'w', encoding="utf-8") as file:
                json.dump(self.notes,file, ensure_ascii=False)
            self.load_notes()
        
        self.new_note()

    def save_note(self):
        title = self.ui.note_title.text().strip()
        if title!="":


            if title != self.name:
                if self.name in self.notes:
                    del self.notes[self.name]
                self.name = title
                self.notes[title] = {}
                self.notes[title]["text"] = self.ui.note_text.toPlainText()
                
            else:
                self.notes[self.name]["text"] = self.ui.note_text.toPlainText()

            now = datetime.now().strftime("%d.%m.%Y %H:%M")
            self.notes[self.name]['datetime'] = now

            with open("notes.json", 'w', encoding="utf-8") as file:
                json.dump(self.notes,file, ensure_ascii=False)
            self.load_notes()
        else:
            error_msg = QMessageBox()
            error_msg.setWindowTitle("Помилка")
            error_msg.setText("Додайте назву нотатки")
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.exec()

    def search_note(self):
        search = self.ui.search_line.text().strip().lower()
        result = {}
        if search != "":    
            title_list = self.notes.keys()
            for title in title_list:
                if search in title.lower():
                    result[title] = self.notes[title]

            self.ui.notes_list.clear()
            self.show_note_list(result)
        else:
            self.ui.notes_list.clear()
            self.show_note_list(self.notes)



app = QApplication([])
ex = SmartNotes()
apply_stylesheet(app, theme='dark_teal.xml')
ex.show()
app.exec_()