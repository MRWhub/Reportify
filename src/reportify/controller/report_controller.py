from model.dashboard.dashboard_developer import DeveloperStats
from model.dashboard.dashboard_organization import OrganizationalDashboard
from model.dashboard.dashboard_repository import GitHubIssueStats
from model.dashboard.dashboard_team import TeamStats
from model.dashboard.dashboard_team_graph import CollaborationGraph
from view.dashboard_view import CredentialsLoader
import os
class ReportController:
    def __init__(self, salvar_markdown, report_dir,token=None,git_repo=None):
        self.save_func = salvar_markdown
        self.report_dir = report_dir
        self.token = token
        self.git_repo = git_repo

    def gerar_todos(self):
        #DeveloperStats(save_func=self.save_func, save_directory=self.report_dir,token=self.token,repo=self.git_repo).run()
        #OrganizationalDashboard(save_func=self.save_func, report_dir=self.report_dir,token=self.token,repo=self.git_repo).run()
        GitHubIssueStats(save_func=self.save_func, report_dir=self.report_dir,token=self.token,repo=self.git_repo).run()
       # TeamStats(save_func=self.save_func, report_dir=self.report_dir).run()
        # CollaborationGraph(save_func=self.save_func, report_dir=self.report_dir).run()
    def open_view(self):
        

        credentials_loader = CredentialsLoader()
        token, repository = credentials_loader.load()
        self.token = token
        self.git_repo = repository
        print('🔑 Usando repositório:', self.git_repo, f'com token: {self.token[:4]}... (ocultando o restante)')
        print('📂 Diretório atual de execução:', os.getcwd())
        self.gerar_todos()