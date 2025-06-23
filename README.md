# 📊 Reportify-IFES

**Reportify-IFES** é uma ferramenta Python para geração de dashboards e relatórios automatizados a partir de dados de repositórios GitHub. Com ele, você obtém insights valiosos sobre sua organização, equipe, colaboração e produtividade no GitHub.

---

## 🚀 Instalação

> ⚠️ **Requisitos:**  
- Python **3.10** obrigatoriamente.  
Outras versões podem não ser compatíveis.

### Instale via pip:

```bash
pip install reportify-ifes
```

⚙️ Configuração
Crie um arquivo .env no diretório raiz do seu projeto com as seguintes variáveis:
```bash
GITHUB_TOKEN=seu_token_github
GITHUB_REPOSITORY=usuario/repositorio
```

🏃‍♂️ Como utilizar
Crie um arquivo Python, por exemplo gerar_relatorio.py, com o seguinte conteúdo:

from reportify import Report

```bash
relatorio = Report()
relatorio.run()
```
📚 Componentes do Relatório
O relatório é composto por diferentes dashboards, cada um focado em uma perspectiva da organização ou projeto no GitHub:

🔹 DeveloperStats
Analisa os desenvolvedores do repositório, gerando métricas como quantidade de commits, issues abertas e fechadas, pull requests e participação individual nas atividades. Relatório consolidado e individual.

🔹 OrganizationalDashboard
Oferece uma visão geral da organização, consolidando dados de múltiplos repositórios e apresentando tendências, produtividade, gargalos e distribuição de tarefas. 

🔹 GitHubIssueStats
Gera estatísticas específicas sobre as issues, como tempo médio de resolução, tempo de abertura, gargalos e ciclos de desenvolvimento.

🔹 TeamStats
Foca na dinâmica da equipe, mostrando como os membros colaboram, distribuição de tarefas, taxas de conclusão e engajamento dentro do repositório.

🔹 CollaborationGraph
Cria um grafo de colaboração que representa visualmente como os membros da equipe interagem entre si por meio de revisões, commits, comentários e interações em issues.