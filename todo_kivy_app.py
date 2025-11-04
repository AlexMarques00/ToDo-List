# Cores usadas no app retiradas de:
# https://rgbacolorpicker.com

import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
kivy.require('2.1.0')

try:
    from todo_terminal_json import carregar_tarefas, salvar_tarefas, ARQUIVO_JSON
except ImportError:
    print("ERRO: Não foi possível encontrar o arquivo 'todo_terminal_json.py'")
    def carregar_tarefas(): return []
    def salvar_tarefas(tarefas): pass
    ARQUIVO_JSON = "tarefas.json"

Window.clearcolor = (0.01, 0.01, 0.01, 1)

class TaskWidget(BoxLayout):
    def __init__(self, task_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "48dp"
        self.spacing = "10dp"
        self.padding = (0, dp(10), 0, dp(5))

        self.task_data = task_data
        self.task_text = task_data["titulo"]
        self.is_done = task_data["feita"]

        # Definição das cores
        NEON_BLUE = (18/255, 18/255, 178/255, 1)
        LIGHT_TEXT = (1, 1, 1, 1)
        self.BRIGHT_RED = (165/255, 4/255, 4/255, 1)
        self.BRIGHT_RED_DOWN = (120/255, 4/255, 4/255, 1) 
        self.button_radius = dp(10)

        self.task_checkbox = CheckBox(
            active = self.is_done,
            size_hint_x = None,
            width = "48dp",
            color = NEON_BLUE
        )
        self.task_checkbox.bind(active = self.on_checkbox_active)

        self.task_label = Label(
            text = self.task_text,
            font_size = "16sp",
            markup = True,
            color = LIGHT_TEXT
        )

        self.remove_button = Button(
            text = "Remover",
            size_hint_x = None,
            width = "140dp",
            background_normal = '',
            background_color = (0, 0, 0, 0),
            color = LIGHT_TEXT
        )
        with self.remove_button.canvas.before:
            self.remove_button_color = Color(*self.BRIGHT_RED)
            self.remove_button_bg = RoundedRectangle(
                pos = self.remove_button.pos,
                size = self.remove_button.size,
                radius = [self.button_radius]
            )
        
        self.remove_button.bind(pos = self.update_remove_button_canvas, size = self.update_remove_button_canvas)
        self.remove_button.bind(on_press = self.remove_task)
        self.remove_button.bind(state = self.on_remove_button_state)
        
        self.add_widget(self.task_checkbox)
        self.add_widget(self.task_label)
        self.add_widget(self.remove_button)

        self.update_label_visual(self.is_done)
    
    def update_remove_button_canvas(self, instance, value):
        self.remove_button_bg.pos = instance.pos
        self.remove_button_bg.size = instance.size

    def on_remove_button_state(self, instance, value):
        if value == 'down':
            instance.background_color.rgba = self.BRIGHT_RED_DOWN
        else: # value == 'normal'
            instance.background_color.rgba = self.BRIGHT_RED

    def on_checkbox_active(self, checkbox_instance, is_active):
        self.update_label_visual(is_active)

    def update_label_visual(self, is_active):
        GRAY_HEX = "#808080"
        LIGHT_HEX = "#E6E6E6"
        if is_active:
            self.task_label.text = f"[color={GRAY_HEX}][s]{self.task_text}[/s][/color]"
        else:
            self.task_label.text = f"[color={LIGHT_HEX}]{self.task_text}[/color]"

    def remove_task(self, button_instance):
        if self.parent:
            self.parent.remove_widget(self)


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.padding = "10dp"

        # Definição de cores
        self.NEON_BLUE = (18/255, 18/255, 178/255, 1)
        self.NEON_BLUE_DOWN = (18/255, 18/255, 130/255, 1)
        self.MAIN_BG_COLOR = (0.01, 0.01, 0.01, 1)
        self.BORDER_COLOR = (0.9, 0.9, 0.9, 1)
        self.button_radius = dp(10)
        self.text_input_radius = dp(10)
        LIGHT_TEXT = (0.9, 0.9, 0.9, 1)
        HINT_TEXT_COLOR = (0.5, 0.5, 0.5, 1)

        self.add_bar_layout = BoxLayout(
            orientation = "horizontal",
            size_hint_y = None,
            height = "48dp",
            spacing = dp(10)
        )

        self.text_input = TextInput(
            hint_text = "Digite uma nova tarefa...",
            size_hint_x = 0.75,
            font_size = "18sp",
            background_normal = '',
            background_color = (0, 0, 0, 0),
            foreground_color = LIGHT_TEXT,
            cursor_color = self.NEON_BLUE,
            hint_text_color = HINT_TEXT_COLOR,
            padding = [dp(10), dp(12), dp(10), dp(12)]
        )

        with self.text_input.canvas.before:
            Color(*self.MAIN_BG_COLOR)
            self.text_input_bg = RoundedRectangle(
                pos = self.text_input.pos,
                size = self.text_input.size,
                radius = [self.text_input_radius]
            )
            Color(*self.BORDER_COLOR)
            self.text_input_border = Line(
                rounded_rectangle = (
                    self.text_input.x,
                    self.text_input.y,
                    self.text_input.width,
                    self.text_input.height,
                    self.text_input_radius
                ),
                width = dp(1.2)
            )
        
        self.text_input.bind(pos = self.update_text_input_canvas, size = self.update_text_input_canvas)

        self.add_button = Button(
            text = "Adicionar",
            size_hint_x = 0.25,
            font_size = "18sp",
            background_normal = '',
            background_color = (0, 0, 0, 0),
            color = (1, 1, 1, 1)
        )

        with self.add_button.canvas.before:
            self.add_button_color = Color(*self.NEON_BLUE)
            self.add_button_bg = RoundedRectangle(
                pos = self.add_button.pos,
                size = self.add_button.size,
                radius = [self.button_radius]
            )

        self.add_button.bind(pos=self.update_add_button_canvas, size=self.update_add_button_canvas)
        self.add_button.bind(state = self.on_add_button_state)
        self.add_button.bind(on_press = self.add_task_pressed)

        self.add_bar_layout.add_widget(self.text_input)
        self.add_bar_layout.add_widget(self.add_button)

        self.scroll_view = ScrollView()

        self.task_list_layout = GridLayout(
            cols = 1,
            size_hint_y = None,
            spacing = dp(5)
        )

        self.task_list_layout.bind(minimum_height = self.task_list_layout.setter("height"))

        self.scroll_view.add_widget(self.task_list_layout)

        self.add_widget(self.add_bar_layout)
        self.add_widget(self.scroll_view)

    def update_text_input_canvas(self, instance, value):
        self.text_input_bg.pos = instance.pos
        self.text_input_bg.size = instance.size
        self.text_input_border.rounded_rectangle = (
            instance.x,
            instance.y,
            instance.width,
            instance.height,
            self.text_input_radius
        )
    
    def update_add_button_canvas(self, instance, value):
        self.add_button_bg.pos = instance.pos
        self.add_button_bg.size = instance.size

    def on_add_button_state(self, instance, value):
        if value == 'down':
            instance.background_color.rgba = self.NEON_BLUE_DOWN
        else: # value == 'normal'
            instance.background_color.rgba = self.NEON_BLUE
    
    def add_task_pressed(self, instance):
        task_text = self.text_input.text
        if task_text:
            new_task_data = {"titulo": task_text, "feita": False}
            self.create_task_widget(new_task_data)

            self.text_input.text = ""
    
    def create_task_widget(self, task_data):
        task_widget = TaskWidget(task_data=task_data)
        
        self.task_list_layout.add_widget(task_widget, index = len(self.task_list_layout.children))

class TodoKivyApp(App):
    def build(self):
        self.main_layout = MainLayout()
        return self.main_layout
    
    def on_start(self):
        print(f"App Iniciado! Carregando dados de {ARQUIVO_JSON}...")
        self.tarefas = carregar_tarefas()

        for task_data in self.tarefas:
            self.main_layout.create_task_widget(task_data)

        print(f"Tarefas carregadas: {len(self.tarefas)}")
    
    def on_stop(self):
        print("App fechando! Salvando tarefas...")
        data_to_save = []
        for task_widget in self.main_layout.task_list_layout.children:
            if isinstance(task_widget, TaskWidget):
                data_to_save.append({
                    "titulo": task_widget.task_text,
                    "feita": task_widget.task_checkbox.active
                })
        
        self.tarefas = data_to_save

        salvar_tarefas(self.tarefas)
        print("Tarefas salvas.")
    
if __name__ == "__main__":
    TodoKivyApp().run()