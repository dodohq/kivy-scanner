from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.lang import Builder

class RootWidget(BoxLayout):

   def __init__(self, **kwargs):
       super(RootWidget, self).__init__(**kwargs)
       
       load_btn = Button(text='Load parcel')
       load_btn.bind(pressed=self.load_pressed)
       self.add_widget(load_btn)
       cb = CustomBtn()
       cb.bind(pressed=self.btn_pressed)
       self.add_widget(cb)
       self.add_widget(Button(text='Get parcel'))

   def btn_pressed(self, instance, pos):
       print ('pos: printed from root widget: {pos}'.format(pos=pos))

class CustomBtn(Widget):

   pressed = ListProperty([0, 0])

   def on_touch_down(self, touch):
       if self.collide_point(*touch.pos):
           self.pressed = touch.pos
           # we consumed the touch. return False here to propagate
           # the touch further to the children.
           return True
       return super(CustomBtn, self).on_touch_down(touch)

   def on_pressed(self, instance, pos):
       print ('pressed at {pos}'.format(pos=pos))

class GuiApp(App):

   def build(self):
       return RootWidget()


if __name__ == '__main__':
   GuiApp().run()
