## OTDR Analyzer

Sistema web de análise de eventos em fibra óptica desenvolvido com Python e Flask

Projeto autoral de desenvolvimento backend | Python • Flask • SQLite • Telecomunicações

Sobre o projeto

O OTDR Analyzer é uma aplicação web criada para auxiliar na interpretação de eventos registrados em medições de fibra óptica.

O projeto surgiu da experiência prática com infraestrutura de telecomunicações e da oportunidade de aplicar conhecimentos de desenvolvimento de software à análise de dados técnicos.

A aplicação permite importar arquivos CSV com eventos OTDR, avaliar perdas ópticas com base em limites configuráveis, identificar possíveis anomalias e consultar análises anteriores.

Status: em desenvolvimento, utilizando dados simulados para demonstração.

Problema abordado

A análise de medições ópticas exige a interpretação de eventos como emendas, conectores, perdas e reflexões.

O OTDR Analyzer busca organizar parte desse processo, aplicando regras de análise aos dados importados e apresentando os resultados em uma interface web.

Funcionalidades

- Importação de arquivos CSV contendo eventos de medições OTDR.
- Identificação e classificação de eventos ópticos.
- Avaliação de perdas com limites configuráveis.
- Apresentação de resultados e possíveis problemas.
- Cadastro, login e confirmação de contas.
- Armazenamento de histórico de análises por usuário.
- Controle de permissões administrativas.
- Mecanismo de bloqueio progressivo de tentativas de login.

Tecnologias

Tecnologia| Aplicação
Python| Processamento e regras de negócio
Flask| Aplicação web e rotas
SQLite| Persistência de dados
Werkzeug| Hash e verificação de senhas
HTML/CSS| Interface web
Git/GitHub| Versionamento

Arquitetura

O projeto organiza suas responsabilidades em módulos:

- "app.py": rotas e integração da aplicação Flask.
- "analisador.py": processamento e avaliação dos eventos.
- "autenticacao.py": autenticação de usuários.
- "banco.py": persistência de dados.
- "limite_login.py": controle de tentativas de acesso.
- "admin.py": recursos administrativos.
- "conta.py": gerenciamento de contas.
- "emails.py": envio de mensagens.
- "validacao.py": validação de dados.
- "config.py": configurações da aplicação.

As interfaces HTML estão em "templates/", com recursos estáticos em "static/".

Formato dos dados

A versão atual utiliza arquivos CSV com os campos:

Campo| Descrição
"distancia_km"| Distância do evento
"tipo"| Tipo de evento
"perda_db"| Perda óptica
"reflectancia_db"| Reflectância

Limitação atual: a aplicação não interpreta diretamente arquivos binários ".SOR".

Instalação e execução

Clone o repositório:

git clone https://github.com/e-tezzon/otdr-analyzer.git
cd otdr-analyzer

Crie um ambiente virtual:

python -m venv .venv

Ative o ambiente:

Windows:

.venv\Scripts\activate

Linux/macOS:

source .venv/bin/activate

Após adicionar e validar o arquivo "requirements.txt", instale as dependências:

pip install -r requirements.txt

Configure as variáveis de ambiente necessárias conforme "config.py", incluindo as credenciais de e-mail quando utilizadas.

Execute localmente:

python app.py

Acesse "http://127.0.0.1:5000".

Importante: não publique arquivos ".env", credenciais ou dados sensíveis no repositório.

Segurança

O projeto documenta mecanismos de autenticação, armazenamento de hashes de senhas, controle de acesso e bloqueio progressivo de login.

A aplicação ainda requer validação de segurança antes de qualquer implantação pública, incluindo revisão de sessões, cookies, CSRF, HTTPS e configurações de produção.

Próximas melhorias

- Testes automatizados das regras de análise.
- Padronização das dependências e da configuração.
- Melhor tratamento de arquivos inválidos.
- Demonstração visual do fluxo completo.
- Avaliação de suporte futuro ao formato ".SOR".

Motivação e aprendizado

Este projeto conecta minha formação em Análise e Desenvolvimento de Sistemas com minha experiência profissional em infraestrutura de fibra óptica.

Seu desenvolvimento envolve organização de código Python, lógica de negócio, persistência, autenticação, desenvolvimento web e tratamento de dados técnicos.

Autor

Eduardo Tezzon

Formado em Análise e Desenvolvimento de Sistemas, com foco em Python e experiência profissional em telecomunicações.

"GitHub — e-tezzon" (https://github.com/e-tezzon)