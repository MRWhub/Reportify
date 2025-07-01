from reportify.controller.report_controller import ReportController
from datetime import datetime
import os   
from dotenv import load_dotenv
from reportify.model.exceptions.team_members_exception import NoTeamMembersError
REPOS = ["1","2","3","4","5"]
class CreateAllReports:
    def __init__(self):
        load_dotenv()

        
        #self.reports = REPOS
        self.reports = ["1"]  # Corrigido para strings
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo = os.getenv("GITHUB_REPOSITORY")

        ReportController(
            self.salvar_markdown,
            token=self.token,
            git_repo=self.repo
        ).gerar_todos(self.reports)

    def salvar_markdown(self,filename, content):
        now = datetime.now()
        report_dir = os.path.join("Reports", f"Report{now.day:02}{now.month:02}{now.year}-{now.hour:02}h:{now.minute:02}min")
        os.makedirs(report_dir, exist_ok=True)

        path = os.path.join(report_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Markdown salvo em: {path}")

    