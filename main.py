from kivy.uix.widget import Widget, WidgetException
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager

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
    except ConnectionResetError as er:
        print(f"connection reset error {er}")
    except Exception as e:
        print(f"Error updating frame: {e}")


def create_texture_from_frame(frame):
    texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
    texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
    texture.flip_vertical()
    return texture


class ElevatedMenu(Widget):
    pass


class SpaceDesktop(MDScreen):
    pass


class StreamingScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = create_socket(IP, 10000)

    def on_enter(self, *args):
        Clock.schedule_interval(lambda dt: update_frame(self.ids.streaming_img, self.socket, dt), 1.0 / 60.0)


class SpaceDesktopApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img = None
        self.socket = None
        self.sm = ScreenManager()  # to manage screens. sm - ScreenManager

    def build(self):
        global callback
        self.img = Image()
        self.sm.add_widget(SpaceDesktop(name="main_screen"))
        self.sm.add_widget(StreamingScreen(name="streaming_screen"))
        # Clock.schedule_interval(lambda dt: update_frame(self.img, self.socket, dt), 1.0 / 60.0)
        # self.socket = create_socket(IP)  # Replace 'PC_IP_ADDRESS' with your PC's IP address
        self.theme_cls.theme_style = "Dark"
        return self.sm

    def btn1_callback(self, *args, **kwargs):
        global callback
        self.img.size = self.root.size
        if callback:
            callback = False
            self.root.clear_widgets()
            self.root.add_widget(SpaceDesktop())
        else:
            callback = True
            btn = MDFlatButton(
                text="Hello, World!",
                on_release=self.btn1_callback,
                md_bg_color=[1, 1, 1, 1],
                theme_text_color="Custom",
                text_color=[0, 0, 0, 0]
            )
            self.root.clear_widgets()
            self.root.add_widget(btn)
            self.root.add_widget(self.img)

    def btn_start_streaming(self):
        self.sm.current = 'streaming_screen'

    def btn_stop_streaming(self):
        self.sm.current = 'main_screen'
        # TODO Stop button must to close connect with server | 
        # there is some part of code 👇
        
        """
        stream = self.sm.get_screen("streaming_screen")
        if stream:
            stream.socket.close()
            stream.socket = None
    
        # Остановка таймера обновления кадров
        Clock.unschedule(None)
        self.sm.current = "main_screen"
        """

if __name__ == '__main__':
    SpaceDesktopApp().run()
