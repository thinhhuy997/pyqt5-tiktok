import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal, Qt

class MySignals(QObject):
    resultReady = pyqtSignal(int)

class MyRunnable(QRunnable):
    def __init__(self, signals, value):
        super(MyRunnable, self).__init__()
        self.signals = signals
        self.value = value

    def run(self):
        # Simulate some time-consuming task
        import time
        time.sleep(2)
        
        result = self.value * 2

        # Emit the result using the custom signal
        self.signals.resultReady.emit(result)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Result: ")
        self.layout.addWidget(self.label)

        self.worker_count_label = QLabel("Number of Running Workers: 0")
        self.layout.addWidget(self.worker_count_label)

        self.start_button = QPushButton("Start Task")
        self.start_button.clicked.connect(self.start_task)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop All Workers")
        self.stop_button.clicked.connect(self.stop_all_workers)
        self.layout.addWidget(self.stop_button)

        # Set up custom signals
        self.signals = MySignals()

        # Set up thread pool
        self.thread_pool = QThreadPool.globalInstance()

    def start_task(self):
        # Create a runnable with a specific value
        my_runnable = MyRunnable(self.signals, 5)

        # Connect the custom signal to the update_label slot
        self.signals.resultReady.connect(self.update_label)

        # Queue the runnable in the thread pool
        self.thread_pool.start(my_runnable)

        # Update the number of running workers
        self.update_worker_count()

    def update_label(self, result):
        # Update the label with the result
        self.label.setText("Result: {}".format(result))

    def update_worker_count(self):
        # Update the label with the number of running workers
        count = self.thread_pool.activeThreadCount()
        self.worker_count_label.setText("Number of Running Workers: {}".format(count))

    def stop_all_workers(self):
        # Remove all workers from the thread pool
        self.thread_pool.clear()
        self.update_worker_count()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())