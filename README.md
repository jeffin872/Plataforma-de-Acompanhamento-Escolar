# Plataforma de Acompanhamento Escolar

[![CI](https://github.com/jeffin872/Plataforma-de-Acompanhamento-Escolar/actions/workflows/ci.yml/badge.svg)](https://github.com/jeffin872/Plataforma-de-Acompanhamento-Escolar/actions/workflows/ci.yml)

## 1. Descrição do Projeto

A aplicação busca centralizar informações escolares que muitas vezes ficam espalhadas entre mensagens, documentos, reuniões e diferentes sistemas. O objetivo é criar uma plataforma que facilite a comunicação entre escola, professores e responsáveis, permitindo o acompanhamento de informações como notas, faltas, ocorrências, documentos e notificações.

**Público-alvo:**
* Escolas públicas e privadas;
* Professores;
* Administradores escolares;
* Pais e responsáveis.

### Funcionalidades Atuais (MVP)
A versão atual do MVP foca na validação da arquitetura e na interligação dos usuários, possuindo:
* Login de usuários e autenticação por perfil (JWT);
* Acesso protegido aos perfis de Responsável, Professor e Administrador;
* Direcionamento automático para o painel correspondente ao tipo de usuário;
* **Fluxo Integrado de Faltas e Atestados:** Uma funcionalidade de ponta a ponta interligando os 3 perfis:
  * **Professor:** Registra a falta do aluno no sistema.
  * **Responsável:** Visualiza a falta pendente e envia um atestado/justificativa.
  * **Administrador:** Recebe o documento, analisa e valida a justificativa da falta.

### Funcionalidades Previstas (Próximas Versões)
* **Responsável:** Acompanhar notas, visualizar ocorrências, consultar estudantes vinculados e acompanhar notificações.
* **Professor:** Visualizar turmas, registrar notas e registrar ocorrências.
* **Administrador:** Cadastrar e gerenciar usuários, cadastrar alunos e turmas, vincular professores e responsáveis e visualizar indicadores gerais.

---

## 2. Tecnologias Utilizadas

O projeto adota uma arquitetura moderna dividida entre cliente e servidor (Frontend e Backend):

* **Frontend:**
  * **React.js + Vite:** Escolhidos pela alta performance na componentização e rapidez no ambiente de desenvolvimento (HMR).
  * **React Router Dom:** Para o gerenciamento de rotas e proteção de páginas (Private Routes).
  * **Axios:** Para consumo da API REST.
* **Backend:**
  * **Python + Flask:** Framework minimalista e leve, ideal para a construção rápida do MVP.
  * **PyJWT:** Para geração e validação de tokens de segurança.
  * **Flask-CORS:** Para gerenciar o compartilhamento de recursos entre origens diferentes.
  * **SQLite:** Banco de dados relacional leve e embutido, ideal para o ambiente de desenvolvimento e prototipação.

---

## 3. Estrutura do Projeto

O repositório está organizado em dois grandes blocos independentes:

```text
Plataforma-de-Acompanhamento-Escolar/
│
├── frontend/               # Aplicação Cliente (React)
│   ├── src/
│   │   ├── api/            # Configurações do Axios e endpoints
│   │   ├── pages/          # Telas da aplicação divididas por perfil
│   │   ├── components/     # Componentes visuais reutilizáveis (Botões, Cards)
│   │   └── routes/         # Lógica de roteamento
│   └── package.json        # Dependências do Node.js
│
├── backend/                # Servidor API (Flask)
│   ├── routes/             # Controladores da API divididos por perfil
│   ├── app.py              # Ponto de entrada do servidor
│   └── requirements.txt    # Dependências do Python
│
└── README.md               # Documentação principal
```

---

## 4. Instalação e Execução

Siga o passo a passo abaixo para rodar o projeto localmente em sua máquina.

### Pré-requisitos
* Node.js (v18+)
* Python (v3.10+)
* Git

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/jeffin872/Plataforma-de-Acompanhamento-Escolar.git
cd Plataforma-de-Acompanhamento-Escolar
```

### Passo 2: Configurar e rodar o Backend (API)
Abra um terminal, acesse a pasta do backend e instale as dependências:
```bash
cd backend
python -m venv venv
```

Ative o ambiente virtual:
* **Windows:** `venv\Scripts\activate`
* **Linux/Mac:** `source venv/bin/activate`

Instale as dependências:
```bash
pip install -r requirements.txt
```

**Crie o arquivo de variáveis de ambiente:**
Na raiz da pasta `backend`, crie um arquivo chamado `.env` e cole os seguintes dados:
```env
DATABASE_URL=sqlite:///dev.db
FRONTEND_ORIGIN=http://localhost:5173
JWT_SECRET_KEY=chave-local-de-desenvolvimento
```

Inicie o servidor Python:
```bash
python app.py
```
*(O servidor rodará em http://localhost:5000)*

### Passo 3: Configurar e rodar o Frontend (Interface)
Abra um **novo terminal** (mantenha o backend rodando), acesse a pasta do frontend e instale as dependências:
```bash
cd frontend
npm ci
```

**Crie o arquivo de variáveis de ambiente:**
Na raiz da pasta `frontend`, crie um arquivo chamado `.env` e cole o seguinte dado:
```env
VITE_API_URL=http://localhost:5000/api
```

Inicie o servidor Vite:
```bash
npm run dev
```
*(A aplicação estará acessível no navegador em http://localhost:5173)*

---

## 5. Processo de Desenvolvimento

O projeto foi desenvolvido de forma incremental e ágil. Primeiro, a equipe criou um protótipo de alta fidelidade no Figma. Durante o desenvolvimento do MVP, as tarefas foram divididas entre frontend, backend, banco de dados, integração, testes e documentação.

O GitHub foi utilizado para controle de versão e organização do código, com commits realizados conforme as funcionalidades e correções eram desenvolvidas.

**Desafios e Soluções:** Durante a Sprint, algumas dificuldades apareceram somente na execução real do projeto, como incompatibilidade de uma dependência do backend com o Python 3.13 e uma configuração externa de gerenciadores de pacotes (Next.js vs Vite) que interferia no frontend. Esses problemas foram corrigidos com sucesso durante os testes locais por meio de *clean installs* e ajustes no `.gitignore` para proteção de dados sensíveis.

---

## 6. Como utilizar a aplicação (Componente Extensionista)

**Qual problema a aplicação busca resolver?**
A aplicação busca melhorar a comunicação entre escola e família, reunindo em um único ambiente informações que normalmente ficam espalhadas entre mensagens, documentos de papel, reuniões e diferentes meios de comunicação.

**Como qualquer usuário pode acessar e utilizar?**
O usuário acessa a plataforma pelo navegador e realiza o login utilizando seu e-mail e senha institucional. Após a autenticação, o sistema identifica automaticamente o perfil da conta e direciona o usuário para o painel correspondente (Responsável, Professor ou Administrador). No MVP atual, o usuário pode navegar pelo seu painel exclusivo e testar o fluxo de registro e justificativa de faltas.

**Quem pode se beneficiar?**
* Escolas públicas e privadas (na gestão de processos);
* Professores e equipes pedagógicas (na centralização de diários e ocorrências);
* Secretarias escolares (na validação de atestados e burocracias);
* Pais, responsáveis e estudantes (no acesso rápido à vida acadêmica).

**Cenários Reais de Utilização:**
Com a plataforma, se um aluno adoecer, o cenário deixa de ser uma troca de bilhetes de papel. O **Professor** registra a ausência pelo celular no painel dele. O **Responsável** vê a notificação em casa, tira uma foto do atestado médico e faz o upload. A **Secretaria (Admin)** recebe o documento na tela, verifica e clica em "Aprovar", justificando a falta automaticamente no diário do professor.

**Impacto da Solução na Sociedade:**
Mesmo estando em uma etapa inicial, a plataforma busca aproximar a família da escola. A democratização e a facilidade do acesso às informações acadêmicas ajudam na identificação rápida de dificuldades relacionadas à frequência e ao desempenho escolar. O sistema empodera os pais a participarem ativamente da rotina escolar, fortalecendo a comunidade e auxiliando diretamente na prevenção de problemas graves, como o baixo desempenho e o abandono escolar.

---

## 7. Integração Contínua (EP1 - GitHub Actions)

### 7.1 Objetivo
Este repositório possui um pipeline de **Integração Contínua (CI)** configurado com o **GitHub Actions**. O objetivo é verificar o código automaticamente a cada alteração, garantindo que o backend continue passando nos testes e que o frontend continue compilando, antes que o código seja aceito na branch `main`.

### 7.2 Onde fica e quando roda
O pipeline está definido em [`.github/workflows/ci.yml`](.github/workflows/ci.yml) e é executado:
* a cada **push** na branch `main`;
* a cada **Pull Request** aberto para a `main`;
* manualmente, na aba **Actions** do GitHub (botão *Run workflow*).

### 7.3 O que o pipeline faz
O workflow tem dois jobs independentes, que rodam em paralelo em uma máquina `ubuntu-latest`:

| Job | Etapas | Para que serve |
|-----|--------|----------------|
| **backend** | Instala Python 3.12 → instala dependências (`requirements-dev.txt`) → `flake8` (lint) → `pytest` (testes) | Detecta erros de sintaxe, imports sobrando e quebras de lógica na API |
| **frontend** | Instala Node 20 → `npm ci` → `npm run build` | Garante que o React/Vite compila sem erros |

**Testes automatizados (`backend/tests/`):** são 10 testes que cobrem o endpoint de saúde, o login (credenciais válidas, inválidas e vazias), a proteção de rotas por token JWT (401 sem token), a separação por perfil (professor recebendo 403 em rota de admin) e o armazenamento de senha como hash. Eles usam **SQLite em memória**, então não precisam de PostgreSQL nem de arquivo `.env`, e por isso rodam igual no computador e no GitHub.

**Decisões de configuração:**
* `npm ci` e `cache` de pip/npm: instalação reproduzível (usa exatamente o `package-lock.json`) e mais rápida.
* Jobs separados: se o frontend quebrar, dá para ver que o backend continua OK (e vice-versa).
* `requirements-dev.txt`: mantém `pytest` e `flake8` fora das dependências de produção.

### 7.4 Como rodar a mesma verificação localmente
```bash
# Backend
cd backend
pip install -r requirements-dev.txt
flake8 .
pytest -v

# Frontend
cd ../frontend
npm ci
npm run build
```

### 7.5 Como ver o resultado no GitHub
1. Abra o repositório no GitHub e clique na aba **Actions**.
2. Selecione a execução mais recente do workflow **CI - Integração Contínua**.
3. Um check verde (✔) indica que tudo passou; um vermelho (✘) indica falha, e dá para abrir o job para ler o log do passo que falhou.

### 7.6 O que é Integração Contínua? (Componente Extensionista)
Integração contínua é uma prática em que, toda vez que alguém do time envia código novo para o repositório, um robô roda automaticamente uma série de verificações: instala o projeto, confere o estilo do código, roda os testes e tenta gerar o build. Se algo der errado, o time é avisado na hora, e não só dias depois, quando já tem muita coisa misturada.

Para quem está aprendendo a programar, isso ajuda por alguns motivos:
* **Feedback rápido:** você descobre o erro minutos depois de enviá-lo, quando ainda lembra o que mexeu.
* **Menos "na minha máquina funciona":** o robô roda em um ambiente limpo, então revela dependências esquecidas ou arquivos que só existiam no seu computador.
* **Segurança para mudar o código:** com testes rodando sozinhos, dá menos medo de refatorar ou de aceitar contribuição de colegas.
* **Hábito profissional:** CI é padrão em praticamente qualquer empresa de software, então aprender cedo já prepara para o mercado.
* **Trabalho em equipe:** o time todo enxerga o mesmo resultado, e o Pull Request só deve ser aceito quando o check estiver verde.

Se você é estudante da UFCA e quer testar, basta criar uma pasta `.github/workflows/` no seu projeto, colocar um arquivo `.yml` com os passos (como o deste repositório) e dar um push. A aba **Actions** do GitHub passa a mostrar a execução.

---

## 8. Status do Projeto

**Status:** MVP Inicial Funcional.

A versão atual possui o frontend integrado ao backend, autenticação JWT, controle de acesso seguro por perfil e o fluxo integrado do sistema. Atualmente, o fluxo de login e acesso aos diferentes perfis está 100% funcional e foi testado localmente com sucesso.
