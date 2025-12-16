#Esse import serve para quando fizemos uma chamada em algo que não existe ainda. Resolve problemas de referências futuras 
from __future__ import annotations
# o datetime é para mostrar datas, como a data de nascimento e futuras datas de avaliação e etc..
from datetime import date

# o typing é usado para indicar o que a váriavel é, aqui a gente usa o List para definir váriaveis dó tipo lista 
# e o Optional para casos de que o retorno de uma função seja none
from typing import List, Optional


# ----------------------------
# USUÁRIO (CLASSE GERAL) essa classe vai ser usada pelos outros usuário que vão herdar os atributos 
# ----------------------------
class Usuario:
    def __init__(self, id_usuario: int, nome: str, email: str):
        self.__id_usuario = id_usuario             # privado (ela será a chave primaria, ou seja, não deve mudar)
        self.__nome = nome                         # privado
        self.__email = email                       # privado

    # Getters
    def get_id_usuario(self) -> int:
        return self.__id_usuario

    def get_nome(self) -> str:
        return self.__nome

    def get_email(self) -> str:
        return self.__email

    # Setters (aqui colocamos validações, para que o usuário não informe dados inválidos)
    def set_nome(self, nome: str) -> None:
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        self.__nome = nome

    def set_email(self, email: str) -> None:
        email = (email or "").strip().lower()
        if "@" not in email:
            raise ValueError("Email inválido.")
        self.__email = email


# =========================
# ALUNO (Como falado acima, os usuários irão pegar os atributos padrões de um user normal, mas com algumas adições dependendo de qual usuário é)
# =========================
class Aluno(Usuario):
    def __init__(self, id_usuario: int, nome: str, email: str, matricula: str, data_nascimento: date):
        super().__init__(id_usuario, nome, email) #aqui vemos a herança, a classe aluno herda alguns atributos básicos de usuário
        self.__matricula = (matricula or "").strip()   # recebemos o valor da matricula ou uma string vazia. O strip remove espaços em branco 
        self.__data_nascimento = data_nascimento       # privado

        # Associações. 
        # Elas se relacionam entre outras classes, como turmas, avaliações e faltas. um aluno pode ter várias turmas, avaliações e faltas

        self.__turmas: List[Turma] = []                
        self.__avaliacoes: List[Avaliacao] = []
        self.__faltas: List[Falta] = []

        if not self.__matricula:
            raise ValueError("Matrícula não pode ser vazia.")

    # Getters
    def get_matricula(self) -> str:
        return self.__matricula

    def get_data_nascimento(self) -> date:
        return self.__data_nascimento

    def get_turmas(self) -> List["Turma"]:
        # o Copy é usado para criar uma copia da lista original, pelo principio de encapsuçamento,
        # não se possa acessar a lista original e mudar ela usando o get
        return self.__turmas.copy() 
    def get_avaliacoes(self) -> List["Avaliacao"]:
        return self.__avaliacoes.copy()

    def get_faltas(self) -> List["Falta"]:
        return self.__faltas.copy() #

    # Métodos de domínio (uso interno do sistema), ou seja, são ações que os sistema vai fazer sem a intervenção do usuário
    # Esses métodos são chamados por outras classes para registrar vínculos e eventos
    def _vincular_turma(self, turma: "Turma") -> None:
        if turma not in self.__turmas:
            self.__turmas.append(turma)
    #Esse registro de avaliação, por exemplo, só é executado na classe professor, quando o professor lança uma nota para o aluno
    def _registrar_avaliacao(self, avaliacao: "Avaliacao") -> None:
        self.__avaliacoes.append(avaliacao)

    def _registrar_falta(self, falta: "Falta") -> None:
        self.__faltas.append(falta)


# =========================
# PROFESSOR (HERDA DE USUÁRIO)
# =========================
class Professor(Usuario):
    def __init__(self, id_usuario: int, nome: str, email: str):
        super().__init__(id_usuario, nome, email)
        # A classe professor tem vínculos com turmas e disciplinas que ele leciona, por isso usamos essas associações
        self.__turmas: List[Turma] = []
        self.__disciplinas: List[Disciplina] = []

    def get_turmas(self) -> List["Turma"]:
        return self.__turmas.copy()

    def get_disciplinas(self) -> List["Disciplina"]:
        return self.__disciplinas.copy()

    def _vincular_turma(self, turma: "Turma") -> None:
        if turma not in self.__turmas:
            self.__turmas.append(turma)
        
        #Aqui o professor vincula a disciplina que ele leciona, pois ele não pode colocar notas em disciplinas que ele não leciona
    def _vincular_disciplina(self, disciplina: "Disciplina") -> None:
        if disciplina not in self.__disciplinas:
            self.__disciplinas.append(disciplina)

    # Processos principais do sistema (lançar nota / falta)
    def lancar_nota(self, aluno: "Aluno", turma: "Turma", disciplina: "Disciplina", valor: float, data_avaliacao: date) -> "Avaliacao": # Essa seta indicada o tipo de retorno da função
        
        # Validações de regras de negócio, testamos aqui se o aluno pertence a turma e se o professor leciona a disciplina nessa turm
        if aluno not in turma.get_alunos():
            raise ValueError("O aluno não pertence a esta turma.")
        if not turma.tem_professor_disciplina(self, disciplina):
            raise ValueError("Professor não está vinculado a essa disciplina nesta turma.")

        avaliacao = Avaliacao(aluno=aluno, professor=self, turma=turma, disciplina=disciplina, valor=valor, data_avaliacao=data_avaliacao)
        aluno._registrar_avaliacao(avaliacao)
        return avaliacao

    def registrar_falta(self, aluno: "Aluno", turma: "Turma", data_falta: date) -> "Falta":
        if aluno not in turma.get_alunos():
            raise ValueError("O aluno não pertence a esta turma.")
        falta = Falta(aluno=aluno, turma=turma, data_falta=data_falta)
        aluno._registrar_falta(falta)
        return falta


