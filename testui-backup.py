import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QLineEdit, QPushButton

class MyTabsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QTabWidget Example')

        # Create a QTabWidget
        tab_widget = QTabWidget(self)

        # Create tabs and add them to the QTabWidget
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Add widgets to each tab
        self.add_widgets_to_tab(tab1, 'Tab 1 Content')
        self.add_widgets_to_tab(tab2, 'Tab 2 Content')
        self.add_widgets_to_tab(tab3, 'Tab 3 Content')

        tab_widget.addTab(tab1, 'Tab 1')
        tab_widget.addTab(tab2, 'Tab 2')
        tab_widget.addTab(tab3, 'Tab 3')

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(tab_widget)

        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 300)

    def add_widgets_to_tab(self, tab, content):
        # Example: Add widgets to each tab
        label = QLabel(content, tab)
        line_edit = QLineEdit(tab)
        button = QPushButton('Click me', tab)

        layout = QVBoxLayout(tab)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyTabsApp()
    ex.show()
    sys.exit(app.exec_())