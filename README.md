# PyNetChat

A user-friendly, Python-based chat application that enables real-time communication through a simple GUI interface using PyQt5.

## Features

- Client-server architecture for network communication
- Real-time messaging with multiple clients
- Clean graphical user interface built with PyQt5
- Server logging functionality
- Cross-platform compatibility (optimized for Windows 10+)

## Prerequisites

- Windows 10 or higher
- Python 3.7 or higher
- PyQt5 library

## Installation

1. Ensure Python is installed:
   ```
   python --version
   ```
   If not installed, download from [python.org](https://www.python.org/downloads/) and tick "Add Python to PATH" during installation.

2. Install PyQt5:
   ```
   pip install PyQt5
   ```

## Usage

### Starting the Server

1. Navigate to the project directory:
   ```
   cd path\to\your\project\folder
   ```

2. Launch the server:
   ```
   python servergui.py
   ```

3. Click "Start Server" in the server GUI to begin listening for connections.

### Starting a Client

1. Navigate to the project directory:
   ```
   cd path\to\your\project\folder
   ```

2. Launch the client:
   ```
   python clientgui.py
   ```

3. Click "Connect" to connect to the server.
4. Use the input box and "Send" button to communicate.
5. Click "Disconnect" to end the session.

Multiple clients can connect from different hosts simultaneously.

## Server Logs

Communication between server and clients is logged in `server.log` in the server's directory.

## Project Structure

- `servergui.py`: Server module with GUI
- `clientgui.py`: Client module with GUI

## License

[MIT](LICENSE) 