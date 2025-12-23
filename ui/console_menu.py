from datetime import date
from service.task_service import TaskService


class ConsoleMenu:

    def __init__(self):
        self.service = TaskService()

    def show(self):
        while True:
            self._print_menu()
            option = input("Escolha uma opção: ")

            if option == "0":
                break
            elif option == "1":
                self._list_tasks()
            elif option == "2":
                self._edit_task()
            elif option == "3":
                self._delete_task()
            elif option == "4":
                self._add_task()
            elif option == "5":
                self._complete_task()

    def _print_menu(self):
        print("\n--- Gerenciador de Tarefas ---")
        print("0 - Sair")
        print("1 - Listar tarefas")
        print("2 - Editar tarefa")
        print("3 - Apagar tarefa")
        print("4 - Incluir nova tarefa")
        print("5 - Concluir tarefa")

    def _list_tasks(self):
        for task in self.service.list_tasks():
            print(
                f"[{task.id}] {task.description} | "
                f"Até: {task.due_date} | Status: {task.status}"
            )

    def _add_task(self):
        desc = input("Descrição: ")
        due = date.fromisoformat(input("Data limite (YYYY-MM-DD): "))
        self.service.add_task(desc, due)

    def _edit_task(self):
        task_id = int(input("ID da tarefa: "))
        desc = input("Nova descrição: ")
        due = date.fromisoformat(input("Nova data limite (YYYY-MM-DD): "))
        self.service.edit_task(task_id, desc, due)

    def _complete_task(self):
        task_id = int(input("ID da tarefa: "))
        self.service.complete_task(task_id)

    def _delete_task(self):
        task_id = int(input("ID da tarefa: "))
        self.service.delete_task(task_id)
