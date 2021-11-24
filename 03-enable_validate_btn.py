from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 02- Fill combo box categories
        self.categories = ["Xmass gifts", "Groceries", "Restaurants", 
                           "Tió sweets", "3 kings gifts", "Decoration"]
        self.ui.category_box.addItems(self.categories)
        
        # 02- Add an action to the validate button
        self.ui.validate_btn.clicked.connect(self.validate_values)

    # 03- Define slot to validate values
    @Slot()
    def validate_values(self):
        concept = self.ui.concept_edit.text()
        amount = self.ui.amount_edit.text()
        category = self.ui.category_box.currentText()
        date = self.ui.date_edit.text()
        
        # for debugging purposes
        print("concept", concept)
        print("amount", amount)
        print("category", category)
        print("date", date)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())