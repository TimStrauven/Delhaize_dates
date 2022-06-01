from kivy.app import App
from kivy.uix.camera import Camera
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from kivy.utils import platform
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.label import Label
import requests
from text_date_extraction import extract_date

if platform == 'android':
    # Android specific imports
    # looks like error but works fine on android
    from android.permissions import request_permissions, Permission

class CamTextures(Camera):

    def on_texture_size(self, instance, value):
        self.build()

    def build(self):
        #self.clear_widgets()
        texture = self.texture
        if not texture:
            return
        tw, th = self.texture_size

        subtexture = texture.get_region(0, 0, tw, th)
        node = Scatter(pos=(0, 0), size=(tw, th))
        with node.canvas:
            Color(0.5, 0.5, 0.5)
            Rectangle(size=node.size, texture=subtexture)
        self.add_widget(node)

        crop_w = 200
        crop_h = 50
        zoom = 0.2  # something between 0.1 and 0.6 works well
        zoompix_w = crop_w * zoom
        zoompix_h = crop_h * zoom

        crop_subtexture = texture.get_region((tw / 2) - (crop_w / 2) + (zoompix_w / 2),
                                             (th / 2) - (crop_h / 2) + (zoompix_h / 2),
                                             (crop_w - zoompix_w), (crop_h - zoompix_h))
        crop_node = Scatter(pos=((tw / 2) - (crop_w / 2), (th / 2) - (crop_h / 2)),
                            size=(crop_w, crop_h))
        with crop_node.canvas:
            Color(1, 1, 1)
            Rectangle(size=crop_node.size, texture=crop_subtexture)
        self.crop_subtexture = crop_subtexture
        self.add_widget(crop_node)
        self.lbl = Label(text='', pos=((tw / 2) - (crop_w / 2), (th / 2) - (2 * crop_h)),
                    size=(crop_w, crop_h), font_size=25)
        self.add_widget(self.lbl)
        self.capturing = True
        self.triggercount = 0
        self.date = ""
        self.datefound = False
        Clock.schedule_once(self.get_frame, 0.5)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.capturing:
                self.capturing = False
            else:
                self.capturing = True
                self.datefound = False
                Clock.schedule_once(self.get_frame, 0.25)
            return True

    def get_frame(self, dt):
        if self.capturing:
            img = Image(self.crop_subtexture)
            img.save('my_capture.png')

            url = 'http://127.0.0.1:5000/cropped'
            files = {'image': open('my_capture.png', 'rb')}
            req = requests.post(url, files=files)
            self.date = req.text
            self.lbl.text = "Detecting dates... " + '\n' + self.date
            self.lbl.color = (1, 1, 1)
            corrected_Date = extract_date(self.date)
            if corrected_Date is not False:
                self.triggercount += 1
                self.lbl.text = corrected_Date
                if self.triggercount > 2:
                    self.capturing = False
                    self.triggercount = 0
                    self.datefound = True
            else:
                self.triggercount = 0
            Clock.schedule_once(self.get_frame, 0.5)
        else:
            if self.datefound:
                self.lbl.text = "Date detected:" + '\n' + self.date
                self.lbl.color = (0, 1, 0)
            else:
                self.lbl.text = 'Capturing stopped.'
                self.lbl.color = (1, 1, 1)


class DelhaizeApp(App):
    def build(self):
        if platform == 'android':
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])

        root = Widget()
        Camtex = CamTextures(resolution=(640, 480), play=True)
        root.add_widget(Camtex)
        return root

DelhaizeApp().run()
