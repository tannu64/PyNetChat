import sys
import socket
import threading
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QObject

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Client(QMainWindow):
    update_signal = pyqtSignal(str)  # Signal to update the text display safely from another thread

    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.initUI()
        self.update_signal.connect(self.updateDisplay)  # Connect the signal to the slot

    def initUI(self):
        self.setWindowTitle('Client')
        self.setGeometry(600, 300, 350, 250)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.textDisplay = QTextEdit()
        self.textDisplay.setReadOnly(True)
        layout.addWidget(self.textDisplay)

        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit)

        self.connectButton = QPushButton('Connect', self)
        self.connectButton.clicked.connect(self.connectToServer)
        layout.addWidget(self.connectButton)

        self.sendButton = QPushButton('Send', self)
        self.sendButton.clicked.connect(self.sendMessage)
        self.sendButton.setEnabled(False)  # Disabled until connected
        layout.addWidget(self.sendButton)

        self.disconnectButton = QPushButton('Disconnect', self)
        self.disconnectButton.clicked.connect(self.disconnectFromServer)
        self.disconnectButton.setEnabled(False)  # Disabled until connected
        layout.addWidget(self.disconnectButton)

    def connectToServer(self):
        if not self.client_socket:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect(('127.0.0.1', 12345))
                self.textDisplay.append('Connected to server.')
                self.sendButton.setEnabled(True)
                self.disconnectButton.setEnabled(True)
                threading.Thread(target=self.receiveMessages, daemon=True).start()
            except Exception as e:
                logging.error("Failed to connect to server: %s", str(e))
                self.textDisplay.append(f'Failed to connect to server: {str(e)}')

    def receiveMessages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.update_signal.emit(message)
                else:
                    raise Exception("Socket closed")
            except Exception as e:
                self.update_signal.emit(f'Disconnected from server: {str(e)}')
                self.disconnectFromServer()
                break

    def sendMessage(self):
        message = self.lineEdit.text()
        try:
            self.client_socket.send(message.encode())
            self.textDisplay.append(f'You: {message}')
            self.lineEdit.clear()
        except Exception as e:
            logging.error("Failed to send message: %s", str(e))
            self.textDisplay.append(f'Failed to send message: {str(e)}')

    def disconnectFromServer(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            self.textDisplay.append('Disconnected from server.')
            self.sendButton.setEnabled(False)
            self.disconnectButton.setEnabled(False)
            logging.info("Disconnected from server.")

    def updateDisplay(self, message):
        self.textDisplay.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Client()
    ex.show()
    sys.exit(app.exec_())
