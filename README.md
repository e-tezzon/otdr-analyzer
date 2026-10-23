# OTDR Analyzer

### Sistema Web de Análise de Eventos em Fibra Óptica

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

> Projeto autoral desenvolvido com Python e Flask, aplicando conhecimentos de desenvolvimento backend à análise de eventos em redes de fibra óptica.

## 📌 Sobre o Projeto

O **OTDR Analyzer** é uma aplicação web desenvolvida para auxiliar na análise de eventos identificados em medições de fibra óptica.

O projeto surgiu da combinação entre minha formação em **Análise e Desenvolvimento de Sistemas** e minha experiência profissional como técnico de fibra óptica.

A aplicação permite importar arquivos CSV contendo eventos OTDR, analisar perdas ópticas, identificar possíveis anomalias e armazenar históricos de análises.

O objetivo é demonstrar como o desenvolvimento de software pode contribuir para a organização e interpretação de dados técnicos em telecomunicações.

**Status:** Em desenvolvimento, utilizando dados simulados para demonstração.

---

## 🎯 Problema Abordado

A interpretação de medições OTDR envolve a avaliação de eventos como:

- Emendas ópticas;
- Conectores;
- Perdas de sinal;
- Reflexões;
- Eventos com atenuação acima dos limites definidos.

O OTDR Analyzer busca automatizar parte desse processo, utilizando regras de análise aplicadas aos dados importados.

---

## 🚀 Funcionalidades

- [x] Importação de eventos OTDR por arquivos CSV;
- [x] Identificação e classificação de eventos;
- [x] Análise de perdas ópticas;
- [x] Limites configuráveis de avaliação;
- [x] Histórico de análises por usuário;
- [x] Cadastro e autenticação de usuários;
- [x] Controle de permissões administrativas;
- [x] Controle de tentativas de login;
- [ ] Testes automatizados abrangentes;
- [ ] Leitura direta de arquivos binários `.SOR`;
- [ ] Preparação e validação para produção.

> **Nota:** A versão atual utiliza dados estruturados em CSV. A leitura direta de arquivos `.SOR` ainda não está implementada.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| Python | Linguagem principal e regras de negócio |
| Flask | Desenvolvimento da aplicação web |
| SQLite | Armazenamento e persistência de dados |
| Werkzeug | Hash e verificação de senhas |
| HTML | Estrutura das páginas |
| CSS | Estilização da interface |
| Git | Controle de versão |
| GitHub | Hospedagem e documentação do código |

---

## 🏗️ Estrutura do Projeto

```text
otdr-analyzer/
├── app.py
├── analisador.py
├── autenticacao.py
├── banco.py
├── limite_login.py
├── admin.py
├── conta.py
├── emails.py
├── validacao.py
├── config.py
├── templates/
├── static/
└── README.md
```

### Responsabilidade dos Módulos

| Arquivo | Responsabilidade |
|---------|------------------|
| `app.py` | Rotas e integração da aplicação Flask |
| `analisador.py` | Processamento e análise dos eventos |
| `autenticacao.py` | Autenticação dos usuários |
| `banco.py` | Persistência dos dados |
| `limite_login.py` | Controle de tentativas de login |
| `admin.py` | Funcionalidades administrativas |
| `conta.py` | Gerenciamento de contas |
| `emails.py` | Recursos de envio de e-mails |
| `validacao.py` | Validação de dados |
| `config.py` | Configurações da aplicação |

---

## 📊 Formato dos Dados

A aplicação utiliza arquivos CSV contendo eventos de medições OTDR.

### Exemplo de entrada

```csv
distancia_km,tipo,perda_db,reflectancia_db
0.50,emenda,0.10,-55
1.20,conector,0.35,-40
2.40,emenda,0.15,-52
3.80,conector,0.60,-35
```

**Campos utilizados:**

| Campo | Descrição |
|-------|-----------|
| `distancia_km` | Distância do evento em quilômetros |
| `tipo` | Classificação do evento |
| `perda_db` | Perda óptica em decibéis |
| `reflectancia_db` | Reflectância do evento em decibéis |

> Os dados acima são fictícios e ilustrativos. O formato deve ser validado conforme as regras do analisador.

---

## ⚙️ Instalação e Execução

### 1. Clonar o repositório

```bash
git clone https://github.com/e-tezzon/otdr-analyzer.git
cd otdr-analyzer
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Instalar dependências

Após criar e validar o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configurar o ambiente

Verifique as configurações necessárias em `config.py` e defina as variáveis de ambiente exigidas pela aplicação.

Não publique senhas, tokens, chaves secretas ou credenciais de e-mail.

### 6. Executar a aplicação

```bash
python app.py
```

Se a aplicação utilizar a configuração padrão de desenvolvimento do Flask, acesse:

```text
http://127.0.0.1:5000
```

> As instruções de execução devem ser confirmadas no ambiente local antes de considerar a instalação reproduzível.

---

## 🔐 Segurança

O projeto contempla recursos relacionados a:

- Autenticação de usuários;
- Armazenamento de hashes de senhas;
- Controle de permissões;
- Gerenciamento de sessões;
- Limitação de tentativas de login.

**Importante:** Esses recursos não representam uma auditoria de segurança concluída.

Antes de disponibilizar a aplicação em produção, é necessário revisar configurações, proteção CSRF, cookies, HTTPS, validação de entradas e tratamento de erros.

---

## 📈 Melhorias Planejadas

- [ ] Ampliar a cobertura de testes com pytest;
- [ ] Padronizar dependências em `requirements.txt`;
- [ ] Aprimorar o tratamento de erros;
- [ ] Documentar o processo de configuração;
- [ ] Adicionar capturas reais da interface;
- [ ] Criar demonstração do funcionamento;
- [ ] Avaliar suporte ao formato `.SOR`;
- [ ] Preparar um ambiente seguro de implantação.

---

## 💡 Motivação e Aprendizado

O OTDR Analyzer foi desenvolvido para conectar duas áreas da minha trajetória profissional:

**Desenvolvimento de software e telecomunicações.**

Durante o projeto, trabalhei com:

- Programação Python;
- Desenvolvimento backend com Flask;
- Organização modular de código;
- Processamento de dados;
- Persistência em banco de dados;
- Autenticação e controle de acesso;
- Regras de negócio aplicadas a um problema técnico.

O projeto faz parte da construção do meu portfólio profissional para oportunidades em **desenvolvimento Python, backend e automação de processos**.

---

## 👨‍💻 Autor

**Eduardo Tezzon**

Formado em Análise e Desenvolvimento de Sistemas — dezembro de 2024.

Desenvolvedor Python com experiência profissional em telecomunicações.

**GitHub:** [github.com/e-tezzon](https://github.com/e-tezzon)

**Repositório:** [OTDR Analyzer](https://github.com/e-tezzon/otdr-analyzer)

---

## 📄 Licença

Consulte as informações de licenciamento do repositório. Na ausência de um arquivo `LICENSE`, não presuma que o código esteja autorizado para reutilização por terceiros.
