import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor

class MyTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Colored Cell Example')

        # Set the number of rows and columns
        self.setRowCount(5)
        self.setColumnCount(3)

        # Fill the cells with data
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem('Cell {}-{}'.format(row, col))
                self.setItem(row, col, item)

        # Change the background color of a specific cell
        self.changeCellColor(2, 1, QColor(255, 0, 0))  # Set color to red for cell (2, 1)

    def changeCellColor(self, row, col, color):
        item = self.item(row, col)
        if item:
            item.setBackground(color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)
    tableWidget = MyTableWidget()
    layout.addWidget(tableWidget)
    window.show()
    sys.exit(app.exec_())