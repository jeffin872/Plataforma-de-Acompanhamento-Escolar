# Backend — Plataforma de Acompanhamento Escolar

API REST em **Flask + SQLAlchemy + PostgreSQL**, seguindo a arquitetura em
camadas definida na documentação do EP2 (Apresentação → Aplicação → Dados)
e a separação por perfil (Administrador, Professor, Responsável).

## 1. Estrutura de pastas

```
backend/
├── app/
│   ├── __init__.py          # application factory (create_app)
│   ├── config.py            # configurações (lidas do .env)
│   ├── extensions.py        # db, migrate, jwt, cors
│   ├── models/               # um arquivo por entidade (SQLAlchemy)
│   ├── auth/                 # login, JWT, decorator @perfil_requerido
│   ├── admin/                 # usuários, turmas, vínculos, dashboard
│   ├── academic/              # área do professor: notas, faltas, ocorrências
│   ├── responsavel/           # área do responsável (somente leitura + notificações)
│   ├── documents/             # upload/validação de documentos (atestados)
│   ├── alerts/                 # regra de excesso de faltas + envio de e-mail
│   └── utils/                  # respostas JSON padronizadas
├── migrations/                # gerado pelo Flask-Migrate (Alembic)
├── seed.py                    # cria usuários e dados de teste
├── run.py                     # ponto de entrada (flask run / python run.py)
├── requirements.txt
└── .env.example                # copie para .env e preencha
```

## 2. Como rodar localmente

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edite o .env: pelo menos DATABASE_URL apontando pro seu PostgreSQL local
# (se não tiver Postgres instalado, dá pra testar rápido trocando
#  DATABASE_URL por algo como sqlite:///dev.db)

flask db upgrade      # cria as tabelas no banco
python seed.py         # cria usuários de teste (admin, professor, responsável)
python run.py           # sobe a API em http://localhost:5000
```

Usuários criados pelo `seed.py`:

| Perfil       | E-mail                  | Senha            |
|--------------|--------------------------|-------------------|
| Admin        | admin@escola.com          | admin123          |
| Professor    | professor@escola.com      | professor123      |
| Responsável  | responsavel@escola.com    | responsavel123    |

## 3. Autenticação

Toda rota (exceto `/api/auth/login` e `/api/saude`) exige o header:

```
Authorization: Bearer <token>
```

O token é obtido em `POST /api/auth/login` e carrega o `perfil` do usuário
como claim. As rotas usam o decorator `@perfil_requerido("admin", ...)`
para bloquear acesso indevido entre perfis (retorna 403).

## 4. Principais rotas por módulo

**Autenticação** (`/api/auth`)
- `POST /login` — retorna token + dados do usuário
- `GET /me` — dados do usuário logado
- `PUT /senha` — trocar a própria senha

**Administração** (`/api/admin`) — perfil `admin`
- `GET|POST /usuarios`, `PUT|DELETE /usuarios/<id>`
- `GET|POST /turmas`, `GET /turmas/<id>`
- `POST /turmas/<id>/alunos` — cadastrar aluno na turma
- `POST /turmas/<id>/vincular-professor` — professor + disciplina numa turma
- `POST /vincular-responsavel` — vincula responsável a um aluno
- `POST /historico/importar` — importa notas/faltas de aluno transferido
- `GET /dashboard` — indicadores gerais da escola

**Área do Professor** (`/api/academic`) — perfil `professor`
- `GET /minhas-turmas`
- `POST /notas`, `GET /turmas/<id>/notas`
- `POST /faltas`, `PUT /faltas/<id>/justificar`, `GET /turmas/<id>/faltas`
- `POST /ocorrencias`, `GET /turmas/<id>/ocorrencias`

**Área do Responsável** (`/api/responsavel`) — perfil `responsavel`
- `GET /meus-alunos`
- `GET /alunos/<id>/notas` | `/faltas` | `/ocorrencias`
- `GET /notificacoes`

**Documentos** (`/api/documentos`)
- `POST ""` (`responsavel`) — envia arquivo (multipart/form-data: `aluno_id`, `tipo`, `arquivo`)
- `GET /meus` (`responsavel`) — meus documentos enviados
- `GET ""` (`admin`, `professor`) — fila de análise (`?status=pendente`)
- `PUT /<id>` (`admin`, `professor`) — aprova/rejeita (`{"status": "aprovado", "observacao": "..."}`)

O módulo de alertas (`app/alerts/service.py`) é chamado automaticamente
sempre que uma falta é registrada; ao atingir `LIMITE_FALTAS_ALERTA`
faltas não justificadas, cria uma `Notificacao` para cada responsável e
dispara um e-mail (por padrão só loga no console — ver `.env.example`).

## 5. Testando sem Postman

Um smoke test de ponta a ponta (login, bloqueio por perfil, lançar nota,
disparo de alerta por excesso de faltas, acesso do responsável) está
descrito no relatório de continuidade entregue junto com este projeto.
Ele roda com SQLite em memória, sem precisar de Postgres configurado.

## 6. Próximos passos sugeridos

- Escrever testes automatizados (pytest) a partir do smoke test manual.
- Trocar `STORAGE_BACKEND` para `s3` e `EMAIL_BACKEND` para `sendgrid`
  quando o projeto for para produção (as duas abstrações já existem em
  `app/documents/storage.py` e `app/alerts/email_sender.py`).
- Conectar com o Frontend (React) — ver o Relatório de Continuidade.
