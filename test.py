from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class ButtonCellWidget(QWidget):
    def __init__(self, parent=None):
        super(ButtonCellWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.button = QPushButton()
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("QTableWidget with Buttons")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self.central_widget)

        table_widget = QTableWidget(self)
        table_widget.setColumnCount(2)
        table_widget.setRowCount(3)

        # Populate the table with buttons
        for row in range(3):
            for col in range(2):
                button_widget = ButtonCellWidget()
                button_widget.button.setText(f"Button {row}-{col}")
                button_widget.button.clicked.connect(self.button_clicked)

                table_widget.setCellWidget(row, col, button_widget)
                table_widget.setItem(row, col, QTableWidgetItem())

        layout.addWidget(table_widget)

    def button_clicked(self):
        button = self.sender()
        if isinstance(button, QPushButton):
            print(f"Button clicked: {button.text()}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())