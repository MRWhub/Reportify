from dotenv import load_dotenv
import os
import getpass
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
import getpass
from reportify.model.exceptions.exit_blank_choice_exception import ExitNoChoice
class CredentialsLoader:
    def __init__(self):


        load_dotenv()


        self.token = None
        self.repository = None

    def load(self):
        """
        Carrega as credenciais de variáveis de ambiente ou solicita via input.
r
        :return: token, repository
        """
        self.token = os.getenv("GITHUB_TOKEN")
        self.repository = os.getenv("GITHUB_REPOSITORY")

        if not self.token:
            self.token = getpass.getpass("🔑 Digite seu GITHUB_TOKEN: ")

        if not self.repository:
            self.repository = input("📦 Digite o GITHUB_REPOSITORY (ex: user/repo): ")

        print("\n✅ Credenciais carregadas com sucesso!")


        return self.token, self.repository

class DashboardSelection:
    """
    Classe responsável por exibir o menu e capturar a seleção
    dos dashboards que o usuário deseja gerar.
    """

    @staticmethod
    def menu():
        print("\n📊 Selecione os relatórios que deseja gerar:")
        print("1 - Developer Stats")
        print("2 - Organization Stats")
        print("3 - Repository Stats (Issues)")
        print("4 - Team Stats")
        print("5 - Collaboration Graph")
        print("0 - Todos")
        print("ENTER - SAIR")
        selections = input("\nDigite os números separados por vírgula (ex: 1,3,5 ou 0 para todos): ")
        selections = selections.replace(" ", "").split(",")
        if selections == [""]:
            raise ExitNoChoice("Nenhuma seleção feita. Saindo...")
        if "0" in selections:
            selections = ["1", "2", "3", "4", "5"]

        print(f"\n🚀 Gerando os relatórios selecionados: {selections}")
        return selections
