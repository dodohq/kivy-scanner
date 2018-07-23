from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

class Keyboard(Widget):
    def __init__(self, mode, text_input):
        self.mode = mode
        self.text_input = text_input
        self._keyboard_mode = 'dock'
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self)
        if self.mode == "number":
            self.bind_numerical_keyboard()
        elif self.mode == "text":
            self.bind_text_keyboard()
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def bind_numerical_keyboard(self):
        if self._keyboard.widget:
            vkeyboard = self._keyboard.widget
            vkeyboard.layout = 'numeric.json'

    def bind_text_keyboard(self):
        pass

    def _keyboard_closed(self):
        print('My keyboard has been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.text_input.insert_text(keycode[1])
        print('The key', keycode, 'has been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

    def _on_key_up(self, keycode):
        print(keycode)

    def submit(self):
        Window.release_all_keyboards()
