from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QHeaderView, QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCharts import QChartView, QPieSeries, QChart
import sys
import csv
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

        # 04- Define the table
        self.items = 0 # to count items in tablewidget
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Concept", "Amount", "Date", "Category"])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # Fit them on the space we have

        # 05- Add an action to the plot button
        self.ui.plot_btn.clicked.connect(self.plot_categories)

        # 05- Add a QChartView
        self.chart_view = QChartView()
        self.ui.verticalLayout_3.addWidget(self.chart_view)
        #self.chart_view.setRenderHint(QPainter.Antialiasing) # uncomment it and import QPainter in QtGui to use antialiasing

        #  06- Menu: File -> Save, Load and Exit options
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        ## Save action (export to a CSV)
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_data)

        ## Load action (read from CSV)
        load_action = QAction("Load", self)
        load_action.setShortcut("Ctrl+L")
        load_action.triggered.connect(self.load_data)

        ## Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)    

        ## Add actions to the save menu
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(exit_action)


    # 03- Define slot to validate values
    @Slot()
    def validate_values(self):
        concept = self.ui.concept_edit.text()
        amount = self.ui.amount_edit.text()
        category = self.ui.category_box.currentText()
        date = self.ui.date_edit.text()

        # 04- Show values in the table
        self.ui.tableWidget.insertRow(self.items)
        self.ui.tableWidget.setItem(self.items, 0, QTableWidgetItem(concept))
        self.ui.tableWidget.setItem(self.items, 1, QTableWidgetItem(str(amount)))
        self.ui.tableWidget.setItem(self.items, 2, QTableWidgetItem(date))
        self.ui.tableWidget.setItem(self.items, 3, QTableWidgetItem(category))
        self.items += 1

    # 05- Defile slot to plot categories
    @Slot()
    def plot_categories(self):
        # Generate a dict of categories to sum the amounts.
        categories_dict = {
            "Xmass gifts" : 0,
            "Groceries" : 0,
            "Restaurants" : 0,
            "Tió sweets" : 0,
            "3 kings gifts" : 0,
            "Decoration" : 0
        }
        
        # Iterate on the table to get the values
        for i in range(self.items):
            categories_dict[self.ui.tableWidget.item(i, 3).text()] += float(self.ui.tableWidget.item(i, 1).text())

        print(categories_dict)

        # Add the chart. We will use a pie chart
        series = QPieSeries()
        for key, value in categories_dict.items():
            if value > 0:
                series.append(key, value)
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

    # 06- Add slots to perform the file_menu actions
    @Slot()
    def save_data(self, checked):
        rows = self.ui.tableWidget.rowCount()
        if rows:
            with open("data.csv", "w", newline="") as f:
                writer = csv.writer(f, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_ALL)
                for i in range(rows):
                    concept = self.ui.tableWidget.item(i, 0).text()
                    amount = self.ui.tableWidget.item(i, 1).text()
                    date = self.ui.tableWidget.item(i, 2).text()
                    category = self.ui.tableWidget.item(i, 3).text()
                    writer.writerow([concept,amount,date,category])
                reply = QMessageBox.information(self, "Save",
                                                "Saved file successfully")
                reply

    @Slot()
    def load_data(self, checked):
        with open('data.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            self.items = 0
            self.ui.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                concept, amount, date, category = row
                self.ui.tableWidget.insertRow(i)
                self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(concept))
                self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(amount))
                self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(date))
                self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(category))
                self.items += 1
            
            reply = QMessageBox.information(self, "Load",
                                            "Load successfully")
            reply

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
