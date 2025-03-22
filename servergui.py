import sys
import socket
import threading
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='server.log', filemode='a')

class Server(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.clients = []  # This will now hold dictionaries for better client management
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Server')
        self.setGeometry(300, 300, 350, 250)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.textDisplay = QTextEdit()
        self.textDisplay.setReadOnly(True)
        layout.addWidget(self.textDisplay)

        self.startButton = QPushButton('Start Server', self)
        self.startButton.clicked.connect(self.startServer)
        layout.addWidget(self.startButton)

        self.stopButton = QPushButton('Stop Server', self)
        self.stopButton.clicked.connect(self.stopServer)
        layout.addWidget(self.stopButton)

    def startServer(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 12345))
        self.server_socket.listen()
        self.textDisplay.append('Server started...')
        logging.info("Server started.")
        threading.Thread(target=self.accept_clients).start()

    def stopServer(self):
        while self.clients:
            client_info = self.clients.pop()
            client_info['socket'].close()
        if self.server_socket:
            self.server_socket.close()
        self.textDisplay.append('Server stopped.')
        logging.info("Server stopped.")

    def accept_clients(self):
        while True:
            try:
                client_sock, addr = self.server_socket.accept()
                client_info = {'socket': client_sock, 'address': addr}
                self.clients.append(client_info)
                self.textDisplay.append(f'Connected with {addr}')
                logging.info(f'Client connected: {addr}')
                threading.Thread(target=self.handle_client, args=(client_info,)).start()
            except Exception as e:
                logging.error(f"Error accepting client: {e}")
                break

    def handle_client(self, client_info):
        client_sock = client_info['socket']
        addr = client_info['address']
        while True:
            try:
                message = client_sock.recv(1024).decode()
                if not message:
                    raise ConnectionResetError("Client disconnected")
                broadcast_message = f'Received from {addr}: {message}'
                self.textDisplay.append(broadcast_message)
                self.broadcast(broadcast_message, client_info)
                self.log_client_activity(client_info, message)
            except ConnectionResetError as e:
                self.textDisplay.append(f'Disconnected from {addr}')
                logging.info(f'Disconnected from {addr}: {e}')
                self.clients.remove(client_info)
                client_sock.close()
                break
            except Exception as e:
                logging.error(f"Error handling client {addr}: {e}")

    def broadcast(self, message, sender_info):
        for client_info in self.clients:
            if client_info != sender_info:
                try:
                    client_info['socket'].send(message.encode())
                except Exception as e:
                    logging.error(f"Error broadcasting to {client_info['address']}: {e}")
                    client_info['socket'].close()
                    self.clients.remove(client_info)

    def log_client_activity(self, client_info, message):
        with open('client_activity.log', 'a') as f:
            f.write(f"{client_info['address']} - {message}\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Server()
    ex.show()
    sys.exit(app.exec_())
