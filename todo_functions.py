import json
import os

ARQUIVO_JSON = "tarefas.json"

def carregar_tarefas():
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, 'r') as f:
                tarefas = json.load(f)
                print("Tarefas carregadas do arquivo!")
                return tarefas
        except Exception as e:
            print(f"Erro ao carregar o arquivo {ARQUIVO_JSON}: {e}")
            return []
    return[]

def salvar_tarefas(tarefas):
    try:
        with open(ARQUIVO_JSON, 'w') as f:
            json.dump(tarefas, f, indent=4)
        print("Tarefas salvas com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}")
