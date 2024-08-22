def adicionar(tarefas):

    """
    Adiciona uma nova tarefa à lista de tarefas.

    Parâmetros:
    - tarefas: lista de dicionários contendo informações sobre as tarefas existentes.

    Uso:
    Chamado quando o usuário deseja adicionar uma nova tarefa ao sistema.
    Solicita ao usuário informações sobre a nova tarefa e a adiciona à lista de tarefas.
    """

    id = int(input("Digite o ID da tarefa: "))
    descricao = input("Digite a descrição da tarefa: ")
    data_de_criacao = input("Digite a data de criação da tarefa (formato YYYY-MM-DD): ")
    prazo_final = input("Digite o prazo final da tarefa (formato YYYY-MM-DD): ")
    urgencia = input("Digite a urgência da tarefa (alta, média, baixa): ")

    nova_tarefa = {
       "id": id,
       "descricao": descricao,
       "data_de_criacao": data_de_criacao,
       "status": "Pendente",
       "prazo_final": prazo_final,
       "urgencia": urgencia
       }
    tarefas.append(nova_tarefa)
    print("Tarefa adicionada com sucesso.")

def listar(tarefas):
    """
    Lista todas as tarefas existentes, separando-as por status (pendentes ou concluídas).

    Parâmetros:
    - tarefas: lista de dicionários contendo informações sobre as tarefas existentes.

    Uso:
    Chamado quando o usuário deseja ver a lista de tarefas existentes.
    Itera sobre as tarefas e imprime suas informações, separadas por status.
    """
    if tarefas:
      print("\nLista de tarefas pendentes:\n")
      for i, tarefa in enumerate(tarefas, 1):
        if tarefa["status"] == "Pendente":
          print(f"{i}.\n - ID: {tarefa['id']}\n- Descrição: {tarefa['descricao']}\n- Data de Criação: {tarefa['data_de_criacao']}\n- Status: {tarefa['status']}\n- Prazo Final: {tarefa['prazo_final']}\n- Urgência: {tarefa['urgencia']}")

      print("\nLista de tarefas concluídas:\n")
      for i, tarefa in enumerate(tarefas, 1):
        if tarefa["status"] == "Concluída":
          print(f"{i}.\n - ID: {tarefa['id']}\n- Descrição: {tarefa['descricao']}\n- Data de Criação: {tarefa['data_de_criacao']}\n- Status: {tarefa['status']}\n- Prazo Final: {tarefa['prazo_final']}\n- Urgência: {tarefa['urgencia']}")

    else:
      print("Não há tarefas para listar")
    return

def marcar(tarefas):
    """
    Marca uma tarefa específica como concluída.

    Parâmetros:
    - tarefas: lista de dicionários contendo informações sobre as tarefas existentes.

    Uso:
    Chamado quando o usuário deseja marcar uma tarefa como concluída.
    Solicita ao usuário o ID da tarefa a ser marcada como concluída e realiza a operação se a tarefa existir.
    """
    id_tarefa = int(input("Digite o ID da tarefa a ser marcada como concluída: "))
    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["status"] = "Concluída"
            print(f"Tarefa com ID {id_tarefa} marcada como concluída")
            return
    print("Tarefa não encontrada")


def remover(tarefas):
    """
    Remove uma tarefa específica da lista de tarefas.

    Parâmetros:
    - tarefas: lista de dicionários contendo informações sobre as tarefas existentes.

    Uso:
    Chamado quando o usuário deseja remover uma tarefa da lista.
    Solicita ao usuário o ID da tarefa a ser removida e realiza a operação se a tarefa existir.
    """
    id_tarefa = int(input("Digite o ID da tarefa a ser removida: "))
    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefas.remove(tarefa)
            print(f"Tarefa com ID {id_tarefa} removida")
            return
    print("Tarefa não encontrada")


def main():
    """
    Função principal que controla o fluxo do programa.

    Uso:
    Inicializa o programa e permite ao usuário interagir com o sistema de gerenciamento de tarefas,
    fornecendo opções de adicionar, listar, marcar como concluída, remover tarefas e encerrar o programa.
    """
    tarefas = []
    while True:
      print("\n---Gerenciamento de tarefas---\n 1-Adicionar tarefa\n 2-Listar tarefas\n 3- Marcar tarefa como concluída\n 4- Remover tarefa\n 5- Encerrar programa ")
      opcao = input("Escolha uma opção: ")

      if opcao == '1':
        adicionar( tarefas)

      elif opcao == '2':
        listar(tarefas)

      elif opcao == '3':
        marcar(tarefas)

      elif opcao == '4':
        remover(tarefas)

      elif opcao == '5':
        break

      else:
        print("Opção inválida")


if __name__ == "__main__":
    main()