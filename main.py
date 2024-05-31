import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import socket
import cv2
import numpy as np

class VideoStreamApp(App):
    def build(self):
        self.img = Image()
        Clock.schedule_interval(self.update_frame, 1.0/30.0)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('192.168.0.14', 8080))  # Replace 'PC_IP_ADDRESS' with your PC's IP address
        return self.img

    def update_frame(self, dt):
        # Receive frame size
        size = int.from_bytes(self.socket.recv(4), byteorder='big')
        
        # Receive frame data
        frame_data = b''
        while len(frame_data) < size:
            packet = self.socket.recv(size - len(frame_data))
            if not packet:
                return
            frame_data += packet
        
        # Decode and display frame
        np_data = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.img.texture = self.create_texture_from_frame(frame)

    def create_texture_from_frame(self, frame):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

if __name__ == '__main__':
    VideoStreamApp().run()