# =========================
# RESPONSÁVEL (HERDA DE USUÁRIO)
# =========================
class Responsavel(Usuario):
    def __init__(self, id_usuario: int, nome: str, email: str):
        super().__init__(id_usuario, nome, email)

        #Essa associação indica quais alunos esse responsável está vinculado
        self.__alunos: List[Aluno] = []

    #aqui eu tenho um get para pegar a lista de alunos vinculados a esse responsável
    def get_alunos(self) -> List["Aluno"]:
        return self.__alunos.copy()

    #aqui eu tenho um método para vincular um aluno a esse responsável
    def vincular_aluno(self, aluno: "Aluno") -> None:
        if aluno not in self.__alunos:
            self.__alunos.append(aluno)


# =========================
# DISCIPLINA
# =========================
class Disciplina:
    def __init__(self, id_disciplina: int, nome: str):
        self.__id_disciplina = id_disciplina     # privado
        self.__nome = (nome or "").strip()       # privado
        if not self.__nome:
            raise ValueError("Nome da disciplina não pode ser vazio.")

    def get_id_disciplina(self) -> int:
        return self.__id_disciplina

    def get_nome(self) -> str:
        return self.__nome

    def set_nome(self, nome: str) -> None:
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("Nome da disciplina não pode ser vazio.")
        self.__nome = nome


# =========================
# TURMA
# =========================

#Classe bem importante, pois ela faz a ligação entre alunos, professores e disciplinas

class Turma:
    def __init__(self, id_turma: int, nome: str, ano_letivo: int):
        self.__id_turma = id_turma
        self.__nome = (nome or "").strip()
        self.__ano_letivo = ano_letivo

        self.__alunos: List[Aluno] = []
        # vínculos: quais professores lecionam quais disciplinas nesta turma
        #conceito bem legal, aqui eu coloco um professor vinculado a uma tupla, onda essa tupla tem a disciplina junto a turma
        # Assim cada elemento da lista desses professores é uma tupla (professor, disciplina). Evita erro de vincular professor a disciplina errada
        self.__professor_disciplina: List[tuple[Professor, Disciplina]] = [] #

        if not self.__nome:
            raise ValueError("Nome da turma não pode ser vazio.")
        if ano_letivo < 2000:
            raise ValueError("Ano letivo inválido.")

    def get_id_turma(self) -> int:
        return self.__id_turma

    def get_nome(self) -> str:
        return self.__nome

    def get_ano_letivo(self) -> int:
        return self.__ano_letivo

    def set_nome(self, nome: str) -> None:
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("Nome da turma não pode ser vazio.")
        self.__nome = nome

    def get_alunos(self) -> List["Aluno"]:
        return self.__alunos.copy()

    def adicionar_aluno(self, aluno: "Aluno") -> None:
        if aluno not in self.__alunos:
            self.__alunos.append(aluno)
            aluno._vincular_turma(self)

    #aqui é criado um vínculo entre o professor e a disciplina que ele leciona nessa turma. Pois se não tiver esse vínculo, o professor não pode lançar notas nessa disciplina
    # muito importante, pois esse metodo é fundamental na classe professor para validar se o professor pode lançar notas e faltas nessa turma e disciplina
    def vincular_professor_disciplina(self, professor: "Professor", disciplina: "Disciplina") -> None:
        par = (professor, disciplina)
        if par not in self.__professor_disciplina:
            self.__professor_disciplina.append(par)
            professor._vincular_turma(self)
            professor._vincular_disciplina(disciplina)

    #valida se tem esse vínculo entre professor e disciplina nessa turma
    def tem_professor_disciplina(self, professor: "Professor", disciplina: "Disciplina") -> bool:
        return (professor, disciplina) in self.__professor_disciplina


# =========================
# AVALIAÇÃO (NOTA)
# =========================


