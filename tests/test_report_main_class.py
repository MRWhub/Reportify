# tests/test_report.py

from src.reportify.report import Report
import os
from datetime import datetime

def test_report_directory_creation():
    report = Report()
    assert os.path.exists("organization_charts")

def test_salvar_markdown():
    report = Report()
    filename = "test.md"
    content = "# Testando Markdown"

    # Salvar arquivo
    report.salvar_markdown(filename, content)

    # Montar caminho do diretório com base no horário atual
    now = datetime.now()
    report_dir = os.path.join(
        "Reports",
        f"Report{now.day:02}{now.month:02}{now.year}-{now.hour:02}h:{now.minute:02}min"
    )
    file_path = os.path.join(report_dir, filename)

    assert os.path.exists(file_path), "❌ O arquivo não foi criado."

    with open(file_path, "r", encoding="utf-8") as f:
        content_read = f.read()

    assert content_read == content, "❌ O conteúdo do arquivo está incorreto."

    print("✅ Teste passou com sucesso.")