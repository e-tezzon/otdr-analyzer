# 🔎 OTDR Analyzer

### Sistema Web de Análise de Eventos em Fibra Óptica

O **OTDR Analyzer** é uma aplicação web desenvolvida em **Python e Flask**, criada para auxiliar técnicos e profissionais de telecomunicações na identificação e análise de eventos em enlaces de fibra óptica.

O sistema permite importar arquivos CSV com dados de medições OTDR, identificar possíveis problemas de atenuação e reflexões, configurar limites de perda e armazenar o histórico de análises realizadas.

O projeto está em desenvolvimento e tem como objetivo oferecer uma ferramenta prática, organizada e acessível para auxiliar na análise técnica de redes ópticas.

---

## 🚀 Funcionalidades

### 📊 Análise de Fibra Óptica

- Importação de arquivos CSV com eventos de medições OTDR.
- Identificação de eventos de emendas e conectores.
- Análise de perdas ópticas em dB.
- Avaliação dos eventos conforme limites configuráveis.
- Identificação de possíveis problemas na fibra.
- Exibição detalhada dos resultados.

### 👤 Autenticação e Gerenciamento de Usuários

- Cadastro de usuários.
- Login com e-mail e senha.
- Confirmação de conta por e-mail.
- Armazenamento seguro de hashes de senhas.
- Gerenciamento de sessão autenticada.
- Área de conta do usuário.
- Acesso administrativo com controle de permissões.

### 🔐 Bloqueio Progressivo de Login

Para dificultar tentativas repetidas de acesso não autorizado, o sistema possui um mecanismo de bloqueio progressivo.

| Tentativas incorretas | Tempo de bloqueio |
|---|---|
| 1ª tentativa | Sem bloqueio |
| 2ª tentativa | 30 minutos |
| 3ª tentativa | 60 minutos |
| 4ª tentativa | 90 minutos |
| 5ª tentativa | 120 minutos |

O bloqueio é registrado no banco SQLite, permanecendo ativo mesmo após o fechamento do navegador ou reinicialização da aplicação.

Após uma autenticação bem-sucedida, o contador de tentativas é zerado.

Durante o período de bloqueio, novas verificações de senha não são realizadas.

### 📁 Histórico de Análises

- Armazenamento das análises realizadas.
- Consulta ao histórico individual dos usuários.
- Visualização de análises anteriores.
- Registro dos eventos e limites utilizados em cada análise.

---

## 🛠️ Tecnologias Utilizadas

- **Python** — linguagem principal do projeto.
- **Flask** — framework para desenvolvimento web.
- **SQLite** — banco de dados.
- **HTML e CSS** — estrutura e apresentação da interface.
- **Werkzeug** — geração e verificação de hashes de senhas.
- **Git e GitHub** — versionamento e gerenciamento do código.

---

## 📂 Estrutura do Projeto

Os principais módulos são:

- `app.py` — aplicação Flask, rotas principais e integração dos módulos.
- `analisador.py` — processamento dos eventos e identificação de problemas.
- `autenticacao.py` — autenticação e controle de acesso.
- `banco.py` — operações com o banco de dados.
- `limite_login.py` — controle de tentativas e bloqueios progressivos.
- `admin.py` — funcionalidades administrativas.
- `conta.py` — gerenciamento de conta.
- `emails.py` — envio de mensagens por e-mail.
- `validacao.py` — validação dos dados de cadastro.
- `config.py` — configurações da aplicação.
- `templates/` — páginas HTML.
- `.env` — variáveis de ambiente privadas, não destinadas ao GitHub.

---

## ⚙️ Instalação

**1. Clone o repositório:**

`git clone https://github.com/e-tezzon/otdr-analyzer.git`

**2. Entre na pasta:**

`cd otdr-analyzer`

**3. Crie um ambiente virtual:**

`python -m venv venv`

**4. Ative o ambiente virtual:**

Windows:

`venv\Scripts\activate`

Linux/macOS:

`source venv/bin/activate`

**5. Instale as dependências:**

`pip install -r requirements.txt`

**6. Configure as variáveis de ambiente:**

Crie um arquivo `.env` na pasta principal e configure os valores necessários, conforme o `config.py`, incluindo `SECRET_KEY` e `BASE_URL`.

Configure também as credenciais de e-mail necessárias para os recursos de confirmação de conta.

**Nunca publique senhas, chaves ou o arquivo `.env` no GitHub.**

**7. Inicie a aplicação localmente:**

`python app.py`

Acesse pelo navegador:

`http://127.0.0.1:5000`

---

## 📄 Formato dos Arquivos de Análise

O sistema trabalha com arquivos CSV contendo as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `distancia_km` | Distância do evento em quilômetros |
| `tipo` | Tipo do evento identificado |
| `perda_db` | Perda óptica em decibéis |
| `reflectancia_db` | Reflectância do evento |

O usuário pode definir limites de perda para conectores e emendas antes de executar a análise.

**Observação:** nesta versão, o sistema utiliza dados de eventos em CSV. A leitura direta de arquivos binários `.SOR` não está implementada.

---

## 🔒 Segurança

O projeto inclui mecanismos de proteção como:

- Senhas armazenadas utilizando hashes.
- Confirmação de e-mail no cadastro.
- Sessões autenticadas.
- Rotas com autenticação obrigatória.
- Controle de acesso administrativo.
- Bloqueio progressivo de tentativas incorretas de login.
- Configuração de credenciais por variáveis de ambiente.

Esses mecanismos representam uma base inicial de segurança, mas não substituem uma auditoria completa.

**Antes da implantação em produção**, devem ser revisados itens como HTTPS, cookies seguros, proteção CSRF, limitação de requisições e configuração do servidor web.

---

## 📈 Melhorias Planejadas

- [ ] Melhorias na visualização dos resultados.
- [ ] Gráficos de eventos e perdas ópticas.
- [ ] Exportação de relatórios.
- [ ] Suporte a formatos adicionais de arquivos OTDR.
- [ ] Aprimoramento da proteção contra ataques automatizados.
- [ ] Melhorias na interface para dispositivos móveis.
- [ ] Expansão das ferramentas administrativas.

---

## 📌 Status do Projeto

**Em desenvolvimento ativo.**

O OTDR Analyzer continua recebendo melhorias em segurança, funcionalidades e experiência do usuário.

A aplicação é destinada ao apoio técnico e não substitui a avaliação profissional das medições ou a validação com equipamentos e softwares especializados.

---

## 👨‍💻 Repositório

Desenvolvimento e manutenção do projeto:

**GitHub:** https://github.com/e-tezzon/otdr-analyzer

---

**OTDR Analyzer — Tecnologia aplicada à análise de redes ópticas.**