from myIP import IP

import cv2
import socket
import numpy as np
import pyautogui


# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, 10000))
server_socket.listen(0)

connection, address = server_socket.accept()
print(f"Connection from: {address}")


# Capture screen and stream
while True:
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
    
    # Encode frame
    ret, buffer = cv2.imencode('.png', frame)
    if not ret:
        continue
    
    # Send frame size and frame
    size = len(buffer)
    connection.sendall(size.to_bytes(4, byteorder='big'))
    connection.sendall(buffer.tobytes())
    """try:
        connection.sendall(size.to_bytes(4, byteorder='big'))
        connection.sendall(buffer.tobytes())
    except ConnectionResetError:
        pass
"""