#
class Avaliacao:
    def __init__(self, aluno: Aluno, professor: Professor, turma: Turma, disciplina: Disciplina, valor: float, data_avaliacao: date):
        self.__aluno = aluno
        self.__professor = professor
        self.__turma = turma
        self.__disciplina = disciplina
        self.__data_avaliacao = data_avaliacao

        #Evitamos nota errado entrando no sistema, chamando o setter que tem as validações das notas
        self.__valor = 0.0
        self.set_valor(valor)

    def get_aluno(self) -> Aluno:
        return self.__aluno

    def get_professor(self) -> Professor:
        return self.__professor

    def get_turma(self) -> Turma:
        return self.__turma

    def get_disciplina(self) -> Disciplina:
        return self.__disciplina

    def get_data_avaliacao(self) -> date:
        return self.__data_avaliacao

    def get_valor(self) -> float:
        return self.__valor

    def set_valor(self, valor: float) -> None:
        # essa função é muito massa. Usamos para verificar se o valor é de um determinado tipo, que nesse caso é int ou float
        if not isinstance(valor, (int, float)):
            raise ValueError("Nota deve ser numérica.")
        if valor < 0 or valor > 10:
            raise ValueError("Nota deve estar entre 0 e 10.")
        self.__valor = float(valor)


# =========================
# FALTA
# =========================

# A classe de falta registra uma falta de um aluno em uma turma em uma data específica
# Ela se inicia como não justificada, mas pode ser justificada posteriormente com um motivo
class Falta:
    def __init__(self, aluno: Aluno, turma: Turma, data_falta: date):
        self.__aluno = aluno
        self.__turma = turma
        self.__data_falta = data_falta
        self.__justificada = False
        self.__motivo_justificativa: Optional[str] = None

    # os getters privados, permitem o acesso aos atributos da falta sem poder modificá-los diretamente
    def get_aluno(self) -> Aluno:
        return self.__aluno

    def get_turma(self) -> Turma:
        return self.__turma

    def get_data_falta(self) -> date:
        return self.__data_falta

    def is_justificada(self) -> bool:
        return self.__justificada

    # Aqui o motivo da justificativa pdoe ser none, caso a falta ainda não tenha sido justificada
    def get_motivo_justificativa(self) -> Optional[str]:
        return self.__motivo_justificativa

    def justificar(self, motivo: str) -> None:
        motivo = (motivo or "").strip() # o strip evita casos de o usuário só colocar espaços em branco
        if not motivo:
            raise ValueError("Informe um motivo para justificar a falta.")
        self.__justificada = True
        self.__motivo_justificativa = motivo

   
# Executando um teste do sistema


if __name__ == "__main__":
    print("=== Iniciando teste da Plataforma de Acompanhamento Escolar ===\n")

    # Criando usuários
    aluno1 = Aluno(
        id_usuario=1,
        nome="Carlos Silva",
        email="carlos@email.com",
        matricula="2025001",
        data_nascimento=date(2008, 5, 20)
    )

    professor1 = Professor(
        id_usuario=2,
        nome="Maria Oliveira",
        email="maria@escola.com"
    )

    responsavel1 = Responsavel(
        id_usuario=3,
        nome="João Silva",
        email="joao.responsavel@email.com"
    )

    # Criando disciplina e turma
    disciplina1 = Disciplina(
        id_disciplina=1,
        nome="Matemática"
    )

    turma1 = Turma(
        id_turma=1,
        nome="9º Ano A",
        ano_letivo=2025
    )

    # Vinculando aluno à turma
    turma1.adicionar_aluno(aluno1)

    # Vinculando responsável ao aluno
    responsavel1.vincular_aluno(aluno1)

    # Vinculando professor à disciplina na turma
    turma1.vincular_professor_disciplina(professor1, disciplina1)

    print("Aluno, professor, responsável, turma e disciplina criados com sucesso.\n")

    # Professor lança uma nota
    avaliacao1 = professor1.lancar_nota(
        aluno=aluno1,
        turma=turma1,
        disciplina=disciplina1,
        valor=8.5,
        data_avaliacao=date.today()
    )

    print(f"Nota lançada: {avaliacao1.get_valor()} em {avaliacao1.get_disciplina().get_nome()}")

    # Professor registra uma falta
    falta1 = professor1.registrar_falta(
        aluno=aluno1,
        turma=turma1,
        data_falta=date.today()
    )

    print("Falta registrada.")

    # Justificando a falta
    falta1.justificar("Atestado médico")

    print("Falta justificada.")
    print(f"Motivo: {falta1.get_motivo_justificativa()}\n")

    # Jutando alguma consultas com os dados criados na tela 
    print("=== CONSULTAS ===")
    print("Aluno:", aluno1.get_nome())
    print("Turmas do aluno:", [t.get_nome() for t in aluno1.get_turmas()])
    print("Notas do aluno:", [a.get_valor() for a in aluno1.get_avaliacoes()])
    print("Total de faltas:", len(aluno1.get_faltas()))
    print("Responsável:", responsavel1.get_nome())
    print("Alunos do responsável:", [a.get_nome() for a in responsavel1.get_alunos()])

    print("\n=== Teste finalizado com sucesso ===")