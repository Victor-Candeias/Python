import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import QTimer
import serial

class SerialMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial = serial.Serial('COM9', 9600, timeout=1)
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 400, 300)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(100)  # Verifica a porta a cada 100ms

    def read_serial(self):
        if self.serial.in_waiting > 0:
            data = self.serial.readline().decode('utf-8').strip()
            self.text_edit.append(f"Recebido: {data}")

    def closeEvent(self, event):
        self.serial.close()

app = QApplication(sys.argv)
monitor = SerialMonitor()
monitor.show()
sys.exit(app.exec_())
