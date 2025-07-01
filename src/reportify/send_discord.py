import os
import requests
from glob import glob
import time
MAX_RETRIES = 3
RETRY_WAIT = 5  # segundos
class SendDiscordSummaries:
    def __init__(self):
        self.API_KEY = os.getenv("GOOGLE_API_KEY")
        self.webhook_url = os.getenv("DISCORD_WEBHOOK")
        self.send_discord_summaries()
        
    def generate_summary_palm(self,text):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.API_KEY}"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
        "contents": [
        {
            "parts": [
            {
                "text": f"Analise as informações possíveis do desenvolvedor ou dos desenvolvedores e retorne um resumo de 1900 caracteres\n\n{text}"
            }
            ]
        }
        ]
    }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Tentativa {attempt} falhou: {e}")
                if attempt < MAX_RETRIES:
                    print(f"⏳ Aguardando {RETRY_WAIT}s para tentar novamente...")
                    time.sleep(RETRY_WAIT)
                else:
                    raise Exception(f"❌ Erro permanente ao tentar gerar resumo: {e}")


    # Buscar o relatório mais recente
    def send_discord_summaries(self):

        report_dirs = glob("Reports/Report*")
        if not report_dirs:
            raise Exception("Nenhum relatório encontrado.")

        latest_dir = max(report_dirs, key=os.path.getmtime)

        print(f"Usando o relatório mais recente: {latest_dir}")
        md_files = glob(os.path.join(latest_dir, "developer_stats_*.md"))


        for md_file in md_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                summary = self.generate_summary_palm(content)
                message = f"📄 **Resumo de `{md_file.split('/')[-1]}`**:\n```markdown\n{summary[:1900]}\n```"
                resp = requests.post(self.webhook_url, json={"content": message})
                if resp.status_code != 204:
                    print(f"Erro enviando ao Discord: {resp.status_code} {resp.text}")
                else:
                    print(f"Resumo de {md_file} enviado.")
            except Exception as e:
                print(f"Erro ao processar {md_file}: {e}")
