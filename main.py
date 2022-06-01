from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty
import numpy as np
import cv2
from kivy.utils import platform

if platform == 'android':
    # Android specific imports
    # looks like error but works fine on android
    from android.permissions import request_permissions, Permission

Builder.load_file('camera.kv')


class AndroidCamera(Camera):
    camera_resolution = (640, 480)
    cam_ratio = camera_resolution[0] / camera_resolution[1]
    #boundbox = (-camera_resolution[0] / 2, -camera_resolution[1] / 2, camera_resolution[0] / 2, camera_resolution[1] / 2)
    boundbox = (0, 0, 0, 0)

    def on_tex(self, camera):
        self.texture = texture = camera.texture
        # get some region
        self.texture = self.texture.get_region(0, 0, 640, 480)
        self.texture_size = list(texture.size)
        self.canvas.ask_update()


class MyLayout(BoxLayout):
    def capture(self):
        app = App.get_running_app()
        app.get_frame(0)


class MyApp(App):
    counter = 0

    if platform == 'android':
        rotation = NumericProperty(-90)
    else:
        rotation = NumericProperty(0)

    def build(self):
        if platform == 'android':
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])

        return MyLayout()

    def on_start(self):
        # Clock.schedule_once(self.get_frame, 3)
        pass

    def get_frame(self, dt):
        cam = self.root.ids.a_cam
        image_object = cam.export_as_image(
            scale=round((400 / int(cam.height)), 2))
        w, h = image_object._texture.size
        frame = np.frombuffer(image_object._texture.pixels,
                              'uint8').reshape(h, w, 4)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
        self.root.ids.frame_counter.text = f'frame: {self.counter}'
        self.counter += 1
        # Clock.schedule_once(self.get_frame, 0.25)


if __name__ == "__main__":
    MyApp().run()