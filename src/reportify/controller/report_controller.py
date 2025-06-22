from reportify.model.dashboard.dashboard_developer import DeveloperStats
from reportify.model.dashboard.dashboard_organization import OrganizationalDashboard
from reportify.model.dashboard.dashboard_repository import GitHubIssueStats
from reportify.model.dashboard.dashboard_team import TeamStats
from reportify.model.dashboard.dashboard_team_graph import CollaborationGraph
from reportify.view.dashboard_view import CredentialsLoader, DashboardSelection
from reportify.model.exceptions.team_members_exception import NoTeamMembersError 
from reportify.model.exceptions.exit_blank_choice_exception import ExitNoChoice
import os
class ReportController:
    def __init__(self, salvar_markdown,token=None,git_repo=None):
        self.save_func = salvar_markdown
        self.token = token
        self.git_repo = git_repo

    def gerar_todos(self, selections):
        """Executa os relatórios de acordo com a seleção do usuário."""

        if "1" in selections:
            DeveloperStats(
                save_func=self.save_func,
               
                token=self.token,
                repo=self.git_repo,
            ).run()

        if "2" in selections:
            OrganizationalDashboard(
                save_func=self.save_func,
              
                token=self.token,
                repo=self.git_repo,
            ).run()

        if "3" in selections:
            GitHubIssueStats(
                save_func=self.save_func,
              
                token=self.token,
                repo=self.git_repo,
            ).run()

        if "4" in selections:
            TeamStats(
                save_func=self.save_func,
          
                token=self.token,
                repo=self.git_repo,
            ).run()

        if "5" in selections:
            CollaborationGraph(
                save_func=self.save_func,
              
                token=self.token,
                repo=self.git_repo,
            ).run()


    
    def open_view(self):
        credentials_loader = CredentialsLoader()
        token, repository = credentials_loader.load()

        self.token = token
        self.git_repo = repository
        run = True
        while run:
            print(f"\n🔑 Usando repositório: {self.git_repo} com token: {self.token[:4]}... (oculto)")
            selections = DashboardSelection.menu()

            try:
                self.gerar_todos(selections)
                break  # Sai do loop se tudo ocorrer bem
            except NoTeamMembersError:
                print("\n⚠️ Retornando ao menu principal pois não há membros na organização.")
                continue  # Retorna ao menu se der problema nos membros
            except ExitNoChoice:
                run = False               
