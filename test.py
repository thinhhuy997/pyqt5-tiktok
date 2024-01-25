from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
import sys

class MyTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a QTableWidget with 3 rows and 3 columns
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)

        # Fill the table with buttons
        for row in range(3):
            for col in range(3):
                button = QPushButton(f"Button {row}-{col}")
                button.setEnabled(True)  # By default, buttons are enabled
                self.tableWidget.setCellWidget(row, col, button)

        # Get the button item at specific row and column
        row_index = 1
        col_index = 2
        item = self.tableWidget.cellWidget(row_index, col_index)

        if isinstance(item, QPushButton):
            item.setEnabled(False)  # Set the button to be disabled
            print(f"Button at row {row_index}, column {col_index} disabled")
        else:
            print(f"No button at row {row_index}, column {col_index}")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('QTableWidget Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyTableWidget()
    sys.exit(app.exec_())