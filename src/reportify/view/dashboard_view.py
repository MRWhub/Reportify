from dotenv import load_dotenv
import os
import getpass
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from dotenv import load_dotenv, find_dotenv
import os
import getpass

class CredentialsLoader:
    def __init__(self, dotenv_path=None):
        """
        Classe responsável por carregar credenciais de um arquivo .env ou do input do usuário.

        :param dotenv_path: Caminho opcional para o arquivo .env.
        """
        if dotenv_path:
            dotenv_file = os.path.abspath(dotenv_path)
        else:
            dotenv_file = find_dotenv()

        if dotenv_file and os.path.exists(dotenv_file):
            load_dotenv(dotenv_file)
            print(f"🔍 Carregando .env encontrado em: {dotenv_file}")
        else:
            print("⚠️ Arquivo .env não encontrado. As credenciais serão solicitadas manualmente.")

        self.token = None
        self.repository = None

    def load(self):
        """
        Carrega as credenciais de variáveis de ambiente ou solicita via input.

        :return: token, repository
        """
        self.token = os.getenv("GITHUB_TOKEN")
        self.repository = os.getenv("GITHUB_REPOSITORY")

        if not self.token:
            self.token = getpass.getpass("🔑 Digite seu GITHUB_TOKEN: ")

        if not self.repository:
            self.repository = input("📦 Digite o GITHUB_REPOSITORY (ex: user/repo): ")

        print("\n✅ Credenciais carregadas com sucesso!")
        print(f"📦 Repositório: {self.repository}")
        print(f"🔑 Token: {self.token[:4]}... (oculto)")

        return self.token, self.repository
