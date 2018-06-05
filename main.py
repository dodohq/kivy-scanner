from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

presentation = Builder.load_file("main.kv")

class MainScreen(Screen):
  pass
  
class LoadScreen(Screen):
  pass
  
class UnlockScreen(Screen):
  pass
    
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(LoadScreen(name='load'))
sm.add_widget(UnlockScreen(name='unlock'))


class Scanner(Widget):

   def on_touch_down(self, touch):
       if self.collide_point(*touch.pos):
           self.pressed = touch.pos
           # we consumed the touch. return False here to propagate
           # the touch further to the children.
           return True
       return super(CustomBtn, self).on_touch_down(touch)

   def on_pressed(self, instance, pos):
       print ('pressed at {pos}'.format(pos=pos))

class MainApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MainApp().run()
