# Plataforma de Acompanhamento Escolar

Sistema web desenvolvido para facilitar o acompanhamento da vida escolar dos estudantes e melhorar a comunicação entre escola, professores e responsáveis.

O projeto surgiu a partir de um protótipo de alta fidelidade e evoluiu para um **MVP funcional**, com frontend, backend, banco de dados e autenticação por perfil.

## Integrantes

* Jefferson da Rocha Teodoro — 2025014000
* Thalis Leandro Bezerra de Lima — 2025014171
* Genildo da Silva Ferreira — 2025013782
* Thalyson de Sousa Batista Maia — 2025014206

## Protótipo no Figma

[Visualizar protótipo](https://www.figma.com/design/ketUbOUk4ML7yAyo9hHTLj/EP1---Painel-de-Coopera%C3%A7%C3%A3o-Escolar---Prot%C3%B3tipo-Alta-Fidelidade?node-id=2-2&t=9yFTB0lXaWHmTjVB-1)

---

## Descrição do projeto

A aplicação busca centralizar informações escolares que muitas vezes ficam espalhadas entre mensagens, documentos, reuniões e diferentes sistemas.

O objetivo é facilitar o acesso a informações como:

* notas;
* faltas;
* ocorrências;
* documentos;
* notificações;
* dados acadêmicos dos estudantes.

### Público-alvo

* escolas públicas e privadas;
* professores;
* administradores escolares;
* pais e responsáveis.

### Principais funcionalidades

**Responsável**

* acompanhar notas e faltas;
* visualizar ocorrências;
* enviar documentos e atestados;
* acompanhar notificações.

**Professor**

* visualizar turmas;
* registrar notas;
* registrar faltas;
* registrar ocorrências.

**Administrador**

* cadastrar e gerenciar usuários;
* cadastrar alunos e turmas;
* vincular professores e responsáveis;
* analisar documentos;
* visualizar indicadores gerais.

---

## Tecnologias utilizadas

### Frontend

* **JavaScript**
* **React**
* **Vite**
* **HTML e CSS**

O React foi escolhido por facilitar a criação de interfaces baseadas em componentes, enquanto o Vite permite um ambiente de desenvolvimento simples e rápido.

### Backend

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-JWT-Extended**
* **Flask-Migrate**
* **Flask-CORS**

O Flask foi escolhido por ser leve e simples para construção de APIs REST. O SQLAlchemy facilita a comunicação com o banco de dados e o JWT é utilizado para autenticação dos usuários.

### Banco de dados

* **SQLite** no desenvolvimento do MVP;
* estrutura preparada para utilização futura de **PostgreSQL**.

### Ferramentas

* Git e GitHub;
* Figma;
* Visual Studio Code.

---

## Estrutura do projeto

```text
Plataforma-de-Acompanhamento-Escolar/
│
├── backend/
│   ├── app/
│   │   ├── admin/
│   │   ├── academic/
│   │   ├── auth/
│   │   ├── documents/
│   │   ├── responsavel/
│   │   └── models/
│   ├── migrations/
│   ├── seed.py
│   └── run.py
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── README.md
└── .gitignore
```

O **frontend** contém as telas e a navegação da aplicação.

O **backend** contém a API, autenticação, regras de negócio e acesso ao banco de dados.

---

## Instalação e execução

### 1. Clonar o projeto

```bash
git clone https://github.com/jeffin872/Plataforma-de-Acompanhamento-Escolar.git
cd Plataforma-de-Acompanhamento-Escolar
```

### 2. Backend

```bash
cd backend
python -m venv venv
```

No Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### Configuração do ambiente

Crie o arquivo `backend/.env` com as configurações locais:

```env
DATABASE_URL=sqlite:///dev.db
FRONTEND_ORIGIN=http://localhost:5173
JWT_SECRET_KEY=chave-local-de-desenvolvimento
```

Execute as migrations:

```bash
flask db upgrade
```

Crie os dados de teste:

```bash
python seed.py
```

Inicie o backend:

```bash
python run.py
```

Backend disponível em:

```text
http://localhost:5000
```

### 3. Frontend

Em outro terminal:

```bash
cd frontend
```

Crie o arquivo `frontend/.env`:

```env
VITE_API_URL=http://localhost:5000
```

Instale as dependências e inicie o projeto:

```bash
npm install
npm run dev
```

Acesse:

```text
http://localhost:5173
```

### Usuários de teste

**Administrador**

```text
admin@escola.com
admin123
```

**Professor**

```text
professor@escola.com
professor123
```

**Responsável**

```text
responsavel@escola.com
responsavel123
```

---

## Processo de desenvolvimento

O projeto foi desenvolvido de forma incremental.

Primeiro, a equipe criou um protótipo de alta fidelidade no Figma. Durante o desenvolvimento do MVP, as tarefas foram divididas entre frontend, backend, banco de dados, integração, testes e documentação.

O GitHub foi utilizado para controle de versão e organização do código, com commits realizados de forma incremental conforme as funcionalidades e correções eram desenvolvidas.

Durante a Sprint, algumas dificuldades apareceram somente na execução real do projeto, como incompatibilidade de uma dependência do backend com Python 3.13 e uma configuração externa de PostCSS que interferia no frontend.

Esses problemas foram identificados através dos testes locais e corrigidos antes da validação do MVP.

Ao final, foram testados os três perfis do sistema: **Administrador, Professor e Responsável**.

---

## Como utilizar a aplicação

O usuário acessa a plataforma pelo navegador e realiza o login utilizando seu e-mail e senha. Após a autenticação, o sistema identifica o perfil da conta e apresenta as funcionalidades correspondentes.

Os três principais perfis são:

* **Responsável:** acompanha notas, faltas e ocorrências dos estudantes vinculados, além de poder enviar documentos e atestados.
* **Professor:** visualiza suas turmas e pode registrar notas, faltas e ocorrências dos alunos.
* **Administrador:** gerencia usuários, alunos, turmas, vínculos e documentos, além de acompanhar informações gerais da escola.

### Problema que a aplicação busca resolver

A aplicação busca melhorar a comunicação entre escola e família, reunindo em um único ambiente informações que muitas vezes ficam espalhadas entre mensagens, documentos, reuniões e outros meios de comunicação.

Com a plataforma, responsáveis podem acompanhar mais facilmente a vida escolar dos estudantes, enquanto professores e administradores conseguem registrar e organizar essas informações.

### Quem pode se beneficiar

A solução pode ser utilizada principalmente por:

* escolas públicas e privadas;
* professores e equipes pedagógicas;
* secretarias escolares;
* pais e responsáveis;
* estudantes.

### Exemplos de utilização

Alguns exemplos de uso da aplicação são:

* um responsável consultar as notas e faltas do estudante;
* um professor registrar uma avaliação ou uma ocorrência;
* um responsável enviar um atestado diretamente pelo sistema;
* a escola identificar um estudante com muitas faltas e entrar em contato com sua família;
* a administração acompanhar documentos pendentes e informações das turmas.

### Impacto da solução

A plataforma pode contribuir para aproximar a família da escola e tornar as informações acadêmicas mais acessíveis.

O acompanhamento de faltas e desempenho também pode ajudar a escola a identificar dificuldades mais cedo, permitindo que responsáveis, professores e equipe pedagógica atuem antes que o problema se agrave.

Dessa forma, a aplicação pode contribuir para melhorar o acompanhamento dos estudantes, aumentar a participação das famílias e auxiliar na prevenção de problemas como baixo desempenho e abandono escolar.

---

## Status do projeto

**MVP funcional.**

A versão atual possui:

* frontend integrado ao backend;
* autenticação JWT;
* banco de dados;
* três perfis de usuário;
* cadastro e acompanhamento acadêmico;
* registro de notas, faltas e ocorrências;
* envio e análise de documentos;
* notificações básicas.

Os três perfis principais foram testados localmente e estão funcionando.
