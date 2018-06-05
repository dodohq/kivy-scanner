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

class MainApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MainApp().run()
