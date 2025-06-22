
from datetime import datetime
import os, shutil
import sys
import os

from reportify.controller.report_controller import ReportController
class Report:

    def __init__(self):



        os.makedirs("organization_charts", exist_ok=True)
    def salvar_markdown(self,filename, content):
        now = datetime.now()
        report_dir = os.path.join("Reports", f"Report{now.day:02}{now.month:02}{now.year}-{now.hour:02}h:{now.minute:02}min")
        os.makedirs(report_dir, exist_ok=True)

        path = os.path.join(report_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Markdown salvo em: {path}")

    def run(self):
        
        controller = ReportController(self.salvar_markdown)
        controller.open_view()  
        print("✅ Relatório gerado com sucesso!")
       
        
        '''   
        if os.path.exists(".cache"):
            shutil.rmtree(".cache")
            print("🧹 Cache removido.")
        '''
        
if __name__ == "__main__":
    Report().run()
    