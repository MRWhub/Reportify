# 📊 Reportify-IFES

**Reportify-IFES** é uma ferramenta Python para geração de dashboards e relatórios automatizados a partir de dados de repositórios GitHub. Com ele, você obtém insights valiosos sobre sua organização, equipe, colaboração e produtividade no GitHub.

---

## 🚀 Instalação

> ⚠️ **Requisitos:**  
- Python **3.10** obrigatoriamente.  
Outras versões podem não ser compatíveis.

### 💡 Caso não tenha essa versão instalada, use `pyenv` para configurar o Python 3.10.12 (Ubuntu/Debian)

1. **Instale as dependências do sistema**:

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
  libffi-dev liblzma-dev git
  curl https://pyenv.run | bash
```
2. **Adicione o pyenv ao seu shell (.bashrc, .zshrc, etc):**

```bash
# Adicione ao final do arquivo
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

```
3. **Após isso, reabra o terminal ou execute:**
```bash
 source ~/.bashrc
 ```
4. **Instale o Python 3.10.12 no diretório que deseja executar a ferramenta:**

```bash
pyenv install 3.10.12
pyenv local 3.10.12
 ```
5. **Crie um ambiente virtual com pyenv-virtualenv:** 

```bash
pyenv virtualenv 3.10.12 reportify-env
pyenv activate reportify-env
 ```
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
```bash
from reportify import Report
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

# 🚀 Agendamento de Resumos Diários dos Desenvolvedores com GitHub Actions 

Este repositório permite gerar os relatórios automaticamente e enviar um resumo todos os dias utilizando **GitHub Actions**, **Gemini AI (Google)** e **Discord Webhooks**.

---

## 📁 Etapas de configuração

### 1. 🔱 Fork do Repositório

Caso deseje usar esse sistema com seu próprio repositório:

1. Clique em **Fork** (canto superior direito)
2. Escolha sua conta para onde o fork será feito

---

### 2. 🔐 Configurar Secrets no repositório

Com o fork criado, acesse:

> **Settings** > **Secrets and variables** > **Actions** > **New repository secret**

Adicione os seguintes **4 secrets obrigatórios**:

| Nome                | Descrição                                           |
|---------------------|-----------------------------------------------------|
| `GITHUB_REPOSITORY` | Nome do repositório GitHub que será analisado, exemplo: `n8n-io/n8n` |
| `GITHUB_TOKEN`      | Token de acesso pessoal (com permissão de leitura de repositório privado, se necessário) |
| `GOOGLE_API_KEY`    | Chave da API do Google Gemini, crie sua chave gratuita [aqui](https://aistudio.google.com/app/apikey).                      |
| `DISCORD_WEBHOOK`   | Webhook do canal ou servidor do Discord            |

---

### 3. 🕐 Ajustar horário de execução no GitHub Actions

O agendamento de execução diária é feito no arquivo:

`.github/workflows/run.yml`

No trecho:

```yaml
on:
  schedule:
    - cron: '0 11 * * *'  # Executa todos os dias às 08h BRT (11h UTC)
```
- Para alterar o horário:

A hora (11) está em formato UTC

Para rodar às 09h da manhã no Brasil (BRT) → use cron: '0 12 * * *'

Para rodar às 06h da manhã no Brasil → cron: '0 9 * * *'

É possível configurar o cron de outras formas: [Saiba mais](https://en.wikipedia.org/wiki/Cron)

#### Após essa configuração, os relatórios serão gerados e os resumos feitos por IA serão enviados automaticamente para o seu canal/servidor discord.