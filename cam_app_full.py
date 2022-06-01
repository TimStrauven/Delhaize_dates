import os
import subprocess
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.utils import platform
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.label import Label
import test_app_model

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
                    size=(crop_w, crop_h))
        self.add_widget(self.lbl)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print('double tap')
            img = Image(self.crop_subtexture)
            img.save('my_capture.png')
            result, image_framed = test_app_model.single_pic_proc('my_capture.png')
            lbltxt = ""
            for key in result:
                print(result[key][1])
                lbltxt += result[key][1] + '\n'
            self.lbl.text = lbltxt
            return True
        #super(CamTextures, self).on_touch_down(touch)


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
