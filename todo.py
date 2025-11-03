tarefas = []

def mostrar_tarefas():
    if not tarefas:
        print("Nenhuma tarefa adicionada ainda.")
    else:
        print("Suas tarefas:\n")
        for i in range(len(tarefas)):
            tarefa = tarefas[i]
            status = "✅" if tarefa["feita"] else "❌"
            print(f"{i+1}. {tarefa['titulo']} [{status}]")
    print()

def adicionar_tarefa():
    titulo = input("Digite a nova tarefa: ")
    tarefas.append({"titulo": titulo, "feita":False})
    print(f"Tarefa '{titulo}' adicionada!\n")

def marcar_como_feita():
    mostrar_tarefas()
    if tarefas:
        try:
            num = int(input("Digite o numero da tarefa concluida: "))
            tarefas[num-1]["feita"] = True
            print("Tarefa marcada como feita!\n")
        except (ValueError, IndexError):
            print("Número inválido.\n")

def remover_tarefa():
    mostrar_tarefas()
    if tarefas:
        try:
            num = int(input("Digite o numero da tarefa para remover:"))
            if 1 <= num <= len(tarefas):
                tarefa = tarefas.pop(num-1)
                print(f"Tarefa '{tarefa['titulo']}' removida!\n")
        except (ValueError, IndexError):
            print("Número inválido.\n")

def sair():
    print("Saindo...")
    return "sair"

def menu():
    while True:
        print("=== To-do List ===")
        print("1. Ver tarefas")
        print("2. Adicionar tarefa")
        print("3. Marcar como feita")
        print("4. Remover tarefa")
        print("5. Sair")
        opcao = input("Escolha uma opcao: ")
        acoes = {
            "1":mostrar_tarefas,
            "2":adicionar_tarefa,
            "3":marcar_como_feita,
            "4":remover_tarefa,
            "5": sair
        }
        acao = acoes.get(opcao, lambda: print("Opcao inválida\n"))
        if acao() == "sair":
            return 0
    return 1

if __name__ == "__main__":
    running = 1
    while running == 1:
        running = menu()


