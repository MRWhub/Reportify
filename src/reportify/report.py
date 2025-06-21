
from datetime import datetime
import os, shutil
import sys
import os

from reportify.controller.report_controller import ReportController
class Report:

    def __init__(self):


        print('📂 Diretório atual de execução:', os.getcwd())
        now = datetime.now()
        self.report_dir = os.path.join("Reports", f"Report{now.day:02}{now.month:02}{now.year}-{now.hour:02}h:{now.minute:02}min")
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs("organization_charts", exist_ok=True)
    def salvar_markdown(self, save_directory, filename, content):
        os.makedirs(save_directory, exist_ok=True)
        path = os.path.join(save_directory, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Markdown salvo em: {path}")

    def run(self):
        
        controller = ReportController(self.salvar_markdown, self.report_dir)
        controller.open_view()  
        print("✅ Relatório gerado com sucesso!")
       
        print(f"📂 Relatório completo em: {self.report_dir}")
        '''
        if os.path.exists(".cache"):
            shutil.rmtree(".cache")
            print("🧹 Cache removido.")
        '''
if __name__ == "__main__":
    Report().run()
    