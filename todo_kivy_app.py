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
kivy.require('2.1.0')

try:
    from todo_terminal_json import carregar_tarefas, salvar_tarefas, ARQUIVO_JSON
except ImportError:
    print("ERRO: Não foi possível encontrar o arquivo 'todo_terminal_json.py'")
    def carregar_tarefas(): return []
    def salvar_tarefas(tarefas): pass
    ARQUIVO_JSON = "tarefas.json"

Window.clearcolor = (0.1,0.1,0.1,1) # Um cinza claro como cor de fundo

class TaskWidget(BoxLayout):
    def __init__(self, task_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "48dp"
        self.spacing = "10dp"

        self.task_data = task_data
        self.task_text = task_data["titulo"]
        self.is_done = task_data["feita"]

        self.task_checkbox = CheckBox(
            active = self.is_done,
            size_hint_x = None,
            width = "48dp"
        )
        self.task_checkbox.bind(active = self.on_checkbox_active)

        self.task_label = Label(
            text = self.task_text,
            font_size = "16sp",
            markup = True
        )

        self.remove_button = Button(
            text = "Remover",
            size_hint_x = None,
            width = "100dp"
        )
        self.remove_button.bind(on_press = self.remove_task)

        self.add_widget(self.task_checkbox)
        self.add_widget(self.task_label)
        self.add_widget(self.remove_button)

        self.update_label_visual(self.is_done)
    
    def on_checkbox_active(self, checkbox_instance, is_active):
        self.update_label_visual(is_active)

    def update_label_visual(self, is_active):
        if is_active:
            self.task_label.text = f"[s]{self.task_text}[/s]"
        else:
            self.task_label.text = self.task_text

    def remove_task(self, button_instance):
        if self.parent:
            self.parent.remove_widget(self)

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.padding = "10dp"

        self.add_bar_layout = BoxLayout(
            orientation = "horizontal",
            size_hint_y = None,
            height = "48dp"
        )

        self.text_input = TextInput(
            hint_text = "Digite uma nova tarefa...",
            size_hint_x = 0.75,
            font_size = "18sp"
        )
        self.add_button = Button(
            text = "Adicionar",
            size_hint_x = 0.25,
            font_size = "18sp"
        )

        self.add_button.bind(on_press = self.add_task_pressed)

        self.add_bar_layout.add_widget(self.text_input)
        self.add_bar_layout.add_widget(self.add_button)

        self.scroll_view = ScrollView()

        self.task_list_layout = GridLayout(
            cols = 1,
            size_hint_y = None
        )

        self.task_list_layout.bind(minimum_height = self.task_list_layout.setter("height"))

        self.scroll_view.add_widget(self.task_list_layout)

        self.add_widget(self.add_bar_layout)
        self.add_widget(self.scroll_view)
    
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