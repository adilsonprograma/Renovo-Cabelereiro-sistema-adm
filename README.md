# ✂️ Renovo Cabeleireiros

O **Renovo Cabeleireiros** é um sistema de gestão comercial e controlo financeiro residencial/local, desenvolvido especificamente para salões de beleza, barbeiros e profissionais autónomos do setor de estética.

Este sistema foi construído focando na leveza, rapidez de resposta e numa interface visual moderna baseada num ecossistema local (Offline-First). Ele transforma o navegador do seu computador num autêntico painel de controlo profissional (Desktop App) através de scripts automatizados de segundo plano.[cite: 1]

---

## 🚀 Funcionalidades Principais

* **📅 Agenda Dinâmica:** Registo e controlo completo de agendamentos diários organizados por horário, cliente, contacto e status (Pendente, Confirmado, Concluído e Cancelado).[cite: 1]
* **💰 Fluxo de Caixa Integrado:** Módulo de faturação com histórico de pagamentos suportando múltiplos métodos (Dinheiro, PIX, Cartão de Crédito e Débito).[cite: 1]
* **📦 Controlo Patrimonial de Estoque:**
    * Gestão automatizada de insumos e produtos com margem de segurança ajustada para alertas de stock baixo.[cite: 1]
    * **Quantidade mínima padrão configurada para 1 unidade**, ideal para otimização de capital.[cite: 1]
    * **Cálculo Patrimonial em Tempo Real:** Dashboard financeiro integrado que exibe o valor exato total investido em stock (`∑ Quantidade × Preço Unitário`).[cite: 1]
* **📊 Relatórios e Métricas Dinâmicas:**
    * Faturamento diário, semanal e mensal consolidado.[cite: 1]
    * Média de faturação diária.[cite: 1]
    * Gráfico nativo dos últimos 30 dias de desempenho do salão.[cite: 1]
    * Ranking dos serviços mais procurados e formas de pagamento mais utilizadas.[cite: 1]

---

## 🛠️ Arquitetura Técnico-Visual

O projeto foi estruturado utilizando a metodologia de microssprints e engenharia reversa visual para garantir máxima performance de renderização no motor Blink do Google Chrome e Microsoft Edge:[cite: 1]

* **Backend:** Python 3.11+ / Flask (Servidor WSGI leve de desenvolvimento local)[cite: 1]
* **Banco de Dados:** SQLite 3 (Armazenamento local em ficheiro único, dispensando servidores externos pesados de BD)[cite: 1]
* **Frontend:** HTML5 semântico, CSS3 moderno (Variáveis nativas, CSS Grid e Flexbox Customizado) e Vanilla JavaScript puro (Zero bibliotecas pesadas de terceiros)[cite: 1]
* **Ícones:** FontAwesome 6.5.1 integrado via CDN para leveza de interface[cite: 1]
* **Automação Desktop:** Arquivos de script nativos do Windows (`wscript` + VBScript ANSI) para ocultação de terminal e bypass de portas de firewall locais (`host='0.0.0.0'`).[cite: 1]

---

## 📁 Estrutura de Pastas do Projeto

```text
salao_app/
│
├── app.py                  # Servidor central Flask, rotas e consultas SQL
├── salao.db                # Banco de dados SQLite local (Gerado automaticamente - Ignorado no Git)
├── requirements.txt        # Dependências de bibliotecas Python
├── ligar_sistema.vbs       # Script de inicialização invisível do Windows
├── .gitignore              # Proteção de dados e exclusão de ficheiros temporários
│
├── templates/              # Telas em HTML (Engine de renderização Jinja2)
│   ├── base.html           # Layout principal e Barra Lateral (Sidebar) do Renovo Cabeleireiros
│   ├── dashboard.html      # Painel inicial de resumo diário
│   ├── agendamentos.html   # Tela de controlo da agenda
│   ├── pagamentos.html     # Histórico de fluxo de caixa e acertos
│   ├── relatorios.html     # Estatísticas, médias e gráfico de desempenho
│   └── estoque.html        # Painel do inventário e valor total investido
│
└── static/                 # Ficheiros estáticos de estilo e comportamento
    ├── css/
    │   └── style.css       # Design visual, paleta roxo/rosa e responsividade mobile
    └── js/
        └── script.js       # Comportamentos dinâmicos e automatizações de formulários
```[cite: 1]

---

## 🔧 Como Executar e Instalar no Computador

### Pré-requisitos
1. Ter o **Python** instalado no computador.[cite: 1]
2. Ter o **Git** configurado (se desejar atualizar o repositório).[cite: 1]

### Inicialização Rápida no Terminal
Se preferir rodar manualmente no PowerShell para inspecionar os logs de desenvolvimento:[cite: 1]
```powershell
cd "$env:USERPROFILE\Desktop\salao_app"
python app.py
```[cite: 1]
Aceda ao endereço no seu navegador: **`http://127.0.0.1:5000`**[cite: 1]

### Modo Aplicativo de Ambiente de Trabalho (Desktop)
Para usar o sistema como um programa nativo do Windows:[cite: 1]
1. Dê dois cliques no atalho **Renovo Cabeleireiros** gerado na sua Área de Trabalho.[cite: 1]
2. O servidor Python iniciará em segundo plano (escondido) e a janela do sistema abrirá automaticamente.[cite: 1]

---

## 🔒 Segurança de Dados (.gitignore)

Para proteger o seu negócio e cumprir as boas práticas de desenvolvimento, este repositório está configurado para **nunca** enviar o ficheiro `salao.db` para a nuvem pública do GitHub. Isto garante que a lista de clientes, números de telefone e faturamento financeiro real fiquem guardados estritamente na memória física do seu computador de trabalho.[cite: 1]

---
Desenvolvido com foco em praticidade e aplicação imediata. 💇‍♀️✂️[cite: 1]
