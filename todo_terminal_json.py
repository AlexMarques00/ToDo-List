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

def mostrar_tarefas(tarefas):
    if not tarefas:
        print("Nenhuma tarefa adicionada ainda.")
    else:
        print("Suas tarefas:\n")
        for i in range(len(tarefas)):
            tarefa = tarefas[i]
            status = "✅" if tarefa["feita"] else "❌"
            print(f"{i+1}. {tarefa['titulo']} [{status}]")
    print()

def adicionar_tarefa(tarefas):
    titulo = input("Digite a nova tarefa: ")
    tarefas.append({"titulo": titulo, "feita":False})
    print(f"Tarefa '{titulo}' adicionada!\n")

def marcar_como_feita(tarefas):
    mostrar_tarefas(tarefas)
    if tarefas:
        try:
            num = int(input("Digite o numero da tarefa concluida: "))
            tarefas[num-1]["feita"] = True
            print("Tarefa marcada como feita!\n")
        except (ValueError, IndexError):
            print("Número inválido.\n")

def remover_tarefa(tarefas):
    mostrar_tarefas(tarefas)
    if tarefas:
        try:
            num = int(input("Digite o numero da tarefa para remover: "))
            if 1 <= num <= len(tarefas):
                tarefa = tarefas.pop(num-1)
                print(f"Tarefa '{tarefa['titulo']}' removida!\n")
        except (ValueError, IndexError):
            print("Número inválido.\n")

def sair(tarefas):
    salvar_tarefas(tarefas)
    print("Saindo...")
    return "sair"

def menu(tarefas):
    print("=== To-do List ===")
    print("1. Ver tarefas")
    print("2. Adicionar tarefa")
    print("3. Marcar como feita")
    print("4. Remover tarefa")
    print("5. Salvar e Sair")
    opcao = input("Escolha uma opcao: ")
    acoes = {
        "1": lambda: mostrar_tarefas(tarefas),
        "2": lambda: adicionar_tarefa(tarefas),
        "3": lambda: marcar_como_feita(tarefas),
        "4": lambda: remover_tarefa(tarefas),
        "5": lambda: sair(tarefas)
    }
    acao = acoes.get(opcao, lambda: print("Opcao inválida\n"))
    if acao() == "sair":
        return 0
    return 1

if __name__ == "__main__":
    running = 1
    tarefas = carregar_tarefas()
    while running == 1:
        running = menu(tarefas)


