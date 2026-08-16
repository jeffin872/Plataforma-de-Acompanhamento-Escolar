## Descrição do projeto

A aplicação busca centralizar informações escolares que muitas vezes ficam espalhadas entre mensagens, documentos, reuniões e diferentes sistemas.

O objetivo é criar uma plataforma que facilite a comunicação entre escola, professores e responsáveis, permitindo futuramente o acompanhamento de informações como notas, faltas, ocorrências, documentos e notificações.

Na versão atual do MVP, já foram implementados o sistema de autenticação e o acesso aos diferentes perfis da aplicação.

### Público-alvo

* escolas públicas e privadas;
* professores;
* administradores escolares;
* pais e responsáveis.

### Funcionalidades atuais

A versão atual possui:

* login de usuários;
* autenticação por perfil;
* acesso aos perfis de **Responsável, Professor e Administrador**;
* direcionamento para o painel correspondente ao tipo de usuário;
* estrutura inicial de frontend, backend e banco de dados.

As demais funcionalidades apresentadas na interface ainda estão em desenvolvimento.

### Funcionalidades previstas

**Responsável**

* acompanhar notas e faltas;
* visualizar ocorrências;
* consultar estudantes vinculados;
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

## Processo de desenvolvimento

O projeto foi desenvolvido de forma incremental.

Primeiro, a equipe criou um protótipo de alta fidelidade no Figma. Durante o desenvolvimento do MVP, as tarefas foram divididas entre frontend, backend, banco de dados, integração, testes e documentação.

O GitHub foi utilizado para controle de versão e organização do código, com commits realizados conforme as funcionalidades e correções eram desenvolvidas.

Durante a Sprint, algumas dificuldades apareceram somente na execução real do projeto, como incompatibilidade de uma dependência do backend com Python 3.13 e uma configuração externa de PostCSS que interferia no frontend.

Esses problemas foram corrigidos durante os testes locais.

Na versão atual, foram validados o login e o acesso aos três perfis do sistema: **Administrador, Professor e Responsável**. As demais funcionalidades continuam sendo desenvolvidas para as próximas versões.

---

## Como utilizar a aplicação

O usuário acessa a plataforma pelo navegador e realiza o login utilizando seu e-mail e senha.

Após a autenticação, o sistema identifica o perfil da conta e direciona o usuário para o painel correspondente:

* **Responsável**
* **Professor**
* **Administrador**

Na versão atual do MVP, esse é o principal fluxo funcional disponível. As funcionalidades internas de acompanhamento e gestão ainda aparecem como **“Em breve”** e serão implementadas nas próximas etapas do projeto.

### Problema que a aplicação busca resolver

A aplicação busca melhorar a comunicação entre escola e família, reunindo em um único ambiente informações que normalmente podem ficar espalhadas entre mensagens, documentos, reuniões e diferentes meios de comunicação.

A proposta é que, com a evolução do sistema, responsáveis possam acompanhar mais facilmente a vida escolar dos estudantes, enquanto professores e administradores possam registrar e organizar essas informações.

### Quem pode se beneficiar

A solução é voltada principalmente para:

* escolas públicas e privadas;
* professores e equipes pedagógicas;
* secretarias escolares;
* pais e responsáveis;
* estudantes.

### Exemplos de utilização previstos

Com a implementação completa das funcionalidades planejadas, alguns cenários de uso serão:

* um responsável consultar notas e faltas do estudante;
* um professor registrar uma avaliação ou ocorrência;
* um responsável enviar um atestado pelo sistema;
* a escola identificar estudantes com muitas faltas;
* a administração acompanhar documentos e informações das turmas.

### Impacto da solução

Mesmo estando em uma etapa inicial, a proposta da plataforma busca aproximar a família da escola e facilitar o acesso às informações acadêmicas.

Com a implementação das próximas funcionalidades, o sistema poderá ajudar na identificação mais rápida de dificuldades relacionadas à frequência e ao desempenho escolar, permitindo uma participação mais próxima de responsáveis, professores e equipe pedagógica.

Dessa forma, a solução tem potencial para contribuir com a organização das informações escolares, fortalecer a comunicação com as famílias e auxiliar na prevenção de problemas como baixo desempenho e abandono escolar.

---

## Status do projeto

**MVP inicial em desenvolvimento.**

A versão atual possui:

* frontend integrado ao backend;
* banco de dados configurado;
* autenticação de usuários;
* controle de acesso por perfil;
* três tipos de usuário: Administrador, Professor e Responsável;
* acesso aos painéis iniciais de cada perfil.

Atualmente, o fluxo de **login e acesso aos diferentes perfis está funcional e foi testado localmente**.

As funcionalidades internas apresentadas nos painéis, como notas, faltas, documentos, notificações, turmas e demais recursos acadêmicos, ainda estão em desenvolvimento e serão implementadas nas próximas etapas do projeto.
