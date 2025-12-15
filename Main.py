#Esse import serve para quando fizemos uma chamada em algo que não existe ainda. Resolve problemas de referências futuras 
from __future__ import annotations
# o ABC serve para dizer que é um modelo abstrato, usamos isso na classe usuários. 
#Pois ela não é instaciada diretamente, serve como base para as outras classes
from abc import ABC
# o datetime é para mostrar datas, como a data de nascimento e futuras datas de avaliação e etc..
from datetime import date

# o typing é usado para indicar o que a váriavel é, aqui a gente usa o List para definir váriaveis dó tipo lista 
# e o Optional para casos de que o retorno de uma função seja none.
from typing import List, Optional



# MODELO DO SISTEMA ESCOLAR

# Processos de software adotados:
# - Separação por domínio: classes representam entidades do mundo real (Aluno, Turma, etc.)
# - Encapsulamento: atributos sensíveis/imutáveis ficam privados e acessados por getters/setters
# - POO: herança (Usuario -> Professor/Aluno/Responsavel) e associações (Turma contém alunos, etc.)
# - Validações: regras básicas (nota 0..10, datas, duplicidade em listas)
#
# Observação:
# - Essas classes são somente o básico do sistema, ainda terá muitas outras para ficar 100%
# -----------------------------------------


# ----------------------------
# USUÁRIO (CLASSE GERAL) essa classe vai ser usada pelos outros usuário que vão herdar os atributos 
# ----------------------------
class Usuario(ABC):
    def __init__(self, id_usuario: int, nome: str, email: str):
        self.__id_usuario = id_usuario             # privado (ela será a chave primeira, ou seja, não deve mudar)
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
        super().__init__(id_usuario, nome, email)
        self.__matricula = (matricula or "").strip()   # privado
        self.__data_nascimento = data_nascimento       # privado

        self.__turmas: List[Turma] = []                # associações
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
        return self.__turmas.copy()

    def get_avaliacoes(self) -> List["Avaliacao"]:
        return self.__avaliacoes.copy()

    def get_faltas(self) -> List["Falta"]:
        return self.__faltas.copy()

    # Métodos de domínio (uso interno do sistema)
    def _vincular_turma(self, turma: "Turma") -> None:
        if turma not in self.__turmas:
            self.__turmas.append(turma)

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
        self.__turmas: List[Turma] = []
        self.__disciplinas: List[Disciplina] = []

    def get_turmas(self) -> List["Turma"]:
        return self.__turmas.copy()

    def get_disciplinas(self) -> List["Disciplina"]:
        return self.__disciplinas.copy()

    def _vincular_turma(self, turma: "Turma") -> None:
        if turma not in self.__turmas:
            self.__turmas.append(turma)

    def _vincular_disciplina(self, disciplina: "Disciplina") -> None:
        if disciplina not in self.__disciplinas:
            self.__disciplinas.append(disciplina)

    # Processos principais do sistema (lançar nota / falta)
    def lancar_nota(self, aluno: "Aluno", turma: "Turma", disciplina: "Disciplina", valor: float, data_avaliacao: date) -> "Avaliacao":
        # Validações de regras de negócio (robustez)
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
        self.__alunos: List[Aluno] = []

    def get_alunos(self) -> List["Aluno"]:
        return self.__alunos.copy()

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
class Turma:
    def __init__(self, id_turma: int, nome: str, ano_letivo: int):
        self.__id_turma = id_turma
        self.__nome = (nome or "").strip()
        self.__ano_letivo = ano_letivo

        self.__alunos: List[Aluno] = []
        # vínculos: quais professores lecionam quais disciplinas nesta turma
        self.__professor_disciplina: List[tuple[Professor, Disciplina]] = []

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

    def vincular_professor_disciplina(self, professor: "Professor", disciplina: "Disciplina") -> None:
        par = (professor, disciplina)
        if par not in self.__professor_disciplina:
            self.__professor_disciplina.append(par)
            professor._vincular_turma(self)
            professor._vincular_disciplina(disciplina)

    def tem_professor_disciplina(self, professor: "Professor", disciplina: "Disciplina") -> bool:
        return (professor, disciplina) in self.__professor_disciplina


# =========================
# AVALIAÇÃO (NOTA)
# =========================
class Avaliacao:
    def __init__(self, aluno: Aluno, professor: Professor, turma: Turma, disciplina: Disciplina, valor: float, data_avaliacao: date):
        self.__aluno = aluno
        self.__professor = professor
        self.__turma = turma
        self.__disciplina = disciplina
        self.__data_avaliacao = data_avaliacao

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
        if not isinstance(valor, (int, float)):
            raise ValueError("Nota deve ser numérica.")
        if valor < 0 or valor > 10:
            raise ValueError("Nota deve estar entre 0 e 10.")
        self.__valor = float(valor)


# =========================
# FALTA
# =========================
class Falta:
    def __init__(self, aluno: Aluno, turma: Turma, data_falta: date):
        self.__aluno = aluno
        self.__turma = turma
        self.__data_falta = data_falta
        self.__justificada = False
        self.__motivo_justificativa: Optional[str] = None

    def get_aluno(self) -> Aluno:
        return self.__aluno

    def get_turma(self) -> Turma:
        return self.__turma

    def get_data_falta(self) -> date:
        return self.__data_falta

    def is_justificada(self) -> bool:
        return self.__justificada

    def get_motivo_justificativa(self) -> Optional[str]:
        return self.__motivo_justificativa

    def justificar(self, motivo: str) -> None:
        motivo = (motivo or "").strip()
        if not motivo:
            raise ValueError("Informe um motivo para justificar a falta.")
        self.__justificada = True
        self.__motivo_justificativa = motivo


#Esse IF é usado para executar o programa
if __name__ == "__main__":
    #Esses dados ficticios foram criados para testes do programa 

    # Usuários
    prof = Professor(1, "Ana Professora", "ana@escola.com",)
    aluno = Aluno(2, "João Aluno", "joao@escola.com", "MAT2025-001", date(2010, 5, 10))
    resp = Responsavel(3, "Maria Responsável", "maria@familia.com")

    # Vínculos
    resp.vincular_aluno(aluno)

    matematica = Disciplina(1, "Matemática")
    turma_6a = Turma(1, "6º A", 2025)

    turma_6a.adicionar_aluno(aluno)
    turma_6a.vincular_professor_disciplina(prof, matematica)

    # Lançamentos
    nota1 = prof.lancar_nota(aluno, turma_6a, matematica, 8.5, date.today())
    falta1 = prof.registrar_falta(aluno, turma_6a, date.today())
    falta1.justificar("Consulta médica")

    print("Aluno:", aluno.get_nome(), aluno.get_matricula())
    print("Nota:", nota1.get_valor(), "Disciplina:", nota1.get_disciplina().get_nome())
    print("Falta justificada:", falta1.is_justificada(), "-", falta1.get_motivo_justificativa())
