from kivy.uix.widget import Widget, WidgetException
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.button import MDFlatButton

from myIP import IP

import socket
import cv2
import numpy as np

callback = False


def create_socket(ip, port=10000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s


def update_frame(img, sock, dt):
    global callback
    try:
        size = int.from_bytes(sock.recv(4), byteorder='big')
        frame_data = sock.recv(size, socket.MSG_WAITALL)  # Efficiently receive all data at once
        np_data = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.texture = create_texture_from_frame(frame)
    except Exception as e:
        print(f"Error updating frame: {e}")


def create_texture_from_frame(frame):
    texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
    texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
    texture.flip_vertical()
    return texture


class HostCard(Widget):
    pass


class SpaceDesktop(Widget):
    pass


class SpaceDesktopApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img = None
        self.socket = None

    def build(self):
        global callback
        self.img = Image()
        Clock.schedule_interval(lambda dt: update_frame(self.img, self.socket, dt), 1.0 / 60.0)
        self.socket = create_socket(IP)  # Replace 'PC_IP_ADDRESS' with your PC's IP address
        self.theme_cls.theme_style = "Dark"
        return SpaceDesktop()

    def btn1_callback(self, *args, **kwargs):
        global callback
        self.img.size = self.root.size
        if callback:
            callback = False
            self.root.clear_widgets()
            btn = MDFlatButton(text="HAHA", on_release=self.btn1_callback)
            self.root.add_widget(SpaceDesktop())
            return
        else:
            callback = True
            try:
                self.root.add_widget(self.img)
            except WidgetException:
                return


if __name__ == '__main__':
    SpaceDesktopApp().run()